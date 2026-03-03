{{
    config(
        materialized='table',
        description='Issue frequency by product: cross-tab for Heatmap (Issue × Product) and Treemap'
    )
}}

with complaints as (
    select * from {{ ref('int_cfpb__complaint_metrics') }}
),

issue_product as (
    select
        coalesce(issue, 'Unknown') as issue,
        coalesce(product, 'Unknown') as product,
        count(*) as complaint_count,
        count_if(is_disputed) as disputed_count,
        round(100.0 * count_if(is_disputed) / count(*), 2) as pct_disputed,
        count(distinct company) as unique_companies,
        count(distinct state) as unique_states
    from complaints
    where issue is not null and product is not null
    group by issue, product
),

total_complaints as (
    select sum(complaint_count) as total from issue_product
)

select
    ip.issue,
    ip.product,
    ip.complaint_count,
    ip.disputed_count,
    ip.pct_disputed,
    ip.unique_companies,
    ip.unique_states,
    round(100.0 * ip.complaint_count / nullif(t.total, 0), 2) as pct_of_all_complaints
from issue_product ip
cross join total_complaints t
order by ip.complaint_count desc
