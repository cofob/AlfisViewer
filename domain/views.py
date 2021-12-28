import json
import re

import alfis_connector
from domain.models import Domain
from block.models import Block
from django.http.response import Http404, HttpResponseRedirect
from django.shortcuts import render
from .utils import get_domain_hash
from alfis_connector import Domains
from binascii import unhexlify


pattern = re.compile(r"(.*)\.(.*)")


def domain(request, domain_id):
    try:
        r = pattern.findall(domain_id)[0]
        d = r[0]
        z = r[1]
    except IndexError:
        raise Http404
    try:
        if not d.startswith("<") and not d.endswith(">"):
            do = get_domain_hash(d, z)
        else:
            d = d[1:-1]
            do = Domain.objects.get(hash=d, zone=z)
    except Domain.DoesNotExist:
        raise Http404
    d_lst = Domains.select().filter(identity=unhexlify(do.hash))
    for d in d_lst:
        data = json.loads(d.data)
        data_str = json.dumps(data, indent=2)
        if data["zone"] == z:
            return render(
                request,
                "domain/index.html",
                context={
                    "domain_obj": do,
                    "domain_data": d,
                    "data": data_str,
                    "title": "View domain",
                    "description": "View domain some data",
                },
            )


def domain_history(request, domain_id):
    try:
        r = pattern.findall(domain_id)[0]
        d = r[0]
        z = r[1]
    except IndexError:
        raise Http404
    try:
        if not d.startswith("<") and not d.endswith(">"):
            do = get_domain_hash(d, z)
        else:
            d = d[1:-1]
            do = Domain.objects.get(hash=d, zone=z)
    except Domain.DoesNotExist:
        raise Http404
    b_lst = Block.objects.filter(domain=do)
    return render(
        request,
        "domain/history.html",
        context={
            "domain_obj": do,
            "blocks": b_lst,
            "title": "Domain history",
            "description": "View domain history",
        },
    )


def domain_solve(request):
    if request.GET.get("domain"):
        try:
            d = get_domain_hash(request.GET.get("domain"))
            return HttpResponseRedirect("/domain/%s.%s" % (d.real_domain, d.zone))
        except Exception as e:
            return render(request, "domain/solve.html", context={"error": True})
    return render(
        request,
        "domain/solve.html",
        context={
            "title": "Solve domain",
            "description": "You can contribute to our domain database",
        },
    )


def domain_list(request):
    try:
        page = int(request.GET.get("p", -1))
    except ValueError:
        return HttpResponseRedirect("/domain/")
    if page < 0:
        return HttpResponseRedirect(
            "/domain/?p=%s" % str(int(alfis_connector.get_domain_count() / 20))
        )
    if page > int(alfis_connector.get_domain_count() / 20):
        return HttpResponseRedirect("/domain/?p=%s" % "0")
    out = Domain.objects.all()[page * 20 : (page + 1) * 20]
    return render(
        request,
        "domain/list.html",
        context={
            "page": page,
            "list": out,
            "title": "All domains",
            "description": "Domain list",
        },
    )
