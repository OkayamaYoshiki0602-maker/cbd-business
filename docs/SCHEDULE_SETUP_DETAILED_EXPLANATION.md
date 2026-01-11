# 7:00のツイート案生成設定について（詳細説明）

## 📋 現在の状況

### 確認結果

**現在設定されているもの:**
- ✅ **12:30** - `approve_tweet.py auto`（承認済みツイート投稿）が実行される

**設定されていないもの:**
- ❌ **7:00** - `scheduled_tweet.py`（ツイート案生成）が実行される設定が**存在しない**

---

## 🚀 7:00にツイート案生成を設定する方法

### 方法A: Launch Agentを使用（推奨）

#### Step 1: Launch Agentファイルを作成

ターミナルで以下を実行：

```bash
nano ~/Library/LaunchAgents/com.cbd.tweet-generation.plist
```

#### Step 2: 以下の内容をコピー＆ペースト

```xml
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
    <key>Label</key>
    <string>com.cbd.tweet-generation</string>
    <key>ProgramArguments</key>
    <array>
        <string>/usr/bin/python3</string>
        <string>/Users/okayamayoshiki/Library/CloudStorage/GoogleDrive-okayamayoshiki0602o@gmail.com/マイドライブ/cursor/automation/social_media/scheduled_tweet.py</string>
    </array>
    <key>WorkingDirectory</key>
    <string>/Users/okayamayoshiki/Library/CloudStorage/GoogleDrive-okayamayoshiki0602o@gmail.com/マイドライブ/cursor</string>
    <key>StartCalendarInterval</key>
    <dict>
        <key>Hour</key>
        <integer>7</integer>
        <key>Minute</key>
        <integer>0</integer>
    </dict>
    <key>RunAtLoad</key>
    <false/>
    <key>StandardOutPath</key>
    <string>/tmp/cbd-tweet-generation.log</string>
    <key>StandardErrorPath</key>
    <string>/tmp/cbd-tweet-generation-error.log</string>
</dict>
</plist>
```

#### Step 3: 保存して終了

- **nanoの場合**: `Ctrl+X` → `Y` → `Enter`

#### Step 4: Launch Agentを読み込む

ターミナルで以下を実行：

```bash
launchctl bootstrap gui/$(id -u) ~/Library/LaunchAgents/com.cbd.tweet-generation.plist
```

#### Step 5: 動作確認

ターミナルで以下を実行：

```bash
# Launch Agentが読み込まれているか確認
launchctl list | grep com.cbd.tweet-generation

# ログを確認（実行後）
tail -f /tmp/cbd-tweet-generation.log
```

---

### 方法B: cronを使用

#### Step 1: crontabを編集

ターミナルで以下を実行：

```bash
crontab -e
```

#### Step 2: 以下を追加

```bash
# 毎日7:00にツイート案生成
0 7 * * * cd "/Users/okayamayoshiki/Library/CloudStorage/GoogleDrive-okayamayoshiki0602o@gmail.com/マイドライブ/cursor" && /usr/bin/python3 automation/social_media/scheduled_tweet.py >> /tmp/cbd-tweet-generation.log 2>&1
```

#### Step 3: 保存して終了

- **vimの場合**: `:wq` で保存して終了
- **nanoの場合**: `Ctrl+X` → `Y` → `Enter`

---

## 🧪 テスト実行

### 手動でテスト

ターミナルで以下を実行：

```bash
cd "/Users/okayamayoshiki/Library/CloudStorage/GoogleDrive-okayamayoshiki0602o@gmail.com/マイドライブ/cursor"
python3 automation/social_media/scheduled_tweet.py
```

### 動作確認

1. **LINE通知が来るか確認**
2. **スプレッドシートに「下書き」として記録されるか確認**
3. **ログを確認**:
   ```bash
   tail -f /tmp/cbd-tweet-generation.log
   ```

---

## 📊 設定後の動作フロー

### 毎朝7:00（自動実行）

1. **`scheduled_tweet.py`が実行**
   - ツイート文案を自動生成
   - LINE通知でプレビュー送信
   - スプレッドシートに「下書き」として記録

### あなたが確認（午前中）

1. **LINEでプレビューを確認**
2. **スプレッドシートで「承認済み」に変更**

### 毎日12:30（自動実行）

1. **`approve_tweet.py auto`が実行**
   - 承認済みツイートを取得
   - X (Twitter)に投稿
   - ステータスを「投稿済み」に更新

---

## ✅ 完了チェックリスト

- [ ] **Launch Agentファイルを作成**（方法A）または **cronに設定**（方法B）
- [ ] **Launch Agentを読み込み**（方法Aの場合）
- [ ] **テスト実行**（手動で実行して動作確認）
- [ ] **ログを確認**（エラーがないか確認）
- [ ] **翌朝7:00に自動実行されることを確認**

---

## 🆘 トラブルシューティング

### Launch Agentが実行されない場合

```bash
# Launch Agentを再読み込み
launchctl bootout gui/$(id -u)/com.cbd.tweet-generation
launchctl bootstrap gui/$(id -u) ~/Library/LaunchAgents/com.cbd.tweet-generation.plist

# ログを確認
tail -f /tmp/cbd-tweet-generation-error.log
```

### LINE通知が来ない場合

- `.env`ファイルに`LINE_NOTIFY_TOKEN`が設定されているか確認
- 手動実行でエラーが出ないか確認

### スプレッドシートに記録されない場合

- `.env`ファイルに`APPROVAL_SPREADSHEET_ID`が設定されているか確認
- スプレッドシートがサービスアカウントに共有されているか確認

---

## 📝 まとめ

**現在の設定:**
- ✅ 12:30に承認済みツイート投稿（設定済み）
- ❌ 7:00にツイート案生成（**未設定**）

**設定方法:**
1. Launch Agentファイルを作成（`com.cbd.tweet-generation.plist`）
2. Launch Agentを読み込む
3. テスト実行で動作確認

**設定後:**
- 毎朝7:00に自動でツイート案が生成される
- LINE通知でプレビューが送信される
- スプレッドシートに「下書き」として記録される
