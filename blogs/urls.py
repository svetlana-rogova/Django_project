from django.urls import path
from .views import BlogListView, BlogUpdateView, BlogDetailView, BlogCreateView, BlogDeleteView

app_name = 'blogs'

urlpatterns = [
    path('list/', BlogListView.as_view(), name='blogs_list'),
    path('update/<int:pk>/', BlogUpdateView.as_view(), name='blog_update'),
    path('detail/<int:pk>/', BlogDetailView.as_view(), name='blog_detail'),
    path('', BlogCreateView.as_view(), name='blog_form'),
    path('delete/<int:pk>/', BlogDeleteView.as_view(), name='blog_delete'),
]