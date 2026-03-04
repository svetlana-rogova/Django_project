from django.shortcuts import render
from django.http import HttpResponse
from catalog.forms import ProductForm
from catalog.models import Product, Contacts
from django.views.generic import ListView, DetailView, UpdateView
from django.views.generic.edit import CreateView, DeleteView
from django.views import View
from django.urls import reverse_lazy


class HomeListView(ListView):
    model = Product
    template_name = 'catalog/home.html'
    context_object_name = 'posts'
    paginate_by = 3

    def get_queryset(self):
        return Product.objects.filter(is_published= True )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['latest_products'] = Product.objects.order_by('-created_at')[:5]
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


class InfoProductDetailView(DetailView):
    model = Product
    template_name = 'catalog/info_product.html'
    context_object_name = 'product'


class InfoProductDeleteView(DeleteView):
    model = Product
    template_name = 'catalog/info_product_confirm_delete.html'
    success_url = reverse_lazy('catalog:home')

class AddInfoCreateView(CreateView):
    model = Product
    form_class = ProductForm
    template_name = 'catalog/add_info.html'

    def form_valid(self, form):
        self.object = form.save()
        return HttpResponse(f"Спасибо! В каталог добавлен новый товар: {self.object.name}")

class AddInfoUpdateView(UpdateView):
    model = Product
    form_class = ProductForm
    template_name = 'catalog/add_info.html'
    success_url = reverse_lazy('catalog:home')

