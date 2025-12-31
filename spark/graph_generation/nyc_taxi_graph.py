import os

import networkx as nx
from matplotlib import pyplot as plt
from pyspark.sql import SparkSession
from pyspark.sql.functions import col
from graphframes import GraphFrame

HADOOP_HOME = "C:\\hadoop"  # folder where winutils.exe is located
os.environ["HADOOP_HOME"] = HADOOP_HOME
os.environ["PATH"] += os.pathsep + os.path.join(HADOOP_HOME, "bin")

spark = (SparkSession.builder.appName("New York City Yellow TaxI Graph Network")
         .config("spark.jars.packages",
                 "graphframes:graphframes:0.8.3-spark3.5-s_2.12").getOrCreate())

df = spark.read.csv("hourly_stats.csv",header=False,inferSchema=True)
df = df.toDF("pickup_hour","avg_trip_distance","avg_fare","avg_total_amount")

nodes = df.selectExpr("CAST(pickup_hour AS STRING) AS id").distinct()

edges = df.select(
    col("pickup_hour").cast("string").alias("src"), (col("pickup_hour") + 1).cast("string").alias("dst"),
    col("avg_total_amount").alias("weight")
)


graph = GraphFrame(nodes, edges)
print("Nodes: ", graph.vertices.count())
print("Edges: ", graph.edges.count())

degree_df = graph.degrees.orderBy("degree", ascending=False)
degree_df.show()

pagerank = graph.pageRank(resetProbability=0.15, maxIter=10)
pagerank.vertices.orderBy("pagerank", ascending=False).show()

edges_pd = graph.edges.select("src", "dst", "weight").toPandas()
G = nx.from_pandas_edgelist(
    edges_pd,
    source="src",
    target="dst",
    edge_attr="weight",
    create_using=nx.DiGraph()
)

plt.figure(figsize=(10, 8))
pos = nx.spring_layout(G, seed=42)

nx.draw(
    G, pos,
    with_labels=True,
    node_size=600,
    font_size=10
)

plt.title("Temporal Graph of NYC Taxi Pickup Hours")
plt.show()

pagerank = pagerank.vertices.select("id", "pagerank").toPandas()
pr_dict = dict(zip(pagerank["id"], pagerank["pagerank"]))

node_sizes = [pr_dict[n] * 3000 for n in G.nodes()]

nx.draw(
    G, pos,
    with_labels=True,
    node_size=node_sizes
)



