from django.contrib import admin

from catalog.models import Category, Product, Contacts


@admin.register(Category)
class CatalogAdmin(admin.ModelAdmin):
    list_display = ('id', 'name',)
    list_filter = ('name',)
    search_fields = ('name',)


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'purchase_price', 'image', 'category', 'created_at', 'updated_at')
    list_filter = ('category',)
    search_fields = ('name', 'description',)


@admin.register(Contacts)
class ContactsAdmin(admin.ModelAdmin):
    list_display = ('phone', 'email')
