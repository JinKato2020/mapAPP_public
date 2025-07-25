st.header("レイアウト・コンテナ")

with st.sidebar:
    st.write("これはサイドバーに表示されます。")

col1, col2 = st.columns(2)
with col1:
    st.write("これは1列目です。")
with col2:
    st.write("これは2列目です。")

tab1, tab2 = st.tabs(["タブ1", "タブ2"])
with tab1:
    st.write("タブ1のコンテンツです。")
with tab2:
    st.write("タブ2のコンテンツです。")

with st.expander("詳細を見る"):
    st.write("ここに詳細情報が表示されます。")