from django.shortcuts import render
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView, DetailView

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

    # Number of visits to this view, as counted in the session variable.
    number_of_visits = request.session.get('number_of_visits', 1)
    request.session['number_of_visits'] = number_of_visits + 1

    context = {
        'number_of_books': number_of_books,
        'number_of_instances': number_of_instances,
        'number_of_available_instances': number_of_available_instances,
        'number_of_authors': number_of_authors,
        'number_of_visits': number_of_visits,
    }

    return render(request, 'catalog.html', context=context)


class BookListView(ListView):
    model = Book
    template_name = 'book_list.html'
    paginate_by = 10


class BookDetailView(DetailView):
    model = Book
    template_name = 'book_detail.html'


class AuthorListView(ListView):
    model = Author
    template_name = 'author_list.html'


class AuthorDetailView(DetailView):
    model = Author
    template_name = 'author_detail.html'


class LoanedBooksCurrentUserListView(LoginRequiredMixin, ListView):
    model = BookInstance
    template_name = 'loaned_books_current_user_list.html'
    paginate_by = 10

    def get_queryset(self):
        return BookInstance.objects.filter(borrower=self.request.user).filter(status__exact='o').order_by('due_back')
