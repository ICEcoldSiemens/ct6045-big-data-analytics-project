-- Loads test.csv - a partial Amazon review dataset
raw_amazon = LOAD '/user/maria_dev/raw_datasets/raw_amazon_datasets/test.csv'
USING PigStorage(',')
AS (
   polarity: chararray,
   review_title: chararray,
   review_body: chararray
);

-- Concatenate review title and body for readability 
amazon_text = FOREACH raw_amazon GENERATE
    polarity,
    CONCAT(
        (review_title IS NOT NULL ? review_title : ' '),
        ' ',
        (review_body IS NOT NULL ? review_body : ' ')
    ) AS full_review;

-- Remove empty reviews
clean_amazon = FOREACH amazon_text 
GENERATE 
   polarity,
   REPLACE(full_review, '"', '') AS full_review;

-- Distribution of reviews by polarity
grouped = GROUP clean_amazon BY polarity;
counts = FOREACH grouped GENERATE
    group AS polarity,
    COUNT(clean_amazon) AS review_count;

DUMP counts;

-- Store cleaned dataset
STORE clean_amazon INTO '/user/maria_dev/clean_datasets/clean_amazon_dataset'
USING PigStorage(',');
