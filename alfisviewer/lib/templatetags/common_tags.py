import binascii

from django import template
from domain.models import Domain

register = template.Library()


# from https://stackoverflow.com/questions/31916408/is-django-can-modify-variable-value-in-template
@register.filter
def update_variable(value):
    return value


# https://stackoverflow.com/questions/8000022/django-template-how-to-look-up-a-dictionary-value-with-a-variable
@register.filter
def get_item(dictionary, key):
    return dictionary.get(key)


@register.filter
def hexlify(value):
    return binascii.hexlify(value).upper().decode()


@register.filter
def get_domain(domain_hash):
    try:
        d = Domain.objects.get(hash=domain_hash)
    except Domain.DoesNotExist:
        d = Domain(hash=domain_hash)
        d.save()
    if d.real_domain:
        return d.real_domain
    return domain_hash
