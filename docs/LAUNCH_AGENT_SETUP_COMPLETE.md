# Launch Agent設定完了

## ✅ 設定完了

Launch Agentファイルを作成しました！

**ファイルパス:** `~/Library/LaunchAgents/com.cbd.auto-tweet.plist`

---

## 📊 設定内容

### 実行タイミング

- **毎日7:15**に自動実行
- **実行内容:** 承認済みツイートを自動投稿

### 実行コマンド

```bash
/usr/bin/python3 automation/social_media/approve_tweet.py auto
```

---

## 🧪 テスト実行

### Step 1: 手動でテスト

```bash
cd "/Users/okayamayoshiki/Library/CloudStorage/GoogleDrive-okayamayoshiki0602o@gmail.com/マイドライブ/cursor"
python3 automation/social_media/approve_tweet.py auto
```

### Step 2: 動作確認

1. **スプレッドシートを開く**
2. **2行目（B2）に「承認済み」と入力**
3. **手動で実行:**
   ```bash
   python3 automation/social_media/approve_tweet.py auto
   ```
4. **X (Twitter)でツイートを確認**

---

## 📝 ログの確認

### 実行ログを確認

```bash
# 実行ログを確認
tail -f /tmp/cbd-auto-tweet.log

# エラーログを確認
tail -f /tmp/cbd-auto-tweet-error.log
```

---

## 🔧 トラブルシューティング

### Launch Agentが実行されない場合

#### 方法1: 再読み込み

```bash
launchctl bootout gui/$(id -u)/com.cbd.auto-tweet
launchctl bootstrap gui/$(id -u) ~/Library/LaunchAgents/com.cbd.auto-tweet.plist
```

#### 方法2: 手動実行で確認

```bash
python3 automation/social_media/approve_tweet.py auto
```

エラーが出た場合は、エラーメッセージを確認してください。

---

## 📊 実行タイミングの変更

### Launch Agentファイルを編集

```bash
nano ~/Library/LaunchAgents/com.cbd.auto-tweet.plist
```

### `Hour`と`Minute`を変更

```xml
<key>Hour</key>
<integer>7</integer>  <!-- 時（0-23） -->
<key>Minute</key>
<integer>15</integer>  <!-- 分（0-59） -->
```

### 再読み込み

```bash
launchctl bootout gui/$(id -u)/com.cbd.auto-tweet
launchctl bootstrap gui/$(id -u) ~/Library/LaunchAgents/com.cbd.auto-tweet.plist
```

---

## ✅ 完了チェックリスト

- [ ] **Launch Agentファイルを作成**
- [ ] **Launch Agentを読み込み**
- [ ] **動作確認**（手動実行でテスト）
- [ ] **ログを確認**

---

## 🚀 次のステップ

1. **テスト実行**（必須）
2. **動作確認**（必須）
3. **毎朝7:15に自動実行されることを確認**（推奨）

詳細は `docs/FINAL_SETUP_GUIDE.md` を参照してください。

---

**結論: Launch Agentの設定が完了しました！毎朝7:15に自動的にツイート投稿が実行されます！**
