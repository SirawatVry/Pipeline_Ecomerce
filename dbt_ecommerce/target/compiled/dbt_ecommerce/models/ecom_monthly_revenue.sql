SELECT
    invoice_month,
        COUNT(DISTINCT invoice_no) AS total_invoices,
        COUNT(DISTINCT customer_id) AS Unique_customers,
        ROUND(SUM(total_price)::numeric, 2) AS revenue
FROM "airflow"."public"."stg_ecom"
GROUP BY invoice_month
ORDER BY invoice_month