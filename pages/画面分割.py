import streamlit as st

st.set_page_config(layout="wide") # 画面全体を使うためにwideレイアウトを設定

st.title("Streamlit 2x4 グリッドレイアウト")

# 1行目
col1_1, col1_2, col1_3, col1_4 = st.columns(4)

with col1_1:
    st.header("左上")
    st.write("ここにコンテンツ1を配置します。")
    st.button("ボタン1")

with col1_2:
    st.header("上から2番目")
    st.image("https://via.placeholder.com/150", caption="画像1")

with col1_3:
    st.header("上から3番目")
    st.slider("スライダー1", 0, 100, 50)

with col1_4:
    st.header("右上")
    st.text_input("テキスト入力1", "デフォルト値")

st.markdown("---") # 区切り線

# 2行目
col2_1, col2_2, col2_3, col2_4 = st.columns(4)

with col2_1:
    st.header("左下")
    st.checkbox("チェックボックス1")
    if st.checkbox("エクスパンダー表示"):
        with st.expander("詳細情報"):
            st.write("これはエクスパンダー内の詳細コンテンツです。")

with col2_2:
    st.header("下から2番目")
    st.selectbox("選択ボックス1", ["オプションA", "オプションB", "オプションC"])

with col2_3:
    st.header("下から3番目")
    st.metric("メトリック1", "123", "1.2%")

with col2_4:
    st.header("右下")
    st.date_input("日付選択1")
    st.progress(70)