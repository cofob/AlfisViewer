import hashlib
import re
from domain.models import Domain
from django.shortcuts import render


def solve(domain: str):
    domain = domain.strip()
    f = re.findall(r'(.*)\.(.*)', domain, flags=re.I)
    name = f[0][0].lower()
    h = hashlib.sha256(hashlib.sha256(name.encode()).hexdigest().encode()).hexdigest().upper()
    try:
        d = Domain.objects.get(hash=h)
        d.real_domain = domain
    except Domain.DoesNotExist:
        print('not found', h, name)
        pass


def index(request):
    msg = None
    if request.GET.get('domain'):
        solve(request.GET.get('domain'))
        msg = 'Success!'
    return render(request, 'solver/index.html', context={'msg': msg})
