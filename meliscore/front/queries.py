__author__ = 'francusa'

import requests

# Methods for making queries to ML API.

URL_BASE = "https://api.mercadolibre.com/"


def get_item(itemid):
    """
    This method makes a GET to the items/<itemid> and
    brings the JSON public info for the item.
    :param itemid: the id of the item
    :return: the JSON returned by the API
    """

    url = URL_BASE + "items/" + itemid
    res = requests.get(url)
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