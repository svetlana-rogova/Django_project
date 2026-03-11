from django.contrib import admin

from blogs.models import Blog


@admin.register(Blog)
class BlogAdmin(admin.ModelAdmin):
    list_display = ('heading', 'content', 'created_at',)
    list_filter = ('heading',)
    search_fields = ('heading',)
