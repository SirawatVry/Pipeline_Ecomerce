
  create view "airflow"."public"."ecom_top_customers__dbt_tmp"
    
    
  as (
    SELECT
    customer_id,
    COUNT(DISTINCT invoice_no)          AS total_orders,
    SUM(quantity)                       AS total_items,
    ROUND(SUM(total_price)::numeric, 2) AS total_spent,
    MIN(invoice_date)                   AS first_purchase,
    MAX(invoice_date)                   AS last_purchase
FROM "airflow"."public"."stg_ecom"
GROUP BY customer_id
ORDER BY total_spent DESC
LIMIT 20
  );