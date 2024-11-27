from typing import Iterable
from django.db import models
from django.utils.text import slugify
from django.contrib.auth.models import User
from unidecode import unidecode 
from users.models import CustomUser
from django.conf import settings

# Create your models here.

class Bd(models.Model):
    title = models.CharField(max_length = 50,verbose_name='Товар')
    content = models.TextField(verbose_name='Описание')
    price = models.FloatField(verbose_name='Цена')
    discount= models.DecimalField(max_digits = 5, decimal_places=2, null=True, blank=True, verbose_name='Pазмер скидки')
    published = models.DateTimeField(auto_now_add=True, db_index=True,verbose_name='Опубликовано')
    rubric=models.ForeignKey('Rubric', null=True, on_delete=models.PROTECT, verbose_name='Рубрика')
    subrubric = models.ForeignKey('SubRubric', null = True, on_delete=models.PROTECT, verbose_name='Подрубрика')
    slug=models.SlugField(max_length=30, unique=True, blank=True, null= True, verbose_name='Slug-bd')
    image = models.ImageField(upload_to="images/", blank=True, null = True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, blank = False, null=False, default ='1')

    
    def save(self, *args, **kwargs) -> None:
        if not self.slug:
            # Преобразуем заголовок в латиницу перед генерацией слага
            base_slug = slugify(unidecode(self.title))  # Генерация базового слага на основе заголовка
            unique_slug = base_slug
            counter =1 

            # Проверка на уникальность
            while Bd.objects.filter(slug = unique_slug).exists():
                unique_slug = f"{base_slug}-{counter}" # Добавление счетчика к слагу
                counter +=1 
            
            self.slug = unique_slug # Присваиваем уникальный слаг
        
        super().save(*args, **kwargs) # Сохранение объекта

    class Meta:
        verbose_name_plural='Объявления'
        verbose_name='Объяление'
        ordering=['-published']
        db_table='bboard_ads'
      

class Rubric(models.Model):
    name=models.CharField(max_length=20, db_index=True, verbose_name='Название')
    slug=models.SlugField(max_length=30, unique=True, blank=True, null= True, verbose_name='Slug-r')
    
    def __str__(self):
        return self.name
    
      
    def save(self, *args, **kwargs) -> None:
        if not self.slug:
            base_slug = slugify(self.name)  # Генерация базового слага на основе заголовка
            unique_slug = base_slug
            counter =1 

            # Проверка на уникальность
            while Bd.objects.filter(slug = unique_slug).exists():
                unique_slug = f"{base_slug}-{counter}" # Добавление счетчика к слагу
                counter +=1 
            
            self.slug = unique_slug # Присваиваем уникальный слаг
        
        super().save(*args, **kwargs) # Сохранение объекта

    class Meta:
        verbose_name_plural='Рубрики'
        verbose_name ='Рубрика'
        ordering=['name']
        db_table='rubric'


class SubRubric(models.Model):
    name = models.CharField(max_length=50, verbose_name='Подрубрика')
    rubric = models.ForeignKey('Rubric', on_delete=models.PROTECT, related_name='subrubrics', verbose_name='Рубрика')
    slug = models.SlugField(max_length=30, unique=True, blank=True, null= True, verbose_name='Slug-sr')

    def __str__(self) -> str:
        return self.name
    
      
    def save(self, *args, **kwargs) -> None:
        if not self.slug:
            base_slug = slugify(self.name)  # Генерация базового слага на основе заголовка
            unique_slug = base_slug
            counter =1 

            # Проверка на уникальность
            while Bd.objects.filter(slug = unique_slug).exists():
                unique_slug = f"{base_slug}-{counter}" # Добавление счетчика к слагу
                counter +=1 
            
            self.slug = unique_slug # Присваиваем уникальный слаг
        
        super().save(*args, **kwargs) # Сохранение объекта

    class Meta:
        verbose_name_plural = 'Подрубрики'
        verbose_name = 'Подрубрика'
        ordering = ['name']
        db_table = 'subrubric'

