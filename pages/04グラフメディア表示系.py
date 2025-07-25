import streamlit as st
import pandas as pd
import numpy as np
from PIL import Image

st.subheader("1. Line, Area, Bar Chart")

# ダミーデータの作成
chart_data = pd.DataFrame(
    np.random.randn(20, 3), # 20行3列のランダムなデータ
    columns=['a', 'b', 'c']
)

st.write("---")
st.write("**折れ線グラフ (st.line_chart)**")
st.line_chart(chart_data)

st.write("---")
st.write("**エリアチャート (st.area_chart)**")
st.area_chart(chart_data)

st.write("---")
st.write("**棒グラフ (st.bar_chart)**")
st.bar_chart(chart_data)


import matplotlib.pyplot as plt

st.subheader("2. Matplotlibグラフ (st.pyplot)")
st.write("---")

# MatplotlibのFigureとAxesを作成
fig, ax = plt.subplots()

# データをプロット
x = [1, 2, 3, 4, 5]
y = [10, 8, 6, 4, 2]
ax.plot(x, y, marker='o', linestyle='--', color='blue')
ax.set_title("シンプルな折れ線グラフ")
ax.set_xlabel("X軸")
ax.set_ylabel("Y軸")
ax.grid(True)

# Streamlitで表示
st.pyplot(fig)

# 複数のサブプロットの例
st.write("---")
st.write("**複数のサブプロット**")
fig2, (ax1, ax2) = plt.subplots(1, 2, figsize=(10, 4)) # 1行2列のサブプロット

ax1.hist(np.random.randn(100), bins=10, color='skyblue')
ax1.set_title("ヒストグラム")

ax2.scatter(np.random.rand(50), np.random.rand(50), color='green', alpha=0.7)
ax2.set_title("散布図")

st.pyplot(fig2)

import altair as alt

st.subheader("3. Altairグラフ (st.altair_chart)")
st.write("---")

# Altair用のデータフレームを作成
source = pd.DataFrame({
    'a': ['A', 'B', 'C', 'D', 'E'],
    'b': [28, 55, 43, 91, 81]
})

# 棒グラフを作成
chart = alt.Chart(source).mark_bar().encode(
    x='a',
    y='b'
).properties(
    title='Altair シンプルな棒グラフ'
)

# Streamlitで表示
st.altair_chart(chart, use_container_width=True)

# 散布図とインタラクションの例
st.write("---")
st.write("**Altair 散布図（インタラクティブ）**")
source_scatter = pd.DataFrame(
    {'x': np.random.randn(100), 'y': np.random.randn(100), 'category': np.random.choice(['Group A', 'Group B'], 100)}
)

chart_scatter = alt.Chart(source_scatter).mark_circle().encode(
    x='x',
    y='y',
    color='category', # カテゴリで色分け
    tooltip=['x', 'y', 'category'] # ホバー時に表示される情報
).interactive() # インタラクティブ（ズーム、パン）を有効にする

st.altair_chart(chart_scatter, use_container_width=True)

import plotly.express as px

st.subheader("4. Plotlyグラフ (st.plotly_chart)")
st.write("---")

# Plotly Expressでサンプルデータセットを読み込み
df_plotly = px.data.iris() # アヤメのデータセット

# 散布図を作成
fig_scatter = px.scatter(
    df_plotly,
    x="sepal_width",
    y="sepal_length",
    color="species",
    title="Plotly Iris 散布図"
)

# Streamlitで表示
st.plotly_chart(fig_scatter, use_container_width=True)

# 3D散布図の例
st.write("---")
st.write("**Plotly 3D散布図**")
fig_3d = px.scatter_3d(
    df_plotly,
    x='sepal_length',
    y='sepal_width',
    z='petal_width',
    color='species',
    title="Plotly Iris 3D散布図"
)
st.plotly_chart(fig_3d, use_container_width=True)

import requests
from PIL import Image
from io import BytesIO

st.subheader("5. 画像表示 (st.image)")
st.write("---")

# URLからの画像表示
image_url = "pages/じろう.JPG"
st.write("**URLからの画像**")
st.image(image_url, caption="Streamlit Logo from URL", width=200)

# ローカルファイルからの画像表示 (※ご自身の環境に合わせてパスを調整してください)
# 例えば、`my_image.png` という画像がスクリプトと同じディレクトリにある場合
# try:
#     st.write("**ローカルファイルからの画像**")
#     st.image("my_image.png", caption="ローカル画像", use_column_width=True)
# except FileNotFoundError:
#     st.warning("`my_image.png` が見つかりませんでした。ローカル画像を表示するには、ファイルを配置してください。")

# NumPy配列からの画像表示 (OpenCVなどを使用した場合)
st.write("---")
st.write("**NumPy配列からの画像 (ダミー)**")
# 実際にはOpenCVなどで画像を読み込む
dummy_image_array = np.random.randint(0, 255, size=(100, 100, 3), dtype=np.uint8)
st.image(dummy_image_array, caption="ダミーのNumPy配列画像")

st.subheader("6. 音声再生 (st.audio)")
st.write("---")

# ダミーの音声ファイルURL (実際には短い効果音など)
audio_url = "https://www.soundhelix.com/examples/mp3/SoundHelix-Song-1.mp3" # 長いファイルなので注意
st.write("**URLからの音声**")
st.audio(audio_url, format='audio/mp3', start_time=10) # 10秒から再生

# ※ ローカルファイルからの音声再生も同様にパスを指定します
# audio_file = open("my_audio.wav", "rb")
# st.audio(audio_file.read(), format="audio/wav")

st.subheader("8. 地図表示 (st.map)")
st.write("---")

# マップ用のダミーデータ (東京駅周辺のランダムなポイント)
map_data = pd.DataFrame(
    np.random.randn(100, 2) / 100 + [35.6812, 139.7671], # 東京駅の緯度経度を中心にランダムな分散
    columns=['latitude', 'longitude']
)

st.map(map_data)

st.write("---")
st.write("**特定の場所を中心にズーム**")
# 渋谷駅周辺
shibuya_lat = 35.6590
shibuya_lon = 139.7037

shibuya_data = pd.DataFrame({
    'latitude': [shibuya_lat + np.random.randn() * 0.01 for _ in range(50)],
    'longitude': [shibuya_lon + np.random.randn() * 0.01 for _ in range(50)]
})

# ズームレベルを調整
st.map(shibuya_data, zoom=13) # ズームレベルを大きくするとより詳細に表示



