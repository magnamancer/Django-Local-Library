from django import forms

class XYChoiceForm(forms.Form):
    x_variable = forms.ChoiceField(label="X-Axis Variable")
    y_variable = forms.ChoiceField(label="Y-Axis Variable")

    def __init__(self, *args, **kwargs):
        # Pop the 'columns' argument before calling the superclass constructor
        # This is because forms.Form.__init__ doesn't expect a 'columns' kwarg
        columns = kwargs.pop("columns", [])
        super().__init__(*args, **kwargs)

        # Create choices list from the columns (e.g., [('column_name', 'Column Name')])
        # Using .replace('_', ' ').title() for cleaner display in dropdown
        column_choices = [
            (col, col.replace("_", " ").title()) for col in columns
        ]

        # Set the choices for the fields
        self.fields["x_variable"].choices = column_choices
        self.fields["y_variable"].choices = column_choices
