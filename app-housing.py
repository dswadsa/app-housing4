import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# 设置 seaborn 主题风格以匹配截图外观
sns.set_theme(style="darkgrid")

# 1. 标题（请将 [Your Name] 替换为你自己的名字）
st.title("California Housing Data (1990) by Xin Li")

# 加载数据函数（使用缓存以提高性能）
@st.cache_data
def load_data():
    df = pd.read_csv("housing.csv")
    return df

df = load_data()

# 2. 滑块：Minimal Median House Value (范围 0 到 500001，默认 200000)
min_house_value = st.slider(
    "Minimal Median House Value",
    min_value=0,
    max_value=500001,
    value=200000
)

# 根据滑块过滤数据
df_filtered = df[df["median_house_value"] >= min_house_value]

# 3. 子标题
st.subheader("See more filters in the sidebar:")

# 4. 侧边栏：多选框（location type / ocean_proximity）
st.sidebar.header("Sidebar Filters")
ocean_options = df["ocean_proximity"].unique().tolist()
selected_ocean = st.sidebar.multiselect(
    "Choose the location type",
    options=ocean_options,
    default=ocean_options
)

# 根据侧边栏位置类型过滤数据
df_filtered = df_filtered[df_filtered["ocean_proximity"].isin(selected_ocean)]

# 5. 侧边栏：单选按钮（income level）与 if 语句过滤
income_level = st.sidebar.radio(
    "Choose income level",
    options=["Low", "Medium", "High"]
)

if income_level == "Low":
    df_filtered = df_filtered[df_filtered["median_income"] <= 2.5]
elif income_level == "Medium":
    df_filtered = df_filtered[(df_filtered["median_income"] > 2.5) & (df_filtered["median_income"] < 4.5)]
elif income_level == "High":
    df_filtered = df_filtered[df_filtered["median_income"] >= 4.5]

# 6. 过滤后街区的地图展示
st.map(df_filtered[['latitude', 'longitude']])

# 7. 地图下方：房屋中位价的直方图（30 个 bins，调整外观使其与截图一致）
st.subheader("Histogram of Median House Value")
fig, ax = plt.subplots(figsize=(8, 5))
sns.histplot(
    data=df_filtered, 
    x="median_house_value", 
    bins=30, 
    ax=ax, 
    color="#1f77b4"  # 标准的蓝条颜色
)
ax.set_xlabel("")
ax.set_ylabel("")
st.pyplot(fig)