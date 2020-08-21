import datetime

from django.shortcuts import render, get_object_or_404
from django.contrib import messages
from django.http import HttpResponseRedirect
from django.urls import reverse, reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.contrib.auth.decorators import permission_required
from django.views.generic import ListView, DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView

from .models import Author, Book, BookInstance, Genre
from .forms import RenewBookForm


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


class LoanedBooksAllUsersListView(LoginRequiredMixin, PermissionRequiredMixin, ListView):
    permission_required = 'catalog.can_mark_returned'
    model = BookInstance
    template_name = 'loaned_books_all_users_list.html'
    paginate_by = 10

    def get_queryset(self):
        return BookInstance.objects.filter(status__exact='o').order_by('due_back')


@permission_required('catalog.can_mark_returned')
def renew_book(request, pk):
    book_instance = get_object_or_404(BookInstance, pk=pk)

    if request.method == 'POST':
        form = RenewBookForm(request.POST)

        if form.is_valid():
            book_instance.due_back = form.cleaned_data['renewal_date']
            book_instance.save()

            return HttpResponseRedirect(reverse('all_books'))

    else:  # GET
        proposed_renewal_date = datetime.date.today() + datetime.timedelta(weeks=3)
        form = RenewBookForm(
            initial={'renewal_date': proposed_renewal_date})

    context = {
        'form': form,
        'book': book_instance,
    }

    return render(request, 'book_renewal.html', context)


class AuthorCreateView(CreateView):
    model = Author
    template_name = "author_form.html"
    fields = '__all__'


class AuthorUpdateView(UpdateView):
    model = Author
    template_name = "author_form.html"
    fields = ['first_name', 'last_name', 'date_of_birth', 'date_of_death']


class AuthorDeleteView(DeleteView):
    model = Author
    template_name = "author_confirm_delete.html"
    success_url = reverse_lazy('authors')


class BookCreateView(CreateView):
    model = Book
    template_name = "book_form.html"
    fields = '__all__'
    initial = {'title': '',
               'summary': '',
               'isbn': ''
               }


class BookUpdateView(UpdateView):
    model = Book
    template_name = "book_form.html"
    fields = '__all__'


class BookDeleteView(DeleteView):
    model = Book
    template_name = "book_confirm_delete.html"
    success_url = reverse_lazy('books')
