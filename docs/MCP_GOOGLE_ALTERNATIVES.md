# Googleサービス連携の代替案

## 🔍 状況

Google系のMCPサーバーパッケージは現在、公式には提供されていません：
- ❌ `@modelcontextprotocol/server-google-drive` - Not found
- ❌ `@modelcontextprotocol/server-google-calendar` - Not found
- ❌ `@modelcontextprotocol/server-gmail` - Not found
- ❌ `@modelcontextprotocol/server-google-sheets` - Not found
- ❌ `@modelcontextprotocol/server-ga4` - Not found

---

## 🚀 代替案

### 案1: PythonスクリプトでGoogle APIを直接使用（推奨）

**メリット:**
- ✅ すぐに実装可能
- ✅ 既存の認証情報を活用可能
- ✅ 柔軟な実装が可能

**実装例:**

```python
# automation/google-services.py
from google.oauth2 import service_account
from googleapiclient.discovery import build

# 認証情報を読み込み
SCOPES = ['https://www.googleapis.com/auth/drive.readonly']
SERVICE_ACCOUNT_FILE = '~/.config/cursor/google-drive-credentials.json'

credentials = service_account.Credentials.from_service_account_file(
    SERVICE_ACCOUNT_FILE, scopes=SCOPES)

# Google Drive APIを呼び出し
service = build('drive', 'v3', credentials=credentials)
results = service.files().list(pageSize=10).execute()
```

**対応サービス:**
- Google Drive API
- Google Calendar API
- Gmail API
- Google Sheets API
- Google Analytics Data API (GA4)

---

### 案2: カスタムMCPサーバーを作成

**メリット:**
- ✅ Cursorから直接操作可能
- ✅ 統一されたインターフェース

**実装方法:**
1. Node.jsまたはPythonでMCPサーバーを実装
2. Google APIと連携
3. CursorのMCP設定に追加

**参考:**
- [MCP SDK](https://github.com/modelcontextprotocol/sdk)
- [MCPサーバーの実装例](https://github.com/modelcontextprotocol/servers)

---

### 案3: 公式MCPサーバーの追加を待つ

**メリット:**
- ✅ 公式サポート
- ✅ メンテナンスが保証される

**デメリット:**
- ❌ 時期不明
- ❌ 実装待ち

---

## 📋 推奨実装順序

### Phase 1: Pythonスクリプトで実装（即座に可能）

1. **Google Drive/Sheets操作**
   - スプレッドシートの読み込み・書き込み
   - ファイル管理

2. **Google Calendar操作**
   - イベント作成・参照・更新

3. **GA4データ取得**
   - アクセス解析データの取得

4. **Gmail操作**
   - メール送信・受信（OAuth 2.0が必要な場合）

### Phase 2: カスタムMCPサーバー作成（将来的に）

必要に応じて、カスタムMCPサーバーを作成し、Cursorから直接操作可能にする。

---

## 🔧 実装準備

### 必要なライブラリ

```bash
pip install google-auth google-auth-oauthlib google-auth-httplib2
pip install google-api-python-client
```

### 認証情報

既に準備済み：
- ✅ サービスアカウント: `cursor-mcp@acoustic-skein-329303.iam.gserviceaccount.com`
- ✅ 認証情報ファイル: `~/.config/cursor/google-drive-credentials.json`
- ✅ オーナー権限: 全てのAPIにアクセス可能

---

## 💡 次のステップ

1. **PythonスクリプトでGoogle APIを使用**
   - STEP 2（自動記事生成）でスプレッドシートからデータ読み込み
   - GA4データ取得スクリプト作成

2. **必要に応じてカスタムMCPサーバーを作成**
   - Cursorから直接操作したい場合

3. **公式MCPサーバーの追加を待つ**
   - 公式で提供された場合に移行

---

## 📝 参考

- [Google API Python Client](https://github.com/googleapis/google-api-python-client)
- [Google API Node.js Client](https://github.com/googleapis/google-api-nodejs-client)
- [MCP SDK](https://github.com/modelcontextprotocol/sdk)
- [Google API Documentation](https://developers.google.com/apis-explorer)
