{{
    config(
        materialized='table',
        description='% disputed per issue: dispute ratio for root cause and theme analysis'
    )
}}

with complaints as (
    select * from {{ ref('int_cfpb__complaint_metrics') }}
),

by_issue as (
    select
        coalesce(issue, 'Unknown') as issue,
        count(*) as total_complaints,
        count_if(is_disputed) as disputed_count,
        round(100.0 * count_if(is_disputed) / count(*), 2) as pct_disputed,
        count(distinct product) as unique_products,
        count(distinct state) as unique_states,
        count(distinct company) as unique_companies
    from complaints
    where issue is not null
    group by issue
)

select * from by_issue
order by total_complaints desc
