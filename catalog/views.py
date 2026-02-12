from django.shortcuts import render
from django.http import HttpResponse
from django.core.paginator import Paginator
from catalog.models import Product, Contacts, Category, ProductForm


def home(request):
    latest_products = Product.objects.order_by('-created_at')[:5]
    products = Product.objects.all()

    paginator = Paginator(products, 3)
    page_number = request.GET.get('page', 1)
    posts = paginator.page(page_number)

    for p in latest_products:
        print(p.name)
    return render(request, 'catalog/home.html', {'latest_products': latest_products,  'posts': posts})


def contacts(request):
    contact = Contacts.objects.first()
    if request.method == 'POST':
        name = request.POST.get("name")
        phone = request.POST.get("phone")
        message = request.POST.get("message")

        return HttpResponse(f"Спасибо {name}! Сообщение получено")
    return render(request, 'catalog/contacts.html', {'contact': contact} )


def info_product(request, product_pk):
    product=Product.objects.get(pk=product_pk)
    return render(request, 'catalog/info_product.html', {'product': product})


def add_info(request):
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return HttpResponse(f"Спасибо! В каталог добавлен новый товар.")
    else:
        form = ProductForm()
    return render(request, 'catalog/add_info.html', {'form': form})
