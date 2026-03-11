from django.db import models

from users.models import CustomUser


class Category(models.Model):
    name = models.CharField(max_length=150, verbose_name='Название')
    description = models.TextField(verbose_name='Описание')

    def __str__(self):
        return f'{self.name}'

    class Meta:
        verbose_name = 'категория'
        verbose_name_plural = 'категории'


class Product(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='products', verbose_name='Категория')
    name = models.CharField(max_length=150, verbose_name='Название')
    description = models.TextField()
    image = models.ImageField(upload_to='images/', verbose_name='Фотография')
    purchase_price = models.IntegerField(verbose_name='Цена')
    is_published = models.BooleanField(default=False, verbose_name="Опубликовать")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Дата изменения')
    owner = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='products', null=True, blank=True)


    def __str__(self):
        return f'{self.name} {self.description}'

    class Meta:
        verbose_name = 'продукт'
        verbose_name_plural = 'продукты'
        permissions = [
            ('can_unpublish_product', 'Can unpublish product'),
        ]


class Contacts(models.Model):
    phone = models.CharField(max_length=20, verbose_name='Номер телефона')
    email = models.EmailField(blank=True, verbose_name='Email')

    def __str__(self):
        return f'{self.phone}, {self.email}'


