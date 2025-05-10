from flask import Flask, jsonify, render_template_string, request
from google.cloud import bigquery
import pandas as pd
import plotly.express as px

app = Flask(__name__)
client = bigquery.Client()

TEMPLATE = """
<!doctype html>
<html>
  <head>
    <title>TheLook Dashboard</title>
    <meta charset="utf-8">
  </head>
  <body>
    <h1>Top 5 Product Categories by Order Count</h1>
    <div>{{ plot_div|safe }}</div>
    <h2>API Access</h2>
    <p>To access the raw data in JSON format, use <code>/api/data</code></p>

    <h2>Run ML Prediction</h2>
    <form action="/predict" method="get">
      <button type="submit">Run ML Clustering Prediction</button>
    </form>
  </body>
</html>
"""

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
    fig = px.bar(df, x='category', y='order_count', title='Top 5 Categories')
    plot_div = fig.to_html(full_html=False)
    return render_template_string(TEMPLATE, plot_div=plot_div)

@app.route("/api/data")
def api_data():
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
    return jsonify(df.to_dict(orient="records"))

@app.route("/predict")
def predict():
    query = """
        SELECT * FROM ML.PREDICT(
          MODEL `comm034coursework-6875078.thelook.customer_segment_clustering`,
          (
            SELECT user_id,
                   ROUND(AVG(sale_price), 2) AS avg_spend,
                   COUNT(DISTINCT order_id) AS count_orders,
                   DATE_DIFF(CURRENT_DATE(), MAX(created_at), DAY) AS days_since_order
            FROM `comm034coursework-6875078.thelook.orders` o
            JOIN `comm034coursework-6875078.thelook.order_items` oi
            ON o.order_id = oi.order_id
            WHERE o.status = 'Complete'
            GROUP BY user_id
          )
        )
    """
    df = client.query(query).to_dataframe()
    return df.to_html()

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
