{{ config(materialized="view") }}

with
    tripdata as (
        select *
        from {{ source("staging", "fhv_tripdata") }}
        where dispatching_base_num is not null
    )
select
    -- identifiers
    {{ dbt_utils.generate_surrogate_key(["dispatching_base_num", "pickup_datetime"]) }}
    as trip_id,
    {{ dbt.safe_cast("dispatching_base_num", api.Column.translate_type("string")) }}
    as dispatching_base_num,
    {{ dbt.safe_cast("PUlocationID", api.Column.translate_type("integer")) }}
    as pickup_location_id,
    {{ dbt.safe_cast("DOlocationID", api.Column.translate_type("integer")) }}
    as dropoff_location_id,

    -- timestamps
    cast(pickup_datetime as timestamp) as pickup_datetime,
    cast(dropoff_datetime as timestamp) as dropoff_datetime,

    -- trip info
    {{ dbt.safe_cast("SR_flag", api.Column.translate_type("integer")) }} as sr_flag
from tripdata
where cast(pickup_datetime as date) between '2019-01-01' and '2019-12-31'
-- where DATE(pickup_datetime) >= DATE('2019-01-01') and DATE(pickup_datetime) <= DATE('2019-12-31')

-- dbt build --select <model_name> --vars '{'is_test_run': 'false'}'
{% if var("is_test_run", default=true) %} limit 100 {% endif %}
