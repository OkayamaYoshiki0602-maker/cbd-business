# 最終セットアップガイド（定期実行スクリプト版）

## 📋 概要

Zapierは使用しない方針です。**定期実行スクリプト**を使用して、完全無料で自動ツイートを実現します。

---

## ✅ 設定完了済み

- ✅ **スプレッドシートID:** `1-2L6C3NpF8vqnXxHWKP-Js3TMFKYE73tTtxdkZVPTaM`
- ✅ **Gemini APIキー:** 設定済み
- ✅ **.envファイル:** 更新済み
- ✅ **ヘッダー行:** 自動設定済み

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

### Step 2: 定期実行スクリプトを設定（macOS）

#### 方法A: Launch Agentを設定（推奨）

1. **Launch Agentファイルを作成:**
   ```bash
   mkdir -p ~/Library/LaunchAgents
   nano ~/Library/LaunchAgents/com.cbd.auto-tweet.plist
   ```

2. **以下をコピー＆ペースト:**
   ```xml
   <?xml version="1.0" encoding="UTF-8"?>
   <!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
   <plist version="1.0">
   <dict>
       <key>Label</key>
       <string>com.cbd.auto-tweet</string>
       <key>ProgramArguments</key>
       <array>
           <string>/usr/bin/python3</string>
           <string>/Users/okayamayoshiki/Library/CloudStorage/GoogleDrive-okayamayoshiki0602o@gmail.com/マイドライブ/cursor/automation/social_media/approve_tweet.py</string>
           <string>auto</string>
       </array>
       <key>WorkingDirectory</key>
       <string>/Users/okayamayoshiki/Library/CloudStorage/GoogleDrive-okayamayoshiki0602o@gmail.com/マイドライブ/cursor</string>
       <key>StartCalendarInterval</key>
       <dict>
           <key>Hour</key>
           <integer>7</integer>
           <key>Minute</key>
           <integer>15</integer>
       </dict>
       <key>RunAtLoad</key>
       <false/>
       <key>StandardOutPath</key>
       <string>/tmp/cbd-auto-tweet.log</string>
       <key>StandardErrorPath</key>
       <string>/tmp/cbd-auto-tweet-error.log</string>
   </dict>
   </plist>
   ```

3. **保存して終了:**
   - nanoの場合: Ctrl+X → Y → Enter

4. **Launch Agentを読み込む:**
   ```bash
   launchctl load ~/Library/LaunchAgents/com.cbd.auto-tweet.plist
   ```

5. **動作確認:**
   ```bash
   launchctl list | grep com.cbd.auto-tweet
   ```

✅ **完了:** [ ] Launch Agentを設定

#### 方法B: cronを使用

1. **crontabを編集:**
   ```bash
   crontab -e
   ```

2. **以下を追加:**
   ```bash
   # 毎日7:00にツイート案生成
   0 7 * * * cd "/Users/okayamayoshiki/Library/CloudStorage/GoogleDrive-okayamayoshiki0602o@gmail.com/マイドライブ/cursor" && /usr/bin/python3 automation/social_media/scheduled_tweet.py >> /tmp/cbd-tweet-generation.log 2>&1

   # 毎日7:15に承認済みツイート投稿
   15 7 * * * cd "/Users/okayamayoshiki/Library/CloudStorage/GoogleDrive-okayamayoshiki0602o@gmail.com/マイドライブ/cursor" && /usr/bin/python3 automation/social_media/approve_tweet.py auto >> /tmp/cbd-auto-tweet.log 2>&1
   ```

3. **保存して終了:**
   - vimの場合: `:wq` で保存して終了
   - nanoの場合: Ctrl+X → Y → Enter

✅ **完了:** [ ] cronを設定

---

## 🧪 テスト実行

### Step 1: 手動でテスト

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

# 4. 承認テスト（行番号を指定、例：行2）
python3 automation/social_media/approval_manager.py approve 2

# 5. 承認済みツイート投稿テスト
python3 automation/social_media/approve_tweet.py auto
```

✅ **完了:** [ ] テスト実行

---

## 📝 完了後のワークフロー

### 毎朝7:00（自動実行）

1. **ツイート案生成**
2. **LINE通知でプレビュー送信**
3. **スプレッドシートに「下書き」として記録**

### あなたが確認

1. **LINEでプレビューを確認**
2. **スプレッドシートで「承認済み」に変更**

### 毎朝7:15（自動実行）

1. **承認済みツイートを自動投稿**
2. **LINE通知で投稿結果を送信**
3. **ステータスを「投稿済み」に更新**

---

## 🚀 即時投稿が必要な場合

承認後、すぐにツイートしたい場合は、手動で実行できます：

```bash
cd "/Users/okayamayoshiki/Library/CloudStorage/GoogleDrive-okayamayoshiki0602o@gmail.com/マイドライブ/cursor"
python3 automation/social_media/approve_tweet.py auto
```

これで即座に投稿されます。

---

## ✅ 完了チェックリスト

### 必須項目

- [ ] **Step 1:** スプレッドシートをサービスアカウントに共有
- [ ] **Step 2:** 定期実行スクリプトを設定（Launch Agentまたはcron）
- [ ] **テスト実行:** 動作確認

### 推奨項目

- [ ] **ログを確認:** `/tmp/cbd-auto-tweet.log`
- [ ] **実行タイミングを調整**（必要に応じて）

---

## 📊 実行タイミングの変更

### Launch Agentの場合

1. **plistファイルを編集:**
   ```bash
   nano ~/Library/LaunchAgents/com.cbd.auto-tweet.plist
   ```

2. **`Hour`と`Minute`を変更:**
   ```xml
   <key>Hour</key>
   <integer>7</integer>  <!-- 時（0-23） -->
   <key>Minute</key>
   <integer>15</integer>  <!-- 分（0-59） -->
   ```

3. **Launch Agentを再読み込み:**
   ```bash
   launchctl unload ~/Library/LaunchAgents/com.cbd.auto-tweet.plist
   launchctl load ~/Library/LaunchAgents/com.cbd.auto-tweet.plist
   ```

### cronの場合

1. **crontabを編集:**
   ```bash
   crontab -e
   ```

2. **実行時刻を変更:**
   ```bash
   # 毎日8:00に実行する場合
   0 8 * * * cd "/Users/okayamayoshiki/Library/CloudStorage/GoogleDrive-okayamayoshiki0602o@gmail.com/マイドライブ/cursor" && /usr/bin/python3 automation/social_media/approve_tweet.py auto >> /tmp/cbd-auto-tweet.log 2>&1
   ```

---

## 🆘 トラブルシューティング

### エラー: "コマンドが見つかりません"

**解決方法:**
- Python3のパスを確認:
  ```bash
  which python3
  ```
- plistファイルまたはcrontabのパスを修正

### エラー: "スプレッドシートにアクセスできません"

**解決方法:**
1. スプレッドシートをサービスアカウントに共有しているか確認
2. `.env`ファイルの設定を確認

### エラー: "X API認証エラー"

**解決方法:**
1. `.env`ファイルのX API認証情報を確認
2. X API認証情報が正しいか確認

---

## 💡 メリット

### 定期実行スクリプトのメリット

- ✅ **完全無料**（Zapier不要）
- ✅ **設定が簡単**
- ✅ **追加サービス不要**
- ✅ **確実に動作**
- ✅ **即時投稿も可能**（手動実行）

### Zapierと比較

| 項目 | Zapier | 定期実行スクリプト |
|------|--------|------------------|
| コスト | 有料（プレミアム機能） | 完全無料 |
| 設定の難易度 | やや複雑 | 簡単 |
| 追加サービス | 必要 | 不要 |
| 動作の確実性 | 依存 | 確実 |

---

## 📚 参考ドキュメント

- `docs/FREE_AUTO_TWEET_SETUP.md`: 定期実行スクリプト設定詳細ガイド
- `docs/SCHEDULED_TWEET_SETUP.md`: 定期実行ツイート設定ガイド

---

## 🚀 次のステップ

1. **Step 1:** スプレッドシートをサービスアカウントに共有（必須）
2. **Step 2:** 定期実行スクリプトを設定（必須）
3. **テスト実行:** 動作確認（必須）

詳細は `docs/FREE_AUTO_TWEET_SETUP.md` を参照してください。

---

**結論: 定期実行スクリプトで、完全無料で自動ツイートを実現できます！**
