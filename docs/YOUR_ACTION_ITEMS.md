# あなたが対応する必要があること（まとめ）

## 📋 設定完了済み

✅ **スプレッドシートID:** `1-2L6C3NpF8vqnXxHWKP-Js3TMFKYE73tTtxdkZVPTaM`
✅ **Gemini APIキー:** 設定済み
✅ **.envファイル:** 更新済み
✅ **ヘッダー行:** 自動設定済み

---

## 🚀 あなたが対応する必要があること（2ステップ）

### Step 1: スプレッドシートをサービスアカウントに共有

1. **スプレッドシートを開く:**
   https://docs.google.com/spreadsheets/d/1-2L6C3NpF8vqnXxHWKP-Js3TMFKYE73tTtxdkZVPTaM/edit

2. **「共有」ボタンをクリック**

3. **以下のサービスアカウントを「編集者」権限で追加:**
   ```
   cursor-mcp@acoustic-skein-329303.iam.gserviceaccount.com
   ```

4. **「送信」をクリック**

✅ **完了:** [ ] サービスアカウントに共有設定

---

### Step 2: ヘッダー行の確認（自動設定済み）

スプレッドシートのヘッダー行は自動設定済みです。念のため確認してください：

1. **スプレッドシートを開く**

2. **1行目（A1からF1）を確認:**

| A1 | B1 | C1 | D1 | E1 | F1 |
|----|----|----|----|----|----|
| タイムスタンプ | ステータス | 記事タイトル | ツイート文案 | 記事URL | ソース |

✅ **完了:** [ ] ヘッダー行を確認（既に設定済み）

---

## 🎯 オプション設定（即時承認機能を使用する場合・無料プラン利用可能）

### Step 3: ZapierでWebhookを作成（無料プランで利用可能）

**✅ 無料プランで利用可能:** 月100タスクまで無料で使用できます！

**推奨:** まずは定期実行（Step 1-2まで）で動作確認してから、必要に応じて設定

#### タスク数の見積もり

- **1回の承認→投稿:** 2タスク（Webhook受信 + X投稿）
- **毎日1回ツイート:** 60タスク/月（推奨・バッファ40タスク）
- **毎日2回ツイート:** 120タスク/月（❌ 100タスク超過）

#### 最短手順（5分で完了）

1. **Zapierにアクセス:** https://zapier.com/
2. **「Create Zap」をクリック**
3. **「Webhooks by Zapier」→「Catch Hook」を選択**
4. **Webhook URLをコピー**（重要！）
5. **「X (Twitter)」→「Create Tweet」を追加**
6. **`{{1__tweet_text}}` を設定**
7. **Zapを公開**
8. **Google Apps ScriptにWebhook URLを設定**

**詳細:** `docs/ZAPIER_QUICK_START.md`（5分で完了）
**詳細手順:** `docs/ZAPIER_WEBHOOK_SETUP_GUIDE.md`（ステップバイステップ）
**無料プラン設計:** `docs/ZAPIER_FREE_PLAN_DESIGN.md`（タスク数管理）

✅ **完了:** [ ] ZapierでWebhookを作成（無料プランで利用可能）

---

## 🧪 テスト実行

### Step 4: 動作確認

```bash
# 1. 設定確認
cd "/Users/okayamayoshiki/Library/CloudStorage/GoogleDrive-okayamayoshiki0602o@gmail.com/マイドライブ/cursor"
python3 -c "
from dotenv import load_dotenv
import os
load_dotenv()
print('✅ APPROVAL_SPREADSHEET_ID:', '設定済み' if os.getenv('APPROVAL_SPREADSHEET_ID') else '❌ 未設定')
print('✅ GEMINI_API_KEY:', '設定済み' if os.getenv('GEMINI_API_KEY') else '❌ 未設定')
"

# 2. ツイート案生成テスト
python3 automation/social_media/scheduled_tweet.py

# 3. 承認待ちリスト確認
python3 automation/social_media/approval_manager.py list
```

✅ **完了:** [ ] テスト実行

---

## ✅ 完了チェックリスト（まとめ）

### 必須項目

- [ ] **Step 1:** スプレッドシートをサービスアカウントに共有
- [ ] **Step 2:** ヘッダー行を確認（既に設定済み）
- [ ] **Step 4:** テスト実行

### 推奨項目（後で設定可能）

- [ ] **Step 3:** ZapierでWebhookを作成（即時承認機能を使用する場合）
  - クイックスタート: `docs/ZAPIER_QUICK_START.md`（5分で完了）
  - 詳細手順: `docs/ZAPIER_WEBHOOK_SETUP_GUIDE.md`

---

## 💡 即時承認機能を使わない場合（推奨・簡単）

**定期実行スクリプトを使用:**
- 毎朝7:15に承認済みツイートを自動投稿
- 設定が簡単（Zapier不要）
- コスト無料

**設定方法:**
```bash
# 毎日7:15に実行（cronやタスクスケジューラで設定）
python3 automation/social_media/approve_tweet.py auto
```

**メリット:**
- ✅ 設定が簡単（この手順不要）
- ✅ 追加サービス不要
- ✅ コスト無料

**デメリット:**
- ⚠️ 承認後、次回の定期実行時刻（7:15）まで待つ必要がある

---

## 📝 完了後のワークフロー

### 毎朝7:00（自動実行）

1. ツイート案生成
2. LINE通知でプレビュー送信
3. スプレッドシートに「下書き」として記録

### あなたが確認

1. LINEでプレビューを確認
2. スプレッドシートで「承認済み」に変更

### 自動投稿

**方法A:** 定期実行（7:15に自動投稿・推奨）
- 設定不要
- 次の定期実行時刻（7:15）に自動投稿

**方法B:** 即時承認（GASトリガー + Zapier）
- Apps Scriptを設定（Step 3）
- 承認した瞬間にツイート投稿

---

## 🚀 次のステップ

1. **Step 1-2を完了**（必須）
2. **テスト実行**（必須）
3. **動作確認**（必須）
4. **Zapierを設定**（オプション・後で設定可能）

---

詳細は `docs/FINAL_SETUP_STEPS.md` と `docs/ZAPIER_QUICK_START.md` を参照してください。

まずは Step 1（スプレッドシートの共有）を完了してください。これで基本機能は動作します！
