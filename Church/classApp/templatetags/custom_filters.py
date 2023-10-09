from django import template

register = template.Library()

@register.filter(name='is_in_list')
def is_in_list(value, arg):
    return value in arg.split(',')
