from django.db import models
from django.urls import reverse
import uuid  # Required for unique book ids
from django.contrib.auth.models import User
from datetime import date


class Author(models.Model):
    # Model representing an author.
    first_name = models.CharField(max_length=100, default='')
    last_name = models.CharField(max_length=100, default='')
    date_of_birth = models.DateField(null=True, blank=True)
    date_of_death = models.DateField('Died', null=True, blank=True)

    class Meta:
        ordering = ['last_name', 'first_name']

    def get_absolute_url(self):
        return reverse('author_detail', kwargs={'pk': self.pk})

    def __str__(self):
        return f'{self.last_name}, {self.first_name}'


class Genre(models.Model):
    # Model representing a book genre
    name = models.CharField(
        max_length=200, help_text='Enter a book genre (e.g. Science Fiction')

    def __str__(self):
        return self.name


class Book(models.Model):
    # Model representing a book (but not a specific copy of a book)
    title = models.CharField(max_length=200)

    # Foreign Key used because book can only have one author, but authors can have multiple books
    author = models.ForeignKey(Author, on_delete=models.SET_NULL, null=True)

    summary = models.TextField(
        max_length=1000, help_text='Enter a brief description of the book')
    isbn = models.CharField(
        'ISBN', max_length=13, help_text='13 Character <a href="https://www.isbn-international.org/content/what-isbn">ISBN number</a>')

    genre = models.ManyToManyField(
        Genre, help_text='Select one or more genres for this book')

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        # Returns the url to access a detail record for this book.
        return reverse('book_detail', kwargs={'pk': self.pk})

    def display_genre(self):
        # Create a string for the Genre. This is required to display genre in Admin.
        return ', '.join(genre.name for genre in self.genre.all()[:3])

    display_genre.short_description = 'Genre'


class BookInstance(models.Model):
    # Model representing a specific copy of a book (i.e. that can be borrowed from the library).
    id = models.UUIDField(primary_key=True, default=uuid.uuid4,
                          help_text='Unique ID for this particular book across whole library')
    book = models.ForeignKey(Book, on_delete=models.SET_NULL, null=True)
    imprint = models.CharField(max_length=200)
    due_back = models.DateField(null=True, blank=True)

    LOAN_STATUS = (
        ('m', 'Maintenance'),
        ('o', 'On loan'),
        ('a', 'Available'),
        ('r', 'Reserved')
    )

    status = models.CharField(max_length=1, choices=LOAN_STATUS,
                              blank=True, default='m', help_text='Book availability')

    borrower = models.ForeignKey(
        User, on_delete=models.SET_NULL, null=True, blank=True)

    class Meta:
        ordering = ['due_back']
        permissions = (('can_mark_returned', 'Set book as returned'),)

    def __str__(self):
        return f'{self.id} ({self.book.title})'

    @property
    def is_overdue(self):
        return self.due_back and date.today() > self.due_back
