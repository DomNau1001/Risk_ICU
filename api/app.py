import streamlit as st
import requests
from datetime import datetime
import pandas as pd

#define webpage
st.markdown("# NY taxi-fare calculator")

col1, col2, col3, col4, col5, col6, col7 = st.columns(7)
date = col1.text_input("Date (format: y-m-d)", value = "2023-03-15")
time = col2.text_input("Time (format: h:m:s)", value = "17:00:00")
pickup_long = col3.text_input("Pickup Longitude", value = -73.968285)
pickup_lat = col4.text_input("Pickup Latitude", value = 40.785091)
dropoff_long = col5.text_input("Dropoff Longitude", value = -73.780968)
dropoff_lat = col6.text_input("Dropoff Latitude", value = 40.641766)
passengers = col7.text_input("Passenger Count", value = 1)


#call API
url = 'https://taxifare.lewagon.ai/predict'

date_time = date + " " + time
date_formatted = datetime.fromisoformat(date_time)


params = {"pickup_datetime": date_formatted,
          "pickup_longitude": pickup_long,
          "pickup_latitude": pickup_lat,
          "dropoff_longitude": dropoff_long,
          "dropoff_latitude": dropoff_lat,
          "passenger_count": passengers}

response = requests.get(url, params=params).json()["fare"]
response = round(response, 2)

#display result to user
st.markdown(f"**Predicted Fare: ${response}**")

data = pd.DataFrame([[float(pickup_lat), float(pickup_long)], [float(dropoff_lat), float(dropoff_long)]],
             columns=['lat', 'lon'])

st.map(data)
