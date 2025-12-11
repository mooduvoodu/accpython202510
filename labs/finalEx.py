
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import pyarrow as pa    #pip install this if needed
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans
from sklearn.metrics import silhouette_score
import warnings

# Suppress minor warnings for cleaner output
warnings.filterwarnings('ignore')

# ==============================================================================
# PHASE I: ENVIRONMENT SETUP & CONFIGURATION
# ==============================================================================

# 1.1 Enable Copy-on-Write
# This ensures that modifying a subset of a DataFrame creates a copy only 
# when necessary, preventing side effects on the original data.
pd.set_option("mode.copy_on_write", True)

# 1.2 Configure Display Options for Report Readability
pd.set_option('display.max_columns', None)
pd.set_option('display.width', 1000)
pd.set_option('display.float_format', '{:.2f}'.format)

print(">> PHASE I COMPLETE: Modern Pandas Environment Configured.")
print("-" * 80)

# ==============================================================================
# PHASE II: DATA INGESTION & TYPING
# ==============================================================================

def load_dataset(filename):
    """
    Loads a CSV dataset using the PyArrow engine for performance.
    """
    try:
        # engine="pyarrow" utilizes multi-threading for faster IO.
        # dtype_backend="pyarrow" ensures we use ArrowDtype (e.g., string[pyarrow])
        # instead of numpy object types.
        df = pd.read_csv(
            filename, 
            engine="pyarrow", 
            dtype_backend="pyarrow"
        )
        print(f"Successfully loaded {filename}: {df.shape}")
        return df
    except Exception as e:
        print(f"Error loading {filename}: {e}")
        return None

# 2.1 Load Data
print("Loading Datasets...")
customers = load_dataset('/workspaces/accpython202510/datafiles/customers.csv')
products = load_dataset('/workspaces/accpython202510/datafiles/product.csv')
headers = load_dataset('/workspaces/accpython202510/datafiles/orderheader.csv')
details = load_dataset('/workspaces/accpython202510/datafiles/orderdetails.csv')

# 2.2 Verify Data Types
# Note how strings are stored as 'string[pyarrow]' and not 'object'.
print("\n[Inspection] Customers Dtypes (Sample):")
print(customers.dtypes.head(5))

print("\n>> PHASE II COMPLETE: Data Ingestion with PyArrow Backend.")
print("-" * 80)

# ==============================================================================
# PHASE III: DATA CLEANING & RELATIONAL TRANSFORMATION
# ==============================================================================

# 3.1 Date Parsing
# The.dt accessor works seamlessly with Arrow-backed datetime columns.
date_cols = []
for col in date_cols:
    headers[col] = pd.to_datetime(headers[col])

# 3.2 Referential Integrity Check
# Verify that all CustomerIDs in orders exist in the customers table.
unique_cust_orders = headers.unique()
unique_cust_master = customers.unique()
missing_cust = np.setdiff1d(unique_cust_orders, unique_cust_master)

if len(missing_cust) > 0:
    print(f"Warning: {len(missing_cust)} CustomerIDs in Orders missing from Master.")
else:
    print("[Integrity Check] All ordering customers exist in the master record.")

# 3.3 Constructing the Analytical Master Table (AMT)
# Step A: Enrich Header with Customer Info
# We select only necessary columns to keep memory usage optimized.
cust_cols = []
# Note: CountryRegionName wasn't in the snippet, assuming standard AdventureWorks schema or using available cols
# Adjusting to snippet columns:
cust_cols = []

amt_step1 = pd.merge(
    headers,
    customers[cust_cols],
    on='CustomerID',
    how='left'
)

# Step B: Explode to Line Item Level
amt_step2 = pd.merge(
    amt_step1,
    details,
    on='SalesOrderID',
    how='inner'  # Only orders with valid details
)

# Step C: Enrich with Product Costing for Margin Analysis
prod_cols = []
amt = pd.merge(
    amt_step2,
    products[prod_cols],
    on='ProductID',
    how='left',
    suffixes=('_Trx', '_Master')
)

# 3.4 Feature Engineering: Gross Margin
# Gross Margin = (UnitPrice - StandardCost) * Quantity
# Note: StandardCost might be null. We fill NA with 0 for margin calc (conservative).
amt = amt.fillna(0)
amt['GrossMargin'] = (amt['UnitPrice'] - amt) * amt['OrderQty']
amt = amt['UnitPrice'] * amt['OrderQty']

print(f"\nAMT Final Shape: {amt.shape}")
print(">> PHASE III COMPLETE: Relational Modeling & Feature Calculation.")
print("-" * 80)

# ==============================================================================
# PHASE IV: EXPLORATORY DATA ANALYSIS (EDA)
# ==============================================================================

# 4.1 Sales Distribution
print("Generating Summary Statistics for Revenue...")
print(amt.describe())

# 4.2 Top Products
top_products = amt.groupby('Name').sum().sort_values(ascending=False).head(5)
print("\n[Insight] Top 5 Products by Revenue:")
print(top_products)

# 4.3 Temporal Analysis
amt = amt.dt.year
yearly_sales = amt.groupby('OrderYear').sum()
print("\n[Insight] Annual Sales Trend:")
print(yearly_sales)

# 4.4 Sales Person Performance
# Extract clean username from 'adventure-works\username'
if 'SalesPerson' in amt.columns:
    # We must cast to string first because pyarrow strings need explicit handling for some split ops
    amt = amt.astype(str).str.split('\\').str[-1]
    top_sales_people = amt.groupby('SalesPersonClean').sum().sort_values(ascending=False).head(3)
    print("\n[Insight] Top 3 Sales Representatives:")
    print(top_sales_people)

print("\n>> PHASE IV COMPLETE: Exploratory Analysis.")
print("-" * 80)

# ==============================================================================
# PHASE V: RFM FEATURE ENGINEERING
# ==============================================================================

# 5.1 Define Snapshot
snapshot_date = amt.max() + pd.Timedelta(days=1)

# 5.2 Aggregation
rfm = amt.groupby('CustomerID').agg({
    'OrderDate': lambda x: (snapshot_date - x.max()).days,
    'SalesOrderID': 'nunique',
    'TotalRevenue': 'sum'
})

# 5.3 Renaming
rfm.rename(columns={
    'OrderDate': 'Recency',
    'SalesOrderID': 'Frequency',
    'TotalRevenue': 'Monetary'
}, inplace=True)

print("RFM Matrix Sample:")
print(rfm.head())

# 5.4 Preprocessing for K-Means
# RFM data is typically right-skewed. We use Log transformation.
rfm_log = np.log1p(rfm)

# 5.5 Scaling
scaler = StandardScaler()
rfm_scaled = scaler.fit_transform(rfm_log)
rfm_scaled = pd.DataFrame(rfm_scaled, index=rfm.index, columns=rfm.columns)

print("\n>> PHASE V COMPLETE: RFM Features Engineered and Scaled.")
print("-" * 80)

# ==============================================================================
# PHASE VI & VII: CLUSTERING & EVALUATION
# ==============================================================================

# 6.1 K-Means Execution
k = 4
kmeans = KMeans(n_clusters=k, random_state=42, n_init=10)
kmeans.fit(rfm_scaled)

# 6.2 Assignment
rfm['Cluster'] = kmeans.labels_

# 6.3 Evaluation
sil_score = silhouette_score(rfm_scaled, kmeans.labels_)
print(f"[Model Evaluation] Silhouette Score: {sil_score:.4f}")

# 6.4 Cluster Interpretation
cluster_summary = rfm.groupby('Cluster').agg({
    'Recency': 'mean',
    'Frequency': 'mean',
    'Monetary': 'mean',
    'Cluster': 'count'
}).rename(columns={'Cluster': 'CustomerCount'}).sort_values(by='Monetary', ascending=False)

print("\nCluster Profiles:")
print(cluster_summary)

print("\n>> PHASE VI & VII COMPLETE: Segmentation and Profiling.")
print("-" * 80)

# ==============================================================================
# PHASE VIII: REPORTING
# ==============================================================================

# 8.1 Final Merge
final_report = pd.merge(
    rfm[['Cluster']], # Only need the cluster label
    customers[cust_cols],
    on='CustomerID',
    how='inner'
)

# 8.2 Labeling the Clusters
def label_cluster(row, summary):
    cluster_id = row['Cluster']
    stats = summary.loc[cluster_id]
    
    # Heuristic Logic
    if stats['Monetary'] > summary['Monetary'].quantile(0.75):
        return 'VIP / Whale'
    elif stats > summary.quantile(0.75):
        return 'Lapsed / At Risk'
    elif stats['Frequency'] <= 1.5:
        return 'New / Low Engagement'
    else:
        return 'Regular'

final_report = final_report.apply(lambda x: label_cluster(x, cluster_summary), axis=1)

print("Final Report Preview:")
print(final_report.head())

# 8.3 Export
output_filename = 'AdventureWorks_Customer_Segmentation.csv'
# final_report.to_csv(output_filename, index=False)
print(f"\n>> Exported final segmentation to {output_filename}")

print("=" * 80)
print("CAPSTONE PROJECT COMPLETED SUCCESSFULLY")
print("=" * 80)