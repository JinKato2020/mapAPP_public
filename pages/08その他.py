import streamlit as st
import pandas as pd

@st.cache_data
def load_data():
    time.sleep(2) # 時間がかかる処理をシミュレート
    return pd.DataFrame({'a': [1, 2, 3], 'b': [4, 5, 6]})

st.header("キャッシュ")
data = load_data()
st.write("キャッシュされたデータ:", data)