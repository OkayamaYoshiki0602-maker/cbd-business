# X API設定ガイド

## 📋 認証情報の設定手順

X Developer Portalで取得した認証情報を、プロジェクトに設定します。

---

## 🔐 必要な認証情報

X APIを使用するために、以下の認証情報が必要です：

1. **API Key** - Consumer Keys セクションから取得
2. **API Secret Key** - Consumer Keys セクションから取得
3. **Access Token** - Authentication Tokens セクションから取得 ✅
4. **Access Token Secret** - Authentication Tokens セクションから取得 ✅
5. **Bearer Token** - Authentication Tokens セクションから取得 ✅

---

## 📝 .envファイルの作成

### Step 1: テンプレートをコピー

```bash
cp config/env_template.txt .env
```

### Step 2: .envファイルを編集

`.env` ファイルを開いて、取得した認証情報を入力してください：

```env
# X (Twitter) API認証情報
X_API_KEY=your_api_key_here          # Consumer Keys から取得
X_API_SECRET_KEY=your_api_secret_key_here  # Consumer Keys から取得
X_ACCESS_TOKEN=1318210166580412416-XarwSysWdCAqnkL9O2n3qJr2eO3BJ3
X_ACCESS_TOKEN_SECRET=X4PgF4cN7wk0SWWmNnNy7ybN4uZFw1KxGNABf89ORfxnC
X_BEARER_TOKEN=AAAAAAAAAAAAAAAAAAAAADuO6wEAAAAAZEp6MT60uHerFb%2FRpXqrYAvRFe0%3DsX73VgKRUJ3Jk0FTT7u2K03Co7xqmNIBUJygqZwrJLzWw7iGe0

# LINE Messaging API認証情報（後で設定）
LINE_CHANNEL_ACCESS_TOKEN=your_channel_access_token_here
LINE_USER_ID=your_user_id_here

# WordPress設定（任意）
WORDPRESS_URL=https://cbd-no-hito.com
WORDPRESS_USERNAME=your_username
WORDPRESS_APP_PASSWORD=your_app_password
```

### Step 3: API Key と API Secret Key を取得

X Developer Portalの「Keys and tokens」タブで：

1. **Consumer Keys** セクションを確認
2. **API Key** をコピー（現在は "****rgJtr8" のように一部のみ表示されている可能性があります）
3. **API Secret Key** を表示するには、シークレットを表示するボタンをクリック
4. 両方を `.env` ファイルに入力

---

## ⚠️ 重要：セキュリティ

### .envファイルは絶対にGitにコミットしない

`.gitignore` ファイルに `.env` が含まれていることを確認してください。

確認方法：
```bash
cat .gitignore | grep .env
```

`.env` が表示されればOKです。

---

## 🚀 次のステップ

### 1. 依存関係のインストール

```bash
cd automation
pip3 install -r requirements.txt
```

### 2. 基本的なテスト

```bash
# ユーザー情報取得テスト
python3 automation/social_media/x_twitter.py user me

# テストツイート投稿（慎重に！）
python3 automation/social_media/x_twitter.py tweet "テストツイートです"
```

---

## 🔍 API Key と API Secret Key の取得方法

X Developer Portalで：

1. 「Projects & Apps」→ プロジェクトを選択
2. 「Keys and tokens」タブを開く
3. **Consumer Keys** セクションで：
   - **API Key** をコピー
   - **API Secret Key** を表示（シークレットを表示ボタンをクリック）
4. 両方を `.env` ファイルに入力

---

## 📝 設定確認チェックリスト

- [ ] `.env` ファイルを作成
- [ ] `X_API_KEY` を設定
- [ ] `X_API_SECRET_KEY` を設定
- [ ] `X_ACCESS_TOKEN` を設定 ✅
- [ ] `X_ACCESS_TOKEN_SECRET` を設定 ✅
- [ ] `X_BEARER_TOKEN` を設定 ✅
- [ ] `.gitignore` に `.env` が含まれていることを確認
- [ ] 依存関係をインストール
- [ ] テスト実行

---

## 🆘 トラブルシューティング

### エラー: "X API認証情報が設定されていません"

**原因:** `.env` ファイルが正しく読み込まれていない

**解決方法:**
1. `.env` ファイルがプロジェクトルートに存在することを確認
2. 環境変数の名前が正しいことを確認（大文字小文字を含む）
3. `.env` ファイルに余分な空白や改行がないことを確認

### エラー: "Could not authenticate you"

**原因:** 認証情報が間違っている

**解決方法:**
1. X Developer Portalで認証情報を再確認
2. API Key と API Secret Key が正しいことを確認
3. Access Token と Access Token Secret が正しいことを確認

---

## 💡 次のステップ

設定が完了したら、以下を実行してください：

1. **依存関係のインストール**
2. **基本的なテスト実行**
3. **LINE Messaging API の設定**（後で）
