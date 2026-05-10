SELECT
    country,
    COUNT(DISTINCT invoice_no)          AS total_orders,
    COUNT(DISTINCT customer_id)         AS unique_customers,
    ROUND(SUM(total_price)::numeric, 2) AS total_revenue
FROM {{ ref('stg_ecom') }}
GROUP BY country
ORDER BY total_revenue DESC