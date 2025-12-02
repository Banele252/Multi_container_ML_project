FROM python:3.11-slim

WORKDIR /app

RUN pip install --no-cache-dir --upgrade pip

COPY requirements.txt /app

RUN pip install --no-cache-dir -r requirements.txt

COPY . /app

EXPOSE 8501

ENV BACKEND_CONTAINER=model_backend_app

CMD ["streamlit", "run", "main.py", "--server.port=8501","--server.address=0.0.0.0","--server.headless=true"]
