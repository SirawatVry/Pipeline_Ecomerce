select
      count(*) as failures,
      count(*) != 0 as should_warn,
      count(*) != 0 as should_error
    from (
      
    
    

select
    invoice_month as unique_field,
    count(*) as n_records

from "airflow"."public"."ecom_monthly_revenue"
where invoice_month is not null
group by invoice_month
having count(*) > 1



      
    ) dbt_internal_test