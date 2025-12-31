-- Load NYC Taxi dataset into Pig Script
nyc_taxi_raw = LOAD '/user/maria_dev/raw_datasets/raw_nyc_taxi_datasets'
USING PigStorage(',')
AS (
    vendor_id: chararray,
    pickup_datetime: chararray,
    dropoff_datetime: chararray,
    passenger_count: int,
    trip_distance: double,
    pickup_longitude: double,
    pickup_latitude: double,
    ratecode_id: int,
    store_fwd_flag: chararray,
    dropoff_longitude: double,
    dropoff_latitude: double,
    payment_type: int,
    fare_amount: double,
    extra: double,
    mta_tax: double,
    tip_amount: double,
    tolls_amount: double,
    improvement_subcharge: double,
    total_amount: double
);

-- Remove invalid or corrupt records
nyc_taxi_clean = FILTER nyc_taxi_raw BY
    passenger_count > 0 AND
    trip_distance > 0 AND
    fare_amount > 0 AND
    total_amount > 0 AND
    pickup_longitude IS NOT NULL AND
    pickup_latitude IS NOT NULL AND
    dropoff_longitude IS NOT NULL AND
    dropoff_latitude IS NOT NULL;

-- Extract pickup hour for time-based analysis
nyc_taxi_time = FOREACH nyc_taxi_clean GENERATE
    vendor_id,
    SUBSTRING(pickup_datetime, 11, 13) AS pickup_hour,
    passenger_count,
    trip_distance,
    fare_amount,
    tip_amount,
    total_amount;

-- Group trips by pickup hour
group_by_hour = GROUP nyc_taxi_time BY pickup_hour;

-- Calculate hourly averages
hourly_stats = FOREACH group_by_hour GENERATE
    group AS pickup_hour,
    AVG(nyc_taxi_time.trip_distance) AS avg_trip_distance,
    AVG(nyc_taxi_time.fare_amount) AS avg_fare,
    AVG(nyc_taxi_time.total_amount) AS avg_total_amount;

-- Flag trips based on tipping behaviour
tip_flagged = FOREACH nyc_taxi_clean GENERATE
    (tip_amount > 0 ? 'TIPPED' : 'NO_TIP') AS tip_status,
    tip_amount,
    total_amount;

-- Group by tip status
group_tip = GROUP tip_flagged BY tip_status;

-- Calculate tipping statistics
tip_stats = FOREACH group_tip GENERATE
    group AS tip_status,
    COUNT(tip_flagged) AS trip_count,
    AVG(tip_flagged.tip_amount) AS avg_tip_amount;

-- Store results to HDFS
STORE hourly_stats
INTO '/user/maria_dev/clean_datasets/clean_nyc_hourly'
USING PigStorage(',');

STORE tip_stats
INTO '/user/maria_dev/clean_datasets/clean_nyc_tip'
USING PigStorage(',');
