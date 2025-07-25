st.header("入力ウィジェット")
if st.button("クリックしてください"):
    st.write("ボタンがクリックされました！")

checked = st.checkbox("チェックボックス")
if checked:
    st.write("チェックされています。")

option = st.radio("好きな色を選んでください:", ('赤', '青', '緑'))
st.write("選択された色:", option)

selected_items = st.multiselect(
    "好きな果物を選んでください:",
    ['りんご', 'バナナ', 'みかん', 'ぶどう']
)
st.write("選択された果物:", selected_items)

age = st.slider("年齢", 0, 100, 25)
st.write("あなたの年齢:", age)

name = st.text_input("名前を入力してください:")
st.write("こんにちは、", name)

uploaded_file = st.file_uploader("ファイルをアップロードしてください:")
if uploaded_file is not None:
    st.write("ファイルがアップロードされました。")