FROM python:3.9

WORKDIR /app

COPY api /app/api
COPY ml_logic /app/ml_logic
COPY api/requirements.txt /app
COPY mm_scaler_1.pkl /app
COPY mm_scaler_24.pkl /app
COPY 1h_model_saved.pkl /app
COPY 24h_model_saved.pkl /app

RUN pip install --upgrade pip
RUN pip install -r requirements.txt

CMD ["uvicorn", "api.fast_api:app", "--host", "0.0.0.0", "--port", "8000"]
