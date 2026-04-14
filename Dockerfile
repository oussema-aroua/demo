FROM python:3.14.4-slim
WORKDIR /app
COPY app.py .
RUN apt-get update && apt-get install -y curl
RUN pip install psycopg2-binary
CMD ["python", "app.py"]
