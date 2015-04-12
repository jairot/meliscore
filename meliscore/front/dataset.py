import pandas as pd
import requests
import json
import collections
from datetime import datetime
from queries import *
import numpy as np
from pandas import DataFrame
import os

URL_BASE = "https://api.mercadolibre.com/"

def get_selling_speeds(itemids):
    """
        Given a list of itemids it calculates
        the number of items sold by hour since
        the beginning of the sale
    """
    data = get_items(itemids, ["id","start_time","sold_quantity", "price"])
    data = pd.read_json(json.dumps(data))
    data['elapsed_time'] = datetime.now() - data.start_time
    # data['elapsed_hours'] = data.elapsed_time / np.timedelta64(1,'h')
    data['elapsed_days'] = data.elapsed_time / np.timedelta64(1,'D')

    data['speed'] = data.sold_quantity / data.elapsed_days

    return data[['price', 'speed']]


def simplify_item(item, prefix, sep):
    """
        Given an item result from the API
        it removes all nested information and returns
        a plain json that is more dataframe-friendly
    """

    items = []
    for k, v in item.items():
        new_key = prefix + sep + k if prefix else k
        if isinstance(v, collections.MutableMapping):
            items.extend(simplify_item(v, new_key, sep=sep).items())
        else:
            items.append((new_key, v))

    return dict(items)


def price_quantiles(df):
    if 'price' in df.columns:
        prices = df['price']
        first, second, third = prices.quantile([.25, .5, .75])
        q = {'first quantile': first,
             'second quantile': second,
             'third quantile': third}

        return q
    else:
        raise NameError('price column does not exist')

def find_seller_score(users):
    scores = []
    for user in users:
        seller_score = user["seller_reputation"]["power_seller_status"]
        scores = scores + [seller_score]
    return pd.Series(scores)

def find_imgcount(items):
    imgcount = []
    for item in items:
        item_id = item['id']
        n_imgs = get_imgcount(item_id)
        imgcount = imgcount + [n_imgs]

    return pd.Series(imgcount)

def find_item_score(items):
    scores = []
    for item in items:
        item_score = item["listing_type_id"]
        scores = scores + [item_score]
    return pd.Series(scores)
    
def create_dataset(item, reduced=False, extra_features=False):
    category_id = item.get('category_id')
    condition = item.get('condition')
    fname = '%s_%s_%s.csv' % (category_id, condition, 'red' if reduced else 'full')
    
    # TODO: guarda con el False!!!!
    if os.path.exists(fname) and False:
        df = pd.read_csv(fname, encoding='utf-8')
    else:
        response = requests.get(URL_BASE + 'sites/MLA/search?category={}&condition={}'.format(category_id, condition))
        data = response.json()

        limit = data['paging']['limit']
        offset = 0
        items_number = min(data['paging']['total'], 500)

        while offset < items_number:
            print offset
            response = requests.get(URL_BASE + 'sites/MLA/search?category=' + category_id + '&offset=' + str(offset))
            data = response.json()
            items = [simplify_item(i, '', '_') for i in data['results']]
            page_df = pd.read_json(json.dumps(items))
            if offset == 0:
                df = page_df
            else:
                df = df.append(page_df)
            offset += limit

        if reduced:
            # reduce dataFrame to items with stock
            # (from which we can calculate a selling price)
            df = df[(df.available_quantity > 5) | (df.id == item['id'])]

        df_speeds = get_selling_speeds(list(df.id))
        df['speed'] = df_speeds.speed

        if extra_features:
            items = get_items(list(df['id']), ['id',"listing_type_id"])
            users = get_users(list(df['id']), ['seller_reputation'])
            df['seller_score'] = find_seller_score(users)
            df['item_score'] = find_item_score(items)
            df['n_images'] = find_imgcount(items)

        df.to_csv(fname, encoding='utf-8')

    return df


def create_dataset_from_item(item):
    """
    Create the dataset from an item dict.
    :param item: the item dict.
    :return:
    """
    create_dataset(item.get('category_id'))


if __name__ == '__main__':
    # iPhone 5 16gb
    category_id = 'MLA121408'
    create_dataset(category_id)
