import os

from sklearn.model_selection import train_test_split
from sklearn.metrics import roc_auc_score, recall_score

from imblearn.over_sampling import RandomOverSampler
import xgboost as xgb


def model_h1(X,y):
    X_train, X_test, y_train, y_test = train_test_split(X,y, test_size=0.3, stratify=y)

    oversampler = RandomOverSampler()
    X_train_balanced, y_train_balanced = oversampler.fit_resample(X_train, y_train)

    xgb_model = xgb.XGBClassifier(subsample= 0.8, n_estimators= 300, max_depth= 5, learning_rate= 0.1, reg_lambda= 0, gamma= 5, colsample_bytree= 0.8, alpha= 5)
    xgb_model.fit(X_train_balanced, y_train_balanced)

    y_score = xgb_model.predict_proba(X_test)[:, 1]
    y_true = y_test
    auc_score = roc_auc_score(y_true, y_score)

    predictions = xgb_model.predict(X_test)
    recall = recall_score(y_test, predictions, average='binary')

    return xgb_model, auc_score, recall


def model_h24(X,y):
    pass


def save_model(model):
    LOCAL_REGISTRY_PATH =  os.path.join(os.path.expanduser('~'), ".lewagon", "risk_icu", "risk_icu", "training_outputs")
    model_path = os.path.join(LOCAL_REGISTRY_PATH, "models", ".h5")
    model.save(model_path)
