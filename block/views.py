from django.shortcuts import render
import alfis_connector as alfis


def block(request, block_id):
    b = alfis.Blocks.get(id=int(block_id))
    return render(request, 'block/block.html', context={'b': b})
