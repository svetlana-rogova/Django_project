from django.urls import reverse_lazy
from django.views.generic.edit import CreateView
from .forms import CustomUserCreationForm
from django.core.mail import send_mail


class RegisterView(CreateView):
    template_name = 'users/register.html'
    form_class = CustomUserCreationForm
    success_url = reverse_lazy('catalog:home')

    def form_valid(self, form):
        user = form.save()
        self.send_welcome_email(user.email)
        return super().form_valid(form)

    def send_welcome_email(self, user_email):
        subject = 'Добро пожаловать'
        massage = 'Спасибо, что зарегистрировались на нашем сайте'
        from_email = 'mifistofiya@gmail.com'
        recipient_list = [user_email]
        send_mail(subject, massage, from_email, recipient_list)