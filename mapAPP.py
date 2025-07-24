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
    gc = gspread.service_account_from_dict(st.secrets["gcp_service_account"])
    st.success("Google Sheets (Streamlit Secrets) 認証成功！")

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