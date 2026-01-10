# LINE Webhook URL 設定ガイド

## 📋 概要

Webhook URL は、LINEからメッセージイベントを受け取るためのURLです。

---

## 💡 今回の用途では不要

### 通知機能のみの場合

**Webhook URL は設定不要です。**

**理由:**
- 今回の用途: **一方向の通知送信のみ**（LINEからメッセージを送信）
- ユーザーからのメッセージを受け取る必要がない
- 自動リプライ機能を使用しない

### Webhook URL が必要な場合

以下の機能を使用する場合、Webhook URL が必要です：

- ✅ ユーザーからのメッセージを受け取る
- ✅ 自動リプライ機能
- ✅ メッセージイベントに基づいた処理

---

## 🔧 Webhook URL の設定方法（将来的に）

将来的にユーザーからのメッセージを受け取る場合の設定方法です。

### Step 1: Webhook URL を準備

Webhook URL は以下の要件を満たす必要があります：

- ✅ **HTTPS必須**（HTTPは不可）
- ✅ パブリックにアクセス可能なURL
- ✅ LINEからの検証リクエストに応答できるサーバー

### Step 2: Webhookエンドポイントを実装

サーバー側でWebhookイベントを受け取るエンドポイントを実装：

```python
# 例: Flaskを使用
from flask import Flask, request, abort
import hmac
import hashlib
import json

app = Flask(__name__)

LINE_CHANNEL_SECRET = '615da785c3f141e9e02f312c9458aa49'

@app.route('/webhook', methods=['POST'])
def webhook():
    # 署名検証
    signature = request.headers.get('X-Line-Signature', '')
    body = request.get_data(as_text=True)
    
    # 署名を検証
    hash = hmac.new(
        LINE_CHANNEL_SECRET.encode('utf-8'),
        body.encode('utf-8'),
        hashlib.sha256
    ).hexdigest()
    
    if signature != hash:
        abort(400)
    
    # イベントを処理
    events = json.loads(body).get('events', [])
    for event in events:
        # メッセージイベントを処理
        if event['type'] == 'message':
            # メッセージを処理
            pass
    
    return 'OK'
```

### Step 3: ローカル開発の場合（ngrok）

ローカルで開発する場合、ngrokなどのトンネリングサービスを使用：

```bash
# ngrokをインストール（Homebrew）
brew install ngrok

# トンネルを作成（ポート5000で実行）
ngrok http 5000
```

ngrokが生成するURL（例: `https://xxxxx.ngrok.io`）を使用：

```
Webhook URL: https://xxxxx.ngrok.io/webhook
```

### Step 4: LINE Developers で設定

1. LINE Developers コンソールで「Messaging API」タブを開く
2. **「Webhook URL」セクション**を探す
3. Webhook URL を入力：
   ```
   https://your-server.com/webhook
   ```
4. **「Verify」または「検証」ボタン**をクリック
5. 検証成功後、「Save」または「保存」ボタンをクリック

### Step 5: Webhookを有効化

1. **「Webhookの利用」**を「利用する」に設定
2. **「自動応答メッセージ」**を「無効」に設定（Messaging APIを使用する場合）

---

## 📝 今回の推奨設定

### Webhook URL

**設定不要**（今回の用途では使用しない）

### その他の設定

- **Webhookの利用:** 無効（使用しない場合）
- **自動応答メッセージ:** 無効（Messaging APIを使用する場合）

---

## 🚀 今後の拡張（オプション）

将来的にWebhook機能を追加する場合：

### ユースケース例

1. **ユーザーからのメッセージ受け取り**
   - 診断ツールの結果をメッセージで受け取る
   - ユーザーからの質問に自動返信

2. **自動リプライ機能**
   - 特定のキーワードで自動返信
   - 診断ツールの結果をLINEで送信

### 実装手順

1. Webhookエンドポイントを実装
2. サーバーをデプロイ（HTTPS必須）
3. Webhook URL を設定
4. 検証
5. 有効化

---

## 💡 まとめ

- ✅ **今回の用途（通知機能のみ）では、Webhook URL は設定不要**
- ✅ 将来的にメッセージを受け取る場合は、Webhook URL が必要
- ✅ Webhook URL はHTTPS必須
- ✅ ローカル開発にはngrokなどを使用

---

## 📋 現在の設定

### 必要な設定

- ✅ Channel ID: 2008863419
- ✅ Channel Secret: 615da785c3f141e9e02f312c9458aa49
- ⏳ Channel Access Token: 取得待ち

### 不要な設定

- ❌ Webhook URL: 設定不要（今回の用途では使用しない）

---

Channel Access Token を取得したら、`.env`ファイルに設定してテストを実行しましょう！
