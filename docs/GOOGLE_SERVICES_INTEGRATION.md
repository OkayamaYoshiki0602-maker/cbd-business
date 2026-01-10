# Googleサービス連携の実装方法

## 🎯 目標

**Cursor一つで全て操作可能にする**

MCPサーバーが存在しないため、以下の方法で実現します。

---

## 🚀 実装方法の選択肢

### 案1: カスタムMCPサーバーを作成（推奨・将来的に）

**メリット:**
- ✅ **Cursorから直接操作可能**（一度作成すれば）
- ✅ 統一されたインターフェース
- ✅ 「Cursor一つで全て」の目標を達成

**実装内容:**
- Node.jsまたはPythonでMCPサーバーを実装
- Google APIと連携
- CursorのMCP設定に追加

**運用:**
- 一度作成すれば、Cursorから直接操作可能
- 毎回スクリプトを実行する必要はない

**実装時期:**
- 将来的に実装（優先度は中）

---

### 案2: PythonスクリプトをCursorから実行（即座に可能）

**メリット:**
- ✅ **すぐに実装可能**
- ✅ Cursorから直接実行可能
- ✅ 柔軟な実装が可能

**実装内容:**
- Pythonスクリプトを作成
- Cursorからターミナルコマンドとして実行
- または、Cursorの拡張機能として実行

**運用:**
- Cursor内でコマンドを実行するだけ
- スクリプトは一度作成すれば、いつでも再利用可能

**実装時期:**
- 即座に実装可能（優先度：高）

---

### 案3: 自動化スクリプトとして実装（効率的）

**メリット:**
- ✅ **自動実行可能**
- ✅ スケジュール実行可能（cron、GitHub Actions等）
- ✅ 手動実行不要

**実装内容:**
- Pythonスクリプトを作成
- cronまたはGitHub Actionsで自動実行
- スケジュール実行またはイベント駆動

**運用:**
- 自動で実行される
- 手動実行は不要

**実装時期:**
- 必要に応じて実装（優先度：中）

---

## 📋 推奨実装順序

### Phase 1: Pythonスクリプトを作成（即座に可能）

**目的:**
- Googleサービスとの連携機能を実装
- Cursorから実行可能にする

**実装内容:**
```
automation/
├── google_services/
│   ├── google_drive.py      # Google Drive操作
│   ├── google_sheets.py     # Google Sheets操作
│   ├── google_calendar.py   # Google Calendar操作
│   ├── gmail.py             # Gmail操作
│   └── ga4.py               # GA4データ取得
└── __init__.py
```

**使用方法:**
```bash
# Cursor内で実行
python automation/google_services/google_sheets.py --read <spreadsheet_id>
python automation/google_services/ga4.py --property 505457597
```

---

### Phase 2: Cursorから簡単に実行できるようにする（効率化）

**目的:**
- Cursorからワンコマンドで実行可能にする

**実装内容:**
- シェルスクリプトやエイリアスを作成
- または、Pythonスクリプトを実行可能にする

**使用方法:**
```bash
# 簡単なコマンドで実行
./scripts/google-sheets-read.sh <spreadsheet_id>
./scripts/ga4-report.sh
```

---

### Phase 3: カスタムMCPサーバーを作成（将来的に）

**目的:**
- Cursorから直接操作可能にする（完全統合）

**実装内容:**
- Node.jsまたはPythonでMCPサーバーを実装
- CursorのMCP設定に追加

**使用方法:**
```
Cursor内で直接操作可能
「Googleスプレッドシートからデータを読み込んでください」
「GA4のアクセス解析データを取得してください」
```

---

## 🔧 実装例

### 例1: Google Sheets読み込みスクリプト

```python
# automation/google_services/google_sheets.py
from google.oauth2 import service_account
from googleapiclient.discovery import build

def read_spreadsheet(spreadsheet_id, range_name):
    """Googleスプレッドシートからデータを読み込む"""
    credentials = service_account.Credentials.from_service_account_file(
        '~/.config/cursor/google-drive-credentials.json',
        scopes=['https://www.googleapis.com/auth/spreadsheets.readonly']
    )
    
    service = build('sheets', 'v4', credentials=credentials)
    result = service.spreadsheets().values().get(
        spreadsheetId=spreadsheet_id,
        range=range_name
    ).execute()
    
    return result.get('values', [])

if __name__ == '__main__':
    import sys
    spreadsheet_id = sys.argv[1] if len(sys.argv) > 1 else 'your_spreadsheet_id'
    data = read_spreadsheet(spreadsheet_id, 'Sheet1!A1:D10')
    print(data)
```

**使用方法:**
```bash
python automation/google_services/google_sheets.py <spreadsheet_id>
```

---

### 例2: GA4データ取得スクリプト

```python
# automation/google_services/ga4.py
from google.oauth2 import service_account
from google.analytics.data_v1beta import BetaAnalyticsDataClient
from google.analytics.data_v1beta.types import RunReportRequest

def get_ga4_data(property_id):
    """GA4からアクセス解析データを取得"""
    credentials = service_account.Credentials.from_service_account_file(
        '~/.config/cursor/google-drive-credentials.json',
        scopes=['https://www.googleapis.com/auth/analytics.readonly']
    )
    
    client = BetaAnalyticsDataClient(credentials=credentials)
    
    request = RunReportRequest(
        property=f"properties/{property_id}",
        date_ranges=[{"start_date": "7daysAgo", "end_date": "today"}],
        metrics=[{"name": "sessions"}, {"name": "screenPageViews"}],
    )
    
    response = client.run_report(request)
    return response

if __name__ == '__main__':
    import sys
    property_id = sys.argv[1] if len(sys.argv) > 1 else '505457597'
    data = get_ga4_data(property_id)
    print(data)
```

**使用方法:**
```bash
python automation/google_services/ga4.py 505457597
```

---

## 💡 推奨アプローチ

### 即座に実装（Phase 1）
1. **Pythonスクリプトを作成**
   - Googleサービス操作用のスクリプト
   - Cursorから実行可能

2. **STEP 2（自動記事生成）で使用**
   - スプレッドシートからデータ読み込み
   - GA4データ取得

### 効率化（Phase 2）
1. **実行を簡略化**
   - シェルスクリプトやエイリアスを作成
   - ワンコマンドで実行可能に

### 完全統合（Phase 3）
1. **カスタムMCPサーバーを作成**
   - Cursorから直接操作可能に
   - 「Cursor一つで全て」を実現

---

## 📝 まとめ

### 「毎回Pythonスクリプトを使用する」のではなく：

1. **Phase 1（即座に可能）:**
   - Pythonスクリプトを作成
   - Cursorから実行可能にする
   - スクリプトは一度作成すれば再利用可能

2. **Phase 2（効率化）:**
   - 実行を簡略化
   - ワンコマンドで実行可能に

3. **Phase 3（将来的に）:**
   - カスタムMCPサーバーを作成
   - Cursorから直接操作可能に（完全統合）

**つまり、スクリプトは一度作成すれば、いつでも再利用可能です。毎回新しく作成する必要はありません。**

---

## 🚀 次のステップ

1. **Phase 1: Pythonスクリプトを作成**（即座に可能）
   - STEP 2（自動記事生成）で使用するスクリプト
   - GA4データ取得スクリプト

2. **必要に応じてPhase 2-3を実装**
   - 効率化や完全統合

準備ができたら、まずはPhase 1から始めましょう！
