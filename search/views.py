from django.shortcuts import render
from domain.models import Domain
from alfis_connector import Blocks
from binascii import unhexlify
from domain.utils import get_domain_hash
from random import choice


def index(request):
    query = request.GET.get("query", "")
    try:
        domain_fullmatch = get_domain_hash(query)
    except:
        domain_fullmatch = None
    domain_results = []
    try:
        domain_results += Domain.objects.filter(
            hash__contains=query.upper().split(".")[0].replace("<", "").replace(">", "")
        )[:40]
    except:
        pass
    domain_results += Domain.objects.filter(
        hash__contains=query.upper().replace("<", "").replace(">", "")
    )[:40]
    domain_results += Domain.objects.filter(real_domain__contains=query.lower())[:40]
    domain_results += Domain.objects.filter(zone__contains=query.lower())[:40]
    domain_results = domain_results[:40]
    try:
        block_results = Blocks.select().filter(hash=unhexlify(query))[:40]
    except:
        block_results = []
    try:
        unhexlify(query)
        if len(query) != 64:
            key = None
        else:
            key = query
    except Exception as e:
        print(e)
        key = None
    return render(
        request,
        "search/index.html",
        context={
            "domain_results": domain_results,
            "block_results": block_results,
            "domain_fullmatch": domain_fullmatch,
            "key": key,
            "query": query,
            "random": choice(
                [
                    "cofob.ygg",
                    "index.ygg",
                    "git.srv",
                    "cr.srv",
                    "site.srv",
                    "rutracker.ygg",
                    "linux.ygg",
                    "gosuslugi.ygg",
                    "yandex.ygg",
                    "ru.ygg",
                    "home.ygg",
                    "lewd.ygg",
                    "naturism.ygg",
                    "forum.ygg",
                    "meduza.ygg",
                ]
            ),
        },
    )
