from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser
from django.contrib.auth import authenticate 
from django.forms import DateInput

class UserRegisterForm(UserCreationForm):
    email = forms.EmailField(required=False, label='Email (или Логин)')
    phone_number = forms.CharField(max_length=15, required=False, label='Телефон (или Логин)')

    class Meta:
        model = CustomUser
        fields = ['name', 'last_name', 'birth_date', 'phone_number','email', 'password1', 'password2']
    
 



class UserLoginForm(forms.Form):
    username = forms.CharField(max_length=50)
    password = forms.CharField(widget=forms.PasswordInput)

    def get_user(self):
        username = self.cleaned_data.get('username')
        password = self.cleaned_data.get('password')

        # Проверка, что оба поля заполнены
        if not username or not password:
            return None

        try:
            # Пробуем найти пользователя по имени (можно сделать поиск только по username)
            user = CustomUser.objects.get(username=username)
        except CustomUser.DoesNotExist:
            return None  # Возвращаем None, если пользователь не найден

        # Проверяем правильность пароля
        if user.check_password(password):
            return user
        return None