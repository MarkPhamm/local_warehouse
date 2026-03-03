{{
    config(
        materialized='table',
        description='Issue volume by month with growth rates for small multiples time-series'
    )
}}

with complaints as (
    select * from {{ ref('int_cfpb__complaint_metrics') }}
),

monthly_issue as (
    select
        coalesce(issue, 'Unknown') as issue,
        complaint_month_date as month_date,
        extract(year from complaint_month_date) as year,
        extract(month from complaint_month_date) as month,
        count(*) as complaint_count,
        count_if(is_disputed) as disputed_count,
        round(100.0 * count_if(is_disputed) / count(*), 2) as pct_disputed
    from complaints
    where issue is not null and complaint_month_date is not null
    group by issue, complaint_month_date
),

with_prior as (
    select
        curr.issue,
        curr.month_date,
        curr.year,
        curr.month,
        curr.complaint_count,
        curr.disputed_count,
        curr.pct_disputed,
        prev_m.complaint_count as prior_month_count,
        prev_y.complaint_count as prior_year_same_month_count
    from monthly_issue curr
    left join monthly_issue prev_m
        on curr.issue = prev_m.issue
        and prev_m.month_date = date_trunc('month', curr.month_date - interval '1 month')
    left join monthly_issue prev_y
        on curr.issue = prev_y.issue
        and prev_y.month_date = date_trunc('month', curr.month_date - interval '1 year')
),

with_growth as (
    select
        issue,
        month_date,
        year,
        month,
        complaint_count,
        disputed_count,
        pct_disputed,
        prior_month_count,
        prior_year_same_month_count,
        case
            when prior_month_count is null or prior_month_count = 0 then null
            else round(100.0 * (complaint_count - prior_month_count) / prior_month_count, 2)
        end as pct_change_mom,
        case
            when prior_year_same_month_count is null or prior_year_same_month_count = 0 then null
            else round(100.0 * (complaint_count - prior_year_same_month_count) / prior_year_same_month_count, 2)
        end as pct_change_yoy
    from with_prior
)

select * from with_growth
order by issue, month_date
