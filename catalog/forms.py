from django import forms
from .models import Product
from django.core.exceptions import ValidationError
from PIL import Image
from django.conf import settings



class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        exclude = ['owner']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['name'].widget.attrs.update({'class':'form-control', 'placeholder':'Введите название'})
        self.fields['description'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Введите описание'})
        self.fields['image'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Добавьте изображение'})
        self.fields['category'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Выберите категорию'})
        self.fields['purchase_price'].widget.attrs.update({'class': 'form-control','type': 'number', 'placeholder': 'Укажите стоимость'})
        self.fields['is_published'].widget.attrs.update({'class': 'form-check-input'})


    def clean_name(self):
        name = self.cleaned_data.get('name')
        for word in settings.FORBIDDEN_WORDS:
            if name and word in name.lower():
                raise ValidationError(f'Слово "{word}" запрещено.')
        return name

    def clean_description(self):
        description = self.cleaned_data.get('description')
        for word in settings.FORBIDDEN_WORDS:
            if description and word in description.lower():
                raise ValidationError(f'Слово "{word}" запрещено.')
        return description

    def clean_purchase_price(self):
        purchase_price = self.cleaned_data.get('purchase_price')
        if purchase_price < 0:
            raise ValidationError('Стоимость товара не может быть отрицательной')
        return purchase_price

    def clean_image(self):
        image = self.cleaned_data.get('image')
        if image.size > 5 * 1024 * 1024:
            raise ValidationError('Размер изображения не должен превышать 5 МБ')
        img = Image.open(image)
        if img.format not in settings.VALID_FORMATS_IMAGE:
            raise ValidationError('Файл должен иметь формат JPEG или PNG')
        return image

