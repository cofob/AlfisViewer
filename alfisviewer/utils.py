from django.views.static import serve
import os


def serve_file(file, content_type):
    def serve_file_middle(request):
        return serve(request, os.path.basename(file), os.path.dirname(file))
    return serve_file_middle
