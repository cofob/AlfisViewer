from django.conf import settings
import alfis_connector as alfis


def commit_hash(request):
    return {"COMMIT_HASH": settings.COMMIT_HASH + ("-dev" if settings.DEBUG else "")}


def block_count(request):
    return {"BLOCK_COUNT": str(alfis.get_block_count())}
