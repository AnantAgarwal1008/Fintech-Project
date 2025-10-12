FROM python:3.11-slim
WORKDIR /app
COPY services/ml_service_py/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY services/ml_service_py/ .
EXPOSE 8000
CMD ["python", "app.py"]
