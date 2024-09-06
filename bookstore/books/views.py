from django.shortcuts import render, redirect
from django.http import JsonResponse
import requests
from .models import Book, Cart, Sel
from dotenv import load_dotenv
import os

load_dotenv()

API_KEY = os.getenv("API_KEY")
API_URL = os.getenv("API_URL")

def home(request):
    return render(request, 'home.html')

def finish_buy(request):
    cart = Cart.objects.get(user=request.user)
    sel = Sel.objects.create(user=request.user)
    sel.livros.set(cart.livros.all())
    sel.total = sum(livro.preco for livro in cart.livros.all())
    sel.save()
    cart.livros.clear() 
    return redirect('historico_compras')

def history(request):
    sels = Sel.objects.filter(user=request.user)
    return render(request, 'history.html', {'sells': sels})


def search_books(request):
    category = request.GET.get('category', '')
    title = request.GET.get('title', '')
    author = request.GET.get('author', '')
    for_sale = request.GET.get('for_sale', '')

    if not category and not title and not author:
        return JsonResponse({"message": "Parametos de pesquisa não informados"}, safe=False, status=400)

    query_params = []

    if category:
        query_params.append(f"subject:{category}")
    if title:
        query_params.append(f"intitle:{title}")
    if author:
        query_params.append(f"inauthor:{author}")

    query_string = '+'.join(query_params)
    full_url = f'{API_URL}volumes?q={query_string}&key:{API_KEY}'

    response = requests.get(full_url)
    

    if response.status_code == 200:
        data = response.json()

        if(for_sale and for_sale == '1'):
            books_for_sale = [book for book in data.get('items', []) if book.get('saleInfo', {}).get('saleability') == 'FOR_SALE']
            response_data = {
                "totalItems": len(books_for_sale),
                "items": books_for_sale
            }
            
            return JsonResponse(response_data, safe=False, status=200)
        
        return JsonResponse(data, safe=False)
    else:
        return JsonResponse({"error": "Erro ao acessar a API"}, status=500)
    
def book_detail(request, book_id):
    if not book_id:
        return JsonResponse({"message": "Parametos de pesquisa não informados"}, safe=False, status=400)
    
    response = requests.get(f'{API_URL}volumes/{book_id}')
    
    if response.status_code == 200:
        data = response.json()
        return JsonResponse(data, safe=False)
    else:
        return JsonResponse({"error": "Livro não encontrado"}, status=404)


def books_for_home(request):
    
    response = requests.get(f'{API_URL}volumes?q=*&maxResults=40')
    
    if response.status_code == 200:
        data = response.json()
        
        books_for_sale = [book for book in data.get('items', []) if book.get('saleInfo', {}).get('saleability') == 'FOR_SALE']
        response_data = {
            "totalItems": len(books_for_sale),
            "items": books_for_sale
        }
            
        return JsonResponse(response_data, safe=False, status=200)
    else:
        return JsonResponse({"error": "Erro ao acessar a API do Google Books"}, status=500)