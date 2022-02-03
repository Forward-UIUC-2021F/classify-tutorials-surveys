from train_data import convert_to_counter
from sklearn import datasets
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.ensemble import RandomForestClassifier
from sklearn.feature_extraction.text import CountVectorizer
import joblib
import csv


'''
tests the accuracy of the classification at a random state
    Parameters:
            feature (array): A 2d-array with all the features for each paper
            label (array): An array that contains all the labels for each paper

    Returns:
            accuracy of the training set.
'''
def test_mag(feature, label):
    # set the train: test = 0.8: 0.2
    train_features, test_features, train_labels, test_labels = train_test_split(feature, label, test_size = 0.20, random_state = 25) 
    rfc = RandomForestClassifier(n_estimators = 1000, random_state = 41)   
    rfc.fit(train_features, train_labels)

    predicitons = rfc.predict(test_features)
    # exactly predicts -1, 0 or 1
    correct_exact = 0
    # predicts and sets apart the difference of -1, 0 vs 1
    correct_broad = 0
    for i in range(len(test_labels)):
        if test_labels[i] == predicitons[i]:
            correct_exact += 1
            correct_broad += 1
        elif (test_labels[i] != 1 and predicitons[i] != 1) or (test_labels[i] == 1 and predicitons[i] == 1):
            correct_broad += 1
    sze = float(len(test_labels))
    return correct_broad / sze

'''
tests the accuracy of the classification at a random state
    Parameters:
            feature (array): A 2d-array with all the features for each paper
            label (array): An array that contains all the labels for each paper

    Returns:
            accuracy of the training set.
'''
def train_scholars(feature, label):
    rfc = RandomForestClassifier(n_estimators = 500, random_state = 42)   
    rfc.fit(feature, label)
    joblib.dump(rfc, "./random_forest.joblib")


'''
tests the accuracy of the classification at a random state
    Parameters:
            feature (array): A 2d-array with all the features for each paper
            label (array): An array that contains all the labels for each paper

    Returns:
            accuracy of the training set.
'''
def train(path):
    features = pd.read_csv(path)
    labels = np.array(features['label'])

    # drop the Keyword and label column 
    features = features.drop('Keyword', axis = 1)
    features = features.drop('label', axis = 1)
    title_counter = convert_to_counter(np.array(features['title']))
    keyword_counter = convert_to_counter(np.array(features['keywords']))

    # drop the title and the keyword from the training features.
    features = features.drop('title', axis = 1)
    features = features.drop('keywords', axis = 1)
    features = np.array(features)
    f = []
    for i in range(len(features)):
        f.append(np.concatenate([features[i], title_counter[i], keyword_counter[i]]))
    return f, labels


# f, l = train('mag_data_1.csv') 
# print(test_mag(f, l))