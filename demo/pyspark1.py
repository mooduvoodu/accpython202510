
#Needed for this code to work. from shell run:   sudo apt-get update && sudo apt-get install -y openjdk-17-jdk
# then run: pip install --upgrade pyspark


# 1. Initialize SparkSession in local mode (no cluster needed)
from pyspark.sql import SparkSession
spark = SparkSession.builder.master("local[*]").appName("PySparkDemo").getOrCreate()

# 2. Read the CSV file into a DataFrame with header and schema inference
csv_file = "/workspaces/ADPPython/datafiles/orderdetails.csv"  # Path in GitHub Codespace environment
df = spark.read.option("header", True) \
               .option("inferSchema", True) \
               .option("sep", "|") \
               .csv(csv_file)

# 3. Display the DataFrame schema to see column names and data types inferred by Spark
df.printSchema()
# Expected schema output:
# root
#  |-- SalesOrderID: integer (nullable = true)
#  |-- SalesOrderDetailID: integer (nullable = true)
#  |-- OrderQty: integer (nullable = true)
#  |-- ProductID: integer (nullable = true)
#  |-- UnitPrice: double (nullable = true)
#  |-- UnitPriceDiscount: double (nullable = true)
#  |-- LineTotal: double (nullable = true)
#  |-- rowguid: string (nullable = true)
#
# Note: inferSchema=True causes Spark to automatically infer column types (int, double, string, etc.)
# instead of reading all columns as strings. Without inferSchema, all columns would default to string types.

# 4. Show a few sample rows of the DataFrame
df.show(5)
# Expected output (first 5 rows):
# +-----------+-----------------+--------+---------+---------+----------------+----------+--------------------+
# |SalesOrderID|SalesOrderDetailID|OrderQty|ProductID|UnitPrice|UnitPriceDiscount|LineTotal|             rowguid|
# +-----------+-----------------+--------+---------+---------+----------------+----------+--------------------+
# |      71774|           110562|       1|      836|  356.898|             0.0| 356.89800|E3A1994C-7A68-4CE...|
# |      71774|           110563|       1|      822|  356.898|             0.0| 356.89800|5C77F557-FDB6-43B...|
# |      71776|           110567|       1|      907|   63.900|             0.0|  63.90000|6DBFE398-D15D-425...|
# |      71780|           110616|       4|      905|  218.454|             0.0| 873.81600|377246C9-4483-48E...|
# |      71780|           110617|       2|      983|  461.694|             0.0| 923.38800|43A54BCD-536D-4A1...|
# +-----------+-----------------+--------+---------+---------+----------------+----------+--------------------+
# only showing top 5 rows

# Create a temporary view to use Spark SQL queries on this DataFrame
df.createOrReplaceTempView("order_details")
# Now we can query "order_details" using SQL syntax via spark.sql()

# 5. Filtering examples (equality, range, pattern matching)
# DataFrame API: filter rows where OrderQty equals 2
df.filter(df.OrderQty == 2).show(5)
# Spark SQL equivalent:
spark.sql("SELECT * FROM order_details WHERE OrderQty = 2 LIMIT 5").show()

# DataFrame API: filter rows where UnitPrice is between 100 and 200 (inclusive range)
from pyspark.sql.functions import col
df.filter((col("UnitPrice") >= 100) & (col("UnitPrice") <= 200)).show(5)
# Spark SQL equivalent using BETWEEN:
spark.sql("SELECT * FROM order_details WHERE UnitPrice BETWEEN 100 AND 200 LIMIT 5").show()

# DataFrame API: filter rows where the string in 'rowguid' starts with '5' (pattern match)
df.filter(col("rowguid").like("5%")).show(5)
# Spark SQL equivalent using LIKE:
spark.sql("SELECT * FROM order_details WHERE rowguid LIKE '5%' LIMIT 5").show()
#
# Note: The .like() method and SQL LIKE allow wildcard pattern matching ( '%' is wildcard for any sequence of characters).
# In this example, we filter for rowguid values beginning with "5".

# 6. Selecting specific columns and aliasing
# DataFrame API: select two columns and rename/alias them
df.select(
    col("SalesOrderID").alias("OrderID"),
    col("LineTotal").alias("TotalPrice")
).show(5)
# Spark SQL equivalent with AS aliases:
spark.sql("SELECT SalesOrderID AS OrderID, LineTotal AS TotalPrice FROM order_details LIMIT 5").show()
#
# Note: Alias changes the column name in the result. This does not rename the column in the DataFrame permanently,
# it only labels the output. To permanently rename, use df.withColumnRenamed() or create a new DataFrame with alias.

# 7. Handling null or missing values
# (The main dataset may not contain nulls, so we'll create a small example DataFrame to demonstrate.)
missing_data = spark.createDataFrame(
    [(1, "Alpha"), (2, None), (3, "Charlie")],
    ["id", "name"]
)
missing_data.createOrReplaceTempView("missing_data")  # create a view for SQL examples
missing_data.show()
# Output:
# +---+-------+
# | id|   name|
# +---+-------+
# |  1|  Alpha|
# |  2|   null|
# |  3|Charlie|
# +---+-------+
# Notice: The second row has a null in the "name" column.

# DataFrame API: Drop rows with any null values
missing_data.dropna().show()
# Output after dropna (row with id=2 is removed because name was null):
# +---+-------+
# | id|   name|
# +---+-------+
# |  1|  Alpha|
# |  3|Charlie|
# +---+-------+

# Spark SQL equivalent: filter out nulls using IS NOT NULL
spark.sql("SELECT * FROM missing_data WHERE name IS NOT NULL").show()
# This yields the same result as dropna(), removing rows where name is null.

# DataFrame API: Fill null values with a default.
missing_data.fillna("Unknown", subset=["name"]).show()
# Output after fillna (null names replaced by "Unknown"):
# +---+-------+
# | id|   name|
# +---+-------+
# |  1|  Alpha|
# |  2|Unknown|
# |  3|Charlie|
# +---+-------+

# Spark SQL equivalent: use COALESCE to replace null with "Unknown"
spark.sql("SELECT id, COALESCE(name, 'Unknown') AS name FROM missing_data").show()
# COALESCE returns the first non-null value (here it substitutes 'Unknown' when name is null).

# 8. Replacing specific values in data
# DataFrame API: Replace a specific value with another in a column.
missing_data.replace("Alpha", "First", subset=["name"]).show()
# Output: "Alpha" in the name column is now replaced with "First":
# +---+-------+
# | id|   name|
# +---+-------+
# |  1|  First|
# |  2|   null|
# |  3|Charlie|
# +---+-------+

# Spark SQL equivalent: use a CASE expression for conditional replacement
spark.sql("""
    SELECT 
        id,
        CASE 
            WHEN name = 'Alpha' THEN 'First'
            ELSE name 
        END AS name
    FROM missing_data
""").show()
# This achieves the same result of replacing "Alpha" with "First".

# 9. GroupBy aggregations
# DataFrame API: Group by a column and aggregate with multiple functions (count, sum, average, etc.)
from pyspark.sql.functions import count, sum, avg
product_stats_df = df.groupBy("ProductID").agg(
    count("*").alias("Count"),            # number of rows for each product
    sum("OrderQty").alias("TotalQuantity"),  # total quantity ordered for each product
    avg("LineTotal").alias("AvgLineTotal")   # average line total for each product
)
product_stats_df.orderBy("ProductID").show(5)
# The above shows statistics for the first 5 ProductIDs. For example:
# +---------+-----+-------------+------------------+
# |ProductID|Count|TotalQuantity|       AvgLineTotal|
# +---------+-----+-------------+------------------+
# |      707|    3|            5|          714.09667|
# |      708|    1|            1|          178.46400|
# |      709|    1|            1|           93.98400|
# |      710|    1|            1|          187.96800|
# |      711|    1|            1|          281.95200|
# +---------+-----+-------------+------------------+
# (Numbers above are just examples; actual values depend on the data.)

# Spark SQL equivalent: GROUP BY query with aggregations and aliases
spark.sql("""
    SELECT 
        ProductID,
        COUNT(*) AS Count,
        SUM(OrderQty) AS TotalQuantity,
        AVG(LineTotal) AS AvgLineTotal
    FROM order_details
    GROUP BY ProductID
    ORDER BY ProductID
    LIMIT 5
""").show()
# This yields the same result as the DataFrame API above for the first 5 product IDs.

# 10. Reading multiple Parquet files as one DataFrame
# (Demonstration of writing the DataFrame to Parquet and reading it back)
df.repartition(2).write.mode("overwrite").parquet("orderdetails_parquet")
# The DataFrame is saved as Parquet in a folder "orderdetails_parquet" with multiple part files.
# Now read all Parquet files in that folder into a single DataFrame:
df_parquet = spark.read.parquet("orderdetails_parquet")
print("Total records in combined DataFrame:", df_parquet.count())
df_parquet.show(2)
# The count should match the original DataFrame (e.g., 542 records), and show() will display rows just like the original.
# Spark can read a directory of Parquet files (or use wildcards) and automatically combine them into one DataFrame.

# 11. Stop the SparkSession (optional in interactive environments, but good practice to release resources)
spark.stop()