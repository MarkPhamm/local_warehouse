{{
    config(
        materialized='table',
        description='Cross-tab Issue × State for state map and geographic filters'
    )
}}

with complaints as (
    select * from {{ ref('int_cfpb__complaint_metrics') }}
),

issue_state as (
    select
        coalesce(issue, 'Unknown') as issue,
        coalesce(state, 'Unknown') as state,
        count(*) as complaint_count,
        count_if(is_disputed) as disputed_count,
        round(100.0 * count_if(is_disputed) / count(*), 2) as pct_disputed,
        count(distinct company) as unique_companies,
        count(distinct product) as unique_products
    from complaints
    where issue is not null and state is not null and state != ''
    group by issue, state
),

total_by_issue as (
    select
        issue,
        sum(complaint_count) as issue_total
    from issue_state
    group by issue
)

select
    ip.issue,
    ip.state,
    ip.complaint_count,
    ip.disputed_count,
    ip.pct_disputed,
    ip.unique_companies,
    ip.unique_products,
    round(100.0 * ip.complaint_count / nullif(t.issue_total, 0), 2) as pct_of_issue_complaints
from issue_state ip
join total_by_issue t on ip.issue = t.issue
order by ip.issue, ip.complaint_count desc
