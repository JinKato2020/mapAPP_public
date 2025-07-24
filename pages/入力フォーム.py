import streamlit as st
import pandas as pd
from datetime import date # 日付の入力に使う
import os
import json
from PIL import Image
import gspread


# --- Google Sheets 認証情報の読み込み ---
# Streamlit Cloudのsecretsから認証情報を取得
# st.secretsは、Streamlit CloudのSecrets管理機能で設定された情報を辞書として提供します。
# secrets.tomlファイルの内容が自動的にst.secretsに読み込まれます。
try:
    # Streamlit Cloudのsecretsから読み込む場合
    # gcp_service_account は、Secretsに設定したセクション名です。
    # 例: [gcp_service_account]
    gc = gspread.service_account_from_dict(st.secrets["service_account"])

except KeyError:
    # ローカル環境でsecrets.tomlがない、またはSecretsが設定されていない場合のフォールバック
    st.warning("Streamlit Secretsが見つかりませんでした。ローカルファイルまたは環境変数で認証を試みます。")
    
    # 開発環境（ローカル）での認証方法の選択
    # 1. service_account.json ファイルから読み込む (ローカル開発用として推奨)
    sa_file_path = "service_account.json"
    if os.path.exists(sa_file_path):
        try:
            gc = gspread.service_account(filename=sa_file_path)
            st.success("Google Sheets (Local file) 認証成功！")
        except Exception as e:
            st.error(f"ローカルファイル認証エラー: {e}")
            st.stop() # エラーでアプリを停止
    # 2. 環境変数からJSON文字列として読み込む (CI/CDなどでの利用も可能)
    elif "GCP_SERVICE_ACCOUNT_JSON" in os.environ:
        try:
            json_key_str = os.environ.get("GCP_SERVICE_ACCOUNT_JSON")
            json_key = json.loads(json_key_str)
            gc = gspread.service_account_from_dict(json_key)
            st.success("Google Sheets (Environment Variable) 認証成功！")
        except Exception as e:
            st.error(f"環境変数認証エラー: {e}")
            st.stop() # エラーでアプリを停止
    else:
        st.error("認証情報が見つかりません。Streamlit Secrets、ローカルのservice_account.json、または環境変数のいずれかを設定してください。")
        st.stop() # 認証情報がない場合はアプリを停止
except Exception as e:
    # その他の認証エラー
    st.error(f"Google Sheets 認証中に予期せぬエラーが発生しました: {e}")
    st.error("認証情報の形式が正しくないか、Google Cloudの権限に問題がある可能性があります。")
    st.stop() # エラーでアプリを停止

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