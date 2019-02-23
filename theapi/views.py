from django.shortcuts import render,HttpResponse
import json
from django.http import JsonResponse
# Create your views here.

def index(request):

    #use GET method
    #use 'direction' as the name
    direction = request.GET.get("direction")
    print(direction)
    return JsonResponse(json.dumps(direction),safe=False)
