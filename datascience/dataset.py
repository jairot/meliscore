import pandas as pd
import requests
import json


URL_BASE = "https://api.mercadolibre.com/"


def create_dataset(category_id):
    response = requests.get(URL_BASE + 'sites/MLA/search?category=' + category_id)
    data = response.json()
    limit = data['paging']['limit']
    offset = data['paging']['offset'] + limit 
    items_number = data['paging']['total']
    df = pd.io.json.read_json(json.dumps(data['results']))
    while (offset <= items_number):
        response = requests.get(URL_BASE + 'sites/MLA/search?category=' + category_id + '&offset=' + str(offset))
        data = response.json()
        df = df.append(pd.io.json.read_json (json.dumps(data['results'])))
        offset += limit
    df.to_csv('iphone5_16gb.csv', encoding='utf-8')
    

if __name__ == '__main__':
    # iPhone 5 16gb
    category_id = 'MLA121408'
    create_dataset(category_id)