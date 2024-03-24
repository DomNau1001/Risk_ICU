import pandas as pd
from ml_logic.model import model_h1, save_model
from ml_logic.preprocessing import preprocessing_1_hour

def main():
    #data
    data = pd.read_csv("raw_data/training_v2.csv")

    # preproc
    X, y = preprocessing_1_hour(data)

    # training
    model, auc_score, recall = model_h1(X,y)

    #save model
    save_model(model)


if __name__ == "__main__":
    main()
