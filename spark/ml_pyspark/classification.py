from pyspark.ml.feature import VectorAssembler, StandardScaler
from pyspark.sql import SparkSession
from pyspark.sql.functions import when
from pyspark.ml.classification import LogisticRegression
from pyspark.ml.classification import RandomForestClassifier
from pyspark.ml.evaluation import MulticlassClassificationEvaluator

spark = SparkSession.builder.appName("New York City Yellow Taxi ML").getOrCreate()

# pickup_hour, trip_distance, fare, total_amount
df = spark.read.csv("hourly_stats.csv",header=False,inferSchema=True)
df = df.toDF("pickup_hour","avg_trip_distance","avg_fare","avg_total_amount")

ass = VectorAssembler(
    inputCols=[
        "pickup_hour",
        "avg_trip_distance",
        "avg_fare",
        "avg_total_amount"
    ], outputCol="features"
)

ass_df = ass.transform(df)
scaler = StandardScaler(
    inputCol="features",
    outputCol="scaled_features",
    withMean=True,
    withStd=True
)

scaled_df = scaler.fit(ass_df).transform(ass_df)

labelled_df = scaled_df.withColumn(
    "peak_hour", when((df.pickup_hour >= 7) & (df.pickup_hour <= 9), 1)
    .when((df.pickup_hour >= 16) & (df.pickup_hour <= 19), 1).otherwise(0)
)

train_df, test_df = labelled_df.randomSplit([0.8, 0.2], seed=42)

#Logistic Regression
lr = LogisticRegression(featuresCol = "scaled_features", labelCol="peak_hour")
lr_model = lr.fit(train_df)
lr_predict = lr_model.transform(test_df)

#Random Forest Algorithm
rf = RandomForestClassifier(
    featuresCol="scaled_features",
    labelCol="peak_hour",
    numTrees=50
)
rf_model = rf.fit(train_df)
rf_predict = rf_model.transform(test_df)


# Model Comparison & Evaluation
evaluator = MulticlassClassificationEvaluator(
    labelCol="peak_hour",
    metricName="accuracy"
)
lr_accuracy = evaluator.evaluate(lr_predict)
rf_accuracy = evaluator.evaluate(rf_predict)

print("Logistic Regression: ", lr_accuracy)
print("Random Forest: ", rf_accuracy)