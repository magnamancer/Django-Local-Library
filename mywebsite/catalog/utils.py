import requests
import pandas as pd
import io
import json
from sklearn.linear_model import LinearRegression
import plotly.graph_objects as go
import os
import zipfile
import tempfile
import shutil
import logging
import numpy as np

# Using Logging on this file for debug
logger = logging.getLogger(__name__)

# Import the Kaggle API client
from kaggle.api.kaggle_api_extended import KaggleApi

# --- Define your data source URL ---
DATA_API_URL = "https://www.kaggle.com/datasets/shivam2503/diamonds"


# Initialize the Kaggle API client once (e.g., at module level)
# It will automatically look for kaggle.json in the standard location
api = KaggleApi()

try:
    api.authenticate()
except Exception as e:
    logger.error(f"Kaggle API authentication failed: {e}")

KAGGLE_DATASET_SLUG = "shivam2503/diamonds"
KAGGLE_FILE_NAME = "diamonds.csv"
KAGGLE_DOWNLOADED_ZIP_NAME = "diamonds.zip"


def _read_zip_csv():
    """
    Downloads the Kaggle dataset file, checks if it's a zip, extracts if necessary,
    and reads the CSV into a pandas DataFrame. Manages its own temporary files.

    Returns:
        tuple[pd.DataFrame | None, str | None]: A tuple containing:
            - The pandas DataFrame if successful, None otherwise.
            - An error message string if an error occurred, None otherwise.
    """
    temp_dir = None
    download_path = "."
    target_file_path = os.path.join(download_path, KAGGLE_FILE_NAME)

    try:
        # Download the file if it doesn't exist
        if not os.path.exists(target_file_path):
            logger.info(f"Downloading {KAGGLE_FILE_NAME} from Kaggle...")
            api.dataset_download_file(
                dataset=KAGGLE_DATASET_SLUG,
                file_name=KAGGLE_FILE_NAME,
                path=download_path,
                force=False,
            )

        # After download attempt, verify existence
        if not os.path.exists(target_file_path):
            error_msg = f"Downloaded file '{target_file_path}' does not exist on disk after download attempt!"
            logger.error(error_msg)
            return None, error_msg

        # Check if the downloaded file is a ZIP by reading its header
        is_zip_file = False
        try:
            with open(target_file_path, "rb") as f:
                header = f.read(4)
                if header == b"PK\x03\x04":  # Standard ZIP file signature
                    is_zip_file = True
        except Exception as e:
            error_msg = (
                f"Could not inspect file header for '{target_file_path}': {e}"
            )
            logger.error(error_msg)
            return None, error_msg

        file_to_read_path = target_file_path

        if is_zip_file:
            temp_dir = (
                tempfile.mkdtemp()
            )  # Create temporary directory for extraction
            try:
                with zipfile.ZipFile(target_file_path, "r") as zip_ref:
                    zip_contents = zip_ref.namelist()
                    csv_name_in_zip = None
                    for name in zip_contents:
                        if name.lower().endswith(".csv"):
                            csv_name_in_zip = name
                            break

                    if not csv_name_in_zip:
                        error_msg = f"No CSV file found inside ZIP archive '{target_file_path}'. Contents: {zip_contents}"
                        logger.error(error_msg)
                        return None, error_msg

                    zip_ref.extract(csv_name_in_zip, path=temp_dir)
                    file_to_read_path = os.path.join(temp_dir, csv_name_in_zip)
            except zipfile.BadZipFile:
                error_msg = f"'{target_file_path}' is not a valid ZIP file. It might be corrupted."
                logger.error(error_msg)
                return None, error_msg
            except Exception as e:
                error_msg = f"Failed during ZIP extraction of '{target_file_path}': {e}"
                logger.error(error_msg)
                return None, error_msg

        if not file_to_read_path or not os.path.exists(file_to_read_path):
            error_msg = f"No valid CSV file found or extracted at '{file_to_read_path}'."
            logger.error(error_msg)
            return None, error_msg

        # Read the CSV file
        df = None
        try:
            df = pd.read_csv(file_to_read_path, encoding="utf-8")
        except UnicodeDecodeError:
            try:
                df = pd.read_csv(file_to_read_path, encoding="latin1")
            except Exception as read_e:
                error_msg = f"Failed to read CSV with common encodings from '{file_to_read_path}': {read_e}"
                logger.critical(error_msg)
                return None, error_msg
        except Exception as read_e:
            error_msg = (
                f"Failed to read CSV from '{file_to_read_path}': {read_e}"
            )
            logger.critical(error_msg)
            return None, error_msg

        if df is not None:
            df.columns = df.columns.str.strip()

        return df, None  # Success, return DataFrame and no error message

    except Exception as e:
        error_msg = f"Unexpected error in _read_zip_csv: {e}"
        logger.error(error_msg)
        return None, error_msg
    finally:
        # Clean up the temporary directory if it was created
        if temp_dir and os.path.exists(temp_dir):
            try:
                shutil.rmtree(temp_dir)
                logger.info(f"Cleaned up temporary directory: {temp_dir}")
            except Exception as e:
                logger.error(
                    f"Failed to clean up temporary directory '{temp_dir}': {e}"
                )


def get_dataset_columns():

    df, error_msg = _read_zip_csv()
    df.columns = df.columns.str.strip()
    # Dropping non-numeric rows
    df = df.select_dtypes(include=np.number)
    columns = list(df.columns)
    return columns


def load_and_process_kaggle_data(x_variable, y_variable):

    df, error_msg = _read_zip_csv()

    if x_variable not in df.columns or y_variable not in df.columns:
        error_msg = f"Selected variable(s) not found in DataFrame. X:'{x_variable}' in_df:{x_variable in df.columns}, Y:'{y_variable}' in_df:{y_variable in df.columns}"
        logger.error(error_msg)
        return (
            json.dumps({"data": [], "layout": {"title": error_msg}}),
            error_msg,
        )

    try:
        df[x_variable] = pd.to_numeric(df[x_variable], errors="coerce")
        df[y_variable] = pd.to_numeric(df[y_variable], errors="coerce")
    except Exception as e:
        error_msg = f"Error converting variables to numeric: {e}"
        logger.error(error_msg)
        return (
            json.dumps({"data": [], "layout": {"title": error_msg}}),
            error_msg,
        )
    # Dropping na valued rows
    df_filtered = df.dropna(subset=[x_variable, y_variable])
    # Dropping non-numeric rows
    df_filtered = df_filtered.select_dtypes(include=np.number)
    if df_filtered.empty:
        error_msg = f"No valid numeric data points for selected variables '{x_variable}' and '{y_variable}' after removing missing values. Please ensure you select numeric columns."
        logger.warning(error_msg)
        return (
            json.dumps({"data": [], "layout": {"title": error_msg}}),
            error_msg,
        )
    elif df_filtered.shape[0] < 2:
        error_msg = "Not enough data points for regression (less than 2 rows after filtering)."
        logger.warning(error_msg)
        return (
            json.dumps({"data": [], "layout": {"title": error_msg}}),
            error_msg,
        )
    elif (
        df_filtered[x_variable].nunique() < 2
        or df_filtered[y_variable].nunique() < 2
    ):
        error_msg = "Not enough distinct data points for linear regression (need at least 2 unique X or Y values)."
        logger.warning(error_msg)
        return (
            json.dumps({"data": [], "layout": {"title": error_msg}}),
            error_msg,
        )

    # Sampling for large DataFrames (keep this, it's good practice for performance)
    if len(df_filtered) > 5000:
        df_filtered = df_filtered.sample(n=5000, random_state=5)

    X = df_filtered[x_variable].values.reshape(-1, 1)
    y = df_filtered[y_variable].values

    model = LinearRegression()
    model.fit(X, y)
    y_pred = model.predict(X)

    fig = go.Figure()
    fig.add_trace(
        go.Scatter(
            x=df_filtered[x_variable],
            y=df_filtered[y_variable],
            mode="markers",
            name="Data Points",
            marker=dict(
                size=7,  # Reverted to a sensible size
                opacity=0.7,
                color="blue",
            ),
        )
    )
    fig.add_trace(
        go.Scatter(
            x=df_filtered[x_variable],
            y=y_pred.flatten(),
            mode="lines",
            name="Regression Line",
            line=dict(color="red", width=2),
        )
    )

    fig.update_layout(
        title=f"Linear Regression: {y_variable.replace('_', ' ').title()} vs. {x_variable.replace('_', ' ').title()}",
        xaxis_title=x_variable.replace("_", " ").title(),
        yaxis_title=y_variable.replace("_", " ").title(),
        hovermode="closest",
    )

    plotly_json = fig.to_json()
    return plotly_json, None
