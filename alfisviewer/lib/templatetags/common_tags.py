import binascii

from django import template
from domain.models import Domain
from datetime import datetime
from time import time

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
    d = Domain.objects.get(hash=domain_hash)
    if d.real_domain:
        return "%s.%s" % (d.real_domain, d.zone)
    return "<%s>.%s" % (d.hash, d.zone)


@register.filter
def get_domain_str(d):
    if d.real_domain:
        return "%s.%s" % (d.real_domain, d.zone)
    return "<%s>.%s" % (d.hash, d.zone)


@register.filter
def get_domains_str(ds):
    d = Domain.objects.get(hash=hexlify(ds.identity).upper())
    if d.real_domain:
        return "%s.%s" % (d.real_domain, d.zone)
    return "<%s>.%s" % (d.hash, d.zone)


@register.filter
def incr(i):
    return i + 1


@register.filter
def decr(i):
    return i - 1


@register.filter
def to_date(timestamp):
    dt_object = datetime.fromtimestamp(timestamp)
    return dt_object.date()


@register.filter
def add_year(timestamp):
    return timestamp+31556926


@register.filter
def is_expired(domain):
    return (domain.timestamp+31556926) < time()
