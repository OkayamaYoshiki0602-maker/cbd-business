# X API認証情報設定完了ガイド

## 📋 .envファイルへの設定

`.env`ファイルを開いて、以下の認証情報を設定してください。

---

## 🔐 設定内容

```env
# X (Twitter) API認証情報
X_API_KEY=vvm4zJSdUvYbRmPqsfIHi8bXy
X_API_SECRET_KEY=NpGMrYZEFPpVsD2jEGM5IkwGpwdYG4Hgs8TKOkFiKXR7Jp8Itb
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

---

## 📝 設定手順

### Step 1: .envファイルを開く

プロジェクトルート（`/Users/okayamayoshiki/Library/CloudStorage/GoogleDrive-okayamayoshiki0602o@gmail.com/マイドライブ/cursor`）にある`.env`ファイルをエディタで開いてください。

### Step 2: 認証情報を設定

上記の内容を`.env`ファイルに貼り付けてください。

特に以下の4行を必ず設定：
- `X_API_KEY=vvm4zJSdUvYbRmPqsfIHi8bXy`
- `X_API_SECRET_KEY=NpGMrYZEFPpVsD2jEGM5IkwGpwdYG4Hgs8TKOkFiKXR7Jp8Itb`
- `X_ACCESS_TOKEN=1318210166580412416-XarwSysWdCAqnkL9O2n3qJr2eO3BJ3`
- `X_ACCESS_TOKEN_SECRET=X4PgF4cN7wk0SWWmNnNy7ybN4uZFw1KxGNABf89ORfxnC`
- `X_BEARER_TOKEN=AAAAAAAAAAAAAAAAAAAAADuO6wEAAAAAZEp6MT60uHerFb%2FRpXqrYAvRFe0%3DsX73VgKRUJ3Jk0FTT7u2K03Co7xqmNIBUJygqZwrJLzWw7iGe0`

### Step 3: ファイルを保存

`.env`ファイルを保存してください。

---

## 🧪 テスト実行

設定が完了したら、以下でテストしてください：

### 1. ユーザー情報取得テスト

```bash
python3 automation/social_media/x_twitter.py user me
```

**期待される結果:**
```
✅ ユーザー情報を取得しました: @yo_nandakanda

ユーザー名: @yo_nandakanda
表示名: [表示名]
ID: [ユーザーID]
```

### 2. ツイート投稿テスト（オプション）

⚠️ **注意:** これは実際にツイートが投稿されます。テストする場合は慎重に！

```bash
python3 automation/social_media/x_twitter.py tweet "テストツイートです 🧪"
```

**期待される結果:**
```
✅ ツイートを投稿しました: [ツイートID]
ツイート内容: テストツイートです 🧪...

ツイートID: [ツイートID]
ツイートURL: https://twitter.com/user/status/[ツイートID]
```

---

## ✅ 設定確認チェックリスト

- [ ] `.env`ファイルに`X_API_KEY`を設定
- [ ] `.env`ファイルに`X_API_SECRET_KEY`を設定
- [ ] `.env`ファイルに`X_ACCESS_TOKEN`を設定
- [ ] `.env`ファイルに`X_ACCESS_TOKEN_SECRET`を設定
- [ ] `.env`ファイルに`X_BEARER_TOKEN`を設定
- [ ] `.env`ファイルを保存
- [ ] ユーザー情報取得テストを実行
- [ ] テストが成功したことを確認

---

## 🆘 トラブルシューティング

### エラー: "X API認証情報が設定されていません"

**原因:** `.env`ファイルが正しく読み込まれていない

**解決方法:**
1. `.env`ファイルがプロジェクトルートに存在することを確認
2. 環境変数の名前が正しいことを確認（大文字小文字を含む）
3. `.env`ファイルに余分な空白や改行がないことを確認
4. `.env`ファイルが保存されていることを確認

### エラー: "Could not authenticate you"

**原因:** 認証情報が間違っている

**解決方法:**
1. X Developer Portalで認証情報を再確認
2. `.env`ファイルの値を再確認（コピー&ペーストの際に余分な空白が入っていないか）
3. Access TokenとAccess Token Secretが正しいことを確認

### エラー: "ModuleNotFoundError: No module named 'tweepy'"

**原因:** 依存関係がインストールされていない

**解決方法:**
```bash
cd automation
pip3 install -r requirements.txt
```

---

## 🚀 次のステップ

設定が完了してテストが成功したら：

1. **LINE通知連携の設定**（次のステップ）
2. **WordPress記事更新検知機能の実装**（Phase 2）
3. **スケジュール投稿機能の実装**（Phase 2）

---

設定が完了したら、テストを実行してください！
