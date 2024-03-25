FROM python:3.9

WORKDIR /app

COPY api /app/api
COPY ml_logic /app/ml_logic
COPY api/requirements.txt /app
COPY mm_scaler.pkl /app
COPY 1_h_model.pkl /app

RUN pip install --upgrade pip
RUN pip install -r requirements.txt

CMD ["uvicorn", "api.fast_api:app", "--host", "0.0.0.0", "--port", "8000"]
