def button_callback():
    st.session_state.button_clicked = True

st.header("コールバックとフォーム")

if 'button_clicked' not in st.session_state:
    st.session_state.button_clicked = False

st.button("コールバック付きボタン", on_click=button_callback)
if st.session_state.button_clicked:
    st.write("コールバックが実行されました！")

with st.form("my_form"):
    name = st.text_input("名前")
    age = st.number_input("年齢", min_value=0)
    submitted = st.form_submit_button("送信")
    if submitted:
        st.write(f"名前: {name}, 年齢: {age}")