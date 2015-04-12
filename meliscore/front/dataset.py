import pandas as pd
import requests
import json
import collections

URL_BASE = "https://api.mercadolibre.com/"


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
    

def create_dataset(item):
    category_id = item.get('category_id')
    condition = item.get('condition')

    response = requests.get(URL_BASE + 'sites/MLA/search?category={}&condition={}'.format(category_id, condition))
    data = response.json()

    limit = data['paging']['limit']
    offset = 0
    items_number = data['paging']['total']

    while offset < items_number:
        response = requests.get(URL_BASE + 'sites/MLA/search?category=' + category_id + '&offset=' + str(offset))
        data = response.json()
        items = [simplify_item(i, '', '_') for i in data['results']]
        page_df = pd.read_json(json.dumps(items))
        if offset == 0:
            df = page_df
        else:
            df = df.append(page_df)
        offset += limit

    df.to_csv('%s.csv' % category_id, encoding='utf-8')

    return df


if __name__ == '__main__':
    # iPhone 5 16gb
    category_id = 'MLA121408'
    create_dataset(category_id)