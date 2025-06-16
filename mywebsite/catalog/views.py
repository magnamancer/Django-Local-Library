from django.shortcuts import render
from .models import Person, Project, Technology, Skill, ProjectImage

# Create your views here.


def home(request):
    """View function for home page of site."""

    # # Generate counts of some of the main objects
    # num_books = Book.objects.all().count()
    # num_instances = BookInstance.objects.all().count()

    # # Available books (status = 'a')
    # num_instances_available = BookInstance.objects.filter(
    #     status__exact="a"
    # ).count()

    # # The 'all()' is implied by default.
    # num_authors = Author.objects.count()

    # context = {
    #     "num_books": num_books,
    #     "num_instances": num_instances,
    #     "num_instances_available": num_instances_available,
    #     "num_authors": num_authors,
    # }

    # Render the HTML template index.html with the data in the context variable
    return render(request, "home.html")  # , context=context)


def landing(request):
    return render(request, "landing.html")


def generic(request):
    return render(request, "generic.html")


def elements(request):
    return render(request, "elements.html")
