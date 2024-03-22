from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def read_root():
    return {"message": "Welcome to the ICU Risk Prediction API!"}

@app.post("/predict_hour")
def predict_after_1_hour():
    # Logic to handle prediction after 1 hour
    return {"prediction": "Prediction after 1 hour"}

@app.post("/predict_day")
def predict_after_24_hours():
    # Logic to handle prediction after 24 hours
    return {"prediction": "Prediction after 24 hours"}
