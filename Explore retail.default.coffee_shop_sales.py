# Databricks notebook source
# MAGIC %md
# MAGIC Task 01 Load & Inspect the Dataset

# COMMAND ----------

import pandas as pd

shop_sales = spark.read.table("retail.default.coffee_shop_sales").toPandas()

# Fix decimal comma if unit_price is still text
if shop_sales['unit_price'].dtype == 'object':
    shop_sales['unit_price'] = shop_sales['unit_price'].astype(str).str.replace(',', '.').astype(float)

# COMMAND ----------

# MAGIC %md
# MAGIC 2. Print the shape, all column names, and data types.

# COMMAND ----------

print("Shape:", shop_sales.shape)


# COMMAND ----------

print("Columns:", shop_sales.columns.tolist())

# COMMAND ----------

shop_sales.isnull().sum()

# COMMAND ----------

shop_sales.describe()

# COMMAND ----------

shop_sales.describe(include='object')

# COMMAND ----------

shop_sales["product_category"].value_counts()

# COMMAND ----------

shop_sales["store_location"].value_counts()

# COMMAND ----------

# MAGIC %md
# MAGIC Task 02 Feature Engineering & Distributions

# COMMAND ----------

 shop_sales["revenue"] =  shop_sales["unit_price"] *  shop_sales["transaction_qty"]

# COMMAND ----------

 shop_sales.head()

# COMMAND ----------

shop_sales['hour'] = pd.to_datetime(shop_sales['transaction_time'], format='%H:%M:%S').dt.hour

# COMMAND ----------

# MAGIC %md
# MAGIC Task 03 Correlation & Group Analysis

# COMMAND ----------

shop_sales['transaction_date'] = pd.to_datetime(shop_sales['transaction_date'])

# COMMAND ----------

import matplotlib.pyplot as plt
import seaborn as sns
plt.figure(figsize=(8,5))
sns.histplot(shop_sales['unit_price'], kde=True, bins=30)
plt.title('Distribution of Unit Price')
plt.xlabel('Unit Price')
plt.ylabel('Count')
plt.show()

# COMMAND ----------

# MAGIC %md
# MAGIC Task 04 Visualisation Library Comparison

# COMMAND ----------

revenue_by_store = shop_sales.groupby('store_location')['revenue'].sum().sort_values(ascending=False)

plt.figure(figsize=(8,5))
revenue_by_store.plot(kind='bar')
plt.title('Total Revenue by Store Location')
plt.ylabel('Total Revenue')
plt.xticks(rotation=45)
plt.show()

# COMMAND ----------

plt.figure(figsize=(10,5))
sns.countplot(x='hour', data=shop_sales)
plt.title('Transactions by Hour of Day')
plt.xlabel('Hour')
plt.ylabel('Number of Transactions')
plt.show()

# COMMAND ----------

import matplotlib.pyplot as plt
import seaborn as sns

# COMMAND ----------

corr = shop_sales[['unit_price', 'transaction_qty', 'revenue']].corr()

plt.figure(figsize=(6,5))
sns.heatmap(corr, annot=True, cmap='coolwarm', fmt='.2f')
plt.title('Correlation Heatmap: Price vs Qty vs Revenue')
plt.show()

# COMMAND ----------

pivot_rev = shop_sales.pivot_table(
    values='revenue', 
    index='store_location', 
    columns='product_category', 
    aggfunc='sum'
)

print(pivot_rev)

# COMMAND ----------

plt.figure(figsize=(10,5))
pivot_rev.plot(kind='bar', stacked=False)  # use stacked=True for stacked bar
plt.title('Revenue by Store Location and Product Category')
plt.ylabel('Total Revenue')
plt.xlabel('Store Location')
plt.xticks(rotation=45)
plt.legend(title='Product Category')
plt.tight_layout()
plt.show()

# COMMAND ----------

# MAGIC %md
# MAGIC 4. Which store earns the most? Which product category drives the most revenue overall?
# MAGIC 1.hells Kitchen
# MAGIC 2. Cofee

# COMMAND ----------

rev_by_cat = shop_sales.groupby('product_category')['revenue'].sum().sort_values(ascending=False).reset_index()

# COMMAND ----------

import matplotlib.pyplot as plt

plt.figure(figsize=(8,5))
plt.bar(rev_by_cat['product_category'], rev_by_cat['revenue'], color='steelblue')
plt.title('Revenue by Product Category')
plt.xlabel('Product Category')
plt.ylabel('Total Revenue')
plt.xticks(rotation=45, ha='right')
plt.tight_layout()
plt.show()

# COMMAND ----------

import seaborn as sns

plt.figure(figsize=(8,5))
sns.barplot(x='product_category', y='revenue', data=rev_by_cat, palette='viridis')
plt.title('Revenue by Product Category')
plt.xlabel('Product Category')
plt.ylabel('Total Revenue')
plt.xticks(rotation=45, ha='right')
plt.tight_layout()
plt.show()

# COMMAND ----------

import plotly.express as px

fig = px.bar(rev_by_cat, x='product_category', y='revenue', 
             title='Revenue by Product Category',
             color='product_category')
fig.update_xaxes(tickangle=45)
fig.update_layout(showlegend=False)
fig.show()

# COMMAND ----------

# MAGIC %md
# MAGIC Task 05 Business Insights

# COMMAND ----------

# MAGIC %md
# MAGIC 1.1. Hell's Kitchen generates the highest total revenue compared to Astoria and Lower Manhattan.
# MAGIC 1.2. the revenue_by_store output showing Hell's Kitchen with the tallest bar
# MAGIC 1.2. investigate reasons for hells to do good and apply it  in other stores.

# COMMAND ----------

# MAGIC %md
# MAGIC 2
# MAGIC 2.1. Coffee is the dominant revenue driver across all stores, far outperforming other categories.
# MAGIC 2.2.Supported by the revenue by product category bar chart where the green 'Coffee' bar is tallest.
# MAGIC 2.3. Introduce premium Coffee bundles or loyalty program to increase average transaction value for the top category.

# COMMAND ----------

3
3.1. Peak Hours
3.2. Supported by the  countplot of transactions by hour, which shows highest counts at hour X
3.3. Schedule more staff and ensure best-selling items like Coffee are fully stocked during peak hour X to reduce wait times and lost sales.

# COMMAND ----------

