select
      count(*) as failures,
      count(*) != 0 as should_warn,
      count(*) != 0 as should_error
    from (
      
    
    



select invoice_month
from "airflow"."public"."ecom_monthly_revenue"
where invoice_month is null



      
    ) dbt_internal_test