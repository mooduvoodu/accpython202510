"""


1. Creating Series objects from test data
2. Building a DataFrame from those Series
3. Exploring and changing the index in Series/DataFrames
4. Subsetting with .loc
5. Broadcasting (vectorized operations)
6. Adding/modifying columns (direct assignment, .assign, .apply)
7. Dropping columns and rows

The script also loads the provided customers.csv file (pipe-delimited) and uses it
for real-world examples.  Run each section interactively (e.g., Jupyter) or all
at once—print statements are included so students can see results.
"""

import pandas as pd

# ---------------------------------------------------------------------
# 1. Create Series objects from test data
# ---------------------------------------------------------------------

# Series from a list (default integer index 0…n-1)
fruits = pd.Series(["Apple", "Banana", "Cherry", "Date"])
print("Series: fruits\n", fruits, "\n")



# Series from a list *with a custom index* (fruit names)
quantities = pd.Series([5, 3, 8, 6],
                       index=["Apple", "Banana", "Cherry", "Date"])
print("Series: quantities\n", quantities, "\n")

# Series from a dictionary (keys become index labels)
prices = pd.Series({"Apple": 0.99, "Banana": 0.50, "Cherry": 2.50})
print("Series: prices\n", prices, "\n")

# ---------------------------------------------------------------------
# 2. Create a DataFrame from those Series
# ---------------------------------------------------------------------

fruit_df = pd.DataFrame({
    "Quantity": quantities,
    "Price": prices
})
print("DataFrame built from Series:\n", fruit_df, "\n")

# ---------------------------------------------------------------------
# 3. Load the customers.csv file (pipe '|' delimited)
# ---------------------------------------------------------------------

# NOTE: Update the path if the file lives elsewhere.
df = pd.read_csv("/workspaces/accpython202507/exampledata/customers.csv", sep="|", na_values=["NULL"], encoding='ISO-8859-1')
print("First 5 rows of customers dataset:\n", df.head(), "\n")
print("Columns:\n", df.columns.tolist(), "\n")

# Set a meaningful index (CustomerID)—makes label lookups intuitive.
df.set_index("CustomerID", inplace=True)
print("DataFrame with CustomerID as index:\n", df.head(3), "\n")

# ---------------------------------------------------------------------
# 4. Subsetting with .loc
# ---------------------------------------------------------------------

# Single row by label
row_1 = df.loc[1]
print("CustomerID 1 (row_1):\n", row_1, "\n")

# Multiple rows by label list
rows_1_5_10 = df.loc[[1, 5, 10], ["FirstName", "LastName", "EmailAddress"]]
print("Selected rows/columns (1,5,10):\n", rows_1_5_10, "\n")

# Label-based slice (inclusive of end label)
slice_1_to_3 = df.loc[1:3, ["FirstName", "LastName"]]
print("Slice CustomerID 1–3:\n", slice_1_to_3, "\n")

# Conditional selection (all customers whose Title == "Ms.")
female_customers = df.loc[df["Title"] == "Ms.", ["FirstName", "LastName", "Title"]]
print("Customers with Title 'Ms.':\n", female_customers.head(), "\n")

# ---------------------------------------------------------------------
# 5. Broadcasting / vectorized operations
# ---------------------------------------------------------------------

# Reset index temporarily to get CustomerID as a normal column for demo
df_reset = df.reset_index()

# Add 10 to every CustomerID (scalar broadcast over Series)
print("CustomerID + 10:\n", (df_reset["CustomerID"] + 10).head(), "\n")

# Multiply an entire numeric column by 2 (NameStyle is 0/1)
df_reset["NameStyle"] = df_reset["NameStyle"] * 2
print("Unique NameStyle values after *2:\n", df_reset["NameStyle"].unique(), "\n")

# Element-wise operation between two Series (length of first + last names)
name_lengths = df_reset["FirstName"].str.len() + df_reset["LastName"].str.len()
print("Name length (First+Last):\n", name_lengths.head(), "\n")

# ---------------------------------------------------------------------
# 6. Adding & modifying columns
# ---------------------------------------------------------------------

# Direct assignment – concat first & last into FullName
df_reset["FullName"] = df_reset["FirstName"] + " " + df_reset["LastName"]
# Constant column
df_reset["Verified"] = True
print("FullName + Verified columns added:\n",
      df_reset[["FirstName", "LastName", "FullName", "Verified"]].head(), "\n")

# .assign – returns a new DF (re-assign or chain)
df_reset = df_reset.assign(
    NameLength=df_reset["FullName"].str.len(),
    EmailDomain=df_reset["EmailAddress"].apply(
        lambda x: x.split("@")[1] if pd.notnull(x) else "")
)
print("After .assign:\n",
      df_reset[["FullName", "NameLength", "EmailDomain"]].head(), "\n")

# .apply on a Series – uppercase the FullName
df_reset["FullName"] = df_reset["FullName"].apply(
    lambda name: name.upper() if isinstance(name, str) else name)
print("FullName upper-cased:\n", df_reset["FullName"].head(), "\n")


# .apply row-wise (axis=1) – "LastName, FirstName"
df_reset = df_reset.assign(
    LastName_First=df_reset.apply(
        lambda row: f"{row['LastName']}, {row['FirstName']}", axis=1)
)
print("Row-wise apply (LastName_First):\n",
      df_reset[["FirstName", "LastName", "LastName_First"]].head(), "\n")

# ---------------------------------------------------------------------
# 7. Dropping columns and rows
# ---------------------------------------------------------------------

# Drop a single column
df_reset = df_reset.drop("NameStyle", axis=1)

# Drop multiple columns
df_reset = df_reset.drop(columns=["Title", "Suffix"])

print("Columns after drops:\n", df_reset.columns.tolist(), "\n")

# Drop rows by label (CustomerID 2 & 3)
df_reset = df_reset.drop(index=[2, 3], errors="ignore")

# Drop rows by condition (LastName == 'Garza')
df_reset = df_reset.drop(index=df_reset[df_reset["LastName"] == "Garza"].index)

# Drop rows with missing EmailAddress
before = df_reset.shape[0]
df_reset = df_reset.dropna(subset=["EmailAddress"])
after = df_reset.shape[0]
print(f"Rows dropped for missing EmailAddress: {before - after}\n")

# Filter (keep) rows instead of drop – customers whose CompanyName contains "Bike"
bike_df = df_reset[df_reset["CompanyName"].str.contains("Bike", na=False)]
print("Filtered rows (CompanyName contains 'Bike'):\n", bike_df.head(), "\n")
