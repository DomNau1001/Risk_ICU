FROM python:3.9

WORKDIR /app

COPY APIs /app/APIs
COPY requirements.txt /app

RUN pip install -r requirements.txt

EXPOSE 8000

CMD ["uvicorn", "APIs.main:app", "--host", "0.0.0.0", "--port", "8000"]
