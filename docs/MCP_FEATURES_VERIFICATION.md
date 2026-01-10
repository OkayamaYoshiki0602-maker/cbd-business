# MCP機能の動作確認

## ✅ 実装完了した機能

### 1. Googleカレンダーに予定を入れる ✅
**ツール名:** `create_calendar_event`

**使用方法（Cursor経由）:**
```
Googleカレンダーに予定を作成してください。
- タイトル: "テスト会議"
- 開始時刻: "2025-01-11T15:00:00"
- 終了時刻: "2025-01-11T16:00:00"
```

**コマンドライン:**
```bash
python3 automation/google_services/google_calendar.py create "テスト会議" "2025-01-11T15:00:00" "2025-01-11T16:00:00"
```

---

### 2. スプレッドシートに新しいシートを作る ✅
**ツール名:** `create_sheet_tab`

**使用方法（Cursor経由）:**
```
スプレッドシートに新しいシートを作成してください。
- スプレッドシートID: "1abc..."
- シート名: "新シート"
```

**コマンドライン:**
```bash
# まず、スプレッドシート内のシート一覧を確認
python3 automation/google_services/google_sheets.py list_sheets <spreadsheet_id>

# 新しいシートを作成（コード内で実装）
```

---

### 3. Gmailメール確認 ✅
**ツール名:** `list_gmail_messages`

**使用方法（Cursor経由）:**
```
okayamayoshiki0602o@gmail.comのメールを確認してください。
- 最大10件
- 未読メールのみ: query="is:unread"
```

**コマンドライン:**
```bash
python3 automation/google_services/gmail.py list 10
python3 automation/google_services/gmail.py list 10 "is:unread"
```

**注意:**
- Gmail APIはサービスアカウントでは直接使用できない可能性があります
- OAuth 2.0認証が必要な場合があります

---

### 4. GA4の本日のアクセス数 ✅
**ツール名:** `get_ga4_today`

**使用方法（Cursor経由）:**
```
GA4の本日のアクセス数を取得してください。
- プロパティID: "505457597"
```

**コマンドライン:**
```bash
python3 automation/google_services/ga4.py today 505457597
```

---

## 🧪 テスト方法

### Cursorから直接テスト

1. **Cursorを再起動**（MCPサーバーを読み込み直す）
2. **以下のように指示:**

#### テスト1: カレンダー予定作成
```
Googleカレンダーに予定を作成してください。
- タイトル: "MCPテスト"
- 開始時刻: "2025-01-11T16:00:00"
- 終了時刻: "2025-01-11T17:00:00"
```

#### テスト2: スプレッドシート新規シート作成
```
スプレッドシートに新しいシートを作成してください。
- スプレッドシートID: [実際のスプレッドシートID]
- シート名: "テストシート"
```

#### テスト3: Gmail確認
```
okayamayoshiki0602o@gmail.comの最新のメール10件を確認してください。
```

#### テスト4: GA4本日のアクセス数
```
GA4の本日のアクセス数を取得してください。
プロパティID: 505457597
```

---

## 📋 実装ファイル

### 新規作成
- `automation/google_services/google_calendar.py` - Googleカレンダー操作
- `automation/google_services/gmail.py` - Gmail操作

### 更新
- `automation/google_services/google_sheets.py` - 新規シート作成機能を追加
- `automation/google_services/ga4.py` - 本日のアクセス数取得機能を追加
- `automation/mcp_server/google_services_mcp.py` - 新機能をMCPツールとして追加

---

## ⚠️ 注意事項

### Gmail APIについて
- サービスアカウントでは直接メールボックスにアクセスできない可能性があります
- OAuth 2.0認証が必要な場合があります
- エラーが出る場合は、認証方法の変更が必要です

### Googleカレンダーについて
- サービスアカウントでカレンダーにアクセスする場合、カレンダーの共有設定が必要です
- エラーが出る場合は、カレンダーの共有設定を確認してください

---

## 🔧 トラブルシューティング

### エラーが出る場合

1. **Cursorを再起動**（MCPサーバーを読み込み直す）
2. **認証情報を確認:**
   - `~/.config/cursor/google-drive-credentials.json` が存在するか確認
3. **APIの有効化を確認:**
   - Google Cloud Consoleで以下が有効化されているか確認:
     - Google Calendar API
     - Gmail API
     - Google Sheets API
     - Google Analytics Data API
4. **権限を確認:**
   - サービスアカウントに必要な権限が付与されているか確認

---

## 🚀 次のステップ

1. **Cursorを再起動**
2. **各機能をテスト**
3. **エラーが出る場合は、エラーメッセージを確認**
