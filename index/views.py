import time

from django.shortcuts import render
import alfis_connector as alfis
from domain.models import Domain
from block.models import Block
from hashlib import sha256
from json import dumps, loads
from binascii import unhexlify


def index(request):
    last_block = alfis.get_latest_block()
    return render(
        request,
        "index/index.html",
        context={
            "last_block": last_block,
            "title": "Alfis blockchain viewer",
            "description": "Welcome to the Alfis blockchain viewer",
        },
    )


def stats(request):
    zone_data = [
        Domain.objects.filter(zone="ygg").count(),
        Domain.objects.filter(zone="anon").count(),
        Domain.objects.filter(zone="btn").count(),
        Domain.objects.filter(zone="conf").count(),
        Domain.objects.filter(zone="index").count(),
        Domain.objects.filter(zone="merch").count(),
        Domain.objects.filter(zone="mirror").count(),
        Domain.objects.filter(zone="mob").count(),
        Domain.objects.filter(zone="screen").count(),
        Domain.objects.filter(zone="srv").count(),
    ]
    week_data = [
        alfis.Blocks.select().filter(timestamp__gt=time.time() - 86400).count(),
        alfis.Blocks.select()
        .filter(
            timestamp__gt=time.time() - 86400 * 2, timestamp__lt=time.time() - 86400
        )
        .count(),
        alfis.Blocks.select()
        .filter(
            timestamp__gt=time.time() - 86400 * 3, timestamp__lt=time.time() - 86400 * 2
        )
        .count(),
        alfis.Blocks.select()
        .filter(
            timestamp__gt=time.time() - 86400 * 4, timestamp__lt=time.time() - 86400 * 3
        )
        .count(),
        alfis.Blocks.select()
        .filter(
            timestamp__gt=time.time() - 86400 * 5, timestamp__lt=time.time() - 86400 * 4
        )
        .count(),
        alfis.Blocks.select()
        .filter(
            timestamp__gt=time.time() - 86400 * 6, timestamp__lt=time.time() - 86400 * 5
        )
        .count(),
        alfis.Blocks.select()
        .filter(
            timestamp__gt=time.time() - 86400 * 7, timestamp__lt=time.time() - 86400 * 6
        )
        .count(),
    ]
    static_domains = 0
    moving_domains = 0
    for domain in Domain.objects.all():
        if Block.objects.filter(domain=domain).count() == 1:
            static_domains += 1
        else:
            moving_domains += 1
    empty_domains = 0
    lst = []
    for d in Domain.objects.all():
        domain = list(alfis.Domains.filter(identity=unhexlify(d.hash)))[-1]
        data = loads(domain.data)
        data["records"] = data.get("records", [])
        if not data["records"]:
            empty_domains += 1
        lst.append(sha256(dumps(data["records"]).encode()).hexdigest())
    b_len = len(lst)
    a_len = len(list(set(lst)))
    same_domains = b_len - a_len
    total_domains = alfis.get_domain_count()
    unsolved_domains = Domain.objects.filter(real_domain=None).count
    return render(
        request,
        "index/stats.html",
        context={
            "zones": str(zone_data),
            "week": str(week_data),
            "static_domains": str([static_domains, moving_domains]),
            "same": same_domains,
            "empty": empty_domains,
            "total": total_domains,
            "unsolved": unsolved_domains,
            "title": "Alfis blockchain statistics",
            "description": "View some interesting stats",
        },
    )
