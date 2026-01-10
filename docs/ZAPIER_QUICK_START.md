# Zapier Webhook クイックスタート（5分で完了）

## 📋 前提条件

✅ **Zapierアカウント:** 持っていない場合は無料で作成可能
✅ **X (Twitter)アカウント:** 既に持っている
✅ **スプレッドシート:** 既に作成済み

---

## 🚀 最短手順（5ステップ）

### Step 1: ZapierでWebhookを作成（2分）

1. **Zapierにアクセス:** https://zapier.com/
2. **「Create Zap」をクリック**
3. **検索ボックスに「Webhooks」と入力**
4. **「Webhooks by Zapier」を選択**
5. **「Catch Hook」を選択**
6. **「Continue」をクリック**
7. **表示されるWebhook URLをコピー**（重要！）
   - 例: `https://hooks.zapier.com/hooks/catch/1234567/abcdefg`
   - **このURLをメモ帳に保存**

✅ **完了:** Webhook URLをコピー

---

### Step 2: X (Twitter)アクションを追加（2分）

1. **「+ Add Step」をクリック**
2. **検索ボックスに「Twitter」と入力**
3. **「X (Twitter)」を選択**
4. **「Create Tweet」を選択**
5. **「Sign in to X (Twitter)」をクリック**
6. **X (Twitter)アカウントで認証**
7. **「Tweet」フィールドをクリック**
8. **「Insert Data」をクリック**
9. **「1. Catch Hook」→ `tweet_text` を選択**
   - または、直接 `{{1__tweet_text}}` と入力

✅ **完了:** X (Twitter)アクションを設定

---

### Step 3: Zapを公開（30秒）

1. **「Publish Zap」をクリック**
2. **「Publish」をクリック**

✅ **完了:** Zapを公開

---

### Step 4: Google Apps Scriptに設定（1分）

1. **スプレッドシートを開く:**
   ```
   https://docs.google.com/spreadsheets/d/1-2L6C3NpF8vqnXxHWKP-Js3TMFKYE73tTtxdkZVPTaM/edit
   ```

2. **「拡張機能」→「Apps Script」を選択**

3. **`google_sheets_trigger.gs` ファイルを開く**

4. **16行目の `WEBHOOK_URL` を更新:**
   ```javascript
   // 変更前:
   WEBHOOK_URL: 'https://hooks.zapier.com/hooks/catch/YOUR/WEBHOOK/ID',
   
   // 変更後（Step 1でコピーしたURLに置き換える）:
   WEBHOOK_URL: 'https://hooks.zapier.com/hooks/catch/1234567/abcdefg',
   ```

5. **ファイルを保存**（Ctrl+S / Cmd+S）

✅ **完了:** Google Apps Scriptに設定

---

### Step 5: テスト実行（30秒）

1. **スプレッドシートの2行目（B2）に「承認済み」と入力**

2. **Enterを押す**

3. **X (Twitter)でツイートを確認**

✅ **完了:** テスト実行

---

## 🆘 困ったときは

### Webhook URLが見つからない

**解決方法:**
- Zapierダッシュボード → 「History」タブ → 最新の実行を確認
- または、Zapを編集して「Catch Hook」ステップを確認

### ツイートが投稿されない

**解決方法:**
1. Zapierの「History」タブでエラーを確認
2. X (Twitter)アカウントの接続を再確認
3. 「Test step」を実行して再テスト

### Apps Scriptでエラーが出る

**解決方法:**
1. Apps Scriptエディタで「実行」→「onEdit」を選択
2. エラーメッセージを確認
3. Webhook URLが正しく設定されているか確認

---

## 💡 もっと簡単な方法（推奨）

GASトリガーの設定が面倒な場合、**定期実行スクリプト**を使用：

```bash
# 毎日7:15に承認済みツイートを自動投稿
python3 automation/social_media/approve_tweet.py auto
```

**メリット:**
- ✅ 設定が簡単（この手順不要）
- ✅ 追加サービス不要
- ✅ コスト無料

**デメリット:**
- ⚠️ 承認後、次回の定期実行時刻（7:15）まで待つ必要がある

---

## 📝 まとめ

### 最短手順（5ステップ）

1. ✅ **ZapierでWebhookを作成**（Webhook URLをコピー）
2. ✅ **X (Twitter)アクションを追加**（`{{1__tweet_text}}` を設定）
3. ✅ **Zapを公開**
4. ✅ **Google Apps ScriptにWebhook URLを設定**
5. ✅ **テスト実行**

詳細は `docs/ZAPIER_WEBHOOK_SETUP_GUIDE.md` を参照してください。

---

上記の5ステップで完了です。不明点があれば知らせてください！
