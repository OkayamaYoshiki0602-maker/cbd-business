# Zapier Webhook セットアップガイド（詳細手順）

## 📋 概要

ZapierでWebhookを作成し、Google Apps Scriptからツイート投稿をトリガーする方法です。

---

## 🚀 Step 1: Zapierアカウントを作成（まだの場合）

### 1-1: Zapierにアクセス

1. **ブラウザで以下にアクセス:**
   ```
   https://zapier.com/
   ```

2. **「Sign Up」または「Get Started」をクリック**

3. **アカウント情報を入力:**
   - Emailアドレスを入力
   - パスワードを設定
   - 「Create account」をクリック

4. **メール認証**（必要に応じて）
   - メールボックスを確認
   - 認証リンクをクリック

✅ **完了:** Zapierアカウント作成

---

## 🚀 Step 2: Webhookをトリガーとして作成

### 2-1: 新しいZapを作成

1. **Zapierダッシュボードにログイン**

2. **「Create Zap」ボタンをクリック**
   - 画面左上の「+ Create Zap」ボタン

3. **トリガーアプリを選択**

### 2-2: Webhooks by Zapierを選択

1. **検索ボックスに「Webhooks」と入力**

2. **「Webhooks by Zapier」を選択**
   - オレンジ色のアイコン
   - 「Webhooks by Zapier」をクリック

3. **トリガーイベントを選択**

4. **「Catch Hook」を選択**
   - 画面に「Catch Hook」というオプションが表示されます
   - 「Catch Hook」をクリック
   - 「Continue」をクリック

### 2-3: Webhook URLを取得

1. **「Continue」をクリック**
   - 「Pick off a child key」画面が表示されます

2. **「Continue」をクリック**
   - 次の画面でWebhook URLが表示されます

3. **Webhook URLをコピー**
   - 画面に表示されるURLをコピー
   - 例: `https://hooks.zapier.com/hooks/catch/1234567/abcdefg`
   - **このURLをメモ帳に保存してください**

4. **「Continue」をクリック**

### 2-4: テストデータを送信

1. **「Test trigger」ボタンをクリック**
   - または「Send Test」をクリック

2. **テストリクエストを送信**
   - 「Send Test to Webhook」画面が表示されます
   - 「Send Test」をクリック

3. **テスト結果を確認**
   - 「Success!」と表示されればOK
   - 「Continue」をクリック

✅ **完了:** Webhookトリガーの作成

---

## 🚀 Step 3: X (Twitter)アクションを設定

### 3-1: アクションアプリを選択

1. **「Action」をクリック**
   - 画面右側の「Action」セクション

2. **「+ Add Step」をクリック**

3. **「Add action」画面で検索ボックスに「Twitter」または「X」と入力**

4. **「X (Twitter)」を選択**
   - 「X (Twitter)」をクリック

5. **アクションイベントを選択**

6. **「Create Tweet」を選択**
   - 「Create Tweet」をクリック
   - 「Continue」をクリック

### 3-2: X (Twitter)アカウントを接続

1. **「Sign in to X (Twitter)」をクリック**

2. **X (Twitter)アカウントでログイン**
   - ブラウザが開きます
   - X (Twitter)の認証画面が表示されます

3. **認証を許可**
   - 「Authorize app」をクリック

4. **「Continue」をクリック**

✅ **完了:** X (Twitter)アカウント接続

### 3-3: ツイート内容を設定

1. **「Tweet」フィールドをクリック**

2. **「Data from previous step」をクリック**

3. **Webhookから送信されるデータを選択**
   - 「1. Catch Hook」をクリック
   - 表示されるフィールドから `tweet_text` を選択
   - または、「Insert Data」ボタンを使用して `{{1__tweet_text}}` を選択

4. **テストを実行**
   - 「Test step」をクリック
   - テストツイートが投稿されます（本番環境では投稿されません）

5. **「Continue」をクリック**

✅ **完了:** アクションの設定

---

## 🚀 Step 4: Zapを公開

1. **「Publish Zap」ボタンをクリック**
   - 画面右上の「Publish Zap」ボタン

2. **Zap名を設定**（オプション）
   - 例: 「承認済みツイート自動投稿」

3. **「Publish」をクリック**

✅ **完了:** Zapの公開

---

## 🚀 Step 5: Google Apps ScriptにWebhook URLを設定

### 5-1: Google Apps Script エディタを開く

1. **スプレッドシートを開く:**
   ```
   https://docs.google.com/spreadsheets/d/1-2L6C3NpF8vqnXxHWKP-Js3TMFKYE73tTtxdkZVPTaM/edit
   ```

2. **「拡張機能」→「Apps Script」を選択**

3. Apps Script エディタが開きます

### 5-2: Webhook URLを設定

1. **`google_sheets_trigger.gs` ファイルを開く**
   - 左側のファイルリストから選択

2. **`WEBHOOK_URL` を更新**
   - 16行目付近の以下を探す:
   ```javascript
   WEBHOOK_URL: 'https://hooks.zapier.com/hooks/catch/YOUR/WEBHOOK/ID',
   ```
   
   - Step 2-3でコピーしたWebhook URLに置き換える:
   ```javascript
   WEBHOOK_URL: 'https://hooks.zapier.com/hooks/catch/1234567/abcdefg',
   ```

3. **ファイルを保存**（Ctrl+S / Cmd+S）

✅ **完了:** Webhook URLの設定

---

## 🧪 Step 6: テスト実行

### 6-1: スプレッドシートでテストデータを追加

1. **スプレッドシートを開く**

2. **2行目（A2からF2）にテストデータを追加:**

| A2 | B2 | C2 | D2 | E2 | F2 |
|----|----|----|----|----|----|
| 2025-01-11T12:00:00 | 下書き | テスト記事 | テストツイート内容 #CBD | https://cbd-no-hito.com/test | manual |

3. **B2セルを「承認済み」に変更**
   - B2セルをクリック
   - 「承認済み」と入力
   - Enterを押す

### 6-2: 実行結果を確認

1. **Zapierダッシュボードで実行履歴を確認**
   - Zapierダッシュボードにアクセス
   - 「History」タブをクリック
   - 最新の実行履歴を確認

2. **X (Twitter)でツイートを確認**
   - X (Twitter)にアクセス
   - 投稿されたツイートを確認

3. **スプレッドシートでステータスを確認**
   - B2セルが「投稿済み」に変更されているか確認

✅ **完了:** テスト実行

---

## 🆘 トラブルシューティング

### エラー: "Webhook URLが正しくありません"

**解決方法:**
1. ZapierでWebhook URLを再確認
2. Apps Scriptの `WEBHOOK_URL` が正しいか確認
3. Webhook URLに余分なスペースや改行がないか確認

### エラー: "ツイートが投稿されない"

**解決方法:**
1. Zapierの実行履歴を確認
   - エラーメッセージを確認
2. X (Twitter)アカウントの接続を再確認
3. 「Test step」を実行して再テスト

### エラー: "Zapが実行されない"

**解決方法:**
1. Zapが公開されているか確認
2. Zapierの無料プランの実行回数制限を確認
3. Webhook URLが正しく設定されているか確認

---

## 💡 代替手段（Zapierが使えない場合）

### 方法A: Make (旧 Integromat) を使用

1. **Makeにアクセス:** https://www.make.com/
2. **同様の手順でWebhookを作成**
3. **X (Twitter)モジュールを設定**

### 方法B: IFTTTを使用

1. **IFTTTにアクセス:** https://ifttt.com/
2. **Webhookトリガーを作成**
3. **X (Twitter)アクションを設定**

### 方法C: 定期実行スクリプトを使用（推奨・簡単）

GASトリガーを設定せず、定期実行スクリプトを使用：

```bash
# 毎日7:15に承認済みツイートを自動投稿
python3 automation/social_media/approve_tweet.py auto
```

**メリット:**
- ✅ 設定が簡単
- ✅ 追加サービス不要
- ✅ コスト無料

**デメリット:**
- ⚠️ 承認後、次回の定期実行時刻（7:15）まで待つ必要がある

---

## 📝 まとめ

### 完了チェックリスト

- [ ] **Step 1:** Zapierアカウント作成
- [ ] **Step 2:** Webhookトリガー作成
- [ ] **Step 3:** X (Twitter)アクション設定
- [ ] **Step 4:** Zapを公開
- [ ] **Step 5:** Google Apps ScriptにWebhook URLを設定
- [ ] **Step 6:** テスト実行

---

## 🚀 次のステップ

1. **ZapierでWebhookを作成**（Step 1-3）
2. **Google Apps ScriptにWebhook URLを設定**（Step 5）
3. **テスト実行**（Step 6）

詳細な手順は上記を参照してください。不明点があれば知らせてください！
