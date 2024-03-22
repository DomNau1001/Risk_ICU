import streamlit as st

# Function to get user input for one hour patient
def get_one_hour_patient_data():
    st.subheader("Enter One Hour Patient Details:")

    bmi = st.number_input("BMI")
    age = st.number_input("Age")
    gender = st.number_input("Gender")
    pre_icu_days = st.number_input("Previous ICU Days")
    elective_surgery = st.number_input("Elective Surgery")
    glucose_min = st.number_input("Glucose Min")
    glucose_max = st.number_input("Glucose Max")
    sysbp_min = st.number_input("SysBP Min")
    sysbp_max = st.number_input("SysBP Max")
    inr_min = st.number_input("INR Min")
    inr_max = st.number_input("INR Max")
    spo2_min = st.number_input("SpO2 Min")
    spo2_max = st.number_input("SpO2 Max")
    hr_max = st.number_input("HR Max")
    hr_min = st.number_input("HR Min")

    # Get user input as dictionary
    one_hour_patient_data = {
        "BMI": bmi,
        "Age": age,
        "Gender": gender,
        "Previous ICU Days": pre_icu_days,
        "Elective Surgery": elective_surgery,
        "Glucose Min": glucose_min,
        "Glucose Max": glucose_max,
        "SysBP Min": sysbp_min,
        "SysBP Max": sysbp_max,
        "INR Min": inr_min,
        "INR Max": inr_max,
        "SpO2 Min": spo2_min,
        "SpO2 Max": spo2_max,
        "HR Max": hr_max,
        "HR Min": hr_min
    }
    return one_hour_patient_data

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

def main():
    # Streamlit page title
    st.title("ICU Risk Prediction")

    # Display welcome message
    st.write("Welcome to ICU Risk Prediction Application!")

    # Display options for the user to choose
    option = st.selectbox("Choose Option:", ["1 hour patient results", "24 hour patient results"])

    # Based on the user's selection, get relevant patient data
    if option == "1 hour patient results":
        one_hour_patient_data = get_one_hour_patient_data()
        # Call API to get prediction result using one_hour_patient_data
        # Display prediction result
    elif option == "24 hour patient results":
        twenty_four_hour_patient_data = get_twenty_four_hour_patient_data()
        # Call API to get prediction result using twenty_four_hour_patient_data
        # Display prediction result

if __name__ == "__main__":
    main()
