import streamlit as st
import requests

# Function to make API requests
def make_api_request(url, data):
    response = requests.post(url, json=data)
    return response.json()

# Streamlit app
def main():
    st.title("ICU Risk Prediction")
    option = st.selectbox("Select Time Interval", ("After 1 hour", "After 24 hours"))

    if option == "After 1 hour":
        if st.button("Predict"):
            # Make API request to predict after 1 hour
            prediction = make_api_request("http://localhost:8000/predict_hour", {})
            st.write(prediction)
    elif option == "After 24 hours":
        if st.button("Predict"):
            # Make API request to predict after 24 hours
            prediction = make_api_request("http://localhost:8000/predict_day", {})
            st.write(prediction)

if __name__ == "__main__":
    main()
