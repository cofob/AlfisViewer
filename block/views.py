import binascii
import json

from domain.models import Domain
from django.shortcuts import render
from django.http.response import Http404
import alfis_connector as alfis


def block_list(request):
    page = int(request.GET.get('p', 0))
    out = alfis.Blocks.select()[page * 20:(page + 1) * 20]
    return render(request, 'block/list.html', context={'page': page, 'list': out})


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
            if context['transaction'].get('class') != 'origin':
                context['d'] = Domain.objects.get(hash=context['transaction']['identity'], zone=context['transaction']['data']['zone'])
            else:
                context['origin'] = True
        except json.JSONDecodeError:
            pass
    try:
        for i in range(1, 5):
            bp = alfis.Blocks.get_by_id(b.id-i)
            if bp.transaction:
                context['bp'] = bp
    except:
        pass
    return render(request, "block/block.html", context=context)


def update_blockchain():
    for b in alfis.Blocks.select().iterator():
        try:
            trans = json.loads(b.transaction)
            data = json.loads(trans['data'])
            try:
                d = Domain.objects.get(hash=trans['identity'], zone=data['zone'])
            except Domain.DoesNotExist:
                d = Domain(hash=trans['identity'], zone=data['zone'])
                d.save()
        except:
            pass
