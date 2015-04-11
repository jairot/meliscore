import pandas as pd
import requests
import json


URL_BASE = "https://api.mercadolibre.com/"


def simplify_item(item):
    """
        Given an item result from the API
        it removes all nested information and returns
        a plain json that is more dataframe-friendly
    """
    return item


def create_dataset(category_id):
    response = requests.get(URL_BASE + 'sites/MLA/search?category=' + category_id)
    items = response.json()['results']
    items = [simplify_item(i) for i in items]
    df = pd.io.json.read_json(json.dumps(items))
    df.to_csv('iphone5_16gb.csv', encoding='utf-8')
    

if __name__ == '__main__':
    # iPhone 5 16gb
    category_id = 'MLA121408'
    create_dataset(category_id)