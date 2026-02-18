from django.db import models

class Blog(models.Model):
    heading = models.CharField(max_length=200, verbose_name='Заголовок')
    content = models.TextField(verbose_name='Содержимое')
    image = models.ImageField(upload_to='images/', verbose_name='Изображение')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')
    published = models.BooleanField(verbose_name='Признак публикации', default=True)
    count_views = models.IntegerField(verbose_name='Количество просмотров', default=0)

    def __str__(self):
        return f'{self.heading}'

    class Meta:
        verbose_name = 'публикация'
        verbose_name_plural = 'публикации'