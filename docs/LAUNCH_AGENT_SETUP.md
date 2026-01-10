# Launch Agent設定ガイド（macOS）

## 📋 概要

macOSで定期実行スクリプトを設定する方法です。**Launch Agent**を使用して、毎日7:15に自動的にツイート投稿を実行します。

---

## 🚀 Step 1: ターミナルを開く

1. **「アプリケーション」→「ユーティリティ」→「ターミナル」を開く**
   - または、Spotlight検索（Cmd + Space）で「ターミナル」と入力

2. **ターミナルが開いたことを確認**

---

## 🚀 Step 2: Launch Agentsディレクトリを作成

ターミナルに以下をコピー＆ペーストして実行：

```bash
mkdir -p ~/Library/LaunchAgents
```

**説明:**
- `mkdir -p` = ディレクトリを作成（既に存在する場合は何もしない）
- `~/Library/LaunchAgents` = Launch Agentファイルを保存するディレクトリ

**実行結果:** 何も表示されなければ成功です。

---

## 🚀 Step 3: Launch Agentファイルを作成

ターミナルに以下をコピー＆ペーストして実行：

```bash
nano ~/Library/LaunchAgents/com.cbd.auto-tweet.plist
```

**説明:**
- `nano` = テキストエディタ（ターミナルで使える簡単なエディタ）
- `~/Library/LaunchAgents/com.cbd.auto-tweet.plist` = 作成するファイルのパス

**実行結果:** テキストエディタ（nano）が開きます。

---

## 🚀 Step 4: 設定をコピー＆ペースト

テキストエディタ（nano）が開いたら、以下を**すべてコピー＆ペースト**してください：

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

**注意:**
- 既存のテキストは削除してから貼り付けてください
- すべての内容を正確にコピーしてください

---

## 🚀 Step 5: ファイルを保存して終了

1. **Ctrl + X** を押す（保存して終了）
2. **Y** を押す（保存を確認）
3. **Enter** を押す（ファイル名を確認）

**実行結果:** ターミナルに戻ります。

---

## 🚀 Step 6: Launch Agentを読み込む

ターミナルに以下をコピー＆ペーストして実行：

```bash
launchctl load ~/Library/LaunchAgents/com.cbd.auto-tweet.plist
```

**説明:**
- `launchctl load` = Launch Agentを読み込むコマンド

**実行結果:** 何も表示されなければ成功です。

---

## 🧪 Step 7: 動作確認

ターミナルに以下をコピー＆ペーストして実行：

```bash
launchctl list | grep com.cbd.auto-tweet
```

**実行結果:** 以下のように表示されれば成功です：
```
-       0       com.cbd.auto-tweet
```

---

## 📊 実行タイミングの確認

### 現在の設定

- **実行時刻:** 毎日7:15
- **実行内容:** 承認済みツイートを自動投稿

### 実行タイミングを変更する場合

1. **ファイルを編集:**
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

3. **保存して終了:** Ctrl+X → Y → Enter

4. **Launch Agentを再読み込み:**
   ```bash
   launchctl unload ~/Library/LaunchAgents/com.cbd.auto-tweet.plist
   launchctl load ~/Library/LaunchAgents/com.cbd.auto-tweet.plist
   ```

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

## 🆘 トラブルシューティング

### エラー: "ファイルが見つかりません"

**解決方法:**
1. ファイルが正しく作成されているか確認:
   ```bash
   ls -la ~/Library/LaunchAgents/com.cbd.auto-tweet.plist
   ```
2. ファイルが存在しない場合、Step 2-5を再実行

### エラー: "コマンドが見つかりません"

**解決方法:**
1. Python3のパスを確認:
   ```bash
   which python3
   ```
2. plistファイルのパスを修正（Step 4を再実行）

### Launch Agentが実行されない

**解決方法:**
1. Launch Agentを再読み込み:
   ```bash
   launchctl unload ~/Library/LaunchAgents/com.cbd.auto-tweet.plist
   launchctl load ~/Library/LaunchAgents/com.cbd.auto-tweet.plist
   ```
2. ログを確認:
   ```bash
   tail -f /tmp/cbd-auto-tweet-error.log
   ```

---

## ✅ 完了チェックリスト

- [ ] **Step 1:** ターミナルを開いた
- [ ] **Step 2:** Launch Agentsディレクトリを作成した
- [ ] **Step 3:** Launch Agentファイルを作成した
- [ ] **Step 4:** 設定をコピー＆ペーストした
- [ ] **Step 5:** ファイルを保存して終了した
- [ ] **Step 6:** Launch Agentを読み込んだ
- [ ] **Step 7:** 動作確認した

---

## 🚀 次のステップ

1. **Launch Agentを設定**（上記の手順）
2. **テスト実行**（手動で実行して動作確認）
3. **動作確認**（毎日7:15に自動実行されることを確認）

詳細は `docs/FINAL_SETUP_GUIDE.md` を参照してください。

---

**結論: Launch Agentファイルは、ターミナルで`nano`コマンドを使って作成します！**
