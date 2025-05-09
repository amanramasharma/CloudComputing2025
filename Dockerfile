FROM python:3.10-slim
RUN pip install flask google-cloud-bigquery pandas
COPY main.py .  
CMD ["flask", "run", "--host=0.0.0.0", "--port=8080"]