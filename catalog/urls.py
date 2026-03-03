from django.urls import path
from .views import HomeListView, ContactsView, InfoProductDetailView, AddInfoCreateView, InfoProductDeleteView, AddInfoUpdateView

app_name = 'catalog'

urlpatterns = [
    path('', HomeListView.as_view(), name='home'),
    path('contacts/', ContactsView.as_view(), name='contact'),
    path('info_product/<int:pk>', InfoProductDetailView.as_view(), name='info_product'),
    path('add_info/', AddInfoCreateView.as_view(), name='add_info'),
    path('delete/<int:pk>', InfoProductDeleteView.as_view(), name='delete'),
    path('update/<int:pk>', AddInfoUpdateView.as_view(), name='update'),
]