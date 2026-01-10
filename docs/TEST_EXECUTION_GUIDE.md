# テスト実行ガイド

## 📋 テスト実行の手順

### Step 1: 設定確認

```bash
cd "/Users/okayamayoshiki/Library/CloudStorage/GoogleDrive-okayamayoshiki0602o@gmail.com/マイドライブ/cursor"
python3 -c "
from dotenv import load_dotenv
import os
load_dotenv()
print('📋 設定確認:')
print('=' * 60)
print(f'✅ APPROVAL_SPREADSHEET_ID: {\"設定済み\" if os.getenv(\"APPROVAL_SPREADSHEET_ID\") else \"❌ 未設定\"}')
print(f'✅ GEMINI_API_KEY: {\"設定済み\" if os.getenv(\"GEMINI_API_KEY\") else \"❌ 未設定\"}')
print(f'✅ X_API_KEY: {\"設定済み\" if os.getenv(\"X_API_KEY\") else \"❌ 未設定\"}')
print(f'✅ LINE_CHANNEL_ACCESS_TOKEN: {\"設定済み\" if os.getenv(\"LINE_CHANNEL_ACCESS_TOKEN\") else \"❌ 未設定\"}')
print('=' * 60)
"
```

**確認項目:**
- すべて「設定済み」と表示されればOK

---

### Step 2: ツイート案生成テスト

```bash
python3 automation/social_media/scheduled_tweet.py
```

**実行内容:**
1. ツイート文案を自動生成
2. LINE通知でプレビュー送信
3. スプレッドシートに「下書き」として記録

**確認項目:**
- エラーなく実行される
- LINE通知が届く
- スプレッドシートに「下書き」が追加される

---

### Step 3: 承認待ちリスト確認

```bash
python3 automation/social_media/approval_manager.py list
```

**実行内容:**
- ステータスが「下書き」または「承認待ち」のツイートを表示

**確認項目:**
- Step 2で生成したツイート案が表示される

---

### Step 4: スプレッドシートで承認

1. **スプレッドシートを開く:**
   https://docs.google.com/spreadsheets/d/1-2L6C3NpF8vqnXxHWKP-Js3TMFKYE73tTtxdkZVPTaM/edit

2. **2行目（B2）のステータスを「承認済み」に変更**

3. **Enterを押す**

---

### Step 5: 承認済みリスト確認

```bash
python3 automation/social_media/approve_tweet.py list
```

**実行内容:**
- ステータスが「承認済み」のツイートを表示

**確認項目:**
- Step 4で承認したツイートが表示される

---

### Step 6: 承認済みツイート投稿テスト

```bash
python3 automation/social_media/approve_tweet.py auto
```

**実行内容:**
1. ステータスが「承認済み」のツイートを取得
2. X (Twitter)に投稿
3. ステータスを「投稿済み」に更新
4. LINE通知で投稿結果を送信

**確認項目:**
- エラーなく実行される
- X (Twitter)でツイートが投稿される
- スプレッドシートのステータスが「投稿済み」に更新される
- LINE通知が届く

---

## 📊 テスト実行チェックリスト

### 設定確認

- [ ] **Step 1:** 設定確認スクリプトを実行
- [ ] すべての設定が「設定済み」と表示される

### ツイート案生成

- [ ] **Step 2:** ツイート案生成スクリプトを実行
- [ ] エラーなく実行される
- [ ] LINE通知が届く
- [ ] スプレッドシートに「下書き」が追加される

### 承認

- [ ] **Step 3:** 承認待ちリストを確認
- [ ] ツイート案が表示される
- [ ] **Step 4:** スプレッドシートで「承認済み」に変更

### 投稿

- [ ] **Step 5:** 承認済みリストを確認
- [ ] 承認したツイートが表示される
- [ ] **Step 6:** 承認済みツイート投稿テストを実行
- [ ] X (Twitter)でツイートが投稿される
- [ ] スプレッドシートのステータスが「投稿済み」に更新される
- [ ] LINE通知が届く

---

## 🆘 トラブルシューティング

### エラー: "スプレッドシートにアクセスできません"

**解決方法:**
1. スプレッドシートをサービスアカウントに共有しているか確認
2. `.env`ファイルの設定を確認

### エラー: "X API認証エラー"

**解決方法:**
1. `.env`ファイルのX API認証情報を確認
2. X API認証情報が正しいか確認

### エラー: "LINE通知が届かない"

**解決方法:**
1. `.env`ファイルのLINE認証情報を確認
2. LINE通知スクリプトを手動で実行して確認

---

## 🚀 次のステップ

1. **テスト実行**（上記のStep 1-6）
2. **動作確認**（すべてのステップが正常に動作することを確認）
3. **Launch Agentを設定**（定期実行を設定）

詳細は `docs/FINAL_SETUP_GUIDE.md` を参照してください。

---

**結論: テスト実行で、すべての機能が正常に動作することを確認してください！**
