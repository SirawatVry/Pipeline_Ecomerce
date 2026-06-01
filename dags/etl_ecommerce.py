from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime
import pandas as pd
import psycopg2
from airflow.operators.bash import BashOperator

default_args = {
    'owner': 'airflow',
    'start_date': datetime(2024, 1, 1),
}

def extract(**context):
    df = pd.read_csv(
        '/opt/airflow/data/data.csv',
        encoding='ISO-8859-1'
    )
    df.to_parquet('/opt/airflow/data/raw.parquet', index=False)
    print(f"Extracted {len(df)} rows")

def transform(**context):
    df = pd.read_parquet('/opt/airflow/data/raw.parquet')
    df = df.dropna(subset=['CustomerID'])
    df = df[df['Quantity'] > 0]
    df = df[df['UnitPrice'] > 0]
    df['TotalPrice'] = df['Quantity'] * df['UnitPrice']
    df['InvoiceDate'] = pd.to_datetime(df['InvoiceDate'])
    df['InvoiceMonth'] = df['InvoiceDate'].dt.to_period('M').astype(str)
    df['CustomerID'] = df['CustomerID'].astype(int)
    df.to_parquet('/opt/airflow/data/clean.parquet', index=False)
    print(f"Transformed {len(df)} rows")

def load(**context):
    df = pd.read_parquet('/opt/airflow/data/clean.parquet')
    conn = psycopg2.connect(
        host='postgres', database='airflow',
        user='airflow', password='airflow'
    )
    cur = conn.cursor()
    cur.execute("""
        CREATE TABLE IF NOT EXISTS ecommerce_sales (
            invoice_no VARCHAR(20),
            stock_code VARCHAR(20),
            description TEXT,
            quantity INT,
            invoice_date TIMESTAMP,
            unit_price FLOAT,
            customer_id INT,
            country VARCHAR(100),
            total_price FLOAT,
            invoice_month VARCHAR(20)
        )
    """)
    cur.execute("TRUNCATE TABLE ecommerce_sales")
    for _, row in df.iterrows():
        cur.execute("""
            INSERT INTO ecommerce_sales 
            (invoice_no, stock_code, description, quantity,
             invoice_date, unit_price, customer_id, country,
             total_price, invoice_month)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """, (
            row['InvoiceNo'], row['StockCode'], row['Description'],
            row['Quantity'], row['InvoiceDate'], row['UnitPrice'],
            row['CustomerID'], row['Country'], row['TotalPrice'],
            row['InvoiceMonth']
        ))
    conn.commit()
    cur.close()
    conn.close()
    print(f"Loaded {len(df)} rows to PostgreSQL")

def transform_tables(**context):
    conn = psycopg2.connect(
        host='postgres', database='airflow',
        user='airflow', password='airflow'
    )
    cur = conn.cursor()

    # 1. ยอดขายรายเดือน
    cur.execute("DROP TABLE IF EXISTS monthly_revenue")
    cur.execute("""
        CREATE TABLE monthly_revenue AS
        SELECT 
            invoice_month,
            COUNT(DISTINCT invoice_no) AS total_orders,
            COUNT(DISTINCT customer_id) AS unique_customers,
            ROUND(SUM(total_price)::numeric, 2) AS revenue
        FROM ecommerce_sales
        GROUP BY invoice_month
        ORDER BY invoice_month
    """)
    print("monthly_revenue created")

    # 2. สินค้าขายดี Top 20
    cur.execute("DROP TABLE IF EXISTS top_products")
    cur.execute("""
        CREATE TABLE top_products AS
        SELECT 
            stock_code,
            description,
            SUM(quantity) AS total_quantity,
            ROUND(SUM(total_price)::numeric, 2) AS total_revenue,
            COUNT(DISTINCT invoice_no) AS times_ordered
        FROM ecommerce_sales
        GROUP BY stock_code, description
        ORDER BY total_revenue DESC
        LIMIT 20
    """)
    print("top_products created")

    # 3. ลูกค้าดีที่สุด Top 20
    cur.execute("DROP TABLE IF EXISTS top_customers")
    cur.execute("""
        CREATE TABLE top_customers AS
        SELECT 
            customer_id,
            COUNT(DISTINCT invoice_no) AS total_orders,
            SUM(quantity) AS total_items,
            ROUND(SUM(total_price)::numeric, 2) AS total_spent,
            MIN(invoice_date) AS first_purchase,
            MAX(invoice_date) AS last_purchase
        FROM ecommerce_sales
        GROUP BY customer_id
        ORDER BY total_spent DESC
        LIMIT 20
    """)
    print("top_customers created")

    # 4. ประเทศที่ขายดี
    cur.execute("DROP TABLE IF EXISTS sales_by_country")
    cur.execute("""
        CREATE TABLE sales_by_country AS
        SELECT 
            country,
            COUNT(DISTINCT invoice_no) AS total_orders,
            COUNT(DISTINCT customer_id) AS unique_customers,
            ROUND(SUM(total_price)::numeric, 2) AS total_revenue
        FROM ecommerce_sales
        GROUP BY country
        ORDER BY total_revenue DESC
    """)
    print("sales_by_country created")

    conn.commit()
    cur.close()
    conn.close()
    print("\nAll summary tables created!")

def summarize(**context):
    conn = psycopg2.connect(
        host='postgres', database='airflow',
        user='airflow', password='airflow'
    )
    cur = conn.cursor()

    print("\nMonthly Revenue:")
    cur.execute("SELECT * FROM monthly_revenue")
    for row in cur.fetchall():
        print(row)

    print("\nTop 5 Products:")
    cur.execute("SELECT description, total_revenue FROM top_products LIMIT 5")
    for row in cur.fetchall():
        print(row)

    print("\nTop 5 Customers:")
    cur.execute("SELECT customer_id, total_spent FROM top_customers LIMIT 5")
    for row in cur.fetchall():
        print(row)

    print("\nTop 5 Countries:")
    cur.execute("SELECT country, total_revenue FROM sales_by_country LIMIT 5")
    for row in cur.fetchall():
        print(row)

    cur.close()
    conn.close()

with DAG(
    'etl_ecommerce',
    default_args=default_args,
    schedule_interval='@daily',
    catchup=False
) as dag:

    t1 = PythonOperator(task_id='extract', python_callable=extract)
    t2 = PythonOperator(task_id='transform', python_callable=transform)
    t3 = PythonOperator(task_id='load', python_callable=load)
    # t4 = PythonOperator(task_id='transform_tables', python_callable=transform_tables)
    # t5 = PythonOperator(task_id='summarize', python_callable=summarize)
    dbt_run = BashOperator(
        task_id='dbt_run',
        bash_command='/home/airflow/.local/bin/dbt run --profiles-dir /home/airflow/.dbt --project-dir /opt/airflow/dbt_ecommerce',
    )

    dbt_test = BashOperator(
        task_id='dbt_test',
        bash_command='/home/airflow/.local/bin/dbt test --profiles-dir /home/airflow/.dbt --project-dir /opt/airflow/dbt_ecommerce',
    )
 
    t1 >> t2 >> t3 >> dbt_run >> dbt_test