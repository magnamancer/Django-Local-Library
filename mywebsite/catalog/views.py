from django.shortcuts import render, get_object_or_404
from .models import Person, Project, Technology, Skill, ProjectMedia
from django.views import generic
from django.http import HttpResponseRedirect
from django.urls import reverse
from .utils import get_dataset_columns, load_and_process_kaggle_data
from .forms import XYChoiceForm
import requests
import pandas as pd
import io
from sklearn.linear_model import LinearRegression
import plotly.graph_objects as go
import json


def home(request):
    """View function for home page of site."""
    context = {}
    return render(request, "home.html", context=context)


def resume(request):
    """View function for resume page of site."""
    context = {}
    return render(request, "resume.html", context=context)


def projects_page(request):
    """View function for projects page of site."""
    # Getting my Object
    project_list = Project.objects.all()

    context = {"project_list": project_list}

    # Render the HTML template index.html with the data in the context variable
    return render(request, "project_list.html", context=context)


class project_detail_view(generic.DetailView):
    """View function for individual project detail views site."""

    model = Project


def landing(request):
    """View function for landing page of site."""
    context = {}
    return render(request, "landing.html", context=context)


def generic(request):
    """View function for generic page of site."""
    context = {}
    return render(request, "generic.html", context=context)


def elements(request):
    """View function for site page with various design elements."""
    return render(request, "elements.html")


def media_detail_view(request, media_type, pk):
    print(
        f"\n--- DEBUG: media_detail_view CALLED for PK: {pk}, Type: {media_type} ---"
    )

    """View function for individual media detail views site."""
    media_instance = get_object_or_404(ProjectMedia, pk=pk)

    # Base context, always available
    context = {
        "projectmedia": media_instance,
        "media_type": media_type,
        "form": None,  # Will be overridden if a form is needed
    }

    if media_type == "html_demo":
        # Create a specific nested dictionary for interactive demo data
        interactive_demo_data = {
            "x_var_selected": None,
            "y_var_selected": None,
            "plotly_data": None,
            "form_error": None,  # For form-related errors
        }
        # Querying available columns in the data set
        available_columns = get_dataset_columns()
        print(f"DEBUG: all_dataset_columns: {available_columns}")
        if not available_columns:
            # This block will execute if get_kaggle_dataset_columns() returns an empty list
            print("DEBUG: all_dataset_columns is empty or not loaded.")
            all_dataset_columns = [
                "Year",
                "Adult Mortality",
            ]  # Fallback for form display
            interactive_demo_data["form_error"] = (
                "Could not load dataset columns for form. Using default placeholders."
            )

        # Update form field choices for this request
        XYChoiceForm.base_fields["x_variable"].choices = available_columns
        XYChoiceForm.base_fields["y_variable"].choices = available_columns

        # Setting default x and y columns
        default_x_var = available_columns[0][0] if available_columns else None
        default_y_var = (
            available_columns[1][0] if len(available_columns) > 1 else None
        )

        if request.method == "POST":
            # Creating form instance bound to input user data
            form = XYChoiceForm(request.POST, columns=available_columns)
            # If the form input is valid, clean and set the columns chosen
            if form.is_valid():
                x_variable = form.cleaned_data["x_variable"]
                y_variable = form.cleaned_data["y_variable"]

            else:
                interactive_demo_data["form_error"] = (
                    "Invalid form submission. Please select valid variables."
                )
                x_variable = default_x_var
                y_variable = default_y_var

        else:  # GET request for "html_0emo"
            form = XYChoiceForm(columns=available_columns)
            # Set the x and y variables to be the default, defined above
            x_variable = default_x_var
            y_variable = default_y_var

        interactive_demo_data["x_var_selected"] = x_variable
        interactive_demo_data["y_var_selected"] = y_variable
        plotly_json, error = load_and_process_kaggle_data(
            x_variable, y_variable
        )
        interactive_demo_data["plotly_data"] = plotly_json

        context["form"] = form
        context["interactive_demo_data"] = interactive_demo_data

    elif media_type == "Image":
        # Specific context for image type, if needed
        context["form"] = None  # No form for images
        pass

    # I plan to add more media types as necessary, here

    """Need to return different templates for different media types, so that
    I can include all sorts of media and designs for different media"""
    template_name = f"catalog/projectmedia_detail_{media_type}.html"
    return render(request, template_name, context=context)
