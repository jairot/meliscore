import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import json
from datetime import datetime
from queries import *
from dataset import *

def get_selling_speeds(itemids):
    """
        Given a list of itemids it calculates
        the number of items sold by hour since
        the beginning of the sale
    """
    data = get_item(itemids, ["id","start_time","sold_quantity", "price"])
    data = pd.read_json(json.dumps(data))
    data['elapsed_time'] = datetime.now() - data.start_time
    # data['elapsed_hours'] = data.elapsed_time / np.timedelta64(1,'h')
    data['elapsed_days'] = data.elapsed_time / np.timedelta64(1,'D')
    data['speed'] = data.sold_quantity / data.elapsed_days

    return data[['price', 'speed']]

def price_quartiles(df):
    if('price' in df.columns):
        prices = df['price']
        first, second, third = prices.quantile([.25, .5, .75])
        return first, second, third
    else:
        raise NameError('price column does not exist')
    
def get_quartile_speeds(quartiles, selling_speeds):
    first = selling_speeds[selling_speeds.price <= quartiles[0]]
    first_average_speed = first['speed'].mean(axis=0)
    second = selling_speeds[(selling_speeds.price > quartiles[0]) & (selling_speeds.price <= quartiles[1])]
    print second
    second_average_speed = second['speed'].mean(axis=0)
    third = selling_speeds[(selling_speeds.price > quartiles[1]) & (selling_speeds.price <= quartiles[2])]
    third_average_speed = third['speed'].mean(axis=0)     
    fourth = selling_speeds[selling_speeds.price > quartiles[2]]
    fourth_average_speed = fourth['speed'].mean(axis=0)     
    return [first_average_speed, second_average_speed, third_average_speed, fourth_average_speed]


def get_sweet_spots(category_id):
    df = create_dataset(category_id)
    big = df[df.available_quantity > 5]
    selling_speeds = get_selling_speeds(list(big.id))
    quartiles = get_quartiles(df)
    quartile_speeds = get_quartile_speeds(quartiles, selling_speeds)

    result = {
        "quartiles": quartiles,
        "speeds": quartile_speeds
    }

    return result

if __name__ == '__main__':
    # df = pd.read_csv('iphone5_16gb.csv',encoding='utf-8')
    df = create_dataset("MLA119876")
    # nuevos = df[df.condition == 'new']
    # usados = df[df.condition == 'used']
    # nuevos.price.describe()
    # usados.price.describe()
    big = df[df.available_quantity > 5]
    selling_speeds = get_selling_speeds(list(big.id))
    print selling_speeds.columns

    quartiles = price_quartiles(df)

    quartile_speeds = get_quartile_speeds(quartiles, selling_speeds)
    



# Idea: dar selling speed por precio
# y encontrar selling_speed medio de cada cuartil

# Ejemplos:
# "id": "MLA119876",
# "name": "Galaxy S4",til