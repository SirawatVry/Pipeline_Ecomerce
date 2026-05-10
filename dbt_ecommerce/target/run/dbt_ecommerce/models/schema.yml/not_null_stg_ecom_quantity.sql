select
      count(*) as failures,
      count(*) != 0 as should_warn,
      count(*) != 0 as should_error
    from (
      
    
    



select quantity
from "airflow"."public"."stg_ecom"
where quantity is null



      
    ) dbt_internal_test