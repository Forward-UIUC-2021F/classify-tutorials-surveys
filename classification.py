import pandas as pd
import numpy as np
from IPython.display import display
from sklearn.decomposition import PCA

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
    PCA_("")    # input filename with dataset
