import streamlit as st
import pandas as pd
from datetime import date # 日付の入力に使う

st.set_page_config(layout="centered") # レイアウトを中央に設定
st.title('個人区域貸出フォーム')

# --- データの初期化 ---
# セッションステートを使ってデータを保持
# アプリが起動したときに、'library_data'がセッションステートになければ初期化する
if 'library_data' not in st.session_state:
    st.session_state.library_data = []

# --- 貸出図書データの入力フォーム ---
st.header('貸出データの入力')

with st.form("book_entry_form"):
    # テキスト入力
    title = st.text_input('書名', placeholder='例：Python入門')
    author = st.text_input('著者名', placeholder='例：山田太郎')

    # 日付入力
    # デフォルト値を今日の日付に設定
    lend_date = st.date_input('貸出日', value=date.today())
    return_date = st.date_input('返却予定日', value=date.today()) # 返却予定日もデフォルトを今日に

    # フォームの送信ボタン
    submitted = st.form_submit_button("登録")

    if submitted:
        # 入力値のバリデーション（書名が必須など）
        if not title or not author:
            st.warning('書名と著者名は必須です。')
        else:
            # 入力データを辞書として作成
            new_entry = {
                '書名': title,
                '著者名': author,
                '貸出日': lend_date.strftime('%Y-%m-%d'), # 日付を文字列形式で保存
                '返却予定日': return_date.strftime('%Y-%m-%d'),
                '返却済': '未返却' # 初期値
            }
            # セッションステートのリストに新しいデータを追加
            st.session_state.library_data.append(new_entry)
            st.success('貸出図書データが追加されました！')
            # フォーム送信後、入力フィールドをクリア（オプション）
            # st.experimental_rerun() # これを使うとページ全体がリロードされるので、
