#!/usr/bin/env python
# -*- coding: utf-8 -*-
import re

from string import punctuation
from queries import get_item, get_item_description, get_user

steps = [(10, "Horrible!",
         "Media pila, mi estimado amigo. Si querés vender más rápidamente, seguí nuestros consejos."),
         (30, "Muy incompleto.", "Seguí nuestros consejos para mejorar tu publicación."),
         (55, "Incompleto."," Seguí nuestros consejos para mejorar tu publicación."),
         (80, "Bastante bien.", "Seguí nuestros consejos para mejorar tu publicación."),
         (95, "Muy bien!", "Tu venta está prácticamente asegurada. Quedan detalles por pulir para que quede excelente."),
         (101, "Excelente!!", "Talvez vos puedas darnos consejos a nosotros. Feliz venta!")]


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

    # photo score
    item_data = get_item(itemid)
    try:
        score, tip = get_photo_score(item_data)
    except:
        pass
    else:
        partial["fotos"] = {"score": int(score*100), "tip": tip}
    # description score
    try:
        description = get_item_description(itemid)
        score, tip = get_description_score(description)
    except:
        pass
    else:
        partial["descripcion"] = {"score": int(score*100), "tip": tip}

    # user score
    try:
        user_data = get_user(item_data['seller_id'])
        score, tip = get_user_score(user_data)
    except:
        pass
    else:
        partial["calificaciones"] = {"score": int(score*100), "tip": tip}

    # calcular score final
    result = {
        "total_score": get_total_score(partial),
        "partial_scores": partial
    }
    title = item_data["title"]
    try:
        photo = item_data["thumbnail"]
    except KeyError:
        pass
    return result, title, photo


def get_photo_score(item_data):
    n_photos = len(item_data["pictures"])
    score = min(6, n_photos) * 1.0 / 6

    if n_photos < 2:
        tip = "Muy pocas fotos!"
    elif n_photos < 4:
        tip = "Bien, pero podrías agregar algunas fotos más!"
    else:
        tip = "Perfecto, tienes la cantidad de fotos justa!"

    return score, tip


def get_user_score(user_data):

    score = user_data["seller_reputation"]["transactions"]["ratings"]["positive"]

    if score < 0.5:
        tip = "Tienes que mejorar tu reputación como vendedor"
    elif score < 0.9:
        tip = "Eres un buen vendedor pero podrias mejorar"
    else:
        tip = "Tu reputación como vendedor es perfecta!"

    return score, tip


def count_images_from_description(description):
    return len(re.findall(r'img src', description['text']))


def get_description_score(description):
    MAX_DESC_LEN = 1000

    text = description["plain_text"]
    if not text:
        strcount = 0
    else:
        text = text.encode("utf-8")
        r = re.compile(r'[{}]'.format(punctuation))
        #re.split(r'[^0-9A-Za-z]+', text)
        newstr = r.sub(' ', text)
        strcount = len(newstr.split())
    imgcount = count_images_from_description(description)
    desc_len = strcount + imgcount * 100
    score = min(desc_len, MAX_DESC_LEN) * 1.0 / MAX_DESC_LEN
    if score <= 0.5:
        tip = "La descripción esta muy floja, explayate un poco más!"
    elif score <= 0.8:
        tip = "La descripción es suficiente pero podria estar más completa"
    else:
        tip = "Tu descripción esta perfecta!"

    return score, tip


def get_total_score(partial_scores):
    score = average([p["score"] for p in partial_scores.values()])
    result = {"score": int(score)}
    for step in steps:
        if score < step[0]:
            result["title"] = step[1]
            result["subtitle"] = step[2]
            break
    return result


def average(it):
    return sum(it)/len(it)


if __name__ == '__main__':
    # URL ejemplo
    # http://articulo.mercadolibre.com.ar/MLA-554524325-apple-iphone-6-16gb-factura-a-b-1-ano-gtia-oficial-_JM
    scores = generate_scores("MLA554524325")
    print scores
