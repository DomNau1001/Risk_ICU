import streamlit as st
import requests

#define webpage
st.title("ICU Risk Prediction")
st.write("Welcome to the Risk Prediction Application for Patients on the Intensive Care Unit!")
option = st.selectbox("Choose Option:", ["Initial Risk Assessment", "Advanced Risk Assessment"])

# Based on the user's selection, present corresponding interface
if option == "Initial Risk Assessment":
    st.subheader("Please Enter Patient Details:")
    col1, col2 = st.columns(2)

    bmi = col1.number_input("BMI (kg/qm)", value = 0)
    age = col2.number_input("Age (years)", value = 0)
    gender = col1.selectbox("Gender", ["M", "F"])
    pre_icu_days = st.number_input("Previous ICU Days", value = 0)
    elective_surg = col2.selectbox("Prior Elective Surgery", ["yes", "no"])
    glucose_min = col1.number_input("Glucose min. (mg/dl)", value = 0)
    glucose_max = col2.number_input("Glucose max. (mg/dl)", value = 0)
    sysbp_min = col1.number_input("Minimal Systolic Blood Pressure (mmHg)", value = 0)
    sysbp_max = col2.number_input("Maximal Systolic Blood Pressure (mmHg)", value = 0)
    inr_min = col1.number_input("INR min.", value = 0)
    inr_max = col2.number_input("INR max.", value =0)
    spo2_min = col1.number_input("SpO2 min. (%)", value =0)
    spo2_max = col2.number_input("SpO2 max. (%)", value =0)
    hr_min = col1.number_input("Minimal Heart Rate (bpm/min)", value =0)
    hr_max = col2.number_input("Maximal Heart Rate (bpm/min)", value =0)

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
        "hr_min": hr_min,
        "hr_max": hr_max}
    response = requests.get(url, params=params).json()["prediction"]
    response = round(response *100, 2)

    # Display prediction result
    if response >=70:
        st.markdown("High Risk")
    elif response >=30 and response <70:
        st.markdown("Intermediate Risk")
    else:
        st.markdown("**Low Risk**")

    st.markdown(f"*Predicted Risk: {response}%*")


elif option == "Advanced Risk Assessment":
    pass
    # Call API to get prediction result using twenty_four_hour_patient_data

    # Display prediction result
