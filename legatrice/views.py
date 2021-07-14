from django.shortcuts import render
from django.http import HttpResponse
from .forms import GeeksForm
import requests
import re
from time import sleep
import json
from legatrice import check_legality as cl

from django.views.decorators.csrf import csrf_exempt
@csrf_exempt
def testFunction(request):
    request_data = request.FILES['files']

    lines = []

    for line in request_data:
        converted = line.decode('utf-8')
        lines.append(converted)

    card_legality_pairs = cl.main(lines, 'standard', False)

    print(card_legality_pairs)

    return HttpResponse(json.dumps(card_legality_pairs))    