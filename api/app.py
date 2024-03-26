import streamlit as st
import requests

#define webpage
PAGES = ['Initial Risk Assessment (1 hour)', 'Advanced Risk Assessment (24 hours)']

header = st.container()
with header:
  # st.image('path/to/your/logo.png')
  st.title("_Risk_ICU_")
  st.title("**A risk assessment tool for healthcare professionals**")

homepage_content = st.container()
with homepage_content:
  # Welcome message and company info
  st.write("Evaluate your ICU patient´s individual mortality risk!")
  st.write("***A MORE DETAILED DECRIPTION.***")

  # Container for buttons with horizontal layout
  button_container = st.container()
  with button_container:
    initial_button = st.button("Initial Risk Assessment (1 hour)", key="initial_button")
    advanced_button = st.button("Advanced Risk Assessment (24 hours)", key="advanced_button")

# Based on the user's selection, present corresponding interface
if initial_button:
    st.subheader("Please Enter Patient Details:")
    col1, col2 = st.columns(2)

    bmi = col1.number_input("BMI (kg/qm)", value = 0)
    age = col2.number_input("Age (years)", value = 0)
    gender = col1.selectbox("Gender", ["M", "F"])
    pre_icu_days = st.number_input("Previous In-Hospital Days", value = 0)
    icu_admit = st.selectbox("Patient Admitted from A&E?", ["yes", "no"])
    elective_surg = col2.selectbox("Prior Elective Surgery", ["yes", "no"])
    cirrhosis = col1.selectbox("Cirrhosis", ["yes", "no"])
    immunosuppression = col2.selectbox("Immunosuppression", ["yes", "no"])
    glucose_min = col1.number_input("Glucose (mmol/L)", value = 0)
    mpb_min = col2.number_input("Mean Arterial Pressure (mmHg)", value = 0)
    sysbp_min = col1.number_input("Systolic Blood Pressure (mmHg)", value = 0)
    rr_min = col2.number_input("Respiratory Rate (breaths/min)", value = 0)
    lactate_max = col1.number_input("Lactate (mmol/L)", value = 0)
    temp_min = col2.number_input("Temperature (°C)", value =0)
    spo2_max = col1.number_input("SpO2 (%)", value =0)
    hr_max = col2.number_input("Heart Rate (bpm/min)", value =0)

    # Call API to get prediction result using one_hour_patient_data
    url = "https://riskicu-ulvty4hw7q-ew.a.run.app/predict_hour"
    params = {
        "bmi": bmi,
        "age": age,
        "gender": gender,
        "pre_icu_days": pre_icu_days,
        "elective_surg": elective_surg,
        "cirrhosis": cirrhosis,
        "immunosuppression": immunosuppression,
        "icu_admit": icu_admit,
        "glucose_min": glucose_min,
        "mpb_min": mpb_min,
        "sysbp_min": sysbp_min,
        "rr_min": rr_min,
        "lactate_max": lactate_max,
        "spo2_max": spo2_max,
        "hr_max": hr_max,
        "temp_min": temp_min}

    response = requests.get(url, params=params).json()["prediction"]
    #response.raise_for_status()
    #if response.status_code != 204:
         #response.json()["prediction"]
    response = round(response * 100, 2)

    # Display prediction result
    if response >= 70:
        st.markdown(f"<div style='background-color: red; color: black; padding: 10px; border-radius: 5px;'>{'HIGH RISK'}</div>", unsafe_allow_html=True)
    elif 30 <= response < 70:
        st.markdown(f"<div style='background-color: yellow; color: black; padding: 10px; border-radius: 5px;'>{'MODERATE RISK'}</div>", unsafe_allow_html=True)
    else:
        st.markdown(f"<div style='background-color: green; color: black; padding: 10px; border-radius: 5px;'>{'LOW RISK'}</div>", unsafe_allow_html=True)

    st.markdown(f"*Predicted Risk: {response}%*")


elif advanced_button:
    st.subheader("Please Enter Patient Details:")
    col1, col2 = st.columns(2)

    age = col1.number_input("Age (years)", value = 0)
    bmi = col2.number_input("BMI (kg/qm)", value = 0)
    temp_min = col1.number_input("Minimal Temperature (°C)", value =0)
    temp_max = col2.number_input("Maximal Temperature (°C)", value =0)
    wbc_min = col1.number_input("Minimal White Blood Cell Count (10^9/L)", value =0)
    wbc_max = col2.number_input("Maximal White Blood Cell Count (10^9/L)", value =0)
    hr_max = col2.number_input("Maximal Heart Rate (bpm/min)", value =0)
    hr_min = col1.number_input("Minimal Heart Rate (bpm/min)", value =0)
    glucose_min = col1.number_input("Minimal Glucose (mmol/L)", value = 0)
    sodium_min = col2.number_input("Minimal Sodium (mmol/L)", value = 0)
    rr_max = col2.number_input("Maximal Respiratory Rate (breaths/min)", value = 0)
    rr_min = col1.number_input("Minimal Respiratory Rate (breaths/min)", value = 0)
    sysbp_max = col2.number_input("Maximal Systolic Blood Pressure (mmHg)", value = 0)
    sysbp_min = col1.number_input("Minimal Systolic Blood Pressure (mmHg)", value = 0)
    mbp_min = col1.number_input("Mean Arterial Pressure (mmHg)", value = 0)
    hco3_max = col2.number_input("Maximal Bicarbonate (mmol/L)", value = 0)
    bun_max = col1.number_input("BUN (mmol/L)", value = 0)
    crea_max = col2.number_input("Creatinine (mmol/L)", value = 0)
    platelets_min = col1.number_input("Minimal Platelets (mmol/L)", value = 0)
    hema_min = col2.number_input("Minimal Hemaglobin (g/dL)", value = 0)
    spo2_min = st.number_input("Minimal SpO2 (%)", value =0)
    gcs_eyes = st.selectbox("GCS Eyes", [1, 2, 3, 4])
    gcs_verbal = st.selectbox("GCS Verbal", [1, 2, 3, 4, 5])
    gcs_motor = st.selectbox("GCS Motor", [1, 2, 3, 4, 5, 6])
    ventilated = st.selectbox("Patient on Ventilation?", ["yes", "no"])
    icu_admit = st.selectbox("Patient Admitted from A&E?", ["yes", "no"])


    # Call API to get prediction result using twenty_four_hour_patient_data
    url = "https://riskicu-ulvty4hw7q-ew.a.run.app/predict_day"
    params = {"age": age,
              "bun_max": bun_max,
              "sysbp_min": sysbp_min,
              "temp_min": temp_min,
              "spo2_min": spo2_min,
              "temp_max": temp_max,
              "wbc_max": wbc_max,
              "hr_max": hr_max,
              "hr_min": hr_min,
              "rr_max": rr_max,
              "rr_min": rr_min,
              "wbc_min": wbc_min,
              "hema_min": hema_min,
              "icu_admit": icu_admit,
              "ventilated": ventilated,
              "platelets_min": platelets_min,
              "bmi": bmi,
              "gcs_eyes": gcs_eyes,
              "sysbp_max": sysbp_max,
              "gcs_motor": gcs_motor,
              "gcs_verbal": gcs_verbal,
              "crea_max": crea_max,
              "hco3_max": hco3_max,
              "mbp_min": mbp_min,
              "glucose_min": glucose_min,
              "sodium_min": sodium_min}

    response = requests.get(url, params=params).json()["prediction"]

    response = round(response*100, 2)

    # Display prediction result
    if response >= 70:
        st.markdown(f"<div style='background-color: red; color: black; padding: 10px; border-radius: 5px;'>{'HIGH RISK'}</div>", unsafe_allow_html=True)
    elif 30 <= response < 70:
        st.markdown(f"<div style='background-color: yellow; color: black; padding: 10px; border-radius: 5px;'>{'MODERATE RISK'}</div>", unsafe_allow_html=True)
    else:
        st.markdown(f"<div style='background-color: green; color: black; padding: 10px; border-radius: 5px;'>{'LOW RISK'}</div>", unsafe_allow_html=True)

    st.markdown(f"*Predicted Risk: {response}%*")
