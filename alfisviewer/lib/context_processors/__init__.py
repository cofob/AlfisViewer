from django.conf import settings
import alfis_connector as alfis
from time import time
from block.views import update_blockchain


settings.BLOCKCHAIN_LAST_UPDATE = 0


def commit_hash(request):
    return {"COMMIT_HASH": settings.COMMIT_HASH + ("-dev" if settings.DEBUG else "")}


def block_count(request):
    return {"BLOCK_COUNT": str(alfis.get_block_count())}


def update_scheduler(request):
    t = int(time())
    if settings.BLOCKCHAIN_LAST_UPDATE + 30 <= t:
        update_blockchain()
        settings.BLOCKCHAIN_LAST_UPDATE = t
    return {"UPDATE_IN": settings.BLOCKCHAIN_LAST_UPDATE-t+30}
