import streamlit as st
import requests
from frontend.user_interface import get_one_hour_patient_data, get_twenty_four_hour_patient_data

#define webpage
st.title("ICU Risk Prediction")
st.write("Welcome to the Risk Prediction Application for Patients at the Intensive Care Unit!")
option = st.selectbox("Choose Option:", ["Initial Risk Assessment", "Advanced Risk Assessment"])

# Based on the user's selection, present corresponding interface
if option == "Initial Risk Assessment":
    bmi, age, gender, pre_icu_days, elective_surg, glucose_min, glucose_max, sysbp_min, sysbp_max, inr_min, inr_max, spo2_min, spo2_max, hr_min, hr_max = get_one_hour_patient_data()

    # Call API to get prediction result using one_hour_patient_data
    url = "http://localhost:8000/predict_hour"
    params = {
        "bmi": bmi,
        "age": age,
        "gender": gender,
        "pre_icu_days": pre_icu_days,
        "elective_surg": elective_surg,
        "glucose_min": glucose_min,
        "glucose_max": glucose_max,
        "sysbp_min": sysbp_min,
        "sysbp_max": sysbp_max,
        "inr_min": inr_min,
        "inr_max": inr_max,
        "spo2_min": spo2_min,
        "spo2_max": spo2_max,
        "hr_max": hr_max,
        "hr_min": hr_min
    }
    response = requests.get(url, params=params).json()["prediction"]

    # Display prediction result
    st.markdown(f"**Predicted Risk: ${response}**")


elif option == "Advanced Risk Assessment":
    twenty_four_hour_patient_data = get_twenty_four_hour_patient_data()
    # Call API to get prediction result using twenty_four_hour_patient_data

    # Display prediction result
