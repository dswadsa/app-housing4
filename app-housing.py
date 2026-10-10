import streamlit as st
import pandas as pd
import numpy as np

# -------- 加载数据 --------
@st.cache_data
def load_data():
    df = pd.read_csv("housing.csv")
    return df

df = load_data()

# 1. 标题（英文，严格匹配作业模板）
st.title("California Housing Data (1990) by Xin Li")

# 2. 滑块：Minimal Median House Price，0~500001，默认200000
min_price = st.slider(
    label="Minimal Median House Price",
    min_value=0,
    max_value=500001,
    value=200000
)

# 3. 子标题
st.subheader("See more filters in the sidebar:")

# ========== 侧边栏 ==========
# 4. 多选框 Choose the location type
location_options = df["ocean_proximity"].unique()
selected_locations = st.sidebar.multiselect(
    label="Choose the location type",
    options=location_options,
    default=location_options
)

# 5. 单选按钮 Choose income level
income_choice = st.sidebar.radio(
    label="Choose income level",
    options=["Low", "Medium", "High"]
)

# -------- 筛选逻辑（if条件，作业硬性要求）--------
filtered_df = df[df["median_house_value"] >= min_price]
filtered_df = filtered_df[filtered_df["ocean_proximity"].isin(selected_locations)]

if income_choice == "Low":
    filtered_df = filtered_df[filtered_df["median_income"] <= 2.5]
elif income_choice == "Medium":
    filtered_df = filtered_df[(filtered_df["median_income"] > 2.5) & (filtered_df["median_income"] < 4.5)]
elif income_choice == "High":
    filtered_df = filtered_df[filtered_df["median_income"] >= 4.5]

# 6. 地图
st.subheader("The map shows the filtered districts:")
st.map(filtered_df)

# 7. 直方图部分：np.histogram 强制30个bin，竖直柱状图模拟直方图
st.subheader("The histogram goes below the map:")
counts, bin_edges = np.histogram(filtered_df["median_house_value"], bins=30)
bin_center = (bin_edges[:-1] + bin_edges[1:]) / 2
hist_df = pd.DataFrame({
    "median_house_value": bin_center,
    "count": counts
})
st.bar_chart(hist_df, x="median_house_value", y="count")