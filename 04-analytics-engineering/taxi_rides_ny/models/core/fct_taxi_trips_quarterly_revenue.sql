{{ config(materialized='table') }}

with trips_data as (
    select * from {{ ref('fact_trips') }}
),

base as (
    select 
    -- Reveneue grouping 
    {{ dbt.date_trunc("quarter", "pickup_datetime") }} as revenue_quarter, 
    service_type, 

    -- Revenue calculation 
    sum(total_amount) as revenue_quarterly_total_amount,

    from trips_data
    group by 1,2

),

lag_calc as (
    select *,
        lag(revenue_quarterly_total_amount, 4) over(partition by service_type order by revenue_quarter) as lagging_quarter
    from base
)

select *,
  case when coalesce(lagging_quarter, 0) != 0 then revenue_quarterly_total_amount / lagging_quarter - 1 else null end as yoy_change
from lag_calc