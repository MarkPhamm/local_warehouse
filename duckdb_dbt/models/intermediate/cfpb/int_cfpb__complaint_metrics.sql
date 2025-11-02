{{
    config(
        materialized='view'
    )
}}

with complaints as (
    select * from {{ ref('stg_cfpb__complaints') }}
),

enriched as (
    select
        *,

        -- calculate days to company response
        datediff('day', date_received, date_sent_to_company) as days_to_response,

        -- flag for timely response
        case
            when timely = 'Yes' then true
            when timely = 'No' then false
            else null
        end as is_timely_response,

        -- flag for consumer dispute
        case
            when consumer_disputed = 'Yes' then true
            when consumer_disputed = 'No' then false
            else null
        end as is_disputed,

        -- flag for complaints with narrative
        case
            when complaint_what_happened is not null then true
            else false
        end as has_narrative,

        -- extract year and month for time-based analysis
        extract(year from date_received) as complaint_year,
        extract(month from date_received) as complaint_month,
        date_trunc('month', date_received) as complaint_month_date

    from complaints
)

select * from enriched
