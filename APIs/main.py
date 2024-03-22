import pandas as pd
from fastapi import FastAPI
from APIs.backend.preprocessor import preprocessing_1_hour, preprocessing_24_hour
from APIs.backend.load_model import load_model

app = FastAPI()

@app.get("/")
def read_root():
    return {"message": "Welcome to the ICU Risk Prediction API!"}

@app.get("/predict_hour")
def predict_after_1_hour(
                         BMI: float,
                         Age: int,
                         Gender: str,
                         pre_icu_days: int,
                         elective_surgery: int,
                         glucose_min: float,
                         glucose_max: float,
                         sysbsp_min: int,
                         sysbs_max:int,
                         inr_min: float,
                         inr_max: float,
                         spo2_min: int,
                         spo2_max: int,
                         hr_max: int,
                         hr_min: int):
    # Logic to handle prediction after 1 hour
    X = pd.DataFrame(dict(
        bmi = BMI,
        age = Age,
        gender = Gender,
        pre_icu_los_days = pre_icu_days,
        elective_surger = elective_surgery,
        glucose_min = glucose_min,
        glucose_max = glucose_max,
        sysbsp_min = sysbsp_min,
        sysbs_max = sysbs_max,
        inr_min = inr_min,
        inr_max = inr_max,
        spo2_min = spo2_min,
        spo2_max = spo2_max,
        heartrate_max = hr_max,
        heartrate_min = hr_min))

    X_pre = preprocessing_1_hour(X)
    model = load_model("model_saved.pkl")
    prediction = model.predict(X_pre)

    return {"prediction": prediction}

@app.get("/predict_day")
def predict_after_24_hours(*args, **kwargs):
    # Logic to handle prediction after 24 hours
    return {"prediction": "Prediction after 24 hours"}
