import pandas as pd
import numpy as np
import joblib
from fetch_training_papers import write_papers_csv, fetch_papers, get_fieldnames, write_papers_csv
from classification import get_features, fill_missing_data

'''
Metadata to be saved with suitable articles
'''
def get_article_info():
    return ['keyword', 'id', 'year', 'title', 'src']

'''
Fills in missing data for DataFrame
    Parameters:
            df(DataFrame): original DataFrame
    Returns:
            df(DataFrame): DataFrame without missing values
'''
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

'''
Fetches suitable papers from MAKES API
    Returns:
            sub_df(DataFrame): DataFrame of papers and 
            relevant metadata (specified by get_article_info)
'''
def get_suitable_papers():
    path = 'sample.csv'
    kPapersPerKeyword = 6
    kKeywords = 75
    papers = fetch_papers(kPapersPerKeyword, kKeywords, "fetch_keywords.txt")
    write_papers_csv(papers, path)
    fill_missing_data(path)

    df_original = pd.read_csv(path, encoding='unicode_escape')
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
    df_original['preds'] = predictions
    sub_df = df_original[relevant_features + ['preds']]
    sub_df = sub_df.loc[sub_df['preds'] == 1]
    return sub_df


if __name__ == '__main__':
    path_to_save = 'suitable1.csv'
    df = get_suitable_papers()
    df.to_csv(path_to_save)
