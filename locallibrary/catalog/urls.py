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
]
