import streamlit as st

# Function to get user input for one hour patient
def get_one_hour_patient_data():
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


    # Get user input as dictionary
    return bmi, age, gender, pre_icu_days, elective_surg, glucose_min, glucose_max, sysbp_min, sysbp_max, inr_min, inr_max, spo2_min, spo2_max, hr_min, hr_max

# Function to get user input for 24 hour patient
def get_twenty_four_hour_patient_data():
    st.subheader("Enter 24 Hour Patient Details")
    # Add input fields for 24 hour patient details
    # Example: age, blood pressure, heart rate, etc.
    age = st.number_input("Age")
    blood_pressure = st.number_input("Blood Pressure")
    heart_rate = st.number_input("Heart Rate")
    # Add more input fields as needed

    # Get user input as dictionary
    twenty_four_hour_patient_data = {
        "age": age,
        "blood_pressure": blood_pressure,
        "heart_rate": heart_rate,
        # Add more data fields as needed
    }
    return twenty_four_hour_patient_data
