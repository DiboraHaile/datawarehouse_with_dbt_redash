{{ config(materialized='table') }}

with traffic_data as (

    select vehicle_type,geo_location,avg_speed,traveled_d as traveled_distance,concat(time_min,'-',time_max) as time_range
    from 
    trajectory
)

select *
from traffic_data