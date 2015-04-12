__author__ = 'francusa'

import requests

# Methods for making queries to ML API.

URL_BASE = "https://api.mercadolibre.com/"


def get_item(itemid, attributes=None):
    """
    This method makes a GET to the items/<itemid> and
    brings the JSON public info for the item.
    :param itemid: the id of the item
    :param attributes: the fields to extract from the item
    :return: the JSON returned by the API
    """

    params = {}
    url = URL_BASE + "items/" + itemid
    if attributes:
        params['attributes'] = ",".join(attributes)
    res = requests.get(url, params=params)
    item_data = res.json()

    return item_data


def get_items(items_list, attributes=None):
    """
    This method makes a GET to the items/items_list[0],..,items_list[N] and
    brings the JSON public info for the item.
    :param items_list: a list of ids (in this case a multiid request
    is generated and the result is a list of items)
    :param attributes: the fields to extract from the item
    :return: the JSON returned by the API
    """

    params = {}
    url = URL_BASE + "items/"
    items_len = len(items_list)

    if attributes:
        params['attributes'] = ",".join(attributes)

    # The ML API allows queries with at most 50 item-ids.
    if items_len <= 50:
        params["ids"] = ",".join(items_list)
        res = requests.get(url, params=params)
        items = res.json()
    else:
        offset = 0
        count = 0
        items = list()
        while count < items_len:
            params["ids"] = ",".join(items_list[offset:offset+50])
            res = requests.get(url, params=params)
            # Append the results.
            items.extend(res.json())
            offset += 50
            count = len(items)

    return items


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