from django.http import JsonResponse
from .models import Track


def index(request):
    data = list(Track.objects.values())
    return JsonResponse(data, safe=False)
