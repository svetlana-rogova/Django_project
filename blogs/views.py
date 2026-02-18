from .models import Blog
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic import ListView, DetailView
from django.urls import reverse_lazy, reverse
from django.core.mail import send_mail

class BlogListView(ListView):
    model = Blog
    template_name = 'blogs/blogs_list.html'
    context_object_name = 'blogs'

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.filter(published=True)

class BlogCreateView(CreateView):
    model = Blog
    fields = ['heading', 'content', 'image', 'published']
    template_name = 'blogs/blog_form.html'
    success_url = reverse_lazy('blogs:blogs_list')

class BlogUpdateView(UpdateView):
    model = Blog
    fields = ['heading', 'content', 'image', 'published']
    template_name = 'blogs/blog_form.html'

    def get_success_url(self):
        return reverse('blogs:blog_detail', kwargs={'pk': self.object.pk})

class BlogDetailView(DetailView):
    model = Blog
    template_name = 'blogs/blog_detail.html'
    context_object_name = 'blog'

    def get_object(self, queryset=None):
        obj = super().get_object(queryset)
        obj.count_views += 1
        obj.save(update_fields=['count_views'])
        if obj.count_views == 100:
            send_mail(
                subject=f'Информация о блоге',
                message=f'Статья "{obj.heading}" набрала {obj.count_views} просмотров. Ура!',
                from_email=None,
                recipient_list=['mifistofiya@gmail.com'],
                fail_silently=False,
            )

        return obj

class BlogDeleteView(DeleteView):
    model = Blog
    template_name = 'blogs/blog_confirm_delete.html'
    success_url = reverse_lazy('blogs:blogs_list')
