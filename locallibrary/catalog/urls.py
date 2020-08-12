from django.urls import path
from . import views

urlpatterns = [
    path('', views.catalog, name='catalog'),
    path("books/", views.BookListView.as_view(), name="books"),
    path("book/<int:pk>", views.BookDetailView.as_view(), name="book_detail")
]
