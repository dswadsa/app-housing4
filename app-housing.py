import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# -------- 加载数据 --------
@st.cache_data
def load_data():
    df = pd.read_csv("housing.csv")
    return df

df = load_data()

# 1.标题（替换【你的名字】）
st.title("加州住房数据(1990)，作者【你的名字】")

# 2.滑块：最小中位房屋价值，0~500001，默认200000
min_price = st.slider(
    label="最小中位房屋价值",
    min_value=0,
    max_value=500001,
    value=200000
)

# 3.副标题
st.subheader("更多过滤器请见侧边栏:")

# ========= 侧边栏组件 =========
location_options = df["ocean_proximity"].unique()
selected_locations = st.sidebar.multiselect(
    label="选择通过的位置类型",
    options=location_options,
    default=location_options
)

income_level = st.sidebar.radio(
    label="选择收入等级",
    options=["最低: ≤2.5 median_income", "中等: 2.5<4.5 median_income", "最高: ≥4.5 median_income"]
)

# -------- 筛选逻辑 --------
filtered_df = df[df["median_house_value"] >= min_price]
filtered_df = filtered_df[filtered_df["ocean_proximity"].isin(selected_locations)]

if income_level == "最低: ≤2.5 median_income":
    filtered_df = filtered_df[filtered_df["median_income"] <= 2.5]
elif income_level == "中等: 2.5<4.5 median_income":
    filtered_df = filtered_df[(filtered_df["median_income"] > 2.5) & (filtered_df["median_income"] < 4.5)]
elif income_level == "最高: ≥4.5 median_income":
    filtered_df = filtered_df[filtered_df["median_income"] >= 4.5]


# -------- 绘制地图 --------
st.subheader("地图显示了筛选后的选区:")
st.map(filtered_df, latitude="latitude", longitude="longitude")

# -------- 直方图，bins=30，和作业截图样式一致，柱子紧密相连 --------
st.subheader("直方图位于地图下方:")
fig, ax = plt.subplots()
ax.hist(filtered_df["median_house_value"], bins=30)
st.pyplot(fig)