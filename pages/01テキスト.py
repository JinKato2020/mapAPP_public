import streamlit as st
import pandas as pd

st.title("Streamlit 関数デモ")
st.header("テキスト表示")
st.write("これは汎用的な **st.write** 関数で表示されたテキストです。")
st.markdown("---") # 区切り線
st.markdown("### Markdown 形式のテキスト")
st.markdown("- アイテム1\n- アイテム2")
st.text("これは固定幅のテキストです。")
st.caption("これはキャプションです。")
st.latex(r"e^{i\pi} + 1 = 0")