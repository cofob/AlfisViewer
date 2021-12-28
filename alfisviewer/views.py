from django.shortcuts import render
import sys
from alfisviewer.utils import get_view_logger
from index.models import Error


log = get_view_logger(__name__)


def handler404(request, exception):
    typ, val, tb = sys.exc_info()
    log.exception(tb)

    return render(
        request,
        "404.html",
        context={
            "title": "Error 404",
            "description": "Page not found",
            "error_id": Error.submit(typ, val, tb),
        },
        status=404,
    )


def handler500(request):
    typ, val, tb = sys.exc_info()
    log.exception(tb)

    return render(
        request,
        "500.html",
        context={
            "title": "Error 500",
            "description": "Something happened...",
            "error_id": Error.submit(typ, val, tb),
        },
        status=500,
    )
