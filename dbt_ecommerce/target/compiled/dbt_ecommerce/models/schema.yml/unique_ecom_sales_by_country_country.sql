
    
    

select
    country as unique_field,
    count(*) as n_records

from "airflow"."public"."ecom_sales_by_country"
where country is not null
group by country
having count(*) > 1


