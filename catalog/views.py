from functools import cache

from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from catalog.forms import ProductForm
from catalog.models import Product, Contacts, Category
from django.views.generic import ListView, DetailView, UpdateView
from django.views.generic.edit import CreateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import View
from django.urls import reverse_lazy
from django.http import HttpResponseForbidden
from django.contrib import messages
from django.core.cache import cache
from django.views.decorators.cache import cache_page
from django.utils.decorators import method_decorator

from catalog.services import get_products


class UnpublishProductView(LoginRequiredMixin, View):
    def post(self, request, pk):
        product = get_object_or_404(Product, id=pk)

        if not request.user.has_perm('catalog.can_unpublish_product'):
            return HttpResponseForbidden('У вас нет права для отмены публикации')

        product.unpublish = True
        product.save()
        return redirect('catalog:info_product', pk=pk)


class HomeListView(ListView):
    model = Product
    template_name = 'catalog/home.html'
    context_object_name = 'posts'
    paginate_by = 3

    def get_queryset(self):
        user = self.request.user
        queryset = cache.get('product_queryset')
        if not queryset:
            if user.is_superuser or user.has_perm('catalog.can_unpublish_product'):
                queryset = Product.objects.all().order_by('-created_at')
            else:
                queryset = Product.objects.filter(is_published= True )
            cache.set('product_queryset', queryset, 60 * 15)
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['latest_products'] = Product.objects.order_by('-created_at')[:5]
        context['categories'] = Category.objects.all()
        for p in context['latest_products']:
            print(p.name)
        return context



class ContactsView(View):
    template_name = 'catalog/contacts.html'

    def get(self, request):
        contact = Contacts.objects.first()
        return render(request, self.template_name, {'contact': contact})

    def post(self, request):
        name = request.POST.get('name')
        phone = request.POST.get('phone')
        message = request.POST.get('message')

        return HttpResponse(f"Спасибо {name}! Сообщение получено")

@method_decorator(cache_page(60 * 15), name='dispatch')
class InfoProductDetailView(LoginRequiredMixin, DetailView):
    model = Product
    template_name = 'catalog/info_product.html'
    context_object_name = 'product'


class InfoProductDeleteView(LoginRequiredMixin, DeleteView):
    model = Product
    template_name = 'catalog/info_product_confirm_delete.html'
    success_url = reverse_lazy('catalog:home')

    def get_queryset(self):
        user = self.request.user
        if user.is_superuser or user.has_perm('catalog.delete_product'):
            return Product.objects.all()
        return Product.objects.filter(owner=user)

class AddInfoCreateView(LoginRequiredMixin, CreateView):
    model = Product
    form_class = ProductForm
    template_name = 'catalog/add_info.html'
    success_url = reverse_lazy('catalog:home')

    def form_valid(self, form):
        form.instance.owner = self.request.user
        response = super().form_valid(form)
        messages.success(self.request, f"Спасибо! В каталог добавлен новый товар: {self.object.name}")
        return response

class AddInfoUpdateView(LoginRequiredMixin, UpdateView):
    model = Product
    form_class = ProductForm
    template_name = 'catalog/add_info.html'
    success_url = reverse_lazy('catalog:home')

    def get_queryset(self):
        user = self.request.user
        if  user.is_superuser or user.has_perm('catalog.update_product') or user.has_perm('catalog.can_unpublish_product'):
            return Product.objects.all()
        return Product.objects.filter(owner=user)

class CategoryProductListView(LoginRequiredMixin, ListView):
    template_name = 'catalog/category_product.html'
    context_object_name = 'products'
    paginate_by = 3

    def get_queryset(self):
        category_name = self.kwargs.get('category')
        user = self.request.user
        cache_key = f'product_queryset_{category_name}_{user.id}'
        queryset = cache.get(cache_key)
        if not queryset:
            list_product = get_products(category_name)
            if user.is_superuser or user.has_perm('catalog.can_unpublish_product'):
                queryset = list_product.order_by('-created_at')
            else:
                queryset = list_product.filter(is_published=True).order_by('-created_at')
            cache.set(cache_key, queryset, 60 * 15)
        return queryset


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        category_name = self.kwargs.get('category')
        context['category'] = Category.objects.get(name=category_name)
        return context
