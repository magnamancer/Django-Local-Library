from .models import Person  # Import your Person model


def contact_info(request):
    """
    Returns contact information for Fenton Clawson to be available in all templates.
    """
    me_object = Person.objects.get(first_name="Fenton")
    email = me_object.email
    phone = me_object.phone
    location = me_object.location

    # Return a dictionary of context variables
    return {
        "email": email,
        "phone": phone,
        "location": location,
    }
