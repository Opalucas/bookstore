from django.shortcuts import render, redirect
import requests
from .models import Book, Cart, Buy

def home(request):
    return render(request, 'home.html')

def get_books(query):
    url = f'https://www.googleapis.com/books/v1/volumes?q={query}'
    response = requests.get(url)
    dados = response.json()
    return dados['items'] if 'items' in dados else []

def list_books(request):
    books = Book.objects.all()
    return render(request, 'books.html', {'books': books})

def add_to_cart(request, book_id):
    book = Book.objects.get(id=book_id)
    cart, created = Cart.objects.get_or_create(user=request.user)
    cart.livros.add(book)
    return redirect('list_books')

def finish_buy(request):
    cart = Cart.objects.get(user=request.user)
    buy = Buy.objects.create(user=request.user)
    buy.livros.set(cart.livros.all())
    buy.total = sum(livro.preco for livro in cart.livros.all())
    buy.save()
    cart.livros.clear() 
    return redirect('historico_compras')

def history(request):
    sells = Buy.objects.filter(user=request.user)
    return render(request, 'history.html', {'sells': sells})
