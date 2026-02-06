import streamlit as st
import pandas as pd
import plotly.express as px

# Set page config
st.set_page_config(page_title="Supply Chain Dashboard", layout="wide")

# Load Data
@st.cache_data
def load_data():
    df = pd.read_csv('supply_chain_dataset1.csv')
    df['Date'] = pd.to_datetime(df['Date'])
    df['Revenue'] = df['Units_Sold'] * df['Unit_Price']
    return df

df = load_data()

# Sidebar Filters
st.sidebar.header("Filter Options")
region = st.sidebar.multiselect("Select Region:", options=df['Region'].unique(), default=df['Region'].unique())
selected_sku = st.sidebar.selectbox("Select SKU for Detail View:", options=df['SKU_ID'].unique())

filtered_df = df[df['Region'].isin(region)]

# --- HEADER STATS ---
st.title("📦 Supply Chain Command Center")
col1, col2, col3, col4 = st.columns(4)
col1.metric("Total Revenue", f"${filtered_df['Revenue'].sum():,.0f}")
col2.metric("Total Units Sold", f"{filtered_df['Units_Sold'].sum():,}")
col3.metric("Avg Lead Time", f"{filtered_df['Supplier_Lead_Time_Days'].mean():.1f} Days")
col4.metric("Inventory Health", f"{(filtered_df['Inventory_Level'] > filtered_df['Reorder_Point']).mean():.1%}")

# --- VISUALIZATIONS ---
c1, c2 = st.columns(2)

with c1:
    st.subheader("Daily Sales Trend")
    daily_sales = filtered_df.groupby('Date')['Units_Sold'].sum().reset_index()
    fig1 = px.line(daily_sales, x='Date', y='Units_Sold', template="plotly_white")
    st.plotly_chart(fig1, use_container_width=True)

    st.subheader("Sales by Region")
    reg_sales = filtered_df.groupby('Region')['Units_Sold'].sum().reset_index()
    fig2 = px.bar(reg_sales, x='Region', y='Units_Sold', color='Region')
    st.plotly_chart(fig2, use_container_width=True)

with c2:
    st.subheader(f"Inventory Analysis: {selected_sku}")
    sku_df = df[df['SKU_ID'] == selected_sku].sort_values('Date')
    fig3 = px.line(sku_df, x='Date', y=['Inventory_Level', 'Reorder_Point'], 
                   color_discrete_map={'Inventory_Level': 'blue', 'Reorder_Point': 'red'})
    st.plotly_chart(fig3, use_container_width=True)

    st.subheader("Forecast vs. Actual Sales")
    fig4 = px.scatter(filtered_df, x='Demand_Forecast', y='Units_Sold', opacity=0.3, 
                      trendline="ols", trendline_color_override="red")
    st.plotly_chart(fig4, use_container_width=True)