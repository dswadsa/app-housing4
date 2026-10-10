import streamlit as st
import pandas as pd

# -------- 加载数据 --------
@st.cache_data
def load_data():
    df = pd.read_csv("housing.csv")
    # 把房价单位转为美元，原数据是万美元
    df["median_house_value"] = df["median_house_value"]
    return df

df = load_data()

# -------- 页面标题（要求：标题带你的名字）--------
st.title("加州住房数据(1990)，作者【你的名字】")

# 1. 滑块：最小中位房屋价值，0~500001，默认200000
min_price = st.slider(
    label="最小中位房屋价值",
    min_value=0,
    max_value=500001,
    value=200000
)

# 2. 副标题
st.subheader("更多过滤器请见侧边栏:")

# ========= 侧边栏组件 =========
st.sidebar.header("筛选面板")

# 多选框：位置类型 ocean_proximity，默认全部选中
location_options = df["ocean_proximity"].unique()
selected_locations = st.sidebar.multiselect(
    label="选择通过的位置类型",
    options=location_options,
    default=location_options
)

# 单选按钮：收入等级 三个选项
income_level = st.sidebar.radio(
    label="选择收入等级",
    options=["最低: ≤2.5 median_income", "中等: 2.5<4.5 median_income", "最高: ≥4.5 median_income"]
)

# -------- 筛选逻辑 --------
# 第一步：价格筛选
filtered_df = df[df["median_house_value"] >= min_price]

# 第二步：位置类型筛选
filtered_df = filtered_df[filtered_df["ocean_proximity"].isin(selected_locations)]

# 第三步：收入等级筛选
if income_level == "最低: ≤2.5 median_income":
    filtered_df = filtered_df[filtered_df["median_income"] <= 2.5]
elif income_level == "中等: 2.5<4.5 median_income":
    filtered_df = filtered_df[(filtered_df["median_income"] > 2.5) & (filtered_df["median_income"] < 4.5)]
elif income_level == "最高: ≥4.5 median_income":
    filtered_df = filtered_df[filtered_df["median_income"] >= 4.5]


# -------- 绘制地图 --------
st.subheader("地图显示了筛选后的选区:")
st.map(filtered_df, latitude="latitude", longitude="longitude")

# -------- 直方图：median_house_value，30个区间 --------
st.subheader("直方图位于地图下方:")
st.histogram(filtered_df["median_house_value"], bins=30)