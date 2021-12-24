import json
import re
from domain.models import Domain
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
        data_str = json.dumps(data, indent=2).split("\n")
        if data["zone"] == z:
            return render(
                request,
                "domain/index.html",
                context={"domain_obj": do, "domain_data": d, "data": data_str},
            )


def domain_solve(request):
    if request.GET.get("domain"):
        try:
            d = get_domain_hash(request.GET.get("domain"))
            return HttpResponseRedirect("/domain/%s.%s" % (d.real_domain, d.zone))
        except Exception as e:
            return render(request, "domain/solve.html", context={"error": True})
    return render(request, "domain/solve.html")


def domain_list(request):
    page = int(request.GET.get("p", 0))
    out = Domains.select()[page * 20 : (page + 1) * 20]
    return render(request, "domain/list.html", context={"page": page, "list": out})
