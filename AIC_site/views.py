from django.shortcuts import render
from django.utils.translation import get_language_from_request


def index(request):
    if get_language_from_request(request).startswith('en'):
        return render(request, 'index-en.html')
    return render(request, 'index.html')
