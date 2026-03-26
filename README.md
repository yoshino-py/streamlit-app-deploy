# 💬 専門家AIチャットボット

StreamlitとOpenAI GPT-4oを使用した専門家モード搭載の高度なチャットボットアプリケーションです。

## 🚀 機能

- **専門家モード**: 6つの専門分野で専門家として振る舞う
  - 🧠 汎用AI（デフォルト）
  - 💻 プログラミング専門家
  - 🏥 医療コンサルタント
  - 💼 ビジネスアドバイザー
  - 🎓 教育専門家
  - ⚖️ 法律コンサルタント

- **GPT-4o統合**: 最新のOpenAI LLMモデルを使用
- **リアルタイム応答**: ストリーミング対応で即座に結果表示
- **カスタマイズ可能な設定**:
  - モデル選択（GPT-4o、GPT-4 Turbo、GPT-3.5 Turbo）
  - 温度（創造性）調整
  - Max Tokens決定
- **会話管理**: 会話履歴の追跡とリセット機能

## 📋 システム要件

- Python 3.8+
- OpenAI APIキー

## 🔧 セットアップ

### 1. リポジトリのクローン
```bash
git clone https://github.com/yoshino-py/streamlit-app-deploy.git
cd streamlit-app-deploy
```

### 2. 仮想環境の作成
```bash
python -m venv env
```

### 3. 仮想環境の有効化

**Windows:**
```bash
env\Scripts\activate.bat
```

**macOS/Linux:**
```bash
source env/bin/activate
```

### 4. パッケージのインストール
```bash
pip install -r requirements.txt
```

### 5. 環境変数の設定

`.env`ファイルを作成し、OpenAI APIキーを追加：
```
OPENAI_API_KEY=sk-proj-...（あなたのAPIキー）
```

## 🏃 実行方法

### ローカルで実行
```bash
streamlit run app.py
```

ブラウザで http://localhost:8501 を開いてアプリにアクセスできます。

### デプロイ（Streamlit Cloud）

#### 自動デプロイスクリプトを使用
```bash
# 環境変数を設定
export STREAMLIT_USERNAME="your-github-username"
export STREAMLIT_APP_NAME="streamlit-app-deploy"

# デプロイスクリプト実行
bash deploy.sh
```

#### 手動デプロイ
1. **Streamlit Cloud にアクセス**
   - [https://streamlit.io/cloud](https://streamlit.io/cloud) を開く

2. **GitHub リポジトリを接続**
   - 「New app」をクリック
   - リポジトリ：`yoshino-py/streamlit-app-deploy`
   - ブランチ：`main`
   - ファイル：`app.py`

3. **環境変数を設定**
   - 「Advanced settings」→「Secrets」
   - 以下を追加：
   ```
   OPENAI_API_KEY=sk-proj-...（あなたのAPIキー）
   ```

4. **デプロイ**
   - 「Deploy」をクリック
   - 数分で自動的にデプロイされます

## 📊 専門家モードの詳細

### 🧠 汎用AI
- 一般的な質問にバランスよく回答
- 幅広いトピックに対応

### 💻 プログラミング専門家
- コード品質と効率を重視
- ベストプラクティスを説明
- デバッグ・最適化アドバイス
- 最新技術トレンドを考慮

### 🏥 医療コンサルタント
- 一般的な健康管理アドバイス
- 予防医療の重要性を強調
- **注意**: 診断・治療は行わず、医療機関受診を推奨

### 💼 ビジネスアドバイザー
- 戦略的な視点からアドバイス
- データ駆動型の意思決定
- 持続可能な成長を重視

### 🎓 教育専門家
- 個別最適化された学習方法
- アクティブラーニングを推奨
- テクノロジーの効果的な活用

### ⚖️ 法律コンサルタント
- 一般的な法的情報提供
- リスクと法的責任の説明
- **注意**: 具体的な法的問題は弁護士相談を推奨

## ⚙️ 設定

### サイドバーで以下をカスタマイズ可能：

| 設定項目 | デフォルト | 範囲 |
|---------|----------|------|
| 専門家モード | 汎用AI | 6つの専門分野 |
| モデル | gpt-4o | gpt-4o, gpt-4-turbo, gpt-3.5-turbo |
| 温度 | 0.7 | 0.0 - 2.0 |
| Max Tokens | 2000 | 100 - 4000 |

## 📊 API コスト

- **GPT-4o**: 入力 $5/1M tokens、出力 $15/1M tokens
- **GPT-4 Turbo**: 入力 $10/1M tokens、出力 $30/1M tokens
- **GPT-3.5 Turbo**: 入力 $0.5/1M tokens、出力 $1.5/1M tokens

## 🐛 トラブルシューティング

### APIキーエラー
```
Error: Invalid API key
```
→ `.env`ファイルの`OPENAI_API_KEY`が正しく設定されているか確認

### モジュールが見つからない
```
ModuleNotFoundError: No module named 'openai'
```
→ `pip install -r requirements.txt`を実行

### 接続タイムアウト
→ インターネット接続を確認し、OpenAI APIが利用可能か確認

### 専門家モードが反映されない
→ ページをリロードするか、会話をリセットしてください

## 📝 ログ

アプリケーションは以下のログを記録します:
- API呼び出し
- エラーメッセージ
- 会話統計

## 🤝 貢献

プルリクエストを歓迎します。大きな変更の場合は、まずissueを開いて変更内容を議論してください。

## 📄 ライセンス

このプロジェクトはMITライセンスの下で公開されています。

## 📞 サポート

問題が発生した場合は、GitHubのissueセクションで報告してください。

---

**作成日**: 2026年3月26日  
**最終更新**: 2026年3月26日
