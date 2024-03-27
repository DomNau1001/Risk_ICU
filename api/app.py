import streamlit as st
import requests
import base64

#define webpage
PAGES = {
    'Homepage': None,
    'Initial RA (1 hour)': 'initial_page',
    'Advanced RA (24 hours)': 'advanced_page'}


def display_homepage():
    def center_vertically(image_path, text):
        """Centers the image and text vertically using columns and CSS."""
        # Read image data as bytes
        with open(image_path, "rb") as image_file:
            image_data = image_file.read()

        # Encode image data as Base64 string
        base64_data = base64.b64encode(image_data).decode("utf-8")

        # Define HTML template for centered image
        image_template = """
            <div style="display: flex; align-items: center;">
            <img src="data:image/png;base64,%s" width="200" height="auto">
            </div>
            """ % base64_data

        # Create Streamlit columns with adjusted weights (more weight for col2)
        col1, col2 = st.columns([1, 2])  # Adjust weights here

        # Display image in left column with centered HTML template
        with col1:
            st.markdown(image_template, unsafe_allow_html=True)

        # Display text in right column with centered CSS
        with col2:
            st.markdown(f"<h1 style='text-align: center;'>{text}</h1>", unsafe_allow_html=True)
    image_path = "clipart2872083.png"
    text = "Welcome to Risk_ICU!"
    center_vertically(image_path, text)
    # Additional content after the container
    st.write("")
    st.write("Summary:")
    st.write("Risk ICU is a tool for assessing risk in ICU patients in the first 24 hrs in the ICU.")
    st.write("In the context of the final project for the Le Wagon Data Science Bootcamp, we have trained and deployed two machine learning models:")
    st.write("- The 1 hr model, is intended to be used as a quick first assessment for ICU patients. The data points used to train the model were minimum, simulating those available for risk assessments in ICUs during the patient’s first hour. To predict the risk, we used the XGBoost model, which was optimized using random search.")
    st.write("- The 24 hr model was trained with patient's values available after 24 hs in the ICU. To predict the risk, we used a combination of decision trees and XGBoost.")
    st.write("To train and test our models we used data from the first 24 hours of intensive care unit, as made available by MIT's GOSSIS community initiative, with privacy certification from the Harvard Privacy Lab. This dataset contains more than 130,000 hospital Intensive Care Unit (ICU) visits from patients, spanning a one-year timeframe.")
    st.subheader("Authors:")
    st.write("- Dominik Naumann: [Connect](https://www.linkedin.com/)")
    st.write("- Francisco Chaves")
    st.write("- William Brudenell")
    st.write("- Julia Decker")
    st.write("You can add more content here, such as:")
    st.write("- Links to documentation or resources")
    st.write("- Contact information")
    st.write("- Information about the development team")
    st.write("- Any other relevant information")



# Based on the user's selection, present corresponding interface
def display_initial_risk_assessment():
    st.subheader("Initial Risk Assessment (1 hour)")
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


def display_advanced_risk_assessment():
    st.subheader("Advanced Risk Assessment (24 hours)")
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


# main function
def run_UI():
    st.set_page_config(
        page_title="Risk_ICU",
        page_icon="🏥",
        initial_sidebar_state="expanded",
        menu_items={
            'Report a bug': "https://www.google.com/",
            'About': "Made with love and care xox"
        }
    )
    st.sidebar.title('Risk_ICU')
    page = st.sidebar.selectbox('Navigation', list(PAGES.keys()), index=0)
    # Display the selected page
    if page == 'Homepage':
        display_homepage()
    elif page == 'Initial RA (1 hour)':
        display_initial_risk_assessment()
    elif page == 'Advanced RA (24 hours)':
        display_advanced_risk_assessment()

if __name__ == '__main__':
    run_UI()
