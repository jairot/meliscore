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


def extract_features(df, itemid):
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
    
    features_item = fdf[df.id == itemid]

    del features_item['id']
    del fdf['id']

    X = fdf.values
    y = df.speed.values
    x = features_item.values

    return X, y, x


def predict_salespeed(itemid):
    item = get_item(itemid)

    print "Creating dataset of similar items (same category and condition)"
    df = create_dataset(item)

    # reduce dataFrame to items with stock
    # (from which we can calculate a selling price)
    df[(df.available_quantity > 5) | (df.id == itemid)]

    print "Extracting numeric features"
    X, y, x = extract_features(df, itemid)
    
    print "Splitting in train and test sets"
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
 
    print "Training regression model"
    # Create linear regression object
    regr = linear_model.LinearRegression()
    # Train the model using the training sets
    regr.fit(X_train, y_train)
    
    # The mean square error
    print "\nModel evaluation"
    print "Residual sum of squares: %.2f" % np.mean((regr.predict(X_test) - y_test) ** 2)
    # Explained variance score: 1 is perfect prediction
    
    print 'Variance score: %.2f' % regr.score(X_test, y_test)


    sale_speed = regr.predict(x)
    print "\nPredicted sale speed %.1f items per day" % sale_speed

    return sale_speed

if __name__ == '__main__':
    # Ejemplos:
    # category_id = "MLA119876", # "Galaxy S4",
    # condition = "new"
    itemid = "MLA550874381"
    
    sale_speed = predict_salespeed(itemid)
