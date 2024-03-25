import pandas as pd

from sklearn.preprocessing import OneHotEncoder, MinMaxScaler


def preprocessing_24_hour(data):
    pass


def preprocessing_1_hour(X):

    #Encoding
    X_cats = X[["gender", "elective_surgery"]]
    X_nums = X.drop(columns = ["gender", "elective_surgery"])

    ohe = OneHotEncoder(sparse_output=False, drop = "if_binary", handle_unknown="ignore")

    ohe.fit(X_cats[["gender"]])
    X_cats[ohe.get_feature_names_out()] = ohe.transform(X_cats[["gender"]])
    X_cats.drop(columns = "gender", inplace = True)

    X_post = pd.concat([X_cats, X_nums], axis = 1, sort = False)

    #Scaling
    mm_scaler = MinMaxScaler()

    X_preprocessed = mm_scaler.fit_transform(X_post)
    X_preprocessed = pd.DataFrame(X_preprocessed, columns = X_post.columns)

    return X_preprocessed
