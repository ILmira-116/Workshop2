from django.db import models
from django.contrib.auth.models import AbstractUser, Group, Permission
from django.core.validators import RegexValidator
import django.utils.timezone as timezone

# Создаем кастомную модель пользователя, наследуя её от AbstractUser
class CustomUser(AbstractUser):
    # Дополнительные поля для пользователя
    name = models.CharField(max_length=30, verbose_name='Имя')  # Имя пользователя
    last_name = models.CharField(max_length=30, verbose_name='Фамилия')  # Фамилия пользователя
    birth_date = models.DateField(null=True, blank=True, verbose_name='Дата рождения')  # Дата рождения
    phone_number = models.CharField(
        max_length=15,
        validators=[RegexValidator(r'^\+?1?\d{9,15}$')],  # Валидация телефона
        help_text="Формат: +79991234567",
        verbose_name="Номер телефона"
    )
    photo = models.ImageField(upload_to='profile_photos/', null=True, blank=True, verbose_name="Фото профиля")  # Фото профиля

    # Для отображения имени пользователя в админке и других местах
    def __str__(self):
        return self.username

    # Мета-настройки
    class Meta:
        swappable = 'AUTH_USER_MODEL'

    # Устанавливаем email как username
    def save(self, *args, **kwargs):
        if not self.username:
            if self.email:
                self.username = self.email
            elif self.phone_number:
                self.username = self.phone_number
            else:
                raise ValueError("Either email or phone_number must be provided.")
        super().save(*args, **kwargs)