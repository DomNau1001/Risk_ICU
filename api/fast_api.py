import pandas as pd
import pickle
from fastapi import FastAPI
from ml_logic.model import load_model, predict

app = FastAPI()

@app.get("/")
def read_root():
    return {"message": "Welcome to the ICU Risk Prediction API!"}


@app.get("/predict_hour")
def predict_after_1_hour(
                         age: int,
                         bmi: float,
                         cirrhosis: str,
                         elective_surg: str,
                         gender: str,
                         glucose_min: float,
                         hr_max: int,
                         lactate_max: float,
                         mpb_min: int,
                         rr_min: int,
                         spo2_max: float,
                         sysbp_min: int,
                         temp_min: float,
                         icu_admit: str,
                         immunosuppression: str,
                         pre_icu_days: int):

    el_sur = 0
    if elective_surg == "yes":
        el_sur = 1

    male_gender = 0
    if gender == "M":
        male_gender = 1

    cirr = 0
    if cirrhosis == "yes":
        cirr = 1

    imsp = 0
    if immunosuppression == "yes":
        imsp = 1

    admit = 0
    if icu_admit == "yes":
        admit = 1


    X = pd.DataFrame(dict(
        age = [age],
        bmi = [bmi],
        cirrhosis = [cirr],
        elective_surgery = [el_sur],
        gender_M = [male_gender],
        h1_glucose_min = [glucose_min],
        h1_heartrate_max = [hr_max],
        h1_lactate_max = [lactate_max],
        h1_mbp_min = [mpb_min],
        h1_resprate_min = [rr_min],
        h1_spo2_max = [spo2_max],
        h1_sysbp_min = [sysbp_min],
        h1_temp_min = [temp_min],
        icu_admit_source_Accident_Emergency = [admit],
        immunosuppression = [imsp],
        pre_icu_los_days = [pre_icu_days]))


    X.sort_index(axis=1, inplace=True)

    mm_scaler = pickle.load(open("mm_scaler_1.pkl", "rb"))


    X_pre = mm_scaler.transform(X)
    model = load_model("1h_model_saved.pkl")
    prediction = predict(model, X_pre)[0][1]

    return {"prediction": float(prediction)}


@app.get("/predict_day")
def predict_after_24_hours(age: int,
                           bun_max: float,
                           sysbp_min: int,
                           temp_min: float,
                           spo2_min: int,
                           temp_max: float,
                           wbc_max: float,
                           hr_max: int,
                           hr_min: int,
                           rr_max: int,
                           rr_min: int,
                           wbc_min: int,
                           hema_min: float,
                           icu_admit: str,
                           ventilated: str,
                           platelets_min: float,
                           bmi: float,
                           gcs_eyes: int,
                           sysbp_max: int,
                           gcs_motor: int,
                           gcs_verbal: int,
                           crea_max: float,
                           hco3_max: float,
                           mbp_min: int,
                           glucose_min: int,
                           sodium_min: float):

    a_e = 0
    if icu_admit == "yes":
        a_e = 1

    vent = 0
    if ventilated == "yes":
        vent = 1


    X = pd.DataFrame(dict(
        age = [age],
        bmi = [bmi],
        d1_bun_max = [bun_max],
        d1_spo2_min = [spo2_min],
        d1_temp_max = [temp_max],
        d1_wbc_max = [wbc_max],
        d1_glucose_min = [glucose_min],
        d1_heartrate_max = [hr_max],
        d1_heartrate_min = [hr_min],
        d1_resprate_max = [rr_max],
        d1_resprate_min = [rr_min],
        d1_hemaglobin_min = [hema_min],
        d1_sysbp_min = [sysbp_min],
        d1_temp_min = [temp_min],
        icu_admit_source_Accident_Emergency = [a_e],
        d1_wbc_min = [wbc_min],
        gcs_verbal = [gcs_verbal],
        gcs_motor = [gcs_motor],
        d1_platelets_min = [platelets_min],
        d1_sysbp_max = [sysbp_max],
        gcs_eyes = [gcs_eyes],
        d1_creatinine_max = [crea_max],
        d1_hco3_max = [hco3_max],
        d1_mbp_min = [mbp_min],
        d1_sodium_min = [sodium_min],
        ventilated = [vent]))

    X.sort_index(axis=1, inplace=True)

    mm_scaler = pickle.load(open("mm_scaler_24.pkl", "rb"))


    X_pre = mm_scaler.transform(X)
    model = load_model("24h_model_saved.pkl")
    prediction = predict(model, X_pre)[0][1]

    return {"prediction": float(prediction)}
