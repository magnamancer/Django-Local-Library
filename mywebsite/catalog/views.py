from django.shortcuts import render
from .models import Person, Project, Technology, Skill, ProjectMedia
from django.views import generic


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


class media_detail_view(generic.DetailView):
    """View function for individual media detail views site."""

    model = ProjectMedia


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
