import streamlit as st
import requests
import base64

#define webpage
PAGES = {
    'Homepage': None,
    'Initial Risk Assessment': 'initial_page',
    'Advanced Risk Assessment': 'advanced_page'}


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
    st.write("Risk_ICU is a tool to assess the mortality risk of patients on the Intensive Care Unit (ICU). It can be used either for a quick initial risk stratification at the first patient encounter or with more laboratory values and further clinical assessment as an advanced risk stratification device.")
    st.write("In the context of the project weeks for the Le Wagon Data Science Bootcamp (Batch 1601), we have trained and deployed two machine learning models:")
    st.write("- The initial risk assessment model, is intended to be used by medical personnel as a quick first assessment for patients that have just entered the ICU. The data points used to train the model were minimum, simulating only those parameters 24/7 available for risk assessments in all ICUs independently of the hospital´s level of care. To predict the risk, we used a XGBoost model, which was optimized using random search after extensive data preprocessing.")
    st.write("- The advanced risk assessment model was trained with more complex values that e.g. require clinical laboratories. We opted against the usage of parameters that require a specific technical infrastructure to make the application available to as many hospitals as possible. For this task we built a machine learning structure optimized via random search consisting of a Decision Tree model with Adaptive Boosting combined through stacking with a XGBoost model.")
    st.write("To train and test our models we used patient data from the first 24 hours of an ICU stay, as made available by MIT's GOSSIS community initiative, with privacy certification from the Harvard Privacy Lab. This dataset contains more than 130,000 individual ICU visits from multiple countries, spanning a one-year timeframe.")
    st.write("Please use the navigation bar on the left to get to the models")
    st.subheader("Authors:")
    st.write("- Julia Decker [Connect on LinkedIn](https://www.linkedin.com/in/juliadeckerpotsdam/)")
    st.write("- William Brudenell [Connect on LinkedIn](https://www.linkedin.com/in/willbrudenell/)")
    st.write("- Francisco Chaves [Connect on LinkedIn](https://www.linkedin.com/in/francisco-chaves-b32798277)")
    st.write("- Dominik Naumann [Connect on LinkedIn](https://www.linkedin.com/in/dr-med-univ-dominik-naumann-37217595)")
    st.write("Feel free to check out the [slides](https://docs.google.com/presentation/d/1VPHEraQF5XaodlEiBV8Vn6eY_enAjMVZZRviK91wvWA/edit?usp=sharing) and the [presentation](https://www.youtube.com) for this project")



# Based on the user's selection, present corresponding interface
def display_initial_risk_assessment():
    st.subheader("Initial Risk Assessment")
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
    lactate_max = col2.number_input("Lactate (mmol/L)", value = 0)
    sysbp_min = col1.number_input("Systolic Blood Pressure (mmHg)", value = 0)
    mpb_min = col2.number_input("Mean Arterial Pressure (mmHg)", value = 0)
    hr_max = col1.number_input("Heart Rate (bpm/min)", value =0)
    temp_min = col2.number_input("Temperature (°C)", value =0)
    rr_min = col1.number_input("Respiratory Rate (breaths/min)", value = 0)
    spo2_max = col2.number_input("SpO2 (%)", value =0)


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
    st.subheader("Advanced Risk Assessment")
    st.subheader("Please Enter Patient Details:")
    col1, col2 = st.columns(2)

    age = col1.number_input("Age (years)", value = 0)
    bmi = col2.number_input("BMI (kg/qm)", value = 0)
    temp_min = col1.number_input("Minimal Temperature (°C)", value =0)
    temp_max = col2.number_input("Maximal Temperature (°C)", value =0)
    hr_max = col2.number_input("Maximal Heart Rate (bpm/min)", value =0)
    hr_min = col1.number_input("Minimal Heart Rate (bpm/min)", value =0)
    sysbp_max = col2.number_input("Maximal Systolic Blood Pressure (mmHg)", value = 0)
    sysbp_min = col1.number_input("Minimal Systolic Blood Pressure (mmHg)", value = 0)
    rr_max = col2.number_input("Maximal Respiratory Rate (breaths/min)", value = 0)
    rr_min = col1.number_input("Minimal Respiratory Rate (breaths/min)", value = 0)
    mbp_min = col1.number_input("Mean Arterial Pressure (mmHg)", value = 0)
    hco3_max = col2.number_input("Maximal Bicarbonate (mmol/L)", value = 0)
    glucose_min = col1.number_input("Minimal Glucose (mmol/L)", value = 0)
    sodium_min = col2.number_input("Minimal Sodium (mmol/L)", value = 0)
    wbc_min = col1.number_input("Minimal White Blood Cell Count (10^9/L)", value =0)
    wbc_max = col2.number_input("Maximal White Blood Cell Count (10^9/L)", value =0)
    bun_max = col1.number_input("BUN (mmol/L)", value = 0)
    crea_max = col2.number_input("Creatinine (mmol/L)", value = 0)
    platelets_min = col1.number_input("Minimal Platelets (mmol/L)", value = 0)
    hema_min = col2.number_input("Minimal Hemaglobin (g/dL)", value = 0)
    gcs_eyes = st.selectbox("GCS Eyes", [1, 2, 3, 4])
    gcs_verbal = st.selectbox("GCS Verbal", [1, 2, 3, 4, 5])
    gcs_motor = st.selectbox("GCS Motor", [1, 2, 3, 4, 5, 6])
    ventilated = st.selectbox("Patient on Ventilation?", ["yes", "no"])
    spo2_min = st.number_input("Minimal SpO2 (%)", value =0)
    icu_admit = st.selectbox("Patient Admitted from the Emergency Room?", ["yes", "no"])


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
    elif page == 'Initial Risk Assessment':
        display_initial_risk_assessment()
    elif page == 'Advanced Risk Assessment':
        display_advanced_risk_assessment()

if __name__ == '__main__':
    run_UI()
