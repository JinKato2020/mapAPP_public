import streamlit as st
import pandas as pd
from datetime import date # 日付の入力に使う
import os
import json
from PIL import Image
import gspread


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

st.title("個人区域管理")
st.write("フォームで入力したデータを表にしています")

st.markdown("---")

# --- スプレッドシートからのデータ読み込みと表示 ---
st.header("スプレッドシートのデータと計算結果")

# データをキャッシュし、頻繁なAPI呼び出しを避ける
@st.cache_data(ttl=60) # データを60秒間キャッシュ
def load_data_from_sheet():
    try:
        # スプレッドシートの全データを読み込む
        data = worksheet.get_all_values()
        if not data:
            return pd.DataFrame(), "スプレッドシートにデータがありません。"

        # 最初の行をヘッダーとして使用
        headers = data[0]
        df = pd.DataFrame(data[1:], columns=headers)

        # 数値列を数値型に変換 (エラーがある場合はNaN、その後0に置換)
        for col in ['値1', '値2']: # スプレッドシートのヘッダー名に合わせてください
            if col in df.columns:
                df[col] = pd.to_numeric(df[col], errors='coerce').fillna(0)
        return df, None
    except Exception as e:
        return pd.DataFrame(), f"データの読み込み中にエラーが発生しました: {e}"

df, error_message = load_data_from_sheet()

if error_message:
    st.error(error_message)
elif not df.empty:

    st.subheader("内部計算結果")
    # --- 内部での計算処理 ---
    if '値1' in df.columns and '値2' in df.columns:
        df['合計'] = df['値1'] + df['値2']
        df['平均'] = (df['値1'] + df['値2']) / 2
        df['値1の2倍'] = df['値1'] * 2
        # ここに任意の計算を追加できます (例: 差分、積など)

        # 表示したい計算結果の列を選択
        st.dataframe(df[['項目名', '値1', '値2', '合計', '平均', '値1の2倍']]) 

        st.write("### 集計値")
        st.write(f"全体の値1の合計: {df['値1'].sum():,.2f}")
        st.write(f"全体の値2の平均: {df['値2'].mean():,.2f}")
    else:
        st.warning("計算に必要な '値1' または '値2' の列がスプレッドシートに見つかりません。")
        st.warning("スプレッドシートのヘッダー行が '項目名', '値1', '値2' となっているか確認してください。")
else:
    st.info("スプレッドシートにデータがありません。上記のフォームからデータを送信してください。")

# データを最新にするボタン
if st.button("最新データに更新"):
    st.cache_data.clear() # キャッシュをクリアして最新データを再読み込み
    st.rerun()