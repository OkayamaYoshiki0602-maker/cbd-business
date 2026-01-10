# LINE Channel Access Token 取得ガイド

## 📋 概要

LINE Messaging API でメッセージを送信するには、**Channel Access Token** が必要です。

---

## 🔐 Channel Access Token の取得方法

### Step 1: LINE Developers コンソールにアクセス

1. LINE Developers にアクセス: https://developers.line.biz/
2. ログイン
3. プロバイダー「CBD WORLD」を選択

### Step 2: チャネルを選択

1. 「Channels」タブまたは「チャネル」セクションを開く
2. 「CBD Auto Tweet」チャネルを選択

### Step 3: Messaging API タブを開く

1. チャネルを選択後、「Messaging API」タブを開く
2. または、「Settings」→「Messaging API」を開く

### Step 4: Channel Access Token を取得

1. **「Channel access token」セクション**を探す
2. **「Issue」または「発行」ボタン**をクリック
3. Channel access token が表示される
4. **コピーして保存**（一度しか表示されません）

---

## 📝 現在取得済みの情報

✅ **Channel ID:** 2008863419
✅ **Channel Secret:** 615da785c3f141e9e02f312c9458aa49
⏳ **Channel Access Token:** 取得待ち

---

## 🔍 Channel Access Token が見つからない場合

### 確認すべき場所

1. **LINE Developers コンソール**
   - プロバイダー「CBD WORLD」→ チャネル「CBD Auto Tweet」→「Messaging API」タブ
   - 「Channel access token」セクション

2. **LINE Official Account Manager**
   - 「設定」→「Messaging API」セクション
   - 「Channel Access Token」セクション

### 見つからない場合

- 「Issue」または「発行」ボタンが表示されない場合、既に発行済みの可能性があります
- その場合は、「Reissue」または「再発行」ボタンをクリック
- **注意:** 再発行すると、既存のトークンが無効になります

---

## 📋 Webhook URL の設定方法

### Webhook URL とは？

Webhook URL は、LINEからメッセージイベントを受け取るためのURLです。

### 今回の用途（通知機能のみ）の場合

**Webhook URL は設定不要です。**

- 今回の用途: **一方向の通知送信のみ**（LINEからメッセージを送信）
- ユーザーからのメッセージを受け取る必要がないため、Webhook URL は不要

### 将来的にメッセージを受け取る場合

Webhook URL を設定する必要があります。

#### 設定方法

1. LINE Developers コンソールで「Messaging API」タブを開く
2. 「Webhook URL」セクションを探す
3. Webhook URL を入力：
   ```
   https://your-server.com/webhook
   ```
4. 「Verify」または「検証」ボタンをクリック
5. 検証成功後、「Save」または「保存」ボタンをクリック

#### Webhook URL の要件

- **HTTPS必須**
- パブリックにアクセス可能なURL
- LINEからの検証リクエストに応答できるサーバーが必要

#### ローカル開発の場合

- **ngrok** などのトンネリングサービスを使用
- または、クラウドサーバーを使用（Heroku、AWS Lambdaなど）

---

## 💡 今回の推奨設定

### Webhook URL の設定

**今回の用途では、Webhook URL は設定しなくてOKです。**

- ✅ 通知送信のみ使用する場合: Webhook URL 不要
- ❌ ユーザーからのメッセージを受け取る場合: Webhook URL 必要

### 今後の設定（オプション）

将来的にユーザーからのメッセージを受け取る場合：

1. サーバーを準備（HTTPS必須）
2. Webhook URL を設定
3. Webhookイベントハンドラーを実装

---

## 🚀 次のステップ

### Step 1: Channel Access Token を取得

1. LINE Developers コンソールで「Messaging API」タブを開く
2. 「Channel access token」セクションで「Issue」をクリック
3. Channel Access Token をコピー

### Step 2: .envファイルに設定

取得したChannel Access Token を`.env`ファイルに設定：

```env
# LINE Messaging API認証情報
LINE_CHANNEL_ACCESS_TOKEN=取得したChannel_Access_Token_をここに貼り付け
LINE_USER_ID=自分のLINE_User_ID_（オプション・後で設定可）
```

### Step 3: テスト実行

```bash
# LINE通知送信テスト
python3 automation/social_media/line_notify.py send "テストメッセージです 📱"
```

---

## 📝 設定確認チェックリスト

- [ ] Channel ID: 2008863419 ✅
- [ ] Channel Secret: 615da785c3f141e9e02f312c9458aa49 ✅
- [ ] Channel Access Token: 取得待ち
- [ ] .envファイルに`LINE_CHANNEL_ACCESS_TOKEN`を設定
- [ ] .envファイルを保存
- [ ] テスト実行

---

## 🔍 Channel Access Token の場所（詳細）

### LINE Developers コンソール経由

1. https://developers.line.biz/ にアクセス
2. 「Providers」→「CBD WORLD」を選択
3. 「Channels」→「CBD Auto Tweet」を選択
4. 「Messaging API」タブを開く
5. 「Channel access token」セクションで「Issue」をクリック

### LINE Official Account Manager経由

1. https://manager.line.biz/ にアクセス
2. 「CBD WORLD」を選択
3. 「設定」タブを開く
4. 「Messaging API」を選択
5. 「Channel Access Token」セクションで「発行」をクリック

---

Channel Access Token を取得したら、お知らせください。`.env`ファイルに設定してテストを実行します！
