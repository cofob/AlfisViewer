import binascii
import json

from domain.models import Domain
from django.shortcuts import render
from django.http.response import Http404
import alfis_connector as alfis


def block(request, block_id):
    b = alfis.Blocks.get_or_none(id=block_id)
    if not b:
        b = alfis.Blocks.get_or_none(hash=binascii.unhexlify(block_id))
    if not b:
        raise Http404
    context = {"b": b}
    if b.transaction is not None:
        try:
            context['transaction'] = json.loads(b.transaction)
            context['transaction']['data'] = json.loads(context['transaction']['data'])
            context['raw'] = json.dumps(context['transaction'], indent=2).split('\n')
        except json.JSONDecodeError:
            pass
    return render(request, "block/block.html", context=context)


for b in alfis.Blocks.select().iterator():
    try:
        trans = json.loads(b.transaction)
        try:
            d = Domain.objects.get(hash=trans['identity'])
        except Domain.DoesNotExist:
            d = Domain(hash=trans['identity'])
            d.save()
    except:
        pass
