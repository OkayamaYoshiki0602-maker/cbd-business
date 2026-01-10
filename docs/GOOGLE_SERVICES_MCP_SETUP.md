# GoogleサービスMCP連携セットアップガイド

## 📋 連携対象サービス

以下のGoogleサービスをCursorと連携し、**Cursor一つで全て操作可能**にします：

1. ✅ **Google Drive**（既に設定済み）
2. ✅ **Googleスプレッドシート**（Google Drive MCPで利用可能）
3. ⏳ **Googleカレンダー**（新規追加）
4. ⏳ **Gmail**（新規追加）
5. ✅ **GA4 (Google Analytics 4)**（既に連携済み）

---

## 🎯 目標

**Cursor一つで全て操作可能にする**
- Googleカレンダー: イベント作成・参照・更新
- Gmail: メール送信・受信・管理
- Googleスプレッドシート: データ読み込み・書き込み・管理
- Google Drive: ファイル管理
- GA4: アクセス解析データの取得・分析

---

## 📊 現在の連携状況

### ✅ 既に設定済み
- **GitHub MCP**: GitHubリポジトリ情報の読み込み
- **Google Drive MCP**: スプレッドシートの読み込み
- **GA4**: https://analytics.google.com で連携済み（`okayamayoshiki0602o@gmail.com`）

### ⏳ 追加が必要
- **Googleカレンダー MCP**: カレンダー操作
- **Gmail MCP**: メール操作
- **GA4 MCP**: Cursorから直接GA4データにアクセス

---

## 🚀 セットアップ手順

### PART 1: Google APIの有効化（既存プロジェクトを利用）

既にGoogle Cloud Consoleでプロジェクトを作成済み（`acoustic-skein-329303`）なので、既存プロジェクトを使用します。

#### STEP 1: 必要なAPIを有効化

1. **Google Cloud Consoleにアクセス**
   - https://console.cloud.google.com にアクセス
   - 既存のプロジェクト `acoustic-skein-329303` を選択

2. **APIとサービス → ライブラリに移動**
   - 左メニューの「APIとサービス」→「ライブラリ」をクリック

3. **以下のAPIを有効化**（まだ有効化していない場合）
   - ✅ **Google Drive API**（既に有効化済み）
   - ⏳ **Google Calendar API**（新規有効化）
   - ⏳ **Gmail API**（新規有効化）
   - ⏳ **Google Sheets API**（新規有効化、Drive APIと併用可能）
   - ⏳ **Google Analytics Data API**（新規有効化、GA4用）

#### STEP 2: 認証情報の確認・追加

既存のサービスアカウント（`cursor-mcp@acoustic-skein-329303.iam.gserviceaccount.com`）を使用します。

1. **APIとサービス → 認証情報に移動**
   - 既存のサービスアカウントを確認

2. **必要に応じて新しい認証情報を作成**
   - OAuth 2.0 クライアントID（Gmail・カレンダー用、個人アカウントアクセス用）

---

### PART 2: サービスアカウントの権限設定

#### Googleカレンダー

1. **Googleカレンダーの共有設定**
   - https://calendar.google.com にアクセス
   - 左側の「マイカレンダー」からカレンダーを選択
   - 「設定と共有」をクリック
   - 「特定のユーザーと共有」セクションで、サービスアカウントのメールアドレス（`cursor-mcp@acoustic-skein-329303.iam.gserviceaccount.com`）を追加
   - 権限: 「変更可能なイベントを表示」または「変更と共有の権限を管理」を選択

#### Gmail

1. **Gmail APIの有効化**
   - Google Cloud ConsoleでGmail APIを有効化
   - 注意: Gmail APIはサービスアカウントでは直接使用できない場合があります
   - OAuth 2.0認証が必要な場合があります

#### Googleスプレッドシート

1. **スプレッドシートの共有設定**
   - 既にGoogle Drive MCPで対応可能
   - サービスアカウントのメールアドレスで共有設定済み

#### GA4

1. **GA4の管理画面で権限付与**
   - https://analytics.google.com にアクセス
   - 「管理」→「プロパティアクセス管理」をクリック
   - 「＋」ボタンをクリック
   - サービスアカウントのメールアドレス（`cursor-mcp@acoustic-skein-329303.iam.gserviceaccount.com`）を追加
   - 権限: 「表示者」または「編集者」を選択

---

### PART 3: MCP設定ファイルの更新

既存のMCP設定ファイルに、新規サービスを追加します。

#### 設定ファイルの場所
```
~/Library/Application Support/Cursor/User/globalStorage/saoudrizwan.claude-dev/settings/cline_mcp_settings.json
```

#### 追加する設定

```json
{
  "mcpServers": {
    "github": {
      "command": "npx",
      "args": [
        "-y",
        "@modelcontextprotocol/server-github"
      ],
      "env": {
        "GITHUB_TOKEN": "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"
      }
    },
    "google-drive": {
      "command": "npx",
      "args": [
        "-y",
        "@modelcontextprotocol/server-google-drive"
      ],
      "env": {
        "GOOGLE_DRIVE_CREDENTIALS": "/Users/okayamayoshiki/.config/cursor/google-drive-credentials.json"
      }
    },
    "google-calendar": {
      "command": "npx",
      "args": [
        "-y",
        "@modelcontextprotocol/server-google-calendar"
      ],
      "env": {
        "GOOGLE_APPLICATION_CREDENTIALS": "/Users/okayamayoshiki/.config/cursor/google-drive-credentials.json"
      }
    },
    "gmail": {
      "command": "npx",
      "args": [
        "-y",
        "@modelcontextprotocol/server-gmail"
      ],
      "env": {
        "GOOGLE_APPLICATION_CREDENTIALS": "/Users/okayamayoshiki/.config/cursor/google-drive-credentials.json"
      }
    },
    "google-sheets": {
      "command": "npx",
      "args": [
        "-y",
        "@modelcontextprotocol/server-google-sheets"
      ],
      "env": {
        "GOOGLE_APPLICATION_CREDENTIALS": "/Users/okayamayoshiki/.config/cursor/google-drive-credentials.json"
      }
    },
    "ga4": {
      "command": "npx",
      "args": [
        "-y",
        "@modelcontextprotocol/server-ga4"
      ],
      "env": {
        "GOOGLE_APPLICATION_CREDENTIALS": "/Users/okayamayoshiki/.config/cursor/google-drive-credentials.json",
        "GA4_PROPERTY_ID": "505457597"
      }
    }
  }
}
```

**注意:** 実際のMCPサーバーパッケージ名は、利用可能なものを確認する必要があります。

---

## 📝 実装ステップ

### ステップ1: API有効化（あなたがやること）

1. **Google Cloud ConsoleでAPIを有効化**
   - Google Calendar API
   - Gmail API
   - Google Sheets API
   - Google Analytics Data API

2. **各サービスで権限を付与**
   - Googleカレンダー: サービスアカウントで共有
   - GA4: サービスアカウントに権限付与

### ステップ2: MCP設定ファイル更新（私がやること）

1. ✅ MCP設定ファイルに新規サービスを追加
2. ✅ 認証情報のパスを確認・設定
3. ✅ GA4のプロパティIDを設定（`505457597`）

### ステップ3: 動作確認（あなたがやること）

1. **Cursorを再起動**
2. **各サービスが動作するか確認**

---

## ⚠️ 注意事項

### Gmail APIの認証

Gmail APIは**OAuth 2.0認証**が必要な場合があります。サービスアカウントでは直接使用できない可能性があります。

**解決策:**
1. OAuth 2.0 クライアントIDを作成
2. 認証フローを実行してトークンを取得
3. MCPサーバーでトークンを使用

### Googleカレンダーの共有

サービスアカウントでカレンダーを共有する必要があります。個人のカレンダーを共有する場合は、プライバシーに注意してください。

### GA4のプロパティID

既に確認済み: `505457597`（`https://cbd-no-hito.com/`）

---

## 🔍 利用可能なMCPサーバーの確認

実際に利用可能なMCPサーバーパッケージを確認する必要があります。

**確認方法:**
```bash
npm search @modelcontextprotocol/server-google
```

または、公式ドキュメントを確認:
- https://github.com/modelcontextprotocol/servers

---

## 📋 チェックリスト

### API有効化
- [ ] Google Calendar API
- [ ] Gmail API
- [ ] Google Sheets API（既にDrive APIで利用可能か確認）
- [ ] Google Analytics Data API

### 権限設定
- [ ] Googleカレンダー: サービスアカウントで共有
- [ ] GA4: サービスアカウントに権限付与
- [ ] Googleスプレッドシート: 既に共有済み（確認）

### MCP設定
- [ ] MCP設定ファイルに新規サービスを追加
- [ ] 認証情報のパスを確認
- [ ] GA4プロパティIDを設定

### 動作確認
- [ ] Cursorを再起動
- [ ] 各サービスが動作するか確認

---

## 🚀 次のステップ

1. **Google Cloud ConsoleでAPIを有効化**
2. **各サービスで権限を付与**
3. **私がMCP設定ファイルを更新**
4. **Cursorを再起動して動作確認**

準備ができたら、まずはAPI有効化から始めましょう！
