from django import template
from django.templatetags.static import static 
from django.utils.safestring import mark_safe  # Импортируем mark_safe 

register = template.Library() # экземпляр библиотеки тегов

@register.filter #pегистрация фильтра
def sell_price(price, discount):
    discount = float(discount)
    """Возвращает цену со скидкой"""
    if discount:
        return round(price-price*discount/100, 2)
    return price


@register.simple_tag
def render_ads_image(ad):
    """Возвращает HTML-код для отображения изображения объявления"""
    if ad.image:
        image_html = f'<img src="{ad.image.url}" alt="{ ad.title }" class="ad-image">'
    else:
    # Используем static для получения URL к изображению "Не найдено"
        not_found_image_url = static("Not_Found_image.png")
        image_html = f'<img src="{not_found_image_url}" alt="Изображение не найдено" class="ad-image">'
    return mark_safe(image_html)  # Оборачиваем строку в mark_safe 