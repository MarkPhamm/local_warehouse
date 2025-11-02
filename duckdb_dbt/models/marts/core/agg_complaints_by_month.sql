{{
    config(
        materialized='table'
    )
}}

with complaints as (
    select * from {{ ref('int_cfpb__complaint_metrics') }}
),

monthly_stats as (
    select
        complaint_month_date,
        extract(year from complaint_month_date) as year,
        extract(month from complaint_month_date) as month,

        -- volume metrics
        count(*) as total_complaints,
        count(distinct company) as unique_companies,
        count(distinct product) as unique_products,
        count(distinct state) as unique_states,

        -- response metrics
        count_if(is_timely_response) as timely_responses,
        round(100.0 * count_if(is_timely_response) / count(*), 2) as pct_timely,

        -- dispute metrics
        count_if(is_disputed) as disputed_complaints,
        round(100.0 * count_if(is_disputed) / count(*), 2) as pct_disputed,

        -- narrative metrics
        count_if(has_narrative) as complaints_with_narrative,
        round(100.0 * count_if(has_narrative) / count(*), 2) as pct_with_narrative,

        -- response time
        round(avg(days_to_response), 2) as avg_days_to_response,
        median(days_to_response) as median_days_to_response

    from complaints
    where complaint_month_date is not null
    group by complaint_month_date
)

select * from monthly_stats
order by complaint_month_date desc
