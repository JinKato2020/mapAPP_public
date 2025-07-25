import time

st.header("ステータス・ユーティリティ")

with st.spinner('処理中...'):
    time.sleep(2)
st.success('処理が完了しました！')

progress_text = "操作の進行状況。"
my_bar = st.progress(0, text=progress_text)
for percent_complete in range(100):
    time.sleep(0.01)
    my_bar.progress(percent_complete + 1, text=progress_text)
st.balloons()

# st.set_page_config() の使用例（通常はスクリプトの先頭に記述）
# st.set_page_config(page_title="マイアプリ", page_icon=":rocket:", layout="wide")

# セッションステートの例
if 'count' not in st.session_state:
    st.session_state.count = 0

if st.button('カウントを増やす'):
    st.session_state.count += 1
st.write('カウント:', st.session_state.count)