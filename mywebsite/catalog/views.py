from django.shortcuts import render
from .models import Person, Project, Technology, Skill, ProjectImage
from django.views import generic

# Create your views here.


def home(request):
    """View function for home page of site."""
    # Getting my Object
    Me_Object = Person.objects.get(first_name="Fenton")
    # Providing contact info
    email = Me_Object.email
    phone = Me_Object.phone
    location = Me_Object.location

    context = {"email": email, "phone": phone, "location": location}

    # Render the HTML template index.html with the data in the context variable
    return render(request, "home.html", context=context)


def resume(request):
    # Getting my Object
    Me_Object = Person.objects.get(first_name="Fenton")
    # Providing contact info
    email = Me_Object.email
    phone = Me_Object.phone
    location = Me_Object.location

    context = {"email": email, "phone": phone, "location": location}

    # Render the HTML template index.html with the data in the context variable
    return render(request, "resume.html", context=context)


def projects_page(request):
    # Getting my Object
    project_list = Project.objects.all()

    context = {"project_list": project_list}

    # Render the HTML template index.html with the data in the context variable
    return render(request, "project_list.html", context=context)


class project_detail_view(generic.DetailView):
    model = Project


def landing(request):
    return render(request, "landing.html")


def generic(request):
    # Getting my Object
    Me_Object = Person.objects.get(first_name="Fenton")
    # Providing contact info
    email = Me_Object.email
    phone = Me_Object.phone
    location = Me_Object.location

    context = {"email": email, "phone": phone, "location": location}

    # Render the HTML template index.html with the data in the context variable
    return render(request, "generic.html", context=context)


def elements(request):
    return render(request, "elements.html")
