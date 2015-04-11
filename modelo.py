#!/usr/bin/env python
# -*- coding: utf-8 -*-
from scipy import average
import requests

URL_BASE = "https://api.mercadolibre.com/"

def generate_scores(itemid):
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
    url = URL_BASE + "items/" + itemid
    res = requests.get(url)
    item_data = res.json()

    n_photos = len(item_data["pictures"])
    score = min(6, n_photos) * 1.0 / 6

    if n_photos < 2:
        tip = "Muy pocas fotos!"
    elif n_photos < 4:
        tip = "Bien, pero podrías agregar"
    else:
        tip = "De diego!"

    partial["photo"] = {
        "score": score,
        "tip": tip
    }
    
    # traer descripción
    partial["description"] = {
        "score": 0,
        "tip": "Media pila che!"
    }

    # traer user score
    partial["user_score"] = {
        "score": 0,
        "tip": "Media pila che!"
    }


    # calcular score final
    result = {
        "total_score": get_total_score(partial),
        "partial_scores": partial
    }    

    return result

def get_total_score(partial_scores):
    return average([p["score"] for p in partial_scores.values()])

if __name__ == '__main__':
    scores = generate_scores("MLA554189135")
    print scores
