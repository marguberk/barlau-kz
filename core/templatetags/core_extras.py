from django import template

register = template.Library()

@register.filter
def split_lines(value):
    """Разделяет текст на строки"""
    if value:
        return value.split('\n')
    return []

@register.filter
def get_city(address):
    """Извлекает название города из адреса"""
    if not address:
        return ''
    
    # Разделяем адрес по запятым
    parts = address.split(',')
    
    # Берем первую часть и очищаем от лишних пробелов
    city = parts[0].strip()
    
    # Если первая часть содержит цифры (возможно, это улица), берем вторую часть
    if any(char.isdigit() for char in city) and len(parts) > 1:
        city = parts[1].strip()
    
    return city 