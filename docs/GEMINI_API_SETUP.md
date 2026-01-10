# Gemini API設定ガイド

## 📋 概要

既にGeminiに課金している場合、Gemini APIを使用してニュース要約を行います。

---

## 🔐 Gemini API キーの取得方法

### Step 1: Google AI Studio にアクセス

1. Google AI Studio にアクセス: https://aistudio.google.com/
2. Googleアカウントでログイン（okayamayoshiki0602o@gmail.com）

### Step 2: APIキーを取得

1. 「Get API key」または「APIキーを取得」をクリック
2. 既存のプロジェクトを選択、または新規プロジェクトを作成
3. APIキーが表示される
4. **コピーして保存**

### Step 3: .envファイルに設定

`.env`ファイルに以下を設定：

```env
AI_SUMMARIZER=gemini
GEMINI_API_KEY=取得したGemini_API_キー_をここに貼り付け
```

---

## 🚀 使用方法

### 1. 依存関係のインストール

```bash
pip3 install google-generativeai
```

### 2. テスト実行

```bash
# ニュース要約テスト
python3 automation/social_media/news_summarizer.py summarize "ニュース本文..." 200 gemini
```

---

## 📊 Gemini APIの料金

### 無料枠

- **60リクエスト/分**（無料）
- 月間制限あり

### 有料プラン

- 既に課金済みのプランを使用
- 料金: $0.0005 / 1K characters（入力+出力）

---

## 💡 Gemini APIの特徴

### メリット

- ✅ **日本語に強い**
- ✅ 既に課金済み（追加コストなし）
- ✅ 無料枠あり（60リクエスト/分）
- ✅ コスト効率が良い

### デメリット

- ⚠️ 無料枠に制限あり（既に課金済みの場合は問題なし）

---

## 📝 設定例

### .envファイル

```env
# AI要約設定
AI_SUMMARIZER=gemini
GEMINI_API_KEY=your_gemini_api_key_here
```

---

## 🧪 テスト実行

設定が完了したら、以下でテスト：

```bash
# ニュース要約テスト
python3 automation/social_media/news_summarizer.py summarize "テストニュース本文です。CBDに関する最新情報をお届けします。" 200 gemini
```

**期待される結果:**
```
📝 ニュースを要約しています... (最大200文字, AI: gemini)

============================================================
要約結果:
============================================================
テストニュース本文です。CBDに関する最新情報をお届けします。

文字数: 30/200
```

---

## ⚠️ トラブルシューティング

### エラー: "GEMINI_API_KEYが設定されていません"

**解決方法:**
1. `.env`ファイルに`GEMINI_API_KEY`が設定されているか確認
2. APIキーが正しいか確認

### エラー: "google-generativeaiライブラリがインストールされていません"

**解決方法:**
```bash
pip3 install google-generativeai
```

---

## 🎯 次のステップ

1. **Gemini APIキーを取得**
2. **.envファイルに設定**
3. **テスト実行**
4. **朝7時の定期実行に統合**

---

詳細は `docs/GEMINI_API_SETUP.md` を参照してください。

Gemini APIキーを取得したら、`.env`ファイルに設定してください。テストを実行します！
