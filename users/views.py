import random
from django.conf import settings
from django.contrib.auth.views import PasswordChangeView
from django.core.mail import send_mail
from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import CreateView, UpdateView
from django.contrib.auth.models import User
from users.forms import RegistrationForm, UserProfileForm, UserPasswordChangeForm
from users.models import User


class RegisterView(CreateView):
    model = User  # Используем модель User
    form_class = RegistrationForm  # Используем форму RegistrationForm
    template_name = 'users/register.html'  # Используем шаблон register.html
    success_url = reverse_lazy('users:code')  # URL для успешной регистрации

    def form_valid(self, form):
        # Генерируем случайный код верификации
        new_pass = ''.join([str(random.randint(0, 9)) for _ in range(9)])
        new_user = form.save(commit=False)
        new_user.ver_code = new_pass  # Присваиваем код верификации новому пользователю
        new_user.save()

        # Отправляем письмо с кодом верификации
        send_mail(
            subject='Подтверждение почты',
            message=f'Код {new_user.ver_code}',
            from_email=settings.EMAIL_HOST_USER,
            recipient_list=[new_user.email]
        )

        return super().form_valid(form)  # Валидация формы


class CodeView(View):
    model = User  # Используем модель User
    template_name = 'users/code.html'  # Используем шаблон code.html

    def get(self, request):
        return render(request, self.template_name)  # Отображаем страницу с формой ввода кода

    def post(self, request):
        code = request.POST.get('code')  # Получаем код из POST запроса
        user = User.objects.filter(ver_code=code).first()  # Получаем пользователя с данным кодом

        if user is not None:
            user.is_active = True  # Активируем пользователя
            user.save()
            return redirect('users:login')  # Перенаправляем на страницу входа

        else:
            return redirect('users:code')  # Перенаправляем на страницу с кодом для повторного ввода


class ProfileView(UpdateView):
    model = User  # Используем модель User
    form_class = UserProfileForm  # Используем форму UserProfileForm
    success_url = reverse_lazy('users:profile')  # URL для успешного обновления профиля
    extra_context = {'default_image': settings.DEFAULT_USER_IMAGE}  # Дополнительный контекст для шаблона

    def get_object(self, queryset=None):
        return self.request.user  # Получаем текущего пользователя

    def form_valid(self, form):
        # Сохраняем изображение профиля, если оно было загружено
        if form.cleaned_data.get('avatar'):
            self.request.user.avatar = form.cleaned_data['avatar']
            self.request.user.save()

        return super().form_valid(form)  # Валидация формы


class UserPasswordChange(PasswordChangeView):
    form_class = UserPasswordChangeForm  # Используем форму UserPasswordChangeForm
    success_url = reverse_lazy("users:password_change_done")  # URL для успешного изменения пароля
    template_name = "users/password_change_form.html"  # Используем шаблон password_change_form.html