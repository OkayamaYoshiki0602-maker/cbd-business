# LINE Messaging API 設定ガイド

## 📋 目的

X自動ツイート機能と連携して、以下の機能を実現：
1. ツイート投稿前のプレビューをLINEで確認
2. ツイート投稿結果をLINEで通知

---

## 🔐 LINE Developers での設定

### Step 1: LINE Developers にアクセス

1. LINE Developers にアクセス: https://developers.line.biz/
2. ログイン（LINEアカウントでログイン）

### Step 2: プロバイダー作成（まだの場合）

1. 「プロバイダー」タブを開く
2. 「新規作成」をクリック
3. プロバイダー名を入力（例: "CBD Auto Tweet"）
4. 「作成」をクリック

### Step 3: Messaging API チャネル作成

1. プロバイダーを選択
2. 「チャネルを追加」をクリック
3. 「Messaging API」を選択
4. チャネル情報を入力：
   - チャネル名: "CBD Auto Tweet"
   - チャネル説明: "CBDサイト運営の自動化システム"
   - 大業種: 「個人」
   - 小業種: 「個人（その他）」
5. 「作成」をクリック
6. 「利用規約」に同意

### Step 4: Channel Access Token を取得

**重要:** Channel Access Token は **LINE Developers コンソール** で取得します。

#### 方法A: LINE Developers コンソール経由（推奨）

1. LINE Developers にアクセス: https://developers.line.biz/
2. プロバイダー「CBD WORLD」を選択
3. チャネル「CBD Auto Tweet」を選択
4. **「Messaging API」タブを開く**
5. **「Channel access token」セクションで「Issue」または「発行」ボタンをクリック**
6. Channel access token が表示される
7. **コピーして保存**（一度しか表示されません）

#### 方法B: LINE Official Account Manager経由

1. LINE Official Account Manager にアクセス: https://manager.line.biz/
2. 「CBD WORLD」を選択
3. 「設定」タブを開く
4. 「Messaging API」を選択
5. **「Channel Access Token」セクションで「発行」ボタンをクリック**
6. Channel access token が表示される
7. **コピーして保存**（一度しか表示されません）

### Step 4-1: Channel Access Token が見つからない場合

- 「Issue」または「発行」ボタンが表示されない場合、既に発行済みの可能性があります
- その場合は、「Reissue」または「再発行」ボタンをクリック
- **注意:** 再発行すると、既存のトークンが無効になります

### Step 5: ユーザーIDの取得（オプション）

LINE通知を特定のユーザーに送信する場合：

1. LINE Developers で「Messaging API」タブを開く
2. 「QRコード」を開く
3. 自分のスマートフォンでQRコードをスキャン
4. 友達追加する
5. LINEアプリで自分のユーザーIDを確認するか、Webhookで確認

**簡単な方法:**
- LINEアプリで「友達追加」→ チャネルを追加
- チャネルにメッセージを送信
- Webhookで受信したイベントからユーザーIDを取得

**または:**
- 一時的にWebhookを有効化して、自分にメッセージを送信したときにユーザーIDを取得

---

## 📝 .envファイルへの設定

`.env`ファイルに以下を追加：

```env
# LINE Messaging API認証情報
LINE_CHANNEL_ACCESS_TOKEN=取得したChannel_Access_Token_をここに貼り付け
LINE_USER_ID=自分のLINE_User_ID_（オプション）
```

---

## 🧪 テスト方法

### Step 1: 基本テスト

```bash
# LINE通知送信テスト
python3 automation/social_media/line_notify.py send "テストメッセージです"
```

### Step 2: ツイートプレビューテスト

```bash
# ツイート投稿前プレビュー送信
python3 automation/social_media/line_notify.py preview "テストツイート内容"
```

---

## 🔧 LINE Messaging API の制限

### 送信方法

**方法1: Push Message（推奨）**
- 特定のユーザーIDに送信
- `LINE_USER_ID` が必要

**方法2: Broadcast Message**
- すべての友だちに送信
- ユーザーID不要
- 注意: すべての友だちに送信される

### レート制限

- **Push Message:** 200件/秒
- **Broadcast Message:** 1,000件/秒
- ただし、無料プランには制限がある可能性

---

## 🚀 実装内容

### 機能

1. **ツイート投稿前プレビュー送信**
   - ツイート内容をLINEで確認
   - 投稿前に人間が確認できる

2. **ツイート投稿結果通知**
   - 投稿成功/失敗をLINEで通知
   - ツイートURLも送信

3. **エラー通知**
   - APIエラーが発生した場合、LINEで通知

---

## ⚠️ 注意事項

### Channel Access Token

- Channel Access Tokenは一度しか表示されません
- 失った場合は、再生成が必要です
- 再生成すると、既存のトークンは無効になります

### Webhook設定（オプション）

- Webhookは必須ではありません（一方向の通知のみの場合）
- ユーザーからのメッセージを受け取る場合は、Webhook設定が必要
- 今回は投稿前確認のみなので、Webhookは不要

---

## 📝 設定確認チェックリスト

- [ ] LINE Developers アカウント作成
- [ ] プロバイダー作成
- [ ] Messaging API チャネル作成
- [ ] Channel Access Token 取得
- [ ] LINE_USER_ID 取得（オプション）
- [ ] .envファイルに設定
- [ ] テスト実行

---

## 🆘 トラブルシューティング

### エラー: "Invalid access token"

**原因:** Channel Access Token が正しくない

**解決方法:**
1. LINE Developers で Channel Access Token を再確認
2. .envファイルの`LINE_CHANNEL_ACCESS_TOKEN`が正しいことを確認
3. トークンに余分な空白がないことを確認

### エラー: "Invalid user ID"

**原因:** LINE_USER_ID が正しくない

**解決方法:**
1. LINE_USER_ID を再確認
2. 友達追加が完了していることを確認
3. または、Broadcast Message を使用（LINE_USER_ID 不要）

---

## 💡 次のステップ

設定が完了したら、以下をテスト：

1. **基本通知テスト**
   ```bash
   python3 automation/social_media/line_notify.py send "テストメッセージ"
   ```

2. **ツイートプレビューテスト**
   ```bash
   python3 automation/social_media/line_notify.py preview "テストツイート内容"
   ```

3. **X自動ツイートとの統合**（次のステップ）
