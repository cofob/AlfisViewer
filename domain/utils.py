from hashlib import sha256
from .models import Domain


def hash_domain(d):
    return sha256(sha256(d.encode('utf-8')).digest())


def get_domain_hash(domain, zone=None):
    if zone:
        full_domain = domain + '.' + zone
    else:
        zone = domain.split('.')[1]
        full_domain = str(domain)
        domain = domain.split('.')[0]
    try:
        return Domain.objects.get(real_domain=domain, zone=zone)
    except Domain.DoesNotExist:
        pass
    h = hash_domain(full_domain).hexdigest().upper()
    d = Domain.objects.get(hash=h, zone=zone)
    if d.real_domain != domain:
        d.real_domain = domain
        d.save()
    return d

