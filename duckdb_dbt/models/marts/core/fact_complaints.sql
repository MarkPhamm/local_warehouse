{{
    config(
        materialized='view',
        description='BI-facing alias for fct_complaints; use for filters and detail-level analysis'
    )
}}

select * from {{ ref('fct_complaints') }}
