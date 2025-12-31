# CT6045_Big_Data_Analytics_Project
Working on a batch analytics pipeline using Hortonworks HDP 2.6.5. Include loading data into HDFS, creating schemas, using Pig and Hive for transformations, running a MapReduce job, and building PySpark models for clustering, classification, and regression. NLP and sentiment analysis, reduce features using PCA or SVD, and graph analysis applied.

1.2 HDP setup and verification: Install or use HDP 2.6.5 on a virtual machine or lab cluster. Show that services are running and HDFS works by creating directories and listing files. Provide screenshots of commands and outputs.

1.3 Data ingestion, Hive and Pig ETL <br></br>
Pick datasets from below:
- One for NLP/Sentiment Analysis: Sentiment140, IMDB reviews, Amazon reviews
- And one from numerical dataset for other tasks: NYC taxi data, airline delays, or UK accidents.
Note: You can download these from Kaggle.com. Use a part of the dataset, with size easily manageable. The size should be large enough to meet the requirements of the tasks.

Sentiment140: https://www.kaggle.com/datasets/kazanova/sentiment140 <br></br>
IMDB reviews: https://www.kaggle.com/datasets/lakshmi25npathi/imdb-dataset-of-50k-movie-reviews <br></br>
Amazon reviews: https://www.kaggle.com/datasets/kritanjalijain/amazon-reviews <br></br>
NYC taxi data: https://www.kaggle.com/datasets/elemento/nyc-yellow-taxi-trip-data <br></br>
Airlines delays: https://www.kaggle.com/datasets/giovamata/airlinedelaycauses <br></br>
UK accidents: https://www.kaggle.com/datasets/silicon99/dft-accident-data <br></br>

 

Upload it to HDFS. Run at least two Hive queries and two Pig scripts on the dataset using different set of commands and analyse its results. Provide scripts, Hive queries, screenshots, and outputs.
Note: Stick to the datasets of your choice for all the following tasks.

1.4 Custom MapReduce job: Write one MapReduce job such as inverted index, top-k terms per category, or a join between two datasets. You may code in Java, use Hadoop streaming with Python, or write a PySpark RDD job that mimics MapReduce logic. Provide code, run commands, and sample outputs.

1.5 NLP and Sentiment Analysis: Use text-based data and apply NLP steps like tokenization, stopword removal, and TF-IDF. Create visuals such as a word cloud or frequency bars. Train at least two classifiers, such as Logistic Regression and Naive Bayes, compare their performance, and discuss misclassified examples. (Need not be on HDP sandbox)

1.6 Dimensionality Reduction: Apply feature selection methods, followed by a dimensionality reduction method (only 1, that suits your dataset e.g., PCA or t-SNE or UMAP). Report difference in accuracy, space and time-complexity. (Need not be on HDP sandbox) <br></br>

1.7 Machine Learning in PySpark: Clustering, Classification, Regression <br></br>
Clustering: use KMeans with different values of k, report silhouette scores, and explain clusters <br></br>
Classification: pick a target other than sentiment, try two algorithms, and compare results <br></br>
Regression: predict a numeric target such as rating, price, or trip duration using Linear Regression and Gradient Boosted Trees. Report metrics like RMSE or MAE, use train/validation split, and discuss feature importance. <br></br>

1.8 Graph generation and social network analysis: Build a small graph such as user-to-item, user-to-hashtag, or airport routes. Compute degree distribution and identify the most central nodes using degree or PageRank. Use GraphFrames in Spark or export to NetworkX and explain your choice.

1.9 Report, reproducibility and reflection: Write a report including objectives, design, results, limitations, and future work. Add a README with exact run commands, file paths, and settings to make work reproducible. Include a short section mapping your work to the four learning outcomes. <br></br>

---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# REPRODUCING BIG DATA ANALYTICS PIPELINE 
# Structure 
data -> contains raw (data/raw) and clean (data/clean) datasets (csv.format) <br><br>
amazon_mapreduce -> java files with Linux execution command for custom MapReduce job to commit polarity count for clean pig Amazon data <br><br>
hive -> commands to configure relevant tables <br><br>
pig -> pig scripts for batch analysis on raw datasets <br><br>
spark -> contains NLP, sentiment analysis and ML based codes <br><br>
screenshots -> screenshots of implemented work <br><br>

# System Requirements
Software included -
- Hortonworks Data Platform (HDP) 2.6.5
- Apache Hadoop (HDFS, YARN, MapReduce), Hive, Pig, Spark
- GraphFrames
- Python (pyspark, pandas, numpy, scikit-learn, nltk, matplotlib, networkx, wordcloud)
- Java (Apache Hadoop libraries)

# Raw Data Required, Data Ingestion into HDP & Hive/Pig
Datasets used: <br><br> 
Amazon reviews: https://www.kaggle.com/datasets/kritanjalijain/amazon-reviews <br></br>
NYC taxi data: https://www.kaggle.com/datasets/elemento/nyc-yellow-taxi-trip-data <br></br>

Run HDP 2.6.5 sandbox and use Ambari to run all services
Useful commands: 
- "hdfs dfs -ls" (will verify HDFS status)
- "hdfs dfs -mkdir -p /user/maria_dev/raw_datasets" and "hdfs dfs -mkdir -p /user/maria_dev/clean_datasets"  (create raw and clean directories for data)
- "hdfs dfs -put data/raw/amazon_review/test.csv /user/maria_dev/raw_datasets/raw_amazon_datasets" and "hdfs dfs -put data/raw/nyc_taxi /user/maria_dev/raw_datasets/raw_nyc_taxi_datasets"  (move unclean datasets from local system into HDFS located directories)
(remember to extract nyc taxi csvs prior to Hive and Pig)


Run Hive, navigate to 'hive' folder and create tables
- "hive -f amazon_table_RAW.hql" and "hive -f nyc_taxi_table_CLEANED.hql" (the former will hold raw amazon review data, the latter will hold clean NYC hourly stats from Pig output)
To verify, run nyc_taxi_table_validation.hql or amazon_review_table_validation.hql (this should output the first five records) 

Run Pig for ETL 
Run the following commands: pig pig/amazon_reviews.pig and pig pig/nyc_taxi.pig where output is stored on "/user/maria_dev/clean_datasets/clean_amazon_dataset" and "/user/maria_dev/clean_datasets/clean_nyc_hourly"

# Custom MapReduce Job, NLP and Sentiment Analysis
Run the custom MapReduce job using screenshot of command located in amazon_mapreduce file with Java code.
To verify, run "hdfs dfs -cat /user/maria_dev/output/polarity_counts/output/part-*" 

Run all NLP/Sentiment Analysis code which includes tokenisation, stopword removal, TF-IDF implementation, LR-NB comparison and PCA 

# PySpark Machine Learning & Graph Generation 
Run all code -> provides clustering, classification, graph configuration (nodes and edges) and analysis with all. 




# DOCUMENTATION 
Documentation: <br></br>
Final Grade: 
