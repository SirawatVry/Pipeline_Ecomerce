select
      count(*) as failures,
      count(*) != 0 as should_warn,
      count(*) != 0 as should_error
    from (
      
    
    



select invoice_no
from "airflow"."public"."stg_ecom"
where invoice_no is null



      
    ) dbt_internal_test