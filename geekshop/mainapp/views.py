from django.shortcuts import render
import json
from mainapp.models import Product, Category

# Create your views here.

def index(request):
    context = {
        'products': Product.objects.all()
    }
    return render(request, 'mainapp/index.html', context)

def products(request):
    context ={
        'links_menu': Category.objects.all()
    }

    return render(request, 'mainapp/products.html', context)

def contact(request):

    with open('static/contact_data.json', encoding='UTF8') as f:
        file_content = f.read()
        addr_data = json.loads(file_content)['data']

    context = {
        'addr_data': addr_data
    }
    return render(request, 'mainapp/contact.html', context)

def products_list(request, pk):
    context = {
        'links_menu': Category.objects.all()
    }
    return render(request, 'mainapp/products.html', context)


