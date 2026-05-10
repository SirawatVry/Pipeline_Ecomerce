
    
    

select
    invoice_month as unique_field,
    count(*) as n_records

from "airflow"."public"."ecom_monthly_revenue"
where invoice_month is not null
group by invoice_month
having count(*) > 1


