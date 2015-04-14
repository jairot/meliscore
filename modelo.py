#!/usr/bin/env python
# -*- coding: utf-8 -*-
from scipy import average
import requests

URL_BASE = "https://api.mercadolibre.com/"

def score(itemid):
    """
        Given an itemid, it creates a score
        for the corresponding publication

        Returns:
            - aggregated score

            - for each component of the score:
                * individual score
                * tip to improve

        Components for this version are:
            * photo: yes or no
            * description: based on length
            * user_score
    """
    partial = {}

    # traer item
    url = URL_BASE + 'items/MLA352546'
    res = requests.get(url)
    item_data = res.json()


    partial["photo"] = {
        "score": 0,
        "tip": "Poné foto culiao!"
    }
    
    # traer descripción
	url_description = URL_BASE + 'items/' + itemid + '/description'
	response_description = requests.get (URLBASE + 'items/MLA554189135/description')
	jresp=response_description.json()
	description = jresp["plain_text"]

    partial["description"] = {
        "score": 0,
        "tip": "Poné foto culiao!"
    }

    # traer user score


    partial["user_score"] = {
        "score": 0,
        "tip": "Poné foto culiao!"
    }


    # calcular score final
    result = {
        "total_score": get_total_score(partial_scores),
        "partial_scores": partial
    }    

    return result

def get_total_score(partial_scores):
    return average([p["score"] for p in partial_scores])
