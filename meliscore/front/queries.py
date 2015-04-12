__author__ = 'francusa'

import requests

# Methods for making queries to ML API.

URL_BASE = "https://api.mercadolibre.com/"


def get_item(itemid, attributes=None):
    """
    This method makes a GET to the items/<itemid> and
    brings the JSON public info for the item.
    :param itemid: the id of the item
        or a list of ids (in this case a multiid request is generated
            and the result is a list of items)
    :return: the JSON returned by the API
    """
    params = {}
    if type(itemid) is list:
        url = URL_BASE + "items/"
        params["ids"] = ",".join(itemid)
    else:
        url = URL_BASE + "items/" + itemid
    if attributes:
        params['attributes'] = ",".join(attributes)
    res = requests.get(url, params=params)
    item_data = res.json()

    return item_data


def get_item_description(itemid):
    """
    This method makes a GET to the items/<itemid>/description and
    brings the JSON public info for the item description.
    :param itemid: the id of the item
    :return: the JSON returned by the API
    """

    url = URL_BASE + "items/" + itemid + "/description"
    res = requests.get(url)
    item_data = res.json()

    return item_data

def get_seller_score(seller_id):
    url = URL_BASE + "users/" + seller_id
    res = requests.get(url)
    data = res.json()
    score = data["seller_reputation"]["power_seller_status"]
    return score

def get_imgcount(itemid):
    """
    Makes a request to items/<itemid>/description and retrieves
    the number of images it has.
    :param itemid: the id of the item.
    :return: the number of images in the description.
    """
    description = get_item_description(itemid)
    return len(re.findall(r'img src', description['text']))

def get_user(userid):
    """
    This method makes a GET to the users/<userid> and
    brings the JSON public info for the user.
    :param userid: the id of the user
    :return: the JSON returned by the API
    """

    url = URL_BASE + "users/" + str(userid)
    res = requests.get(url)
    item_data = res.json()

    return item_data