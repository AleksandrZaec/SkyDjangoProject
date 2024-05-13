from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin, UserPassesTestMixin
from django.forms import inlineformset_factory
from django.http import Http404
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth.decorators import login_required

from product.forms import *
from product.models import *
from users.models import User


class ProductListView(LoginRequiredMixin, ListView):  # Определяем ListView для списка продуктов
    model = Product  # Указываем модель для ListView

    # Переопределяем метод get_context_data для добавления пользовательских данных контекста
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)  # Получаем стандартные данные контекста
        products = context['product_list']  # Получаем список продуктов из контекста

        # Создаем словарь с активными версиями для каждого продукта
        active_versions_per_product = {
            product.id: Version.objects.filter(product=product, active=True).first() for
            product in products
        }

        context['active_versions'] = active_versions_per_product  # Добавляем active_versions в контекст

        return context


class ProductDetailView(DetailView):  # Определяем DetailView для продуктов
    model = Product  # Указываем модель для DetailView


@login_required
def contacts(request):  # Определяем функцию представления для контактов
    if request.method == 'POST':  # Проверяем, если метод запроса POST
        form = ContactForm(request.POST)  # Создаем экземпляр формы с данными POST
        if form.is_valid():  # Проверяем, валидна ли форма
            # Получаем данные из формы
            first_name = request.POST.get('first_name')
            email = request.POST.get('email')
            question = request.POST.get('question')
            print(f'Имя: {first_name}, email: ({email}), Вопрос {question}')  # Печатаем данные из формы
            return redirect('product:contacts')  # Перенаправляем на URL 'product:contacts'
    else:
        form = ContactForm()  # Создаем пустой экземпляр формы

    return render(request, 'product/contacts.html', {'form': form})  # Рендерим шаблон contacts.html с формой


class ProductCreateView(LoginRequiredMixin, PermissionRequiredMixin, CreateView):  # Определяем CreateView для создания продуктов
    model = Product  # Указываем модель для CreateView
    form_class = ProductForm  # Указываем класс формы
    template_name = 'product/product_form.html'  # Указываем шаблон
    success_url = reverse_lazy('product:index')  # Указываем URL для успешного создания продукта
    permission_required = 'product.add_product'  # Указываем необходимое разрешение

    # Переопределяем метод get_context_data для добавления пользовательских данных контекста
    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)  # Получаем стандартные данные контекста
        VersionFormset = inlineformset_factory(Product, Version, form=VersionForm, extra=1)  # Создаем формсет
        if self.request.method == 'POST':  # Проверяем, если метод запроса POST
            context_data['formset'] = VersionFormset(self.request.POST)  # Создаем формсет с данными POST
        else:
            context_data['formset'] = VersionFormset()  # Создаем пустой формсет
            for form in context_data['formset']:
                if not self.request.user.is_staff:  # Если пользователь не является персоналом
                    form.fields['active'].widget = forms.HiddenInput()  # Скрываем поле 'active'

        return context_data

    # Переопределяем метод form_valid для обработки данных формы
    def form_valid(self, form):
        form.instance.user = self.request.user  # Устанавливаем пользователя
        self.object = form.save()  # Сохраняем форму
        formset = inlineformset_factory(Product, Version, form=VersionForm)(self.request.POST, instance=self.object)  # Создаем формсет
        if formset.is_valid():  # Проверяем, валиден ли формсет
            formset.save()  # Сохраняем формсет
            return super().form_valid(form)  # Возвращаем результат формы
        else:
            return self.form_invalid(form)  # Если форма невалидна, возвращаем ошибку

    # Переопределяем метод get_form для получения формы
    def get_form(self, form_class=None):
        form = super().get_form(form_class)  # Получаем стандартную форму
        if not self.request.user.is_staff:  # Если пользователь не является персоналом
            del form.fields['active']  # Удаляем поле 'active'

        VersionFormset = inlineformset_factory(Product, Version, form=VersionForm, extra=1)  # Создаем формсет
        formset = VersionFormset()  # Создаем формсет
        for subform in formset.forms:
            if not self.request.user.is_staff:  # Если пользователь не является персоналом
                del subform.fields['active']  # Удаляем поле 'active'
        return form

    # Проверяем функцию test_func
    def test_func(self):
        return not self.request.user.is_staff  # Возвращаем True, если пользователь не является персоналом


class ProductUpdateView(LoginRequiredMixin, UpdateView):  # Определяем UpdateView для обновления продуктов
    model = Product  # Указываем модель для UpdateView
    form_class = ProductForm  # Указываем класс формы
    template_name = 'product/product_form.html'  # Указываем шаблон

    # Получаем URL для успешного обновления продукта
    def get_success_url(self):
        return reverse_lazy('product:view', args=[self.object.pk])

    # Переопределяем метод get_form для получения формы
    def get_form(self, form_class=None):
        form = super().get_form(form_class)  # Получаем стандартную форму
        if not self.request.user.is_staff:  # Если пользователь не является персоналом
            del form.fields['active']  # Удаляем поле 'active'
            return form
        elif self.request.user.is_superuser:  # Если пользователь суперпользователь
            return form
        else:
            for field_name in ['title', 'image', 'price']:
                del form.fields[field_name]  # Удаляем поля 'title', 'image', 'price'
            return form

    # Переопределяем метод get_context_data для добавления пользовательских данных контекста
    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)  # Получаем стандартные данные контекста
        FormSet = inlineformset_factory(Product, Version, form=VersionForm, extra=1)  # Создаем формсет
        if self.request.method == 'POST':  # Проверяем, если метод запроса POST
            context_data['formset'] = FormSet(self.request.POST, instance=self.object)  # Создаем формсет с данными POST
        else:
            context_data['formset'] = FormSet(instance=self.object)  # Создаем пустой формсет
        return context_data

    # Получаем объект
    def get_object(self, queryset=None):
        self.object = super().get_object(queryset)  # Получаем объект
        staff_list = User.objects.filter(is_staff=True)  # Получаем список персонала
        if self.request.user in staff_list:  # Если пользователь в списке персонала
            return self.object
        elif self.request.user == self.object.user:  # Если пользователь - владелец продукта
            return self.object
        else:
            raise Http404("Вы не являетесь владельцем этого товара")  # Возвращаем ошибку 404

    # Переопределяем метод form_valid для обработки данных формы
    def form_valid(self, form):
        formset = self.get_context_data()['formset']  # Получаем формсет из контекста
        self.object = form.save()  # Сохраняем форму
        if formset.is_valid():  # Проверяем, валиден ли формсет
            formset.instance = self.object  # Устанавливаем экземпляр для формсета
            formset.save()  # Сохраняем формсет

        return super().form_valid(form)  # Возвращаем результат формы


class ProductDeleteView(UserPassesTestMixin, DeleteView):  # Определяем DeleteView для удаления продуктов
    model = Product  # Указываем модель для DeleteView
    success_url = reverse_lazy('product:index')  # Указываем URL для успешного удаления продукта

    # Проверяем функцию test_func
    def test_func(self):
        return self.request.user.is_superuser  # Возвращаем True, если пользователь суперпользователь