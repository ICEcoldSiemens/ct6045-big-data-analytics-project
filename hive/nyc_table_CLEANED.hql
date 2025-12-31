CREATE TABLE NYC_TAXI_TABLE (
pickup_hour INT, 
avg_trip_distance DOUBLE, 
avg_fare DOUBLE,
avg_total_amount DOUBLE
)

ROW FORMAT DELIMITED
FIELDS TERMINATED BY ',' 
LOCATION '/user/maria_dev/clean_datasets/clean_nyc_hourly/hourly_stats.csv'