from django.shortcuts import render

from .models import Author, Book, BookInstance, Genre


def catalog(request):
    # View function for home page of site.

    # Generate counts of some of the main objects
    number_of_books = Book.objects.all().count()
    number_of_instances = BookInstance.objects.all().count()

    # Available books
    number_of_available_instances = BookInstance.objects.filter(
        status__exact='a').count()

    number_of_authors = Author.objects.count()

    context = {
        'number_of_books': number_of_books,
        'number_of_instances': number_of_instances,
        'number_of_available_instances': number_of_available_instances,
        'number_of_authors': number_of_authors,
    }

    return render(request, 'catalog.html', context=context)
