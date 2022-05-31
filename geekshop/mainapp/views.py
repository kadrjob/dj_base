from django.shortcuts import render
import json
# Create your views here.

def index(request):
    context = {
        'user_list':[
            {
                'first_name' : 'Oleg',
                'last_name' : 'Maslov',
                'age' : 31
            },
            {
                'first_name': 'Ivan',
                'last_name': 'Ivanov',
                'age': 35
            }
        ]
    }
    return render(request, 'mainapp/index.html', context)

def products(request):
    links_menu = [
        {'href':'products_all', 'title':'все'},
        {'href': 'products_home', 'title': 'дом'},
        {'href': 'products_office', 'title': 'офис'},
        {'href': 'products_modern', 'title': 'модерн'},
        {'href': 'products_classic', 'title': 'классика'},
    ]

    context ={
        'links_menu':links_menu
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