# あなたが対応する必要があること（まとめ）

## 📋 設定完了済み

✅ **スプレッドシートID:** `1-2L6C3NpF8vqnXxHWKP-Js3TMFKYE73tTtxdkZVPTaM`
✅ **Gemini APIキー:** 設定済み
✅ **.envファイル:** 更新済み

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

### Step 2: スプレッドシートにヘッダー行を設定

1. **スプレッドシートを開く**

2. **1行目（A1からF1）に以下を入力:**

| A1 | B1 | C1 | D1 | E1 | F1 |
|----|----|----|----|----|----|
| タイムスタンプ | ステータス | 記事タイトル | ツイート文案 | 記事URL | ソース |

3. **保存**（自動保存されます）

✅ **完了:** [ ] ヘッダー行を設定

---

## 🎯 オプション設定（即時承認機能を使用する場合）

### Step 3: Apps Scriptを設定

**推奨:** まずは定期実行（Step 2まで）で動作確認してから、必要に応じて設定

**詳細:** `docs/GAS_TRIGGER_SETUP_COMPLETE.md`

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

---

## ✅ 完了チェックリスト

### 必須項目

- [ ] **Step 1:** スプレッドシートをサービスアカウントに共有
- [ ] **Step 2:** スプレッドシートにヘッダー行を設定
- [ ] **Step 4:** テスト実行

### 推奨項目（後で設定可能）

- [ ] **Step 3:** Apps Scriptを設定（即時承認機能を使用する場合）

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

**方法A:** 定期実行（7:15に自動投稿）
- 設定不要
- 次の定期実行時刻（7:15）に自動投稿

**方法B:** 即時承認（GASトリガー）
- Apps Scriptを設定（Step 3）
- 承認した瞬間にツイート投稿

---

## 🚀 次のステップ

1. **Step 1-2を完了**（必須）
2. **テスト実行**（必須）
3. **動作確認**（必須）
4. **Apps Scriptを設定**（オプション・後で設定可能）

---

詳細は `docs/FINAL_SETUP_STEPS.md` を参照してください。

上記の2ステップを完了すれば、基本機能は動作します！
