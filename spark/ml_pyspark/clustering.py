from pyspark.ml.evaluation import ClusteringEvaluator
from pyspark.sql import SparkSession
from pyspark.ml.feature import VectorAssembler, VectorSlicer, StandardScaler
from pyspark.ml.clustering import KMeans

spark = SparkSession.builder.appName("New York City Yellow Taxi ML").getOrCreate()

# pickup_hour, trip_distance, fare, total_amount
df = spark.read.csv("hourly_stats.csv", header=False,inferSchema=True)
df = df.toDF("pickup_hour","avg_trip_distance","avg_fare","avg_total_amount")
df.show(20)

# Feature Vector creation - defining attributes as features
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
    withMean=False,
    withStd=True
)

scaled_df = scaler.fit(ass_df).transform(ass_df)

kmeans = KMeans(
    featuresCol="scaled_features",
    k = 3,
    seed=42
)

kmeans_model = kmeans.fit(scaled_df)
kmeans_predict = kmeans_model.transform(scaled_df)
kmeans_predict.select("pickup_hour", "prediction").show(10)


evaluator = ClusteringEvaluator(
    featuresCol="scaled_features",
    metricName="silhouette",
    distanceMeasure="squaredEuclidean"
)

silhouette = evaluator.evaluate(kmeans_predict)
print("Silhouette Score:", silhouette)


for k in [2, 3, 4, 5]:
    kmeans = KMeans(featuresCol="scaled_features", k=k, seed=42)
    model = kmeans.fit(scaled_df)
    preds = model.transform(scaled_df)
    score = evaluator.evaluate(preds)
    print(f"k={k}, silhouette={score}")

