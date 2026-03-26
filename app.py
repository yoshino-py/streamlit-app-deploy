import streamlit as st
from dotenv import load_dotenv
import os
from openai import OpenAI

# .env ファイルから環境変数を読み込む
load_dotenv()

# OpenAI API キーを設定
api_key = os.getenv("OPENAI_API_KEY")
client = OpenAI(api_key=api_key)

# Streamlit ページ設定
st.set_page_config(page_title="LLM チャットボット", layout="wide", initial_sidebar_state="expanded")

# スタイル設定
st.markdown("""
<style>
    body {
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
    }
    .main-header {
        text-align: center;
        color: #1f77b4;
        margin-bottom: 30px;
    }
</style>
""", unsafe_allow_html=True)

st.markdown("<h1 class='main-header'>💬 LLM チャットボット</h1>", unsafe_allow_html=True)

# サイドバー設定
with st.sidebar:
    st.header("⚙️ 設定")
    
    # モデル選択
    model = st.radio(
        "LLM モデルを選択:",
        ["gpt-4o", "gpt-4-turbo", "gpt-3.5-turbo"],
        index=0
    )
    
    # 温度設定（創造性）
    temperature = st.slider(
        "温度（創造性）:",
        min_value=0.0,
        max_value=2.0,
        value=0.7,
        step=0.1,
        help="高いほど創造的、低いほど一貫性がある"
    )
    
    # Max tokens
    max_tokens = st.slider(
        "Max Tokens:",
        min_value=100,
        max_value=4000,
        value=2000,
        step=100
    )
    
    st.divider()
    st.markdown("### ℹ️ 情報")
    st.markdown(f"**モデル:** {model}")
    st.markdown(f"**温度:** {temperature}")


# セッション状態の初期化
if "messages" not in st.session_state:
    st.session_state.messages = []

if "conversation_count" not in st.session_state:
    st.session_state.conversation_count = 0


# 会話ログを表示
def display_messages():
    """チャット履歴を表示"""
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])


# LLM に質問
def get_llm_response(user_message):
    """LLMからレスポンスを取得"""
    try:
        # メッセージを履歴に追加
        st.session_state.messages.append({
            "role": "user",
            "content": user_message
        })
        
        # APIを呼び出し
        response = client.chat.completions.create(
            model=model,
            messages=st.session_state.messages,
            temperature=temperature,
            max_tokens=max_tokens
        )
        
        # レスポンスを取得
        assistant_message = response.choices[0].message.content
        
        # 履歴に追加
        st.session_state.messages.append({
            "role": "assistant",
            "content": assistant_message
        })
        
        st.session_state.conversation_count += 1
        
        return assistant_message
    
    except Exception as e:
        error_message = f"❌ エラーが発生しました: {str(e)}"
        return error_message


# メイン UI
col1, col2 = st.columns([6, 1])

with col1:
    if st.session_state.messages:
        st.markdown("### 📋 会話履歴")
        display_messages()
    else:
        st.info("👋 こんにちは！何かお手伝いできることはございますか？")

with col2:
    if st.button("🗑️ リセット", use_container_width=True):
        st.session_state.messages = []
        st.session_state.conversation_count = 0
        st.rerun()


# チャット入力
st.divider()

# ユーザー入力
user_input = st.chat_input("メッセージを入力してください...")

if user_input:
    # ユーザーメッセージを表示
    with st.chat_message("user"):
        st.markdown(user_input)
    
    # LLM レスポンスを取得
    with st.spinner("🔄 応答を生成中..."):
        response = get_llm_response(user_input)
    
    # アシスタントメッセージを表示
    with st.chat_message("assistant"):
        st.markdown(response)


# フッター
st.divider()
col1, col2, col3 = st.columns(3)

with col1:
    st.metric("💬 会話数", st.session_state.conversation_count)

with col2:
    st.metric("📞 メッセージ数", len(st.session_state.messages))

with col3:
    st.markdown("<p style='text-align: center; color: gray; font-size: 12px;'>© 2026 LLM Chat App</p>", unsafe_allow_html=True)