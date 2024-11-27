from django.shortcuts import render, redirect
from .forms import UserRegisterForm, UserLoginForm
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
from django.contrib import messages
from django.views import View
from bboard.models import Bd, Rubric, SubRubric 
from django.contrib.auth.decorators import login_required
from django.conf import settings
from django.contrib.auth.forms import PasswordChangeForm, UserChangeForm
from users.models import CustomUser
from django.views.generic.base import TemplateView 
from typing import Dict, Any 


class RegisterLoginView(TemplateView):
    template_name = 'users/register_login.html'
    register_form_class = UserRegisterForm
    login_form_class = UserLoginForm

    # Метод для формирования контекста (GET-запросы)
    def get_context_data(self, **kwargs) -> Dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context['register_form'] = self.register_form_class()
        context['login_form'] = self.login_form_class()
        return context

    # Метод для обработки POST-запросов
    def post(self, request, *args, **kwargs):
        # Если была отправлена форма регистрации
        if 'register' in request.POST:
            return self.register_user(request)

        # Если была отправлена форма входа
        elif 'login' in request.POST:
            return self.login_user(request)

        # Если не удалось определить форму, возвращаем шаблон без изменений
        return self.render_to_response(self.get_context_data())

    # Логика для обработки регистрации пользователя
    def register_user(self, request):
        form = self.register_form_class(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('users:user_profile')  # Перенаправляем на профиль

        # Если форма не прошла валидацию, возвращаем страницу с ошибками
        context = self.get_context_data()
        context['register_form'] = form
        return self.render_to_response(context)

    # Логика для обработки входа пользователя
    def login_user(self, request):
        form = self.login_form_class(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            if user:
                login(request, user)
                return redirect('users:user_profile')

            # Если пользователь не найден, добавляем общую ошибку
            form.add_error(None, 'Неверные данные для входа')

        # Если форма не прошла валидацию, возвращаем страницу с ошибками
        context = self.get_context_data()
        context['login_form'] = form
        return self.render_to_response(context)

            




@login_required
def user_profile(request):
    return render(request, 'users/user_profile.html', {'user':request.user})



