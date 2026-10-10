import streamlit as st
import pandas as pd
import numpy as np

# -------- 加载数据 --------
@st.cache_data
def load_data():
    df = pd.read_csv("housing.csv")
    return df

df = load_data()

# 1. 标题，严格英文模板 California Housing Data (1990) by 你的名字
st.title("California Housing Data (1990) by Xin Li")

# 2.滑块：Minimal Median House Price，0~500001 默认200000
min_price = st.slider(
    label="Minimal Median House Price",
    min_value=0,
    max_value=500001,
    value=200000
)

# 3.子标题 See more filters in the sidebar:
st.subheader("See more filters in the sidebar:")

# ==========侧边栏组件==========
# 4.多选框 Choose the location type，ocean_proximity，默认全部选中
location_options = df["ocean_proximity"].unique()
selected_locations = st.sidebar.multiselect(
    label="Choose the location type",
    options=location_options,
    default=location_options
)

# 5.单选 Choose income level，Low / Medium / High
income_choice = st.sidebar.radio(
    label="Choose income level",
    options=["Low", "Medium", "High"]
)

# --------筛选逻辑（if语句，作业硬性要求）--------
filtered_df = df[df["median_house_value"] >= min_price]
filtered_df = filtered_df[filtered_df["ocean_proximity"].isin(selected_locations)]

if income_choice == "Low":
    filtered_df = filtered_df[filtered_df["median_income"] <= 2.5]
elif income_choice == "Medium":
    filtered_df = filtered_df[(filtered_df["median_income"] > 2.5) & (filtered_df["median_income"] < 4.5)]
elif income_choice == "High":
    filtered_df = filtered_df[filtered_df["median_income"] >= 4.5]


# 6.地图
st.subheader("The map shows the filtered districts:")
st.map(filtered_df)

# 7.直方图：30 bins，用numpy计算区间，bar_chart，消除空隙，竖直直方图
st.subheader("The histogram goes below the map:")
counts, bin_edges = np.histogram(filtered_df["median_house_value"], bins=30)
# 计算每个bin的中心点作为x坐标
bin_centers = (bin_edges[:-1] + bin_edges[1:]) / 2
hist_data = pd.DataFrame({
    "median_house_value": bin_centers,
    "count": counts
})
# bar_width设为区间宽度，填满间隙，模拟无缝直方图
st.bar_chart(hist_data, x="median_house_value", y="count", width=bin_edges[1]-bin_edges[0])