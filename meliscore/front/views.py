import re
import json

from django.shortcuts import render_to_response
from django.template import RequestContext
from django.http import JsonResponse


from modelo import generate_scores

def home(request, *args, **kwargs):
    return render_to_response('index.html', locals(),
                              context_instance=RequestContext(request))


def score(request, *args, **kwargs):
    url = "http://articulo.mercadolibre.com.ar/MLA-548587141-iphone-5s-apple-16gb-retina-tactil-3g-liberado-chip-a6-ios7-_JM"
    try:
        item_id = re.findall("MLA-\d+", url)[0]
    except IndexError:
        #TODO: retornar al home con un mensaje de error
        pass
    item_id  = item_id.replace("-", "")
    score = generate_scores(item_id)
    #return JsonResponse(score)
    return render_to_response('score_ugly.html', locals(),
                              context_instance=RequestContext(request))
