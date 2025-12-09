
import pandas as pd
# The CSV files use '|' as delimiter and contain special characters (e.g., accented names), 
# so we specify the delimiter and an encoding that can handle these characters (latin1).
customers = pd.read_csv('/workspaces/accpython202510/datafiles/customers.csv', delimiter='|', encoding='latin1')
products = pd.read_csv('/workspaces/accpython202510/datafiles/product.csv', delimiter='|', encoding='latin1')
orders = pd.read_csv('/workspaces/accpython202510/datafiles/orderheader.csv', delimiter='|', encoding='latin1')
details = pd.read_csv('/workspaces/accpython202510/datafiles/orderdetails.csv', delimiter='|', encoding='latin1')

# Let's inspect if data loaded correctly (e.g., special characters appear properly):
print(customers.loc[7, 'SalesPerson'])  # Should show 'adventure-works\josé1'

# 1. Missing Data Handling (finding, checking, replacing NaN/NA)
# Pandas represents missing data as NaN (Not a Number) for numeric types, or NaT (Not a Time) for datetime, etc.
# We can find missing values using isnull() or isna(), which returns a boolean mask indicating missing entries:contentReference[oaicite:0]{index=0}.
missing_counts = products.isna().sum()  # Count of missing values in each column of products DataFrame
print("Missing values per column in products:\n", missing_counts)

# We see some columns (e.g., Color, Size, Weight, SellEndDate, DiscontinuedDate) have missing values.
# For example, many products have no recorded Weight or Size (NaN), and dates like SellEndDate are NaN when not applicable.
# We can handle missing data by filling with default values or removing those entries.
# Let's fill missing numeric data (e.g., Weight) with a substitute (like 0 or mean), 
# and fill missing categorical/text data (e.g., Size) with a placeholder.
weight_nulls_before = products['Weight'].isna().sum()
products['Weight'] = products['Weight'].fillna(0.0)  # replace NaN weight with 0.0 (for example)
weight_nulls_after = products['Weight'].isna().sum()
print(f"Weight - missing before: {weight_nulls_before}, after fill: {weight_nulls_after}")

size_nulls_before = products['Size'].isna().sum()
products['Size'] = products['Size'].fillna('Missing')  # placeholder for missing sizes
size_nulls_after = products['Size'].isna().sum()
print(f"Size - missing before: {size_nulls_before}, after fill: {size_nulls_after}")

# We could also drop rows with missing data using dropna(), but that would remove those products entirely.
# (e.g., products.dropna() would drop any product with *any* missing value).
# In many cases, filling or imputing is preferable to dropping data.

# 2. Common Data Types and Conversions (including categorical data)
# Each DataFrame column has a dtype (data type). Let's check some types:
print("Data types of order columns before conversion:\n", orders.dtypes)

# We notice OrderDate, DueDate, ShipDate are object (strings) currently, and CustomerID, etc., are int64.
# The customers DataFrame has 'NameStyle' as 0/1 (int64), which is essentially a boolean flag.
# We can convert numeric types to other types, for example:
orders['OnlineOrderFlag'] = orders['OnlineOrderFlag'].astype(bool)  # convert 0/1 to Boolean True/False
print("OnlineOrderFlag unique values after conversion:", orders['OnlineOrderFlag'].unique())

# Convert a string field to a categorical type to save memory and enforce limited choices.
# For example, 'Color' in products has a limited set of values.
print("Product Color dtype before:", products['Color'].dtype)
products['Color'] = products['Color'].astype('category')  # convert Color to categorical type
print("Product Color dtype after:", products['Color'].dtype)
print("Product Color categories:", products['Color'].cat.categories.tolist())

# Converting to categorical reduces memory usage if there are many repeated values, 
# and it also lets us define a logical order if needed (ordered categories).

# We can also convert numeric data types, e.g., convert a float to int (if we don't need the fractional part).
# (Be cautious: converting float to int will truncate decimals.)
products['ListPrice_int'] = products['ListPrice'].astype(int)
print("ListPrice (original) vs ListPrice_int (converted):", products[['ListPrice', 'ListPrice_int']].head(1).to_dict(orient='records'))

# 3. Common String/Text Data Transformations
# Pandas provides vectorized string operations via the .str accessor:
# # These methods allow us to manipulate text in each cell easily, while automatically skipping missing values.
# Example: create a full name for customers by concatenating first and last name.
customers['FullName'] = customers['FirstName'] + ' ' + customers['LastName']
print("FullName example:", customers['FullName'].head(3).tolist())

# We can search within text using methods like str.contains():
# Find how many customers have "Bike" in their CompanyName (case-insensitive search).
bike_companies = customers['CompanyName'].str.contains('bike', case=False)
print("Number of customers with 'Bike' in company name:", bike_companies.sum())
print("Example companies with 'Bike':", customers.loc[bike_companies, 'CompanyName'].head(3).tolist())

# We can also split text into parts. For example, split the EmailAddress into username and domain.
customers[['EmailUser', 'EmailDomain']] = customers['EmailAddress'].str.split('@', expand=True)
print("Email split example:", customers[['EmailAddress', 'EmailUser', 'EmailDomain']].head(1).to_dict(orient='records'))

# Other useful string transformations include str.lower(), str.upper(), str.strip() (to trim whitespace), 
# str.replace() for simple substitutions, and many more (pandas' str methods mirror Python's string methods).

# 4. Regex (Regular Expressions) for searching and data validation
# Pandas string methods can utilize regular expressions for powerful pattern matching.
# For example, let's validate the format of email addresses and phone numbers using regex patterns.
import re
email_pattern = r'^[A-Za-z0-9._-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}$'  # basic email pattern (alphanumeric + some allowed symbols)
email_valid = customers['EmailAddress'].str.match(email_pattern)
print("Emails matching pattern:", email_valid.sum(), "out of", len(customers))

# If some emails do not match, they might contain characters our pattern didn't account for (e.g., a hyphen in the username or other special chars).
# We can adjust the regex accordingly if needed. For now, let's see an example of an email that failed the validation:
invalid_emails = customers.loc[~email_valid, 'EmailAddress'].head(1).tolist()
print("Example invalid email (pattern mismatch):", invalid_emails)

# Now, validate phone numbers. Suppose we expect phone format ###-###-####.
phone_pattern = r'^\d{3}-\d{3}-\d{4}$'
phone_valid = customers['Phone'].str.match(phone_pattern)
print("Phones matching ###-###-#### pattern:", phone_valid.sum(), "out of", len(customers))
invalid_phones = customers.loc[~phone_valid, 'Phone'].head(1).tolist()
print("Example phone not matching pattern:", invalid_phones)

# Indeed, some phone numbers include country codes or parentheses which our simple pattern did not capture.
# Regex helps identify such inconsistencies for cleaning or further processing.

# Regex can also be used to find and replace text. 
# For instance, remove all non-digit characters from phone numbers to keep only digits:
customers['PhoneDigits'] = customers['Phone'].str.replace(r'\D', '', regex=True)
print("Phone digits extraction:", customers[['Phone', 'PhoneDigits']].head(3).to_dict(orient='records'))

# 5. Dates and Times: datetime objects and common operations
# Our orders data has dates as strings. We typically convert them to datetime objects for easy date operations.
orders['OrderDate'] = pd.to_datetime(orders['OrderDate'])  # convert to datetime
orders['ShipDate'] = pd.to_datetime(orders['ShipDate'])
print("OrderDate dtype after conversion:", orders['OrderDate'].dtype)

# Now we can easily extract parts of the date or perform calculations.
orders['OrderYear'] = orders['OrderDate'].dt.year  # extract year
orders['OrderMonth'] = orders['OrderDate'].dt.month  # extract month
print("Order year and month example:", orders[['OrderDate', 'OrderYear', 'OrderMonth']].head(1).to_dict(orient='records'))

# Calculate the shipping duration in days for each order:
orders['ShipDays'] = (orders['ShipDate'] - orders['OrderDate']).dt.days
print("Shipping days for first order:", orders.loc[0, ['OrderDate', 'ShipDate', 'ShipDays']].to_dict())

# We can also filter or index by dates easily. For example, count how many orders were in 2008:
orders_2008 = orders[orders['OrderDate'].dt.year == 2008]
print("Orders in 2008:", len(orders_2008))

# Dates and times with the Arrow library (an alternative to datetime):
# Arrow provides a more human-friendly API for dates and times. 
# (Make sure to install Arrow first: `pip install arrow`).
import arrow
# Parse a date string using Arrow:
date_str = orders.loc[0, 'DueDate']  # take a sample date string (DueDate) from the orders data
arw = arrow.get(date_str, 'YYYY-MM-DD HH:mm:ss.SSS')
# Arrow can easily shift dates and provide human-readable outputs.
print("Parsed with Arrow:", arw.format('YYYY-MM-DD HH:mm:ss'))
print("One week later (Arrow):", arw.shift(days=7).format('YYYY-MM-DD HH:mm:ss'))
print("Humanized relative time:", arw.humanize())  # e.g., "17 years ago" (relative to now)

# Arrow simplifies timezone handling, shifting, and formatting. For example, arrow.utcnow().shift(hours=-5) 
# would give current time minus 5 hours, and .to('US/Pacific') would convert timezone.