from django.urls import path
from . import views

app_name = 'catalog'

urlpatterns = [
    path('', views.home, name='home'),
    path('contacts/', views.show_contact, name='contact'),
    path('info_product/<int:product_id>', views.info_product, name='info_product')
]