import os
import pickle

from sklearn.ensemble import AdaBoostClassifier, StackingClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import roc_auc_score, recall_score

from imblearn.over_sampling import RandomOverSampler
from sklearn.neural_network import MLPClassifier
from sklearn.tree import DecisionTreeClassifier
import xgboost as xgb


def model_h1(X,y):
    X_train, X_test, y_train, y_test = train_test_split(X,y, test_size=0.3, stratify=y, random_state = 42)

    oversampler = RandomOverSampler()
    X_train_balanced, y_train_balanced = oversampler.fit_resample(X_train, y_train)

    model = xgb.XGBClassifier(subsample= 0.8, n_estimators= 300, max_depth= 5, learning_rate= 0.1, reg_lambda= 0, gamma= 5, colsample_bytree= 0.8, alpha= 5)
    model.fit(X_train_balanced, y_train_balanced)

    y_score = model.predict_proba(X_test)[:, 1]
    y_true = y_test
    auc_score = roc_auc_score(y_true, y_score)

    predictions = model.predict(X_test)
    recall = recall_score(y_test, predictions, average='binary')

    return model, auc_score, recall


def model_h24(X,y):
    X_train, X_test, y_train, y_test = train_test_split(X,y, test_size=0.3, stratify=y, random_state = 42)

    oversampler = RandomOverSampler()
    X_res, y_res = oversampler.fit_resample(X_train, y_train)

    tree = DecisionTreeClassifier(class_weight = "balanced", min_samples_split=12, min_samples_leaf=6, max_leaf_nodes=45, max_features=None, max_depth = 2, criterion = "entropy", splitter = "random", min_impurity_decrease=0.0)
    tree.fit(X_res, y_res)

    ada_tree = AdaBoostClassifier(tree, n_estimators=100, learning_rate = 0.2, algorithm = "SAMME.R",random_state=42)
    ada_tree.fit(X_res, y_res)

    xgb_model = xgb.XGBClassifier(
    objective='binary:logistic',
    n_estimators=100,
    reg_alpha=0.5,
    max_depth=3,
    learning_rate=0.1
    )

    xgb_model.fit(X_res, y_res)

    classifier1 = ada_tree
    classifier2 = xgb_model

    model = StackingClassifier(
    estimators=[('tree', classifier1), ('xgb', classifier2)],
    final_estimator=MLPClassifier(hidden_layer_sizes=50, activation='logistic', learning_rate='adaptive', solver='adam', batch_size=64)
    )

    model.fit(X_res, y_res)

    y_score = model.predict_proba(X_test)[:, 1]
    y_true = y_test
    auc_score = roc_auc_score(y_true, y_score)

    predictions = model.predict(X_test)
    recall = recall_score(y_test, predictions, average='binary')

    return model, auc_score, recall

def save_model(model):
    file_name = "model_saved.pkl"
    pickle.dump(model, open(file_name, "wb"))


def load_model(file_name):
    model = pickle.load(open(file_name, "rb"))
    return model


def predict(model, X):
    result = model.predict(X)
    return result
