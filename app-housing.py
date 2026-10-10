import streamlit as st
import pandas as pd

# 加载数据
@st.cache_data
def load_data():
    df = pd.read_csv("housing.csv")
    return df

df = load_data()

# -------------------- 1. 标题 --------------------
st.title("California Housing Data (1990) by Xin Li")

# -------------------- 2. 房价滑块 --------------------
min_price = st.slider(
    label="Minimal Median House Price",
    min_value=0,
    max_value=500001,
    value=200000
)

# -------------------- 3. 子标题 --------------------
st.subheader("See more filters in the sidebar:")

# -------------------- 4. 侧边栏多选：位置类型 --------------------
location_options = df["ocean_proximity"].unique()
selected_locations = st.sidebar.multiselect(
    label="Choose the location type",
    options=location_options,
    default=location_options
)

# -------------------- 5. 侧边栏单选：收入等级 --------------------
income_choice = st.sidebar.radio(
    label="Choose income level",
    options=["Low", "Medium", "High"]
)

# ---------- 筛选逻辑 ----------
# 第一步：房价筛选
filtered_df = df[df["median_house_value"] >= min_price]
# 第二步：地理位置筛选
filtered_df = filtered_df[filtered_df["ocean_proximity"].isin(selected_locations)]
# 第三步：收入等级 if 判断
if income_choice == "Low":
    filtered_df = filtered_df[filtered_df["median_income"] <= 2.5]
elif income_choice == "Medium":
    filtered_df = filtered_df[(filtered_df["median_income"] > 2.5) & (filtered_df["median_income"] < 4.5)]
elif income_choice == "High":
    filtered_df = filtered_df[filtered_df["median_income"] >= 4.5]

# -------------------- 6. 地图 --------------------
st.map(filtered_df)

# -------------------- 7. 直方图！！st.histogram，bins=30，作业原版！ --------------------
st.histogram(
    filtered_df["median_house_value"],
    bins=30
)