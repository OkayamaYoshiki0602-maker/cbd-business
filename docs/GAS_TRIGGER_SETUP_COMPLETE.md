# GASトリガー設定完了ガイド

## 📋 設定内容

以下の設定が完了しました：

### ✅ 設定完了

- **スプレッドシートID:** `1-2L6C3NpF8vqnXxHWKP-Js3TMFKYE73tTtxdkZVPTaM`
- **Gemini API Key:** 設定済み
- **.envファイル:** 更新済み

---

## 🚀 GASトリガーの設定手順

### Step 1: Google Apps Script エディタを開く

1. **スプレッドシートを開く:**
   https://docs.google.com/spreadsheets/d/1-2L6C3NpF8vqnXxHWKP-Js3TMFKYE73tTtxdkZVPTaM/edit

2. **「拡張機能」→「Apps Script」を選択**

3. Apps Script エディタが開きます

---

### Step 2: スクリプトをコピー＆ペースト

1. **`automation/google_services/google_sheets_trigger.gs` の内容を開く**
   - ファイルパス: `automation/google_services/google_sheets_trigger.gs`
   - すべてのコードをコピー

2. **Apps Script エディタにペースト**
   - Apps Script エディタのコード欄（`function onEdit(e) { ... }` の部分）を削除
   - コピーしたコードを貼り付け

3. **ファイルを保存**（Ctrl+S / Cmd+S）

---

### Step 3: Webhook URLを設定（方法A: Zapier推奨）

#### ZapierでWebhookを作成

1. **Zapier にアクセス:** https://zapier.com/
2. **アカウント作成**（まだの場合）
3. **「Create Zap」をクリック**
4. **Trigger:** 「Webhooks by Zapier」→「Catch Hook」を選択
5. **「Continue」をクリック**
6. **Webhook URLをコピー**（例: `https://hooks.zapier.com/hooks/catch/1234567/abcdefg`）

#### Apps Scriptに設定

1. **Apps Script エディタに戻る**
2. **`WEBHOOK_URL` を更新:**

```javascript
const CONFIG = {
  WEBHOOK_URL: 'https://hooks.zapier.com/hooks/catch/YOUR/WEBHOOK/ID',  // ここにZapierのWebhook URLを貼り付け
  // ...
};
```

3. **ファイルを保存**

#### ZapierでX APIアクションを設定

1. **Zapierで「Action」を追加**
2. **「X (Twitter)」→「Create Tweet」を選択**
3. **X API認証情報を設定**（初回のみ）
   - `.env`ファイルの認証情報を使用
4. **ツイート文案を設定:**
   - 「Tweet Text」: Webhookから `tweet_text` フィールドを選択
5. **「Test」をクリックしてテスト**
6. **「Publish」をクリックして公開**

---

### Step 4: 承認機能をテスト

1. **スプレッドシートを開く**
2. **テスト用のデータを追加:**
   - A2: `2025-01-11T12:00:00`
   - B2: `下書き`（または `承認待ち`）
   - C2: `テスト記事`
   - D2: `テストツイート内容 #CBD`
   - E2: `https://cbd-no-hito.com/test`
   - F2: `manual`

3. **ステータスを「承認済み」に変更:**
   - B2セルを `承認済み` に変更

4. **Zapierの実行履歴を確認:**
   - Zapierダッシュボードで実行履歴を確認
   - ツイートが投稿されているか確認

---

## 📝 設定確認チェックリスト

- [ ] Apps Scriptエディタを開いた
- [ ] `google_sheets_trigger.gs` のコードをコピー＆ペーストした
- [ ] ファイルを保存した
- [ ] ZapierでWebhookを作成した
- [ ] `WEBHOOK_URL` を設定した
- [ ] ZapierでX APIアクションを設定した
- [ ] テスト実行して動作確認した

---

## 🆘 トラブルシューティング

### エラー: "Webhook URLが正しくありません"

**解決方法:**
1. ZapierのWebhook URLが正しいか確認
2. `WEBHOOK_URL` が正しく設定されているか確認
3. Apps Scriptを再保存

### エラー: "ツイートが投稿されない"

**解決方法:**
1. Zapierの実行履歴を確認
2. X API認証情報が正しいか確認
3. Zapierの「Test」を実行して確認

---

## 💡 代替方法（GASトリガー不要）

GASトリガーの設定が面倒な場合、**定期実行スクリプト**を使用：

```bash
# 毎日7:15に承認済みツイートを自動投稿
python3 automation/social_media/approve_tweet.py auto
```

この場合、スプレッドシートで「承認済み」に変更した後、次回の定期実行時刻（7:15）に自動投稿されます。

---

## 🚀 次のステップ

1. **Apps Scriptを設定**
2. **ZapierでWebhookを作成**
3. **テスト実行**
4. **動作確認**

---

詳細は `docs/GOOGLE_APPS_SCRIPT_TRIGGER.md` を参照してください。

Apps Scriptの設定が完了したら、テストを実行して確認してください！
