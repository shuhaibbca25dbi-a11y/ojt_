import streamlit as st
import pandas as pd
import plotly.express as px

# -----------------------
# Page Configuration
# -----------------------
st.set_page_config(
    page_title="NovaMart Sales Dashboard",
    page_icon="📊",
    layout="wide"
)

# -----------------------
# Title
# -----------------------
st.title("📊 NovaMart Sales Dashboard")
st.write("Prepared by: Jazeel Ahmed | Version 4")

# -----------------------
# Load Dataset
# -----------------------
import os

BASE_DIR = os.path.dirname(__file__)
df = pd.read_csv(os.path.join(BASE_DIR, "..", "Data", "cleaned_novamart_data.csv"))

# -----------------------
# Sidebar Filters
# -----------------------
st.sidebar.header("Filters")

selected_region = st.sidebar.selectbox(
    "Select Region",
    ["All"] + sorted(df["region"].unique())
)

selected_category = st.sidebar.selectbox(
    "Select Category",
    ["All"] + sorted(df["category"].unique())
)

selected_month = st.sidebar.selectbox(
    "Select Month",
    ["All"] + sorted(df["month"].unique().tolist())
)

# -----------------------
# Apply Filters
# -----------------------
filtered_df = df.copy()

if selected_region != "All":
    filtered_df = filtered_df[
        filtered_df["region"] == selected_region
    ]

if selected_category != "All":
    filtered_df = filtered_df[
        filtered_df["category"] == selected_category
    ]

if selected_month != "All":
    filtered_df = filtered_df[
        filtered_df["month"] == selected_month
    ]

# -----------------------
# KPI Calculations
# -----------------------
total_sales = filtered_df["sales"].sum()
total_profit = filtered_df["profit"].sum()
total_orders = filtered_df["order_id"].nunique()
avg_discount = filtered_df["discount"].mean()

# -----------------------
# KPI Cards
# -----------------------
col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric("💰 Total Sales", f"${total_sales:,.2f}")

with col2:
    st.metric("📈 Total Profit", f"${total_profit:,.2f}")

with col3:
    st.metric("🛒 Total Orders", total_orders)

with col4:
    st.metric("🏷️ Avg Discount", f"{avg_discount:.2%}")

# -----------------------
# Charts
# -----------------------

left_col, right_col = st.columns(2)

# Sales by Category
sales_by_category = (
    filtered_df.groupby("category")["sales"]
    .sum()
    .reset_index()
)

fig1 = px.bar(
    sales_by_category,
    x="category",
    y="sales",
    title="Sales by Category"
)

fig1.update_layout(height=450)

with left_col:
    st.plotly_chart(fig1, use_container_width=True)

# Sales by Region
sales_by_region = (
    filtered_df.groupby("region")["sales"]
    .sum()
    .reset_index()
)

fig2 = px.pie(
    sales_by_region,
    names="region",
    values="sales",
    title="Sales by Region"
)

fig2.update_layout(height=450)

with right_col:
    st.plotly_chart(fig2, use_container_width=True)

# -----------------------
# Monthly Sales Trend
# -----------------------

month_order = [
    "January",
    "February",
    "March",
    "April",
    "May",
    "June"
]

monthly_sales = (
    filtered_df.groupby("month")["sales"]
    .sum()
    .reset_index()
)

monthly_sales["month"] = pd.Categorical(
    monthly_sales["month"],
    categories=month_order,
    ordered=True
)

monthly_sales = monthly_sales.sort_values("month")

fig3 = px.line(
    monthly_sales,
    x="month",
    y="sales",
    markers=True,
    title="Monthly Sales Trend"
)

fig3.update_layout(height=450)

st.plotly_chart(fig3, use_container_width=True)

# -----------------------
# Top 10 Products by Sales
# -----------------------

top_products = (
    filtered_df.groupby("product_name")["sales"]
    .sum()
    .sort_values(ascending=False)
    .head(10)
    .reset_index()
)

fig4 = px.bar(
    top_products,
    x="sales",
    y="product_name",
    orientation="h",
    title="Top 10 Products by Sales"
)

fig4.update_layout(height=500)

st.plotly_chart(fig4, use_container_width=True)

# -----------------------
# Profit by Category
# -----------------------

profit_by_category = (
    filtered_df.groupby("category")["profit"]
    .sum()
    .reset_index()
)

fig5 = px.bar(
    profit_by_category,
    x="category",
    y="profit",
    title="Profit by Category"
)

fig5.update_layout(height=450)

st.plotly_chart(fig5, use_container_width=True)

# -----------------------
# Sales vs Profit
# -----------------------

fig6 = px.scatter(
    filtered_df,
    x="sales",
    y="profit",
    color="category",
    size="quantity",
    hover_data=["product_name"],
    title="Sales vs Profit Analysis"
)

fig6.update_layout(height=500)

st.plotly_chart(fig6, use_container_width=True)

# -----------------------
# Download Filtered Data
# -----------------------

csv = filtered_df.to_csv(index=False).encode("utf-8")

st.download_button(
    label="📥 Download Filtered Data (CSV)",
    data=csv,
    file_name="filtered_novamart_data.csv",
    mime="text/csv"
)

# -----------------------
# Dataset Preview
# -----------------------
filtered_df = df.copy()
st.subheader("Dataset Preview")
st.dataframe(filtered_df.head())
