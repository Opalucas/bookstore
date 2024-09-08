from django.shortcuts import render
from django.http import JsonResponse
import requests
from .models import Order, Addres
from dotenv import load_dotenv
import os
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from django.contrib.auth.models import User
from django.views.decorators.csrf import csrf_exempt
from django.utils.dateparse import parse_datetime
import json

load_dotenv()

API_KEY = os.getenv("API_KEY")
API_URL = os.getenv("API_URL")

def home(request):
    return render(request, 'home.html')

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

@csrf_exempt
def user_orders(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            user_id = data.get('user_id')
            
            if not user_id:
                return JsonResponse({"error": "Parâmetro user_id ausente"}, status=400)
            
            try:
                user = User.objects.get(id=user_id)
            except User.DoesNotExist:
                return JsonResponse({"error": "Usuário não encontrado"}, status=404)
            
            orders = Order.objects.filter(user=user)

            response_data = []

            for order in orders:
                response_data.append({
                    'data': order.data,
                    'product': order.product,
                    'quantity': order.quantity,
                    'unit_price': str(order.unit_price),
                    'total_price': str(order.total_price)
                })

            return JsonResponse(response_data, status=200, safe=False)
        
        except json.JSONDecodeError:
            return JsonResponse({"error": "Erro ao decodificar o JSON"}, status=400)
    
    else:
        return JsonResponse({'error': 'Only POST method allowed'}, status=405)

@csrf_exempt
def checkout(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            user_id = data.get('user_id')
            items = data.get('items')

            try:
                user = User.objects.get(id=user_id)
            except User.DoesNotExist:
                return JsonResponse({"error": "Usuário não encontrado"}, status=404)

            if items and isinstance(items, list):
                for item in items:
                    product = item.get('product')
                    quantity = item.get('quantity')
                    unit_price = item.get('unit_price')
                    total_price = item.get('total_price')
                    item_data = item.get('data')

                    try:
                        order_date = parse_datetime(item_data)
                        if order_date is None:
                            raise ValueError("Data inválida")
                    except (ValueError, TypeError):
                        return JsonResponse({"error": "Formato de data inválido"}, status=400)

                    Order.objects.create(
                        user=user,
                        product=product,
                        quantity=quantity,
                        unit_price=unit_price,
                        total_price=total_price,
                        data=order_date
                    )
                
                return JsonResponse({"success": "Compra finalizada com sucesso"}, status=200)
            else:
                return JsonResponse({"error": "Erro ao processar itens do carrinho"}, status=400)

        except json.JSONDecodeError:
            return JsonResponse({"error": "Erro ao decodificar o JSON"}, status=400)
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)

    else:
        return JsonResponse({"error": "Only POST method allowed"}, status=405)

@csrf_exempt
def create_user(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            firstname = data.get('firstname')
            lastname = data.get('lastname')
            email = data.get('email')
            password = data.get('password')
            street = data.get('street')
            neighborhood = data.get('neighborhood')
            city = data.get('city')
            number = data.get('number')
            
            if not (firstname and lastname and email and password and street and neighborhood and city):
                return JsonResponse({'error': 'Preencha todos os campos obrigatórios'}, status=400)
            
            address = Addres.objects.create(
                street=street,
                neighborhood=neighborhood,
                city=city,
                number=number
            )
            
            user = User.objects.create_user(
                username=email,
                email=email,
                password=password,
                first_name=firstname,
                last_name=lastname
            )
            
            return JsonResponse({'message': 'Usuário criado com sucesso', 'user_id': user.id, 'email': user.email}, status=201)
        except json.JSONDecodeError:
            return JsonResponse({'error': 'Verifique os dados enviados na consulta'}, status=400)
    else:
        return JsonResponse({'error': 'Only POST method allowed'}, status=405)
    
@csrf_exempt
def login(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            username = data.get('username')
            password = data.get('password')
            
            user = authenticate(request, username=username, password=password)
            if user is not None:
                auth_login(request, user)

                response_data = {
                    'message': 'Login successful',
                    'user_id': user.id,
                    'username': user.username,
                    'email': user.email
                }
                return JsonResponse(response_data, status=200)
            else:
                return JsonResponse({'error': 'Invalid credentials'}, status=401)
        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON'}, status=400)
    else:
        return JsonResponse({'error': 'Only POST method allowed'}, status=405)   
    
@csrf_exempt
def logout_user(request):
    if request.method == 'POST':
        try:
            auth_logout(request) 
            return JsonResponse({'message': 'Logout successful'}, status=200)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)
    else:
        return JsonResponse({'error': 'Only POST method allowed'}, status=405)