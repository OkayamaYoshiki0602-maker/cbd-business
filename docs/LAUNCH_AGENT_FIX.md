# Launch Agent設定修正（新しいmacOS対応）

## 📋 問題

新しいmacOSでは、`launchctl load`が非推奨でエラーが出ることがあります。

**エラーメッセージ:**
```
Load failed: 5: Input/output error
Try running `launchctl bootstrap` as root for richer errors.
```

---

## ✅ 解決方法

### 新しいmacOSでは`launchctl bootstrap`を使用

#### Step 1: 既存のLaunch Agentを停止

```bash
launchctl bootout gui/$(id -u)/com.cbd.auto-tweet
```

#### Step 2: 新しい方法で読み込み

```bash
launchctl bootstrap gui/$(id -u) ~/Library/LaunchAgents/com.cbd.auto-tweet.plist
```

#### Step 3: 動作確認

```bash
launchctl list | grep com.cbd.auto-tweet
```

**正常な表示:**
```
-	0	com.cbd.auto-tweet
```

---

## 📊 動作確認

### 手動でテスト実行

```bash
cd "/Users/okayamayoshiki/Library/CloudStorage/GoogleDrive-okayamayoshiki0602o@gmail.com/マイドライブ/cursor"
python3 automation/social_media/approve_tweet.py auto
```

### スプレッドシートでテスト

1. **スプレッドシートを開く:**
   https://docs.google.com/spreadsheets/d/1-2L6C3NpF8vqnXxHWKP-Js3TMFKYE73tTtxdkZVPTaM/edit

2. **2行目（B2）に「承認済み」と入力**

3. **手動で実行:**
   ```bash
   python3 automation/social_media/approve_tweet.py auto
   ```

4. **X (Twitter)でツイートを確認**

---

## 🔧 コマンドの違い

### 旧コマンド（非推奨）

```bash
launchctl load ~/Library/LaunchAgents/com.cbd.auto-tweet.plist
```

### 新コマンド（推奨）

```bash
launchctl bootstrap gui/$(id -u) ~/Library/LaunchAgents/com.cbd.auto-tweet.plist
```

**説明:**
- `gui/$(id -u)` = 現在のユーザーのGUIセッションID
- `bootstrap` = 新しいmacOSで推奨される方法

---

## 📝 停止方法

### Launch Agentを停止する場合

```bash
launchctl bootout gui/$(id -u)/com.cbd.auto-tweet
```

### 再起動する場合

```bash
launchctl bootout gui/$(id -u)/com.cbd.auto-tweet
launchctl bootstrap gui/$(id -u) ~/Library/LaunchAgents/com.cbd.auto-tweet.plist
```

---

## 🆘 トラブルシューティング

### エラー: "Load failed: 5: Input/output error"

**解決方法:**
1. `launchctl bootstrap`を使用（新しいmacOS対応）
2. ファイルが正しく作成されているか確認:
   ```bash
   ls -la ~/Library/LaunchAgents/com.cbd.auto-tweet.plist
   ```

### エラー: "No such file or directory"

**解決方法:**
1. Launch Agentsディレクトリを作成:
   ```bash
   mkdir -p ~/Library/LaunchAgents
   ```
2. ファイルを作成:
   ```bash
   nano ~/Library/LaunchAgents/com.cbd.auto-tweet.plist
   ```

---

## ✅ 完了チェックリスト

- [ ] **Launch Agentファイルを作成**
- [ ] **`launchctl bootstrap`で読み込み**（新しいmacOS対応）
- [ ] **動作確認**（`launchctl list`で確認）
- [ ] **テスト実行**（手動で実行して動作確認）

---

## 🚀 次のステップ

1. **`launchctl bootstrap`で再読み込み**（上記のStep 1-2）
2. **動作確認**（`launchctl list`で確認）
3. **テスト実行**（手動で実行して動作確認）

詳細は `docs/LAUNCH_AGENT_SETUP_COMPLETE.md` を参照してください。

---

**結論: 新しいmacOSでは`launchctl bootstrap`を使用してください！**
