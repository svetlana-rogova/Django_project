from .models import Product


def get_products(category_name):
    return Product.objects.filter(category__name = category_name)