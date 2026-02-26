FROM python:3.13-slim

WORKDIR /app

RUN apt-get update && apt-get install -y 

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt


RUN playwright install chromium
RUN playwright install-deps chromium

COPY . .

EXPOSE 8501

CMD ["streamlit", "run", "app/main.py", "--server.port=8501", "--server.address=0.0.0.0"]