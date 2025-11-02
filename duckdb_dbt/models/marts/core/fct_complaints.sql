{{
    config(
        materialized='table'
    )
}}

with complaint_metrics as (
    select * from {{ ref('int_cfpb__complaint_metrics') }}
),

final as (
    select
        -- identifiers
        complaint_id,

        -- dimensions
        product,
        sub_product,
        issue,
        sub_issue,
        company,
        state,
        zip_code,
        submitted_via,
        company_response,
        company_public_response,

        -- dates
        date_received,
        date_sent_to_company,
        complaint_year,
        complaint_month,
        complaint_month_date,

        -- metrics
        days_to_response,
        is_timely_response,
        is_disputed,
        has_narrative,
        consumer_consent_provided,

        -- text (for detailed analysis)
        complaint_what_happened,
        tags

    from complaint_metrics
)

select * from final
