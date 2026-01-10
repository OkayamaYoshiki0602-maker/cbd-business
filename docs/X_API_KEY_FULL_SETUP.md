# X API Key 完全取得ガイド

## 📋 API Key と API Secret Key の取得方法

API Key が "****rgJtr8" のように一部のみ表示されている場合の対処法です。

---

## 🔍 完全なAPI Keyを取得する方法

### 方法1: Regenerate（再生成）ボタンを使用

1. **Consumer Keys** セクションで「Regenerate」ボタンをクリック
2. 確認ダイアログで「OK」をクリック
3. **再生成されたAPI KeyとAPI Secret Keyが完全に表示されます**
4. 両方をコピーして`.env`ファイルに貼り付け

⚠️ **注意:** 再生成すると、既存のAccess Tokenが無効になる可能性があります。その場合は、Access Tokenも再生成が必要です。

### 方法2: 既存のキーを確認

1. **Consumer Keys** セクションで「API Key」の右側を確認
2. 「View」や「表示」ボタンがあればクリック
3. 完全なAPI Keyが表示される

---

## 🔐 API Secret Key の取得方法

1. **Consumer Keys** セクションで「API Secret Key」の下を確認
2. **「Reveal」または「シークレットを表示」ボタンをクリック**
3. 完全なAPI Secret Keyが表示されます
4. コピーして`.env`ファイルに貼り付け

⚠️ **重要:** API Secret Keyは一度しか表示されない場合があります。必ずコピーして保存してください。

---

## 📝 推奨手順

### Step 1: Consumer Keysを再生成

1. X Developer Portal で「Keys and tokens」タブを開く
2. **Consumer Keys** セクションで「Regenerate」ボタンをクリック
3. 確認ダイアログで「OK」をクリック
4. 新しい**API Key**と**API Secret Key**が完全に表示されます
5. 両方をコピー

### Step 2: Access Tokenも再生成（必要に応じて）

Access Tokenが無効になった場合：

1. **Authentication Tokens** セクションで「Access Token and Secret」の「Generate」ボタンをクリック
2. 新しいAccess TokenとAccess Token Secretが表示されます
3. 両方をコピー

### Step 3: .envファイルに設定

`.env`ファイルに以下のように設定：

```env
X_API_KEY=新しい完全なAPI_Key_をここに貼り付け
X_API_SECRET_KEY=新しい完全なAPI_Secret_Key_をここに貼り付け
X_ACCESS_TOKEN=新しいAccess_Token_（再生成した場合）
X_ACCESS_TOKEN_SECRET=新しいAccess_Token_Secret_（再生成した場合）
X_BEARER_TOKEN=AAAAAAAAAAAAAAAAAAAAADuO6wEAAAAAZEp6MT60uHerFb%2FRpXqrYAvRFe0%3DsX73VgKRUJ3Jk0FTT7u2K03Co7xqmNIBUJygqZwrJLzWw7iGe0
```

---

## ⚙️ アプリ設定の確認

画像から確認できる設定について：

### ✅ 正しい設定（確認済み）

- **App permissions:** "Read and write and Direct message" が選択されている ✅
  - これは正しい設定です。ツイート投稿には「Read and write」以上が必要です。

### ⚠️ 変更が必要な可能性がある設定

- **Type of App:** "Native App" が選択されている
  - **推奨:** "Web App, Automated App or Bot" に変更することを推奨します
  - 理由: サーバーサイドで実行する自動化スクリプトには「Web App」の方が適しています

### App Info設定（任意）

以下の設定も行うことを推奨：

- **Website URL:** `https://cbd-no-hito.com`
- **Callback URI / Redirect URL:** `http://localhost:3000/callback`（開発用）
- **Organization name:** 任意（例: "CBD WORLD"）
- **Organization URL:** `https://cbd-no-hito.com`

---

## 🚀 設定変更手順

### Type of App を変更する場合

1. 「Settings」タブを開く
2. 「User authentication settings」セクションで「Edit」をクリック
3. **Type of App** で「Web App, Automated App or Bot」を選択
4. 「Save」をクリック

---

## 📝 最終確認

設定が完了したら、以下の情報を`.env`ファイルに設定：

- ✅ API Key（完全版）
- ✅ API Secret Key（完全版）
- ✅ Access Token（再生成した場合）
- ✅ Access Token Secret（再生成した場合）
- ✅ Bearer Token（既に取得済み）

---

## 🧪 テスト実行

設定が完了したら、以下でテスト：

```bash
python3 automation/social_media/x_twitter.py user me
```

成功すれば、設定は完了です！
