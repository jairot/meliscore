#!/usr/bin/env python
# -*- coding: utf-8 -*-
from scipy import average
import requests
import re
from string import punctuation

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

    score, tip =  get_photo_score(item_data)
    partial["photo"] = {
        "score": score,
        "tip": tip
    }
    
    # traer descripción
    url_description = URL_BASE + 'items/' + itemid + '/description'
    response_description = requests.get (URL_BASE + 'items/' + itemid + '/description')
    description=response_description.json()
    score = get_description_score(description)

    partial["description"] = {
        "score": score,
        "tip": "Media pila che!"
    }

    # traer user score
    seller_id = item_data['seller_id']
    url = URL_BASE + "users/%d" % seller_id
    user_data = requests.get(url).json()
    
    score, tip = get_user_score(user_data)
    partial["user_score"] = {
        "score": score,
        "tip": tip
    }

    # calcular score final
    result = {
        "total_score": get_total_score(partial),
        "partial_scores": partial
    }    

    return result


def get_description_score(desc_data):
    return 0, ""


def get_photo_score(item_data):
    n_photos = len(item_data["pictures"])
    score = min(6, n_photos) * 1.0 / 6

    if n_photos < 2:
        tip = "Muy pocas fotos!"
    elif n_photos < 4:
        tip = "Bien, pero podrías agregar"
    else:
        tip = "De diego!"

    return score, tip


def get_user_score(user_data):
    user_level = int(user_data["seller_reputation"]["level_id"][0])
    score = user_level * 1.0 / 5
    if user_level < 3:
        tip = "Flojísimo!"
    elif user_level < 4:
        tip = "Va queriendo"
    else:
        tip = "bien ahí!"

    return score, tip


def get_total_score(partial_scores):
    return average([p["score"] for p in partial_scores.values()])

def count_images_from_description (description):
    return len(re.findall(r'img src', description['text']))
    
def get_description_score(description):
    text = description["plain_text"]
    if (not text):
        strcount= 0
    else:
        text = text.encode("utf-8")
        r = re.compile(r'[{}]'.format(punctuation))
        #re.split(r'[^0-9A-Za-z]+', text)
        newstr = r.sub(' ', text)
        strcount = len(newstr.split())
    imgcount = count_images_from_description(description)
    return strcount + imgcount * 100


if __name__ == '__main__':
    # URL ejemplo
    # http://articulo.mercadolibre.com.ar/MLA-554524325-apple-iphone-6-16gb-factura-a-b-1-ano-gtia-oficial-_JM
    scores = generate_scores("MLA554524325")
    print scores
