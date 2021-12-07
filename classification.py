import pandas as pd
import numpy as np
from IPython.display import display
from sklearn.decomposition import PCA
import time
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.feature_extraction.text import CountVectorizer
import joblib

'''
Gets the full feature list to be used as a training dataset
    Parameters:
            path(string): path of the file to be used
    Returns:
        f: the list of features that would be used for training
        labels: the labels of what the paper was classified as
'''
def train(path):
    features = pd.read_csv(path)
    labels = np.array(features['label'])

    # drops column keyword and label
    features = features.drop('keyword', axis=1)
    features = features.drop('label', axis=1)
    features = features.drop('src', axis=1)
    features = features.drop('result_order', axis=1)
    features = features.drop('title', axis=1)
    features = np.array(features)
    # print(np.shape(features))
    # print(features)

    f = []
    for i in range(len(features)):
        f.append(features[i])
    return f, labels

'''
Gets the full feature list to be used as a training dataset
    Parameters:
        feature(list): The dataset of features
        label(list): List of labels
    Returns:
        The accuracy of the classifier in correctly identifying suitable articles (labelled 1)
# '''
def test_scholars(feature, label):
    train_features, test_features, train_labels, test_labels = train_test_split(feature, label, test_size=0.20)
    rfc = RandomForestClassifier(n_estimators=500, random_state=int(time.time()))
    rfc.fit(train_features, train_labels)
    joblib.dump(rfc, "./random_forest.joblib")
    predictions = rfc.predict(test_features)
    correct_broad = 0
    correct_exact = 0
    for i in range(len(test_labels)):
        if test_labels[i] == predictions[i]:
            correct_exact += 1
            correct_broad += 1
        elif (test_labels[i] != 1 and predictions[i] != 1) or (test_labels[i] == 1 and predictions[i] == 1):
            correct_broad += 1

    return correct_broad * 100.0 / len(test_labels)

'''
Store the random forrest tree classifier.
    Parameters:
        feature(list): The dataset of features
        label(list): List of labels
'''
def train_scholars(feature, label):
    rfc = RandomForestClassifier(n_estimators=500)
    rfc.fit(feature, label)
    joblib.dump(rfc, "./random_forest.joblib")

'''
Fill in the missing data by dummy values that could help them get ignored
    Parameters:
        path(string): path of the file to be modified
'''
def fill_missing_data(path):
    df = pd.read_csv(path)
    df["year"].fillna("2010", inplace=True)
    df["pdf"].fillna("FALSE", inplace=True)
    df["book"].fillna("FALSE", inplace=True)
    df["edu"].fillna("FALSE", inplace=True)
    df["org"].fillna("FALSE", inplace=True)
    df["com"].fillna("FALSE", inplace=True)
    df["other_domain"].fillna("FALSE", inplace=True)
    df["exact_keyword_title"].fillna("FALSE", inplace=True)
    df["all_word"].fillna("FALSE", inplace=True)
    df["citation#"].fillna(-1, inplace=True)
    df["title_length"].fillna(0, inplace=True)
    df["occurences_title"].fillna(0, inplace=True)
    df["colon"].fillna("FALSE", inplace=True)
    df["doc"].fillna("FALSE", inplace=True)
    df["survey"].fillna("FALSE", inplace=True)
    df["tutorial"].fillna("FALSE", inplace=True)
    df["review"].fillna("FALSE", inplace=True)
    df.to_csv(path, index=False)

def get_average_accuracy():
    accs = []
    for i in range(250):
        # fill_missing_data('testing__.csv')
        f, l = train('training_data_labeled_Updated.csv')
        train_scholars(f, l)
        x = test_scholars(f, l)
        accs.append(x)
        print(x, sum(accs) / len(accs))

    print("average acc: ", sum(accs) / len(accs))  # average classifier accuracy

def PCA_(filename):
    try:
        model_data = pd.read_csv(filename)
        print(model_data)
        print('Success: Data loaded into dataframe.')
    except Exception as e:
        print('Data load error: ', e)
        return
    train_data = model_data
    dropped_columns = ["keyword", "position_k", "position_d", "label", "pdf", "occurrences_summary"]
    # use commented lines below to specify n selected features
    # n_cols = train_data.drop(dropped_columns, axis=1).dropna(how='any', axis=0).shape[1]
    # pca = PCA(n_components=n_cols)
    pca = PCA()
    pca.fit(train_data.drop(dropped_columns, axis=1))
    print(pca.explained_variance_ratio_)
    print(pca.singular_values_)
    print(pca.components_)

if __name__ == '__main__':
    get_average_accuracy()