from sklearn import datasets
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.ensemble import RandomForestClassifier
from bs4 import BeautifulSoup
import requests
import joblib
import re
import csv
from fetch_training_papers import write_papers_csv, fetch_papers, get_fieldnames, write_papers_csv
from classification import get_features, fill_missing_data
# from train_data import train
# from train_data import train_scholars

def get_article_info():
    return ['keyword', 'id', 'year', 'title', 'src']

def fill_missing(df):
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
    return df

def get_suitable_papers():
    path = 'sample.csv'
    path_to_save = 'suitable1.csv'
    papers = fetch_papers(6, 75, "fetch_keywords.txt")
    write_papers_csv(papers, path)
    fill_missing_data(path)

    df_original = pd.read_csv(path, encoding= 'unicode_escape')
    labels = np.array(df_original['label'])
    features = df_original[get_features()]
    features = np.array(features)
    try:
        loaded_rf = joblib.load("./random_forest.joblib")
    except Exception as e:
        print("Model joblib file not found. Please train and test model with"
              "classification.py before running.")
        print(e)
        exit(0)
    try:
        predictions = loaded_rf.predict(features)
    except Exception as e:
        print("Page not loaded", e)

    relevant_features = get_article_info()
    suitable_papers_df = pd.DataFrame(columns = relevant_features)
    # print(df.head())


    # for i in range(len(predictions)):
    #     prediction = predictions[i]
    #     if prediction == 1:
    #         print('here')
    #         suitable_papers_df = pd.concat([suitable_papers_df, df_original[relevant_features].iloc(i)])
    df_original['preds'] = predictions
    sub_df = df_original[relevant_features + ['preds']]
    # print(sub_df.head())
    print('rows: ', sub_df.shape[0])
    sub_df = sub_df.loc[sub_df['preds'] == 1]
    print(sub_df)
    sub_df.to_csv(path_to_save)
    print(suitable_papers_df)
    # suitable_papers_df.to_csv(path_to_save)

    print(len(predictions), features.shape)

get_suitable_papers()