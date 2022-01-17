from django.views.static import serve
import os
import logging
from django.conf import settings


# from https://stackoverflow.com/questions/59254843/add-custom-log-records-in-django
def get_view_logger(view_name):
    logger = logging.getLogger(view_name)
    logger.setLevel(logging.INFO)
    handler = logging.FileHandler(
        filename=str(settings.BASE_DIR / "logs" / (view_name + ".txt")), encoding="utf8"
    )
    formatter = logging.Formatter("%(asctime)s [%(levelname)s] : %(message)s")
    handler.setFormatter(formatter)
    logger.addHandler(handler)
    return logger


def serve_file(file, content_type):
    def serve_file_middle(request):
        return serve(request, os.path.basename(file), os.path.dirname(file))

    return serve_file_middle


def get_page(curr, max_val):
    if curr == 0:
        return 1
    out = int(curr / max_val)
    if curr % max_val == 0:
        out -= 1
    return out
