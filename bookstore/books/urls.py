from django.urls import path
from . import views

urlpatterns = [
    path('books/', views.search_books, name='search_books'),
    path('books/<str:book_id>/', views.book_detail, name='book_detail'),
    path('home/', views.books_for_home, name='books_for_home'),
    
]