{{
    config(
        materialized='view'
    )
}}

with source as (
    select * from {{ source('raw', 'cfpb_complaints') }}
),

renamed as (
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

        -- dates
        date_received::date as date_received,
        date_sent_to_company::date as date_sent_to_company,

        -- responses
        company_response,
        company_public_response,
        timely,
        consumer_disputed,
        consumer_consent_provided,

        -- text
        complaint_what_happened,
        tags,

        -- metadata
        _dlt_extracted_at as dbt_extracted_at,
        _dlt_load_id as dbt_load_id

    from source
)

select * from renamed
