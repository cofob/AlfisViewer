from django.shortcuts import render
import alfis_connector as alfis


def index(request):
    last_block = alfis.get_latest_block()
    return render(request, 'index/index.html', context={'last_block': last_block})
