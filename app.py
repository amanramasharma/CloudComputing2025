from flask import Flask, render_template_string
from google.cloud import bigquery
import pandas as pd
import plotly.express as px
import plotly.io as pio

app = Flask(__name__)
client = bigquery.Client()

TEMPLATE = """
<!doctype html>
<html>
<head>
  <title>Business Insights Dashboard</title>
  <meta charset="utf-8">
</head>
<body>
  <h1>Revenue by Traffic Source and Age Group</h1>
  <div>{{ traffic_chart|safe }}</div>

  <h2>Top Product Categories by Order Count</h2>
  <div>{{ category_chart|safe }}</div>
</body>
</html>
"""

@app.route("/")
def dashboard():
    traffic_df = get_traffic_data()
    category_df = get_category_data()

    fig1 = px.bar(
        traffic_df,
        x="traffic_source",
        y="total_revenue",
        color="age_group",
        title="Revenue by Traffic Source and Age Group"
    )
    traffic_chart = pio.to_html(fig1, full_html=False)

    fig2 = px.pie(
        category_df,
        names="category",
        values="order_count",
        title="Top Product Categories by Orders"
    )
    category_chart = pio.to_html(fig2, full_html=False)

    return render_template_string(TEMPLATE, traffic_chart=traffic_chart, category_chart=category_chart)

def get_traffic_data():
    query = """
        SELECT
          u.traffic_source,
          CASE
            WHEN u.age < 25 THEN 'Under 25'
            WHEN u.age BETWEEN 25 AND 34 THEN '25–34'
            WHEN u.age BETWEEN 35 AND 44 THEN '35–44'
            WHEN u.age BETWEEN 45 AND 54 THEN '45–54'
            ELSE '55+'
          END AS age_group,
          ROUND(SUM(oi.sale_price), 2) AS total_revenue
        FROM `comm034coursework-6875078.thelook.users` u
        JOIN `comm034coursework-6875078.thelook.orders` o ON u.id = o.user_id
        JOIN `comm034coursework-6875078.thelook.order_items` oi ON o.order_id = oi.order_id
        WHERE o.status = 'Complete'
        GROUP BY traffic_source, age_group
        ORDER BY total_revenue DESC
    """
    return client.query(query).to_dataframe()

def get_category_data():
    query = """
        SELECT
          p.category,
          COUNT(*) AS order_count
        FROM `comm034coursework-6875078.thelook.order_items` oi
        JOIN `comm034coursework-6875078.thelook.products` p ON oi.product_id = p.id
        GROUP BY category
        ORDER BY order_count DESC
        LIMIT 5
    """
    return client.query(query).to_dataframe()

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
