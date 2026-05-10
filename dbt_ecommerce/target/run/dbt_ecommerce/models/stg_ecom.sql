
  create view "airflow"."public"."stg_ecom__dbt_tmp"
    
    
  as (
    SELECT
    "invoice_no"     AS invoice_no,
    "stock_code"     AS stock_code,
    "description"   AS description,
    "quantity"      AS quantity,
    "invoice_date"::timestamp AS invoice_date,
    "unit_price"     AS unit_price,
    "customer_id"::int AS customer_id,
    "country"       AS country,
    "quantity" * "unit_price" AS total_price,
    TO_CHAR("invoice_date"::timestamp, 'YYYY-MM') AS invoice_month
FROM ecommerce_sales
WHERE "customer_id" IS NOT NULL
  AND "quantity" > 0
  AND "unit_price" > 0
  );