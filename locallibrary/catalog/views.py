from django.shortcuts import render
from .models import Book, Author, BookInstance, Genre
from django.views import generic


# Create your views here.
def index(request):
    """View function for home page of site."""

    # Generate counts of some of the main objectss
    num_books = Book.objects.all().count()
    num_instances = BookInstance.objects.all().count()
    genres = Genre.objects.all().count()
    his_counter = Book.objects.filter(title__icontains="His").count()

    # Available books (status = 'a')
    num_instances_available = BookInstance.objects.filter(
        status__exact="a"
    ).count()

    # The 'all()' is implied by default.
    num_authors = Author.objects.count()

    context = {
        "num_books": num_books,
        "num_instances": num_instances,
        "num_instances_available": num_instances_available,
        "num_authors": num_authors,
        "genres": genres,
        "his_counter": his_counter,
    }

    # Render the HTML template index.html with the data in the context variable
    return render(request, "index.html", context=context)


class BookListView(generic.ListView):
    model = Book
    paginate_by = 10


class BookDetailView(generic.DetailView):
    model = Book


class AuthorListView(generic.ListView):
    model = Author
    paginate_by = 10


class AuthorDetailView(generic.DetailView):
    model = Author
