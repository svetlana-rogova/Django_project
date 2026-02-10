from django.shortcuts import render
from django.http import HttpResponse

from catalog.models import Product, Contacts


def home(request):
    latest_products = Product.objects.order_by('-created_at')[:5]
    for p in latest_products:
        print(p.name)
    return render(request, 'catalog/home.html', {'latest_products': latest_products})

def contacts(request):
    if request.method == 'POST':
        name = request.POST.get("name")
        phone = request.POST.get("phone")
        message = request.POST.get("message")

        return HttpResponse(f"Спасибо {name}! Сообщение получено")
    return render(request, 'catalog/contacts.html')

def show_contact(request):
    contact=Contacts.objects.first()
    return render(request, 'catalog/contacts.html', {'contact': contact})