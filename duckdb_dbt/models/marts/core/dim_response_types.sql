{{
    config(
        materialized='table'
    )
}}

with complaints as (
    select * from {{ ref('int_cfpb__complaint_metrics') }}
),

response_stats as (
    select
        company_response,

        -- complaint counts
        count(*) as total_complaints,
        count(distinct company) as unique_companies,
        count(distinct product) as unique_products,
        count(distinct state) as unique_states,

        -- timeliness metrics
        count_if(is_timely_response) as timely_responses,
        round(100.0 * count_if(is_timely_response) / count(*), 2) as pct_timely,

        -- dispute metrics
        count_if(is_disputed) as disputed_complaints,
        round(100.0 * count_if(is_disputed) / count(*), 2) as pct_disputed,

        -- narrative metrics
        count_if(has_narrative) as complaints_with_narrative,
        round(100.0 * count_if(has_narrative) / count(*), 2) as pct_with_narrative,

        -- response time metrics
        round(avg(days_to_response), 2) as avg_days_to_response,
        median(days_to_response) as median_days_to_response,
        min(days_to_response) as min_days_to_response,
        max(days_to_response) as max_days_to_response,

        -- date range
        min(date_received) as first_complaint_date,
        max(date_received) as last_complaint_date,

        -- most common associations
        mode() within group (order by product) as most_common_product,
        mode() within group (order by issue) as most_common_issue,
        mode() within group (order by company) as most_complained_company

    from complaints
    where company_response is not null
    group by company_response
)

select * from response_stats
order by total_complaints desc
