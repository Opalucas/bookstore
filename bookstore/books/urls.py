from django.urls import path
from . import views

urlpatterns = [
    path('books/', views.search_books, name='search_books'),
    path('books/<str:book_id>/', views.book_detail, name='book_detail'),
    path('home/', views.books_for_home, name='books_for_home'),
    path('user-orders/', views.user_orders, name='user_orders'),
    path('checkout/', views.checkout, name='checkout'),
    path('login/', views.login, name='login'),
    path('create-user/', views.create_user, name='create_user'),
    path('logout-user/', views.logout_user, name='logout_user'),
]