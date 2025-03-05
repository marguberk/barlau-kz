from django import template

register = template.Library()

@register.filter
def split_lines(value):
    """Разделяет текст на строки"""
    if value:
        return value.split('\n')
    return [] 