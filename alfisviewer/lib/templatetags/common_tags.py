from django import template
from django.conf import settings
from hashlib import sha256
import datetime

register = template.Library()


# from https://stackoverflow.com/questions/31916408/is-django-can-modify-variable-value-in-template
@register.filter
def update_variable(value):
    return value


# https://stackoverflow.com/questions/8000022/django-template-how-to-look-up-a-dictionary-value-with-a-variable
@register.filter
def get_item(dictionary, key):
    return dictionary.get(key)
