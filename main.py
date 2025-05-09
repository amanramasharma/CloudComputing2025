from flask import Flask
from google.cloud import bigquery

app = Flask(__name__)
client = bigquery.Client()

@app.route("/")
def index():
    query = "SELECT category, COUNT(*) AS order_count FROM `comm034coursework-6875078.thelook.order_items` GROUP BY category ORDER BY order_count DESC LIMIT 5"
    result = client.query(query).to_dataframe()
    return result.to_html()