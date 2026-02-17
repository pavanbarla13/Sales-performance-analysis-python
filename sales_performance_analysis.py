import pandas as pd
df = pd.read_csv("sales_raw.csv")

df["order_date"] = pd.to_datetime(df["order_date"])

df["total_amount"]= df["quantity"]*df["price"]

df["month"]=df["order_date"].dt.to_period("M")
monthly_sales = df.groupby("month")["total_amount"].sum()
print(monthly_sales)

city_sales = df.groupby("city")["total_amount"].sum().sort_values(ascending=False)
print("\nsales by city")
print(city_sales)

product_sales = df.groupby("product")["total_amount"].sum().sort_values(ascending=False)
print("\nproduct by sales")
print(product_sales)

category_sales = df.groupby("category")["total_amount"].sum().sort_values(ascending=False)
print("\ncategories by sales")
print(category_sales)

#Monthly revenue
monthly_sales = (df.groupby("month")["total_amount"].sum().sort_index())
monthly_growth = monthly_sales.pct_change()*100
print("\nMonthly revenue:")
print(monthly_sales)

#Monthly orders
monthly_orders = (df.groupby("month")["order_id"].nunique().sort_index())
monthly_growth = monthly_sales.pct_change()*100
print("\nMonthly orders:")
print(monthly_orders)

#Monthly AOV
monthly_aov = monthly_sales/monthly_orders
print("\nMonthly average order value:")
print(monthly_aov)

#monthly growth
monthly_growth=monthly_sales.pct_change()*100
print("\nMonthly Growth %:")
print(monthly_growth)

customer_sales = df.groupby("customer_id")["total_amount"].sum().sort_values(ascending=False)
print("\nTop Customers by revenue")
print(customer_sales.head(6))

total_revenue = df["total_amount"].sum()
total_orders = df["order_id"].nunique()

average_order_value = total_revenue/total_orders
print("\nTotal Revenue:", total_revenue)
print("Total orders:",total_orders)
print("Average order value",average_order_value)

#Revenue contribution%(Category share)
total_revenue = df["total_amount"].sum()
category_sales = df.groupby("category")["total_amount"].sum()

category_contribution = (total_revenue/category_sales)*100
print("\nCategory contribution",category_contribution)

#which month generated highest revenue?
monthly_sales = (df.groupby("month")["total_amount"].sum().sort_index())
best_month = monthly_sales.idxmax
best_month_revenue = monthly_sales.max()
print("\nBest month",best_month)
print("Best month revenue",best_month)

#Worst performing month

worst_month = monthly_sales.idxmin()
worst_month_revenue = monthly_sales.min()

print("\nWorst month",worst_month)
print("Worst month revenue",worst_month_revenue)

#Repeat VS One-time customers
customer_orders = df.groupby("customer_id")["order_id"].nunique()

repeat_customers = customer_orders[customer_orders > 1].count()
one_time_customer = customer_orders[customer_orders==1].count()

print("\nRepeat customers",repeat_customers)
print("one time customers",one_time_customer)

# on average, how much revenue does one customer generate? AOV = per order and CLV = per customer
customer_revenue= df.groupby("customer_id")["total_amount"].sum()
average_clv = customer_revenue.mean()
print("/nAverage customers lifetime value:",average_clv)

#Monthly revenue by city ... which city performs best each month?
city_monthly_Sales =(df.groupby(["month","city"])["total_amount"].sum().sort_index())
print("\nMonthly Revenue by city:")
print(city_monthly_Sales)

#Monthly revenue by category
category_monthly_sales = (df.groupby(["month","category"])["total_amount"].sum().sort_index)
print("\nMonthly Revenue by category:")
print(category_monthly_sales)

# Top 3 customers contribution
total_revenue = df["total_amount"].sum()

customer_revenue =(df.groupby("customer_id")["total_amount"].sum().sort_values(ascending=False))
top3_revenue= customer_revenue.head(3).sum()

top3_contribution = (top3_revenue/total_revenue)*100
print("\ntop3 contributions:")
print(top3_contribution)

#Executive KPI summary

kpi_summary = {"Total Revenue": 
               df["total_amount"].sum(),
               "Total orders":
               df["order_id"].nunique(),
               "Total customers":
               df["customer_id"].nunique(),
               "Average order value":
               df["total_amount"].sum()/df["order_id"].unique(),
               "Average CLV":df.groupby("customer_id")["total_amount"].sum().mean()}
print("\nExcutive KPI summary:")
for key, value in kpi_summary.items():
    print(f"{key}:{value}")


#Retation rate

customer_orders = df.groupby("customer_id")["order_id"].nunique()
repeat_customers = customer_orders[customer_orders > 1].count()
total_customers = customer_orders.count()

retention_rate = (repeat_customers/total_customers)*100

print("Repeat customers:", repeat_customers)
print("Total customers:", repeat_customers)
print("retention rate (%):", retention_rate)

#calculate average monthly growth
monthly_sales =(df.groupby("month")["total_amount"].sum().sort_index())
monthly_growth = monthly_sales.pct_change()
average_growth = monthly_growth.mean()

print("average Monthly growth:", average_growth)

# forecast next month
last_month_revenue = monthly_sales.iloc[-1]

forecast_next_month = last_month_revenue *(1 + average_growth) # New value = Old value * (1+Growth rate)

print("Last Month Revenue:", last_month_revenue)
print("Forecast Next month revenue:", forecast_next_month)

import matplotlib.pyplot as plt
monthly_sales.index = monthly_sales.index.astype(str)

plt.figure()
plt.plot(monthly_sales.index,monthly_sales.values)
plt.title("Monthly Revenue Trend")
plt.xlabel("month")
plt.ylabel("Revenue")
plt.xticks(rotation=45)
plt.show()