from django.conf import settings
import alfis_connector as alfis
from time import time
from block.views import update_blockchain
import threading


settings.BLOCKCHAIN_LAST_UPDATE = 0


def commit_hash(request):
    return {"COMMIT_HASH": settings.COMMIT_HASH + ("-dev" if settings.DEBUG else "")}


def block_count(request):
    return {"BLOCK_COUNT": str(alfis.get_block_count()), "BLOCK_PAGE": str(int(alfis.get_block_count()/20))}


def domain_count(request):
    return {"DOMAIN_COUNT": str(alfis.get_domain_count())}


def update_scheduler(request):
    t = int(time())
    if settings.BLOCKCHAIN_LAST_UPDATE + 30 <= t:
        thread = threading.Thread(target=update_blockchain)
        thread.start()
        settings.BLOCKCHAIN_LAST_UPDATE = t
    return {"UPDATE_IN": settings.BLOCKCHAIN_LAST_UPDATE - t + 30}
