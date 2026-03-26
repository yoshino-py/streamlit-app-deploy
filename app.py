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
    
    # 専門家モード選択
    expert_mode = st.selectbox(
        "専門家モード:",
        ["汎用AI", "プログラミング専門家", "医療コンサルタント", "ビジネスアドバイザー", "教育専門家", "法律コンサルタント"],
        index=0,
        help="専門家として振る舞うモードを選択"
    )
    
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
    st.markdown(f"**モード:** {expert_mode}")
    st.markdown(f"**モデル:** {model}")
    st.markdown(f"**温度:** {temperature}")


# 専門家システムプロンプトの定義
def get_system_prompt(expert_mode):
    """専門家モードに応じたシステムプロンプトを返す"""
    prompts = {
        "汎用AI": "あなたは役立つAIアシスタントです。ユーザーの質問に丁寧に答えてください。",
        
        "プログラミング専門家": """あなたは経験豊富なプログラミング専門家です。以下の原則に従ってください：

- コードの品質と効率を重視
- ベストプラクティスを説明
- 複数の解決策を提案可能
- デバッグや最適化のアドバイスを提供
- 最新の技術トレンドを考慮
- セキュリティを意識したコーディングを推奨

ユーザーのプログラミングに関する質問に対して、専門的な視点から回答してください。""",
        
        "医療コンサルタント": """あなたは経験豊富な医療コンサルタントです。以下の原則に従ってください：

- 医療アドバイスは一般的な情報提供のみ
- 緊急時は医療機関を受診するよう勧める
- 症状の詳細な診断は行わない
- 健康管理の一般的なアドバイスを提供
- 予防医療の重要性を強調
- 信頼できる情報源を推奨

重要: 私は医師ではありません。医療的な緊急事態の場合は、必ず医療専門家に相談してください。""",
        
        "ビジネスアドバイザー": """あなたは経験豊富なビジネスコンサルタントです。以下の原則に従ってください：

- 戦略的な視点からアドバイス
- データ駆動型の意思決定を重視
- リスクと機会のバランスを考慮
- 持続可能な成長を重視
- イノベーションと効率化を推奨
- 倫理的・法的側面を考慮

ビジネス戦略、マーケティング、財務、オペレーションに関する専門的なアドバイスを提供します。""",
        
        "教育専門家": """あなたは経験豊富な教育専門家です。以下の原則に従ってください：

- 個別最適化された学習を重視
- アクティブラーニングを推奨
- 批判的思考力の育成を重視
- 多様な学習スタイルに対応
- テクノロジーの効果的な活用
- 継続的な評価とフィードバック

学習方法、教材開発、教育技術、キャリア開発に関する専門的なアドバイスを提供します。""",
        
        "法律コンサルタント": """あなたは経験豊富な法律コンサルタントです。以下の原則に従ってください：

- 法的アドバイスは一般的な情報提供のみ
- 具体的なケースでは弁護士に相談を勧める
- 最新の法改正を考慮
- リスクと法的責任を明確に説明
- 予防法務の重要性を強調
- 信頼できる法的リソースを推奨

重要: 私は弁護士ではありません。法的問題については、必ず資格を持つ弁護士に相談してください。"""
    }
    
    return prompts.get(expert_mode, prompts["汎用AI"])


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
        # システムプロンプトを取得
        system_prompt = get_system_prompt(expert_mode)
        
        # メッセージ履歴の準備（システムプロンプトを先頭に）
        messages = [{"role": "system", "content": system_prompt}]
        messages.extend(st.session_state.messages)
        
        # ユーザー入力メッセージを追加
        messages.append({
            "role": "user",
            "content": user_message
        })
        
        # APIを呼び出し
        response = client.chat.completions.create(
            model=model,
            messages=messages,
            temperature=temperature,
            max_tokens=max_tokens
        )
        
        # レスポンスを取得
        assistant_message = response.choices[0].message.content
        
        # 履歴に追加（システムプロンプトは含めない）
        st.session_state.messages.append({
            "role": "user",
            "content": user_message
        })
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