# セットアップチェックリスト（ユーザー対応必須）

## 📋 概要

X自動ツイート機能を動作させるために、**あなたが対応する必要がある設定**を順番にまとめました。

---

## ✅ チェックリスト

### 1. 承認待ちリスト用スプレッドシートの作成

**状態:** ⏳ 未完了

**手順:**

1. Googleスプレッドシートを開く: https://docs.google.com/spreadsheets/
2. 「空白」を選択して新しいスプレッドシートを作成
3. スプレッドシート名を「承認待ちリスト」に変更（任意）
4. 以下のヘッダー行を**A1からF1**に設定：

| A列 | B列 | C列 | D列 | E列 | F列 |
|-----|-----|-----|-----|-----|-----|
| タイムスタンプ | ステータス | 記事タイトル | ツイート文案 | 記事URL | ソース |

5. スプレッドシートIDをコピー
   - URL: `https://docs.google.com/spreadsheets/d/[スプレッドシートID]/edit`
   - `[スプレッドシートID]` の部分をコピー

**完了確認:**
- [ ] スプレッドシートが作成できた
- [ ] ヘッダー行が正しく設定できた
- [ ] スプレッドシートIDをコピーした

---

### 2. .envファイルの設定

**状態:** ⏳ 未完了

**手順:**

1. プロジェクトルートにある`.env`ファイルを開く
2. 以下の項目を設定（既に設定済みのものは確認のみ）：

```env
# X (Twitter) API認証情報（✅ 既に設定済み）
X_API_KEY=21hs4xf42RqZKg50s4oXafaaR
X_API_SECRET_KEY=jjgMdSrhcWMZQtymH3bmK2ymdZ9oYcvv9AF7yQ7b9ZfTxljxQi
X_ACCESS_TOKEN=1318210166580412416-OkcCDApUUmH6TnXVB1SUE2IWF6kjDL
X_ACCESS_TOKEN_SECRET=ZaltrsQzGamF0sxTUNF5pIfQSJnUe91n5m1j9Fjup1B5R
X_BEARER_TOKEN=AAAAAAAAAAAAAAAAAAAAADuO6wEAAAAAZEp6MT60uHerFb%2FRpXqrYAvRFe0%3DsX73VgKRUJ3Jk0FTT7u2K03Co7xqmNIBUJygqZwrJLzWw7iGe0

# LINE Messaging API認証情報（✅ 既に設定済み）
LINE_CHANNEL_ACCESS_TOKEN=eCyxNGmF7984+NCLBO2Ru5pijfdNkxg+pw2eOMd9LwcmBpKTpWQG/E1+mcdqFRHb0eFUyX3xZbm3bKvUkcUCiCEHcj7zfMnuEgMXRKEb/OXPO0XZ3wnbnb3TlmUxUFv7RDPdQ51bHLHtq4jp2BwY/wdB04t89/1O/w1cDnyilFU=
LINE_BOT_BASIC_ID=@335xppnw
LINE_CHANNEL_ID=2008863419
LINE_CHANNEL_SECRET=615da785c3f141e9e02f312c9458aa49

# WordPress設定（✅ 既に設定済み）
WORDPRESS_URL=https://cbd-no-hito.com

# 定期実行時刻設定（✅ 既に設定済み）
TWEET_GENERATION_TIME=07:00
TWEET_POSTING_TIME=07:15

# 承認待ちリスト用スプレッドシートID（⏳ 要設定）
APPROVAL_SPREADSHEET_ID=ここにスプレッドシートIDを貼り付け

# AI要約設定（⏳ 要設定）
AI_SUMMARIZER=gemini
GEMINI_API_KEY=ここにGemini_API_キーを貼り付け
```

3. `.env`ファイルを保存

**完了確認:**
- [ ] `APPROVAL_SPREADSHEET_ID`を設定した
- [ ] `GEMINI_API_KEY`を設定した
- [ ] `.env`ファイルを保存した

---

### 3. Gemini APIキーの取得

**状態:** ⏳ 未完了

**手順:**

1. Google AI Studio にアクセス: https://aistudio.google.com/
2. Googleアカウントでログイン（okayamayoshiki0602o@gmail.com）
3. 「Get API key」または「APIキーを取得」をクリック
4. 既存のプロジェクトを選択、または新規プロジェクトを作成
5. APIキーが表示される
6. **APIキーをコピー**（一度しか表示されない場合があります）
7. `.env`ファイルの`GEMINI_API_KEY`に貼り付け

**完了確認:**
- [ ] Gemini APIキーを取得した
- [ ] `.env`ファイルに設定した

**参考:** `docs/GEMINI_API_SETUP.md`

---

### 4. 承認待ちリスト用スプレッドシートの共有設定

**状態:** ⏳ 未完了

**手順:**

1. 作成したスプレッドシートを開く
2. 「共有」ボタンをクリック
3. 以下のサービスアカウントに「編集者」権限で共有：
   ```
   cursor-mcp@acoustic-skein-329303.iam.gserviceaccount.com
   ```
4. 「送信」をクリック

**完了確認:**
- [ ] サービスアカウントに共有設定した

---

### 5. GASトリガーの設定（スキップ）

**状態:** ❌ 不要（定期実行スクリプトを使用）

**方針変更:** Zapierが使用できないため、**定期実行スクリプト**を使用します。

**参考:** 以前の設定方法（Zapier使用）は `docs/ZAPIER_TWITTER_ALTERNATIVES.md` を参照してください。

---

#### Step 1: Google Apps Script エディタを開く

1. 承認待ちリスト用スプレッドシートを開く
2. 「拡張機能」→「Apps Script」を選択
3. Apps Script エディタが開きます

#### Step 2: スクリプトをコピー＆ペースト

**⚠️ 重要:** このファイル（SETUP_CHECKLIST.md）ではなく、**`automation/google_services/google_sheets_trigger.gs`** の内容をコピーしてください。

1. **`automation/google_services/google_sheets_trigger.gs` の内容を開く**
   - ファイルパス: `automation/google_services/google_sheets_trigger.gs`
   - または `docs/GAS_SETUP_GUIDE.md` を参照
2. **すべてをコピー**
3. **Apps Script エディタにペースト**

#### Step 3: Webhook URLを設定

**方法A: Zapierを使用（推奨・最も簡単）**

1. Zapier にアクセス: https://zapier.com/
2. アカウント作成（まだの場合）
3. 「Create Zap」をクリック
4. **Trigger:** 「Webhooks by Zapier」→「Catch Hook」を選択
5. Webhook URLをコピー
6. Apps Script の `WEBHOOK_URL` に貼り付け：

```javascript
const CONFIG = {
  WEBHOOK_URL: 'https://hooks.zapier.com/hooks/catch/YOUR/WEBHOOK/ID',  // ここに貼り付け
  // ...
};
```

7. Zapierで**Action**を設定：
   - 「X (Twitter)」→「Create Tweet」を選択
   - X API認証情報を設定
   - ツイート文案を設定（Webhookから取得）

**方法B: 定期実行を使用（シンプル・推奨）**

GASトリガーは設定せず、定期実行スクリプトを使用：
- 7:15に承認済みツイートを自動投稿
- 設定が簡単（GASトリガー不要）

**完了確認（方法Aの場合）:**
- [ ] Apps Scriptにスクリプトを貼り付けた
- [ ] Webhook URLを設定した
- [ ] ZapierでWebhookとX APIアクションを設定した
- [ ] テスト実行して動作確認した

**参考:** `docs/GOOGLE_APPS_SCRIPT_TRIGGER.md`

---

### 6. 定期実行スクリプトの開始

**状態:** ⏳ 未完了

**手順:**

#### 方法A: schedule ライブラリで実行（推奨）

```bash
# バックグラウンドで実行
python3 automation/scripts/daily_tweet_scheduler.py &
```

**注意:** ターミナルを閉じると停止します。永続的に実行するには、方法BまたはCを使用してください。

#### 方法B: cron で実行（macOS/Linux）

1. crontabを編集：
```bash
crontab -e
```

2. 以下を追加：
```cron
# 毎日7:00にツイート案生成
0 7 * * * cd /Users/okayamayoshiki/Library/CloudStorage/GoogleDrive-okayamayoshiki0602o@gmail.com/マイドライブ/cursor && /usr/bin/python3 automation/social_media/scheduled_tweet.py

# 毎日7:15に承認済みツイート投稿
15 7 * * * cd /Users/okayamayoshiki/Library/CloudStorage/GoogleDrive-okayamayoshiki0602o@gmail.com/マイドライブ/cursor && /usr/bin/python3 automation/social_media/approve_tweet.py auto
```

#### 方法C: 手動実行（テスト用）

```bash
# ツイート案生成
python3 automation/social_media/scheduled_tweet.py

# 承認済みツイート投稿
python3 automation/social_media/approve_tweet.py auto
```

**完了確認:**
- [ ] 定期実行スクリプトを開始した（方法A、B、またはC）

**参考:** `docs/SCHEDULED_TWEET_SETUP.md`

---

## 📝 設定完了後のテスト

### 1. 設定確認

```bash
# 認証情報の確認
python3 -c "
from dotenv import load_dotenv
import os
load_dotenv()

print('✅ 設定確認:')
print(f'APPROVAL_SPREADSHEET_ID: {\"設定済み\" if os.getenv(\"APPROVAL_SPREADSHEET_ID\") else \"未設定\"}')
print(f'GEMINI_API_KEY: {\"設定済み\" if os.getenv(\"GEMINI_API_KEY\") else \"未設定\"}')
print(f'TWEET_GENERATION_TIME: {os.getenv(\"TWEET_GENERATION_TIME\", \"未設定\")}')
"
```

### 2. 手動テスト

```bash
# 1. ツイート案生成テスト
python3 automation/social_media/scheduled_tweet.py

# 2. 承認待ちリスト確認
python3 automation/social_media/approval_manager.py list

# 3. 承認テスト（行番号を指定）
python3 automation/social_media/approval_manager.py approve 2

# 4. 承認済みツイート投稿テスト
python3 automation/social_media/approve_tweet.py
```

---

## 🎯 優先順位

### 必須設定（動作に必要）

1. ✅ **承認待ちリスト用スプレッドシートの作成**
2. ✅ **APPROVAL_SPREADSHEET_IDの設定**
3. ✅ **Gemini APIキーの取得と設定**
4. ✅ **スプレッドシートの共有設定**

### 推奨設定（機能を拡張）

5. ✅ **GASトリガーの設定**（即時承認機能・オプション）
6. ✅ **定期実行スクリプトの開始**（自動実行・推奨）

---

## ✅ 完了チェックリスト（まとめ）

### 必須項目

- [ ] 承認待ちリスト用スプレッドシートを作成
- [ ] `.env`ファイルに`APPROVAL_SPREADSHEET_ID`を設定
- [ ] Gemini APIキーを取得
- [ ] `.env`ファイルに`GEMINI_API_KEY`を設定
- [ ] スプレッドシートをサービスアカウントに共有

### 推奨項目

- [ ] GASトリガーを設定（即時承認機能・オプション）
- [ ] ZapierでWebhookを作成（GASトリガーを使用する場合）
- [ ] 定期実行スクリプトを開始

### テスト項目

- [ ] 設定確認スクリプトを実行
- [ ] ツイート案生成テストを実行
- [ ] 承認待ちリスト確認を実行
- [ ] 承認テストを実行
- [ ] 承認済みツイート投稿テストを実行

---

## 🆘 トラブルシューティング

### エラーが出た場合

1. `.env`ファイルの設定を確認
2. スプレッドシートIDが正しいか確認
3. スプレッドシートの共有設定を確認
4. エラーメッセージを確認して対処

---

## 📚 参考ドキュメント

- `docs/GEMINI_API_SETUP.md`: Gemini API設定ガイド
- `docs/GOOGLE_APPS_SCRIPT_TRIGGER.md`: GASトリガー実装ガイド
- `docs/SCHEDULED_TWEET_SETUP.md`: 定期実行ツイート設定ガイド

---

上記の手順を順番に実行してください。各ステップが完了したら、チェックボックスにチェックを入れましょう！
