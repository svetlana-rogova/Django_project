from .models import Blog
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic import ListView, DetailView
from django.urls import reverse_lazy, reverse
from django.core.mail import send_mail
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect, get_object_or_404
from django.http import Http404


class BlogListView(ListView):
    model = Blog
    template_name = 'blogs/blogs_list.html'
    context_object_name = 'blogs'

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.filter(published=True)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['can_edit'] = self.request.user.groups.filter(name='Контент-менеджер').exists() or self.request.user.is_superuser
        return context

class BlogCreateView(LoginRequiredMixin, CreateView):
    model = Blog
    fields = ['heading', 'content', 'image', 'published']
    template_name = 'blogs/blog_form.html'
    success_url = reverse_lazy('blogs:blogs_list')

    def dispatch(self, request, *args, **kwargs):
        if not request.user.groups.filter(name='Контент-менеджер').exists() and not request.user.is_superuser:
            return redirect('blogs:blogs_list')
        return super().dispatch(request, *args, **kwargs)

class BlogUpdateView(LoginRequiredMixin, UpdateView):
    model = Blog
    fields = ['heading', 'content', 'image', 'published']
    template_name = 'blogs/blog_form.html'

    def get_object(self, queryset=None):
        obj = get_object_or_404(Blog, pk=self.kwargs['pk'])
        if not self.request.user.groups.filter(name='Контент-менеджер').exists() and not self.request.user.is_superuser:
            raise Http404("Нет доступа к этой статье")
        return obj

    def get_success_url(self):
        return reverse('blogs:blog_detail', kwargs={'pk': self.object.pk})

class BlogDetailView(LoginRequiredMixin, DetailView):
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

class BlogDeleteView(LoginRequiredMixin, DeleteView):
    model = Blog
    template_name = 'blogs/blog_confirm_delete.html'
    success_url = reverse_lazy('blogs:blogs_list')

    def get_object(self, queryset=None):
        obj = get_object_or_404(Blog, pk=self.kwargs['pk'])
        if not self.request.user.groups.filter(name='Контент-менеджер').exists() and not self.request.user.is_superuser:
            raise Http404("Нет доступа к этой статье")
        return obj
