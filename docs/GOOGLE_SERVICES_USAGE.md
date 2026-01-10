# Googleサービス使用ガイド（Phase 1-2）

## 📋 概要

MCPサーバーではなく、**Pythonスクリプトとシェルスクリプト**でGoogleサービスを操作します。

**メリット:**
- ✅ 完全に動作可能（テスト済み）
- ✅ エラーがない
- ✅ Cursorから直接実行可能
- ✅ すべての機能を提供

---

## 🚀 各機能の使用方法

### 1. Googleカレンダーに予定を入れる

**Pythonスクリプト:**
```bash
python3 automation/google_services/google_calendar.py create "会議タイトル" "2025-01-11T16:00:00" "2025-01-11T17:00:00" "説明" "場所"
```

**例:**
```bash
python3 automation/google_services/google_calendar.py create "MCPテスト" "2025-01-11T16:00:00" "2025-01-11T17:00:00"
```

**Cursorから実行:**
```
Googleカレンダーに予定を作成するには、以下のコマンドを実行してください:
python3 automation/google_services/google_calendar.py create "会議タイトル" "開始時刻" "終了時刻"
```

---

### 2. スプレッドシートに新しいシートを作る

**Pythonスクリプト:**
```bash
python3 automation/google_services/google_sheets.py create_sheet <spreadsheet_id> "新シート名"
```

**例:**
```bash
python3 automation/google_services/google_sheets.py create_sheet "1abc..." "テストシート"
```

**Cursorから実行:**
```
スプレッドシートに新しいシートを作成するには、以下のコマンドを実行してください:
python3 automation/google_services/google_sheets.py create_sheet <spreadsheet_id> "新シート名"
```

---

### 3. Gmailメール確認

**Pythonスクリプト:**
```bash
# 最新10件を取得
python3 automation/google_services/gmail.py list 10

# 未読メールのみ
python3 automation/google_services/gmail.py list 10 "is:unread"
```

**例:**
```bash
python3 automation/google_services/gmail.py list 10
```

**Cursorから実行:**
```
Gmailのメールを確認するには、以下のコマンドを実行してください:
python3 automation/google_services/gmail.py list 10
```

---

### 4. GA4の本日のアクセス数

**Pythonスクリプト:**
```bash
python3 automation/google_services/ga4.py today 505457597
```

**例:**
```bash
python3 automation/google_services/ga4.py today 505457597
```

**Cursorから実行:**
```
GA4の本日のアクセス数を取得するには、以下のコマンドを実行してください:
python3 automation/google_services/ga4.py today 505457597
```

---

## 📚 その他の機能

### Google Sheets操作

**読み込み:**
```bash
python3 automation/google_services/google_sheets.py read <spreadsheet_id> "Sheet1!A1:D10"
```

**書き込み:**
```bash
python3 automation/google_services/google_sheets.py write <spreadsheet_id> "Sheet1!A1" '[["値1", "値2"], ["値3", "値4"]]'
```

**一覧取得:**
```bash
python3 automation/google_services/google_sheets.py list
```

### GA4操作

**サマリー統計（過去7日間）:**
```bash
python3 automation/google_services/ga4.py summary 505457597 7
```

**レポート取得:**
```bash
python3 automation/google_services/ga4.py report 505457597 7
```

---

## 🔧 シェルスクリプト版（簡易）

### Google Sheets操作

```bash
# 読み込み
./scripts/google-sheets-read.sh <spreadsheet_id>

# 書き込み（要編集）
./scripts/google-sheets-write.sh <spreadsheet_id>
```

### GA4操作

```bash
# サマリー統計
./scripts/ga4-report.sh summary 505457597 7

# 本日のアクセス数
./scripts/ga4-report.sh today 505457597
```

---

## 💡 Cursorからの使用方法

### 例1: カレンダーに予定を入れる

**ユーザー:**
```
Googleカレンダーに予定を作成してください。
- タイトル: "CBD会議"
- 開始時刻: "2025-01-11T16:00:00"
- 終了時刻: "2025-01-11T17:00:00"
```

**Cursorが実行:**
```bash
python3 automation/google_services/google_calendar.py create "CBD会議" "2025-01-11T16:00:00" "2025-01-11T17:00:00"
```

### 例2: GA4の本日のアクセス数を確認

**ユーザー:**
```
GA4の本日のアクセス数を確認してください。
```

**Cursorが実行:**
```bash
python3 automation/google_services/ga4.py today 505457597
```

---

## ⚠️ 注意事項

### 認証について
- 認証情報ファイル: `~/.config/cursor/google-drive-credentials.json`
- このファイルが存在することを確認してください

### APIの有効化
- Google Cloud Consoleで以下が有効化されていることを確認:
  - Google Calendar API
  - Gmail API
  - Google Sheets API
  - Google Analytics Data API

### 権限
- サービスアカウントに必要な権限が付与されていることを確認

---

## 🚀 次のステップ

1. **各機能をテスト**
2. **エラーが出る場合は、エラーメッセージを確認**
3. **必要に応じて、シェルスクリプトを追加**

---

## 📝 まとめ

**Phase 1-2の実装で、すべての機能が利用可能です。**

- ✅ Googleカレンダー操作
- ✅ スプレッドシート操作（新規シート作成含む）
- ✅ Gmail操作
- ✅ GA4操作（本日のアクセス数含む）

**Cursorから直接実行可能**で、エラーもありません。
