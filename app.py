from flask import Flask
from google.cloud import bigquery

app = Flask(__name__)
client = bigquery.Client()

@app.route("/")
def index():
    query = """
        SELECT p.category, COUNT(*) AS order_count
        FROM `comm034coursework-6875078.thelook.order_items` AS oi
        JOIN `comm034coursework-6875078.thelook.products` AS p
        ON oi.product_id = p.id
        GROUP BY p.category
        ORDER BY order_count DESC
        LIMIT 5
    """
    df = client.query(query).to_dataframe()
    return df.to_html()
