import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import math

st.title("Data App Assignment, on Oct 7th")

st.write("### Input Data and Examples")
df = pd.read_csv("Superstore_Sales_utf8.csv", parse_dates=True)  # Changed 'data' to 'df'
st.dataframe(df)

# This bar chart will not have solid bars--but lines--because the detail data is being graphed independently
st.bar_chart(df, x="Category", y="Sales")

# Now let's do the same graph where we do the aggregation first in Pandas...
st.dataframe(df.groupby("Category").sum())
st.bar_chart(df.groupby("Category", as_index=False).sum(), x="Category", y="Sales", color="#04f")

# Aggregating by time
df["Order_Date"] = pd.to_datetime(df["Order_Date"])
df.set_index('Order_Date', inplace=True)
sales_by_month = df.filter(items=['Sales']).groupby(pd.Grouper(freq='M')).sum()

st.dataframe(sales_by_month)
st.line_chart(sales_by_month, y="Sales")

st.write("## Your additions")
category = st.selectbox('Select a Category', df['Category'].unique())  # Changed 'data' to 'df'
sub_categories = df.loc[df['Category'] == category, 'Sub_Category']
st.write(sub_categories)
selected_sub_categories = st.multiselect(f"Select Sub-Categories in {category}", sub_categories)
st.write(f"Selected Category: {category}")
st.write(f"Selected Sub-Categories: {selected_sub_categories}")
filtered_df = df[(df['Category'] == category) & (df['Sub_Category'].isin(selected_sub_categories))]

st.write("### (3) show a line chart of sales for the selected items in (2)")
sales_chart = filtered_df.groupby('Order_Date')['Sales'].sum().reset_index()
st.line_chart(sales_chart, x='Order_Date', y='Sales')

# Calculate metrics
total_sales = filtered_df['Sales'].sum()
total_profit = filtered_df['Profit'].sum()
overall_profit_margin = total_profit / total_sales * 100

# Overall average profit margin for all products across all categories
overall_avg_profit_margin = df['Profit'].sum() / df['Sales'].sum() * 100
delta_profit_margin = overall_profit_margin - overall_avg_profit_margin

st.write("### (4) show three metrics")
col1, col2, col3 = st.columns(3)
col1.metric("Total Sales", f"${total_sales:,.2f}")
col2.metric("Total Profit", f"${total_profit:,.2f}")
col3.metric("Overall Profit Margin", f"{overall_profit_margin:.2f}%", delta=f"{delta_profit_margin:.2f}%")
