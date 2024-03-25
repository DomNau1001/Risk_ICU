import pandas as pd
from fastapi import FastAPI
from api.backend.api_preprocessor import preprocessing_1_hour, preprocessing_24_hour
from ml_logic.model import load_model, predict

app = FastAPI()

@app.get("/")
def read_root():
    return {"message": "Welcome to the ICU Risk Prediction API!"}


@app.get("/predict_hour")
def predict_after_1_hour(
                         bmi: float,
                         age: int,
                         gender: str,
                         pre_icu_days: int,
                         elective_surg: str,
                         glucose_min: float,
                         glucose_max: float,
                         sysbp_min: int,
                         sysbp_max:int,
                         inr_min: float,
                         inr_max: float,
                         spo2_min: float,
                         spo2_max: float,
                         hr_min: int,
                         hr_max: int):
    # Logic to handle prediction after 1 hour

    el_sur = 0
    if elective_surg == "yes":
        el_sur = 1
    else:
        el_sur = 0

    male_gender = 0
    if gender == "M":
        male_gender = 1
    else:
        male_gender = 0

    X = pd.DataFrame(dict(
        gender_M = [male_gender],
        age = [age],
        bmi = [bmi],
        elective_surgery = [el_sur],
        pre_icu_los_days = [pre_icu_days],
        h1_heartrate_max = [hr_max],
        h1_heartrate_min = [hr_min],
        h1_spo2_max = [spo2_max],
        h1_spo2_min = [spo2_min],
        h1_sysbp_max = [sysbp_max],
        h1_sysbp_min = [sysbp_min],
        h1_glucose_max = [glucose_max],
        h1_glucose_min = [glucose_min],
        h1_inr_max = [inr_max],
        h1_inr_min = [inr_min]))

    X_pre = preprocessing_1_hour(X)
    model = load_model("model_saved.pkl")
    prediction = predict(model, X_pre)[0][1]

    return {"prediction": float(prediction)}


@app.get("/predict_day")
def predict_after_24_hours(*args, **kwargs):
    # Logic to handle prediction after 24 hours
    return {"prediction": "Prediction after 24 hours"}
