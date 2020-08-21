from django.urls import path
from . import views

urlpatterns = [
    path('', views.catalog, name='catalog'),
    path('books/', views.BookListView.as_view(), name='books'),
    path('book/<int:pk>', views.BookDetailView.as_view(), name='book_detail'),
    path('book/<uuid:pk>/renew/', views.renew_book, name='renew_book'),
    path('mybooks/', views.LoanedBooksCurrentUserListView.as_view(), name='my_books'),
    path('allbooks/', views.LoanedBooksAllUsersListView.as_view(), name='all_books'),
    path('authors/', views.AuthorListView.as_view(), name='authors'),
    path('author/<int:pk>', views.AuthorDetailView.as_view(), name='author_detail'),
    path('author/create/', views.AuthorCreateView.as_view(), name='author_create'),
    path('author/<int:pk>/update/',
         views.AuthorUpdateView.as_view(), name='author_update'),
    path('author/<int:pk>/delete/',
         views.AuthorDeleteView.as_view(), name='author_delete'),
    path('book/create/', views.BookCreateView.as_view(), name='book_create'),
    path('book/<int:pk>/update/',
         views.BookUpdateView.as_view(), name='book_update'),
    path('book/<int:pk>/delete/',
         views.BookDeleteView.as_view(), name='book_delete'),
]
