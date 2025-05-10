FROM python:3.11-slim
WORKDIR /app
RUN apt-get update && apt-get install -y build-essential
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
EXPOSE 8080
ENV FLASK_APP=app.py
ENV PORT=8080
CMD ["flask", "run", "--host=0.0.0.0", "--port=8080"]