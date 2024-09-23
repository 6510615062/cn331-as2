from django.http import HttpResponse


def index(request):
    return HttpResponse("Hello, world. JUST AN INDEX PAGE")