SELECT
    stock_code,
    description,
    SUM(quantity)                       AS total_quantity,
    ROUND(SUM(total_price)::numeric, 2) AS total_revenue,
    COUNT(DISTINCT invoice_no)          AS times_ordered
FROM {{ ref('stg_ecom') }}
GROUP BY stock_code, description
ORDER BY total_revenue DESC
LIMIT 20