select
      count(*) as failures,
      count(*) != 0 as should_warn,
      count(*) != 0 as should_error
    from (
      
    
    



select revenue
from "airflow"."public"."ecom_monthly_revenue"
where revenue is null



      
    ) dbt_internal_test