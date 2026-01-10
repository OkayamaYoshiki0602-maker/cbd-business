# 最終セットアップ手順（あなたの対応が必要）

## 📋 設定完了済み

✅ **スプレッドシートID:** `1-2L6C3NpF8vqnXxHWKP-Js3TMFKYE73tTtxdkZVPTaM`
✅ **Gemini APIキー:** 設定済み
✅ **.envファイル:** 更新済み

---

## 🚀 あなたが対応する必要があること

### Step 1: スプレッドシートをサービスアカウントに共有

1. **スプレッドシートを開く:**
   https://docs.google.com/spreadsheets/d/1-2L6C3NpF8vqnXxHWKP-Js3TMFKYE73tTtxdkZVPTaM/edit

2. **「共有」ボタンをクリック**

3. **以下のサービスアカウントを「編集者」権限で追加:**
   ```
   cursor-mcp@acoustic-skein-329303.iam.gserviceaccount.com
   ```

4. **「送信」をクリック**

✅ **完了:** サービスアカウントに共有設定

---

### Step 2: スプレッドシートにヘッダー行を設定

1. **スプレッドシートを開く**

2. **1行目（A1からF1）に以下を入力:**

| A1 | B1 | C1 | D1 | E1 | F1 |
|----|----|----|----|----|----|
| タイムスタンプ | ステータス | 記事タイトル | ツイート文案 | 記事URL | ソース |

3. **保存**（自動保存されます）

✅ **完了:** ヘッダー行を設定

---

### Step 3: Apps Scriptを設定（即時承認機能を使用する場合・オプション）

#### 3-1: Google Apps Script エディタを開く

1. **スプレッドシートを開く:**
   https://docs.google.com/spreadsheets/d/1-2L6C3NpF8vqnXxHWKP-Js3TMFKYE73tTtxdkZVPTaM/edit

2. **「拡張機能」→「Apps Script」を選択**

3. Apps Script エディタが開きます

#### 3-2: スクリプトをコピー＆ペースト

1. **ファイル `automation/google_services/google_sheets_trigger.gs` を開く**
   - すべてのコードをコピー

2. **Apps Script エディタにペースト**
   - 既存のコードを削除
   - コピーしたコードを貼り付け

3. **ファイルを保存**（Ctrl+S / Cmd+S）

#### 3-3: ZapierでWebhookを作成（推奨）

**方法A: Zapierを使用（推奨）**

1. **Zapier にアクセス:** https://zapier.com/
2. **アカウント作成**（まだの場合）
3. **「Create Zap」をクリック**
4. **Trigger:** 「Webhooks by Zapier」→「Catch Hook」を選択
5. **「Continue」をクリック**
6. **Webhook URLをコピー**（例: `https://hooks.zapier.com/hooks/catch/1234567/abcdefg`）

7. **Apps Scriptに戻って `WEBHOOK_URL` を更新:**

```javascript
const CONFIG = {
  WEBHOOK_URL: 'https://hooks.zapier.com/hooks/catch/YOUR/WEBHOOK/ID',  // ここにZapierのWebhook URLを貼り付け
  // ...
};
```

8. **ZapierでActionを設定:**
   - 「X (Twitter)」→「Create Tweet」を選択
   - X API認証情報を設定
   - ツイート文案を設定（Webhookから `tweet_text` を取得）

9. **「Test」をクリックしてテスト**
10. **「Publish」をクリックして公開**

✅ **完了:** Apps ScriptとZapierの設定

**方法B: 定期実行を使用（シンプル・推奨）**

GASトリガーは設定せず、定期実行スクリプトを使用：
- 毎朝7:15に承認済みツイートを自動投稿
- 設定が簡単

---

### Step 4: テスト実行

#### 4-1: 設定確認

```bash
cd "/Users/okayamayoshiki/Library/CloudStorage/GoogleDrive-okayamayoshiki0602o@gmail.com/マイドライブ/cursor"
python3 -c "
from dotenv import load_dotenv
import os
load_dotenv()
print('✅ APPROVAL_SPREADSHEET_ID:', '設定済み' if os.getenv('APPROVAL_SPREADSHEET_ID') else '❌ 未設定')
print('✅ GEMINI_API_KEY:', '設定済み' if os.getenv('GEMINI_API_KEY') else '❌ 未設定')
"
```

#### 4-2: 手動テスト

```bash
# 1. ツイート案生成テスト
python3 automation/social_media/scheduled_tweet.py

# 2. 承認待ちリスト確認
python3 automation/social_media/approval_manager.py list

# 3. 承認テスト（行番号を指定、例：行2）
python3 automation/social_media/approval_manager.py approve 2

# 4. 承認済みツイート投稿テスト
python3 automation/social_media/approve_tweet.py
```

---

## ✅ 完了チェックリスト

### 必須項目

- [ ] **Step 1:** スプレッドシートをサービスアカウントに共有
- [ ] **Step 2:** スプレッドシートにヘッダー行を設定
- [ ] **Step 4-1:** 設定確認テストを実行
- [ ] **Step 4-2:** 手動テストを実行

### 推奨項目（即時承認機能を使用する場合）

- [ ] **Step 3:** Apps Scriptを設定
- [ ] **Step 3-3:** ZapierでWebhookを作成
- [ ] **Step 3-3:** ZapierでX APIアクションを設定

---

## 🎯 優先順位

### 今すぐ実行（必須）

1. ✅ **スプレッドシートをサービスアカウントに共有**
2. ✅ **スプレッドシートにヘッダー行を設定**
3. ✅ **テスト実行**

### 後で設定（オプション）

4. ✅ **Apps Scriptを設定**（即時承認機能を使用する場合）
5. ✅ **ZapierでWebhookを作成**（Apps Scriptを使用する場合）

---

## 📝 設定例

### ヘッダー行の設定

スプレッドシートの1行目（A1からF1）に以下を入力：

```
タイムスタンプ | ステータス | 記事タイトル | ツイート文案 | 記事URL | ソース
```

### サービスアカウントへの共有

以下のメールアドレスを「編集者」権限で追加：

```
cursor-mcp@acoustic-skein-329303.iam.gserviceaccount.com
```

---

## 🚀 次のステップ

1. **Step 1-2を完了**
2. **テスト実行**
3. **動作確認**

詳細は `docs/GAS_TRIGGER_SETUP_COMPLETE.md` を参照してください。

---

上記の手順を順番に実行してください。各ステップが完了したら、チェックボックスにチェックを入れましょう！
