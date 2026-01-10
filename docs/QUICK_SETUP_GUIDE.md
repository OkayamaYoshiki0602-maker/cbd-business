# クイックセットアップガイド

## 📋 5分で完了！最小限の設定

X自動ツイート機能を最小限の設定で動作させる手順です。

---

## 🚀 必須設定（3ステップ）

### Step 1: 承認待ちリスト用スプレッドシートを作成

1. **Googleスプレッドシートを開く:** https://docs.google.com/spreadsheets/
2. **新しいスプレッドシートを作成**
3. **ヘッダー行を設定**（A1からF1）：
   ```
   タイムスタンプ | ステータス | 記事タイトル | ツイート文案 | 記事URL | ソース
   ```
4. **スプレッドシートIDをコピー**
   - URL: `https://docs.google.com/spreadsheets/d/[スプレッドシートID]/edit`
   - `[スプレッドシートID]` の部分をコピー

✅ **完了:** スプレッドシートIDをメモ

---

### Step 2: Gemini APIキーを取得

1. **Google AI Studio にアクセス:** https://aistudio.google.com/
2. **「Get API key」をクリック**
3. **APIキーをコピー**

✅ **完了:** APIキーをメモ

---

### Step 3: .envファイルに設定

1. **プロジェクトルートの`.env`ファイルを開く**
2. **以下を追加・更新：**

```env
# 承認待ちリスト用スプレッドシートID
APPROVAL_SPREADSHEET_ID=Step1でコピーしたスプレッドシートID

# AI要約設定
AI_SUMMARIZER=gemini
GEMINI_API_KEY=Step2でコピーしたAPIキー
```

3. **ファイルを保存**

✅ **完了:** `.env`ファイルを保存

---

### Step 4: スプレッドシートを共有

1. **作成したスプレッドシートを開く**
2. **「共有」ボタンをクリック**
3. **以下を「編集者」権限で追加：**
   ```
   cursor-mcp@acoustic-skein-329303.iam.gserviceaccount.com
   ```
4. **「送信」をクリック**

✅ **完了:** 共有設定完了

---

## 🧪 テスト実行

### 1. 設定確認

```bash
cd "/Users/okayamayoshiki/Library/CloudStorage/GoogleDrive-okayamayoshiki0602o@gmail.com/マイドライブ/cursor"
python3 -c "
from dotenv import load_dotenv
import os
load_dotenv()
print('✅ APPROVAL_SPREADSHEET_ID:', '設定済み' if os.getenv('APPROVAL_SPREADSHEET_ID') else '未設定')
print('✅ GEMINI_API_KEY:', '設定済み' if os.getenv('GEMINI_API_KEY') else '未設定')
"
```

### 2. 手動テスト

```bash
# ツイート案生成テスト
python3 automation/social_media/scheduled_tweet.py
```

**期待される結果:**
- LINE通知が送信される
- スプレッドシートに「下書き」として記録される

---

## ✅ 完了チェックリスト

- [ ] スプレッドシートを作成
- [ ] スプレッドシートIDをコピー
- [ ] Gemini APIキーを取得
- [ ] `.env`ファイルに設定
- [ ] スプレッドシートを共有
- [ ] テスト実行

---

## 🎯 次のステップ（オプション）

### 即時承認機能（GASトリガー）

承認した瞬間にツイートする場合：
1. `docs/GOOGLE_APPS_SCRIPT_TRIGGER.md` を参照
2. Apps Scriptを設定
3. ZapierでWebhookを作成

### 定期実行の開始

毎朝7時に自動実行する場合：
1. `docs/SCHEDULED_TWEET_SETUP.md` を参照
2. cronまたは定期実行スクリプトを設定

---

## 📚 詳細ドキュメント

- `docs/SETUP_CHECKLIST.md`: 詳細なセットアップチェックリスト
- `docs/GEMINI_API_SETUP.md`: Gemini API設定ガイド

---

上記の3ステップで基本機能は動作します！テストを実行して確認してください。
