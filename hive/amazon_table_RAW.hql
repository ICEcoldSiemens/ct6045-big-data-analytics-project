CREATE TABLE AMAZON_REVIEW_TABLE (
polarity STRING, 
review_title STRING, 
review_body STRING
)

ROW FORMAT DELIMITED
FIELDS TERMINATED BY ',' 
LOCATION '/user/maria_dev/raw_datasets/raw_amazon_datasets/test.csv'