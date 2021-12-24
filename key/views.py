from django.shortcuts import render
from django.http.response import Http404
from binascii import unhexlify
import alfis_connector as alfis


def key(request, key_id):
    b = unhexlify(key_id)
    blocks = alfis.Blocks.select().filter(pub_key=b)
    domains = alfis.Domains.select().filter(signing=b)
    if not blocks:
        raise Http404
    return render(
        request, "key/index.html", context={"blocks": blocks, "domains": domains}
    )
