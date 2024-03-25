import pandas as pd

from sklearn.preprocessing import OneHotEncoder, MinMaxScaler


def preprocessing_24_hour(data):
    pass


def preprocessing_1_hour(X):

    mm_scaler = MinMaxScaler()

    X_preprocessed = mm_scaler.fit_transform(X)
    X_preprocessed = pd.DataFrame(X_preprocessed, columns = X.columns)

    X_preprocessed.sort_index(axis=1, inplace=True)

    return X_preprocessed
