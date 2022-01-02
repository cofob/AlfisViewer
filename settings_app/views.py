from django.shortcuts import render
from django.http.response import JsonResponse
from django.utils import translation
from django.conf import settings


def index(request):
    return render(request, "settings/index.html")


def set_lang(request, lang_code):
    resp = {}
    lang_code = lang_code.lower()
    if len(lang_code) != 2:
        return JsonResponse(
            {"ok": False, "error": "Language code can be only 2 characters length."}
        )
    if lang_code not in settings.LANGUAGE_CODES:
        lang = "en"
        resp["warn"] = "Language not found, using default."
    else:
        lang = lang_code
    translation.activate(lang)
    resp["ok"] = True
    resp["lang"] = lang
    response = JsonResponse(resp)
    response.set_cookie(settings.LANGUAGE_COOKIE_NAME, lang)
    return response
