import pandas as pd

orders = pd.read_csv("olist_orders_dataset.csv")

date_cols = [
    "order_purchase_timestamp",
    "order_delivered_customer_date",
    "order_estimated_delivery_date"
]

for col in date_cols:
    orders[col] = pd.to_datetime(orders[col], errors="coerce")

orders["delivery_days"] = (
    orders["order_delivered_customer_date"]
    - orders["order_purchase_timestamp"]
).dt.total_seconds() / (24 * 3600)

orders["is_late"] = (
    orders["order_delivered_customer_date"]
    > orders["order_estimated_delivery_date"]
)

delivered = orders.dropna(subset=["order_delivered_customer_date"]).copy()

on_time_rate = (~delivered["is_late"]).mean() * 100
avg_delivery_days = delivered["delivery_days"].mean()
late_rate = delivered["is_late"].mean() * 100

print(f"On-Time Delivery Rate: {on_time_rate:.2f}%")
print(f"Average Delivery Time: {avg_delivery_days:.2f} days")
print(f"Late Delivery Rate: {late_rate:.2f}%")
