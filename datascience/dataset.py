import pandas as pd
import requests
import json


URL_BASE = "https://api.mercadolibre.com/"


def create_dataset(category_id):
    response = requests.get(URL_BASE + 'sites/MLA/search?category=' + category_id)
    data = response.json()
    df = pd.io.json.read_json(json.dumps(data['results']))
    df.to_csv('iphone5_16gb.csv', encoding='utf-8')
    

if __name__ == '__main__':
    # iPhone 5 16gb
    category_id = 'MLA121408'
    create_dataset(category_id)