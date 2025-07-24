import streamlit as st
import pandas as pd
from datetime import date # 日付の入力に使う
import os
import json
from PIL import Image
import gspread
import streamlit as st
import gspread
import pandas as pd
import os

# --- Google Sheets 認証情報の読み込み (ローカル実行用) ---
# service_account.json ファイルを直接読み込みます。
# このファイルは app.py と同じディレクトリに配置してください。
SERVICE_ACCOUNT_FILE = "manage-personal-map.json"

if not os.path.exists(SERVICE_ACCOUNT_FILE):
    st.error(f"認証情報ファイル '{SERVICE_ACCOUNT_FILE}' が見つかりません。")
    st.error("Google Cloud Platformでサービスアカウントキーをダウンロードし、")
    st.error(f"このファイルと同じディレクトリに '{SERVICE_ACCOUNT_FILE}' として保存してください。")
    st.stop() # 認証情報がない場合はアプリを停止

try:
    gc = gspread.service_account(filename=SERVICE_ACCOUNT_FILE)
except Exception as e:
    st.error(f"Google Sheets 認証エラー: {e}")
    st.error("service_account.json ファイルの内容が正しいか、権限が適切か確認してください。")
    st.stop() # 認証情報エラーの場合はアプリを停止

# スプレッドシート名 (あなたが作成したスプレッドシート名に変更してください)
SPREADSHEET_NAME = "個人区域管理"

try:
    sh = gc.open(SPREADSHEET_NAME)
    worksheet = sh.sheet1 # 最初のシート（通常はSheet1）を使用
except gspread.exceptions.SpreadsheetNotFound:
    st.error(f"スプレッドシート '{SPREADSHEET_NAME}' が見つかりません。")
    st.error("Googleスプレッドシートの名前が正しいか、")
    st.error("サービスアカウントのメールアドレスがスプレッドシートに「編集者」として共有されているか確認してください。")
    st.stop()
except Exception as e:
    st.error(f"スプレッドシートへのアクセスエラー: {e}")
    st.stop()

st.title("データ入力＆計算デモアプリ")
st.write("このアプリは、Googleスプレッドシートと連携し、データの入力、表示、計算を行います。")

# --- データ入力フォーム ---
with st.form("data_input_form"):
    st.header("新しいデータ入力")
    item_name = st.text_input("項目名", help="例: 商品A, サービスB")
    value1 = st.number_input("値1", min_value=0.0, step=0.1, help="例: 100.5")
    value2 = st.number_input("値2", min_value=0.0, step=0.1, help="例: 200.3")
    
    submitted = st.form_submit_button("データ送信")

    if submitted:
        if item_name and value1 is not None and value2 is not None:
            new_data = [item_name, value1, value2]
            try:
                worksheet.append_row(new_data)
                st.success("データがスプレッドシートに正常に送信されました！")
                # フォーム送信後にデータを再読み込みするためにキャッシュをクリア
                st.cache_data.clear()
                st.rerun() # ページをリロードして最新データを表示
            except Exception as e:
                st.error(f"データの書き込み中にエラーが発生しました: {e}")
        else:
            st.warning("すべてのフィールドを入力してください。")