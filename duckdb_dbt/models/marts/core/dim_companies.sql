{{
    config(
        materialized='table'
    )
}}

with complaints as (
    select * from {{ ref('int_cfpb__complaint_metrics') }}
),

company_stats as (
    select
        company,

        -- complaint counts
        count(*) as total_complaints,
        count_if(is_disputed) as disputed_complaints,
        count_if(is_timely_response) as timely_responses,
        count_if(has_narrative) as complaints_with_narrative,

        -- percentages
        round(100.0 * count_if(is_disputed) / count(*), 2) as pct_disputed,
        round(100.0 * count_if(is_timely_response) / count(*), 2) as pct_timely,

        -- response time metrics
        round(avg(days_to_response), 2) as avg_days_to_response,
        median(days_to_response) as median_days_to_response,
        min(days_to_response) as min_days_to_response,
        max(days_to_response) as max_days_to_response,

        -- date range
        min(date_received) as first_complaint_date,
        max(date_received) as last_complaint_date

    from complaints
    where company is not null
    group by company
)

select * from company_stats
order by total_complaints desc
