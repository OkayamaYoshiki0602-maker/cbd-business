# 完全無料！定期実行スクリプトで自動ツイート設定

## 📋 概要

Zapierの有料プランは不要です。定期実行スクリプトを使用すれば、完全無料で自動ツイートできます。

---

## ✅ メリット

- ✅ **完全無料**（Zapier不要）
- ✅ **設定が簡単**
- ✅ **追加サービス不要**
- ✅ **確実に動作**
- ✅ **セキュリティ上の懸念が少ない**

---

## ⚠️ デメリット

- ⚠️ 承認後、次回の定期実行時刻（7:15）まで待つ必要がある
  - ただし、通常は15分以内に投稿される
  - 即座に投稿したい場合は、手動で実行も可能

---

## 🚀 設定方法（macOS）

### Step 1: 定期実行スクリプトをテスト

まず、手動でテスト実行して動作確認:

```bash
cd "/Users/okayamayoshiki/Library/CloudStorage/GoogleDrive-okayamayoshiki0602o@gmail.com/マイドライブ/cursor"
python3 automation/social_media/approve_tweet.py auto
```

✅ **動作確認完了:** エラーなく実行されればOK

---

### Step 2: Launch Agentを設定（macOS推奨）

#### 2-1: Launch Agentファイルを作成

```bash
# Launch Agentsディレクトリを作成（存在しない場合）
mkdir -p ~/Library/LaunchAgents

# plistファイルを作成
nano ~/Library/LaunchAgents/com.cbd.auto-tweet.plist
```

#### 2-2: 以下を追加

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

#### 2-3: 保存して終了

- **nanoの場合:** Ctrl+X → Y → Enter

#### 2-4: Launch Agentを読み込む

```bash
launchctl load ~/Library/LaunchAgents/com.cbd.auto-tweet.plist
```

#### 2-5: 動作確認

```bash
# Launch Agentが読み込まれているか確認
launchctl list | grep com.cbd.auto-tweet

# ログを確認（実行後）
tail -f /tmp/cbd-auto-tweet.log
```

✅ **完了:** Launch Agentの設定

---

### Step 3: 別の方法（cronを使用）

Launch Agentが使えない場合は、cronを使用:

#### 3-1: crontabを編集

```bash
crontab -e
```

#### 3-2: 以下を追加

```bash
# 毎日7:15に承認済みツイートを自動投稿
15 7 * * * cd "/Users/okayamayoshiki/Library/CloudStorage/GoogleDrive-okayamayoshiki0602o@gmail.com/マイドライブ/cursor" && /usr/bin/python3 automation/social_media/approve_tweet.py auto >> /tmp/cbd-auto-tweet.log 2>&1
```

#### 3-3: 保存して終了

- **vimの場合:** `:wq` で保存して終了
- **nanoの場合:** Ctrl+X → Y → Enter

✅ **完了:** cronの設定

---

## 🧪 テスト実行

### Step 1: 手動でテスト

```bash
cd "/Users/okayamayoshiki/Library/CloudStorage/GoogleDrive-okayamayoshiki0602o@gmail.com/マイドライブ/cursor"
python3 automation/social_media/approve_tweet.py auto
```

### Step 2: スプレッドシートで確認

1. **スプレッドシートを開く**
2. **2行目（B2）に「承認済み」と入力**
3. **手動で実行:**
   ```bash
   python3 automation/social_media/approve_tweet.py auto
   ```
4. **X (Twitter)でツイートを確認**

✅ **完了:** テスト実行

---

## 🔧 トラブルシューティング

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

## 📝 実行タイミングの変更

### 実行時刻を変更する場合

#### Launch Agentの場合

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

#### cronの場合

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

## 🚀 手動実行も可能

承認後、すぐにツイートしたい場合:

```bash
cd "/Users/okayamayoshiki/Library/CloudStorage/GoogleDrive-okayamayoshiki0602o@gmail.com/マイドライブ/cursor"
python3 automation/social_media/approve_tweet.py auto
```

これで即座に投稿されます。

---

## ✅ 完了チェックリスト

### 必須項目

- [ ] **Step 1:** 手動でテスト実行
- [ ] **Step 2:** Launch Agentまたはcronを設定
- [ ] **Step 3:** テスト実行

### 推奨項目

- [ ] **ログを確認**（`/tmp/cbd-auto-tweet.log`）
- [ ] **実行タイミングを調整**（必要に応じて）

---

## 📝 まとめ

### メリット

- ✅ **完全無料**（Zapier不要）
- ✅ **設定が簡単**
- ✅ **追加サービス不要**
- ✅ **確実に動作**

### デメリット

- ⚠️ 承認後、次回の定期実行時刻（7:15）まで待つ必要がある
  - ただし、手動実行も可能

---

## 🚀 次のステップ

1. **手動でテスト実行**（必須）
2. **Launch Agentまたはcronを設定**（必須）
3. **動作確認**（必須）

詳細は `docs/FREE_ALTERNATIVES.md` を参照してください。

---

**結論: Zapierの有料プランは不要です。定期実行スクリプトを使用すれば、完全無料で動作します！**
