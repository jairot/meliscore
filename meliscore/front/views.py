import re
import json

from django.shortcuts import render_to_response
from django.template import RequestContext
from django.http import JsonResponse


from sweet_price_spot import get_sweet_spots
from sale_speed_prediction import predict_salespeed
from modelo import generate_scores


def home(request, *args, **kwargs):
    return render_to_response('index.html', locals(),
                              context_instance=RequestContext(request))


def score(request, itemid=None, *args, **kwargs):
    if not itemid:
        url = request.POST["url"]
        try:
            itemid = re.findall("MLA-\d+", url)[0]
        except IndexError:
            return render_to_response('index.html', {'error_msg': 'La Url ingresada no pertenece a un item valido'},
                                      context_instance=RequestContext(request))

    itemid  = itemid.replace("-", "")
    score, title, photo = generate_scores(itemid)
    return render_to_response('score.html', locals(),
                              context_instance=RequestContext(request))

def sweetspot(request, itemid=None, *args, **kwargs):
    results = get_sweet_spots(itemid)
    data = {"data": results}
    return JsonResponse(data)


def salespeed(request, itemid=None, *args, **kwargs):
    results = predict_sale_speed(itemid)
    data = {"data": results}
    return JsonResponse(data)


