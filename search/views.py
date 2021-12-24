from django.shortcuts import render
from domain.models import Domain
from alfis_connector import Blocks
from binascii import unhexlify
from domain.utils import get_domain_hash


def index(request):
    query = request.GET.get('query', '')
    try:
        domain_fullmatch = get_domain_hash(query)
    except:
        domain_fullmatch = None
    domain_results = []
    domain_results += Domain.objects.filter(hash=query.upper())[:20]
    domain_results += Domain.objects.filter(real_domain=query.lower())[:20]
    domain_results = domain_results[:20]
    try:
        block_results = Blocks.select().filter(hash=unhexlify(query))[:20]
    except:
        block_results = []
    return render(request, 'search/index.html', context={'domain_results': domain_results,
                                                         'block_results': block_results,
                                                         'domain_fullmatch': domain_fullmatch})
