#!/bin/bash

# Streamlit Cloud デプロイスクリプト
echo "🚀 Streamlit Cloud デプロイを開始します..."

# 必要な環境変数の確認
if [ -z "$STREAMLIT_USERNAME" ]; then
    echo "❌ STREAMLIT_USERNAME が設定されていません"
    echo "GitHub のユーザー名を設定してください"
    exit 1
fi

if [ -z "$STREAMLIT_APP_NAME" ]; then
    echo "❌ STREAMLIT_APP_NAME が設定されていません"
    echo "アプリ名を設定してください"
    exit 1
fi

echo "📋 デプロイ情報:"
echo "  ユーザー名: $STREAMLIT_USERNAME"
echo "  アプリ名: $STREAMLIT_APP_NAME"
echo "  リポジトリ: https://github.com/$STREAMLIT_USERNAME/$STREAMLIT_APP_NAME.git"

# デプロイURLの生成
DEPLOY_URL="https://$STREAMLIT_USERNAME-$STREAMLIT_APP_NAME.streamlit.app"

echo ""
echo "🔗 デプロイURL: $DEPLOY_URL"
echo ""
echo "📝 デプロイ手順:"
echo "1. ブラウザで https://streamlit.io/cloud を開く"
echo "2. 'New app' をクリック"
echo "3. 以下の情報を入力:"
echo "   - Repository: $STREAMLIT_USERNAME/$STREAMLIT_APP_NAME"
echo "   - Branch: main"
echo "   - Main file path: app.py"
echo "4. 'Advanced settings' を開く"
echo "5. 'Secrets' に以下を追加:"
echo "   OPENAI_API_KEY=sk-proj-...（あなたのAPIキー）"
echo "6. 'Deploy' をクリック"
echo ""
echo "✅ デプロイ準備完了！"