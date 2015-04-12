#!/usr/bin/env python
# -*- coding: utf-8 -*-
import numpy as np
from sklearn import linear_model
from sklearn.cross_validation import train_test_split
from dataset import create_dataset
import pandas as pd
from queries import get_item


def create_featurized_dataset(itemid):
    df = create_dataset(itemid)


def extract_features(df):
    """
        Given a dataframe of data about items
        it creates matrices for machine learning
        tasks, where:

        X (input features):
            - normalized_price
                price normalized to [0, 1] interval
            - title_n_words
                number of words in title
            - title_digits_ratio
                ratio of the non blank characters in title that
                are digits
            - seller_score
                score of selling user
            - item_score (gold, bronze, ...)
            - n_images
                number of images in description
            - list_ranking
                position in the list of results

        y (learned variable): selling_speed
    """
    fdf = pd.DataFrame()
    fdf['id'] = df.id

    max_price = df.price.max()
    fdf['norm_price'] = df.price

    count_words = lambda t: len(t.split())
    fdf['title_n_words'] = df.title.apply(count_words)

    def get_digit_rate(t):
        return 0.5
    fdf['title_digits_ratio'] = df.title.apply(get_digit_rate)

    # fdf['seller_score'] = ...

    # fdf['item_score'] = ...

    # fdf['n_images'] = ...

    fdf['list_ranking'] = df.index * 1.0 / len(df)

    # IMPORTANT: return normalization constants.
    # (We need them to fit the features of the input item)

    del fdf['id']

    X = fdf.values
    y = df.speed.values

    return X, y





if __name__ == '__main__':
    # Ejemplos:
    # category_id = "MLA119876", # "Galaxy S4",
    # condition = "new"
    itemid = "MLA550874381"
    
    item = get_item(itemid)

    df = create_dataset(item)

    # reduce dataFrame to items with stock
    # (from which we can calculate a selling price)
    df = df[df.available_quantity > 5]

    X, y = extract_features(df)
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
 
    # Train the model using the training sets
    regr.fit(X_train, y_train)

    # The coefficients
    print 'Coefficients:'
    print regr.coef_
    
    # The mean square error
    rss = np.mean((regr.predict(X_test) - y_test) ** 2)
    print "Residual sum of squares: %.2f" % rss

    # Explained variance score: 1 is perfect prediction
    print('Variance score: %.2f' % regr.score(X_test, y_test))
