import os,pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
BASE=os.path.dirname(os.path.dirname(os.path.abspath(__file__))); 
csv=os.path.join(BASE,"data","Coffee_Shop_Sales.csv"); 
out=os.path.join(BASE,"output"); os.makedirs(out,exist_ok=True)
df=pd.read_csv(csv); 
df["transaction_date"]=pd.to_datetime(df.transaction_date,format="%m/%d/%y",errors="coerce"); 
df["transaction_time"]=pd.to_datetime(df.transaction_time,format="%H:%M:%S",errors="coerce"); 
print(df.isna().sum());
print("Duplicates:",df.duplicated().sum()); 
df=df.drop_duplicates().dropna(subset=["transaction_date","transaction_time"]); 
df["month"]=df.transaction_date.dt.to_period("M").astype(str); 
df["day_of_week"]=df.transaction_date.dt.day_name(); 
df["hour"]=df.transaction_time.dt.hour; 
df["revenue"]=df.transaction_qty*df.unit_price; 
sns.set_theme(style="whitegrid")

# 1 Monthly revenue
monthly = df.groupby("month", as_index=False)["revenue"].sum()
plt.figure(figsize=(10, 5))
sns.lineplot(data=monthly, x="month", y="revenue", marker="o")
plt.title("Monthly Revenue Trend")
plt.xlabel("Month"); plt.ylabel("Revenue")
plt.xticks(rotation=45); plt.tight_layout()
plt.savefig(os.path.join(OUT_DIR, "monthly_revenue_trend.png"), dpi=150); plt.close()

# 2 Store revenue
store = df.groupby("store_location", as_index=False)["revenue"].sum().sort_values("revenue")
plt.figure(figsize=(9, 5))
sns.barplot(data=store, x="revenue", y="store_location")
plt.title("Revenue by Store Location")
plt.xlabel("Revenue"); plt.ylabel("Store")
plt.tight_layout()
plt.savefig(os.path.join(OUT_DIR, "revenue_by_store.png"), dpi=150); plt.close()

# 3 Top 10 quantity
top_qty = df.groupby("product_detail", as_index=False)["transaction_qty"].sum().nlargest(10, "transaction_qty").sort_values("transaction_qty")
plt.figure(figsize=(10, 6))
sns.barplot(data=top_qty, x="transaction_qty", y="product_detail")
plt.title("Top 10 Products by Quantity Sold")
plt.xlabel("Quantity Sold"); plt.ylabel("Product")
plt.tight_layout()
plt.savefig(os.path.join(OUT_DIR, "top10_products_qty.png"), dpi=150); plt.close()

# 4 Top 10 revenue
top_rev = df.groupby("product_detail", as_index=False)["revenue"].sum().nlargest(10, "revenue").sort_values("revenue")
plt.figure(figsize=(10, 6))
sns.barplot(data=top_rev, x="revenue", y="product_detail")
plt.title("Top 10 Products by Revenue")
plt.xlabel("Revenue"); plt.ylabel("Product")
plt.tight_layout()
plt.savefig(os.path.join(OUT_DIR, "top10_products_revenue.png"), dpi=150); plt.close()

# 5 Category revenue
cat = df.groupby("product_category", as_index=False)["revenue"].sum().sort_values("revenue")
plt.figure(figsize=(10, 6))
sns.barplot(data=cat, x="revenue", y="product_category")
plt.title("Sales by Product Category")
plt.xlabel("Revenue"); plt.ylabel("Category")
plt.tight_layout()
plt.savefig(os.path.join(OUT_DIR, "sales_by_category.png"), dpi=150); plt.close()

# 6 Peak hours
peak = df.groupby("hour").size().reset_index(name="transaction_count")
plt.figure(figsize=(10, 5))
sns.barplot(data=peak, x="hour", y="transaction_count")
plt.title("Transaction Count by Hour")
plt.xlabel("Hour of Day"); plt.ylabel("Transactions")
plt.tight_layout()
plt.savefig(os.path.join(OUT_DIR, "peak_hours.png"), dpi=150); plt.close()

# 7 Day of week
order = ["Monday","Tuesday","Wednesday","Thursday","Friday","Saturday","Sunday"]
dow = df.groupby("day_of_week")["revenue"].sum().reindex(order).reset_index()
plt.figure(figsize=(10, 5))
sns.barplot(data=dow, x="day_of_week", y="revenue")
plt.title("Revenue by Day of Week")
plt.xlabel("Day"); plt.ylabel("Revenue")
plt.xticks(rotation=30); plt.tight_layout()
plt.savefig(os.path.join(OUT_DIR, "sales_by_day_of_week.png"), dpi=150); plt.close()

# 8 Category share
share = df.groupby("product_category")["revenue"].sum()
plt.figure(figsize=(8, 8))
plt.pie(share.values, labels=share.index, autopct="%1.1f%%", startangle=90)
plt.title("Revenue Share by Product Category")
plt.tight_layout()
plt.savefig(os.path.join(OUT_DIR, "category_revenue_share.png"), dpi=150); plt.close()

# 9 Hour x day heatmap
heat = pd.crosstab(df["hour"], df["day_of_week"]).reindex(columns=order)
plt.figure(figsize=(11, 8))
sns.heatmap(heat, annot=False, cmap="YlOrBr")
plt.title("Transaction Count Heatmap: Hour × Day of Week")
plt.xlabel("Day of Week"); plt.ylabel("Hour")
plt.tight_layout()
plt.savefig(os.path.join(OUT_DIR, "hourly_heatmap.png"), dpi=150); plt.close()

# 10 Unit price distribution
plt.figure(figsize=(10, 5))
sns.histplot(df["unit_price"], bins=30, kde=True)
plt.title("Unit Price Distribution")
plt.xlabel("Unit Price"); plt.ylabel("Frequency")
plt.tight_layout()
plt.savefig(os.path.join(OUT_DIR, "unit_price_distribution.png"), dpi=150); plt.close()

# Statistical summary
print("\\nDescriptive statistics:")
print(df[["transaction_qty", "unit_price", "revenue"]].describe())

daily = df.groupby("transaction_date")["revenue"].sum()
print("\\nTop 5 highest-revenue days:")
print(daily.nlargest(5))
print("\\nTop 5 lowest-revenue days:")
print(daily.nsmallest(5))
print(f"\\nSaved 10 charts to: {OUT_DIR}")