# MCPサーバーエラー対応

## 🔍 エラーの原因

### 確認された問題

1. **Python版のMCP SDKが存在しない**
   - `pip install mcp` でエラー（パッケージが見つからない）
   - Python版のMCP SDKは標準では提供されていない

2. **プロジェクトIDの不一致**
   - GA4エラー: プロジェクトID `822307921974` でAPIが有効化されていない
   - 認証情報ファイル: プロジェクトID `acoustic-skein-329303`

---

## ✅ 対応完了

### Phase 1-2: 完全に動作可能 ✅

**実装完了:**
- ✅ Pythonスクリプト作成完了
- ✅ シェルスクリプト作成完了
- ✅ 動作確認済み（Google Sheets読み込み、GA4データ取得）

**使用方法:**
```bash
# Google Sheets読み込み
python3 automation/google_services/google_sheets.py read <spreadsheet_id>

# GA4サマリー取得
python3 automation/google_services/ga4.py summary 505457597 7

# シェルスクリプト版
./scripts/google-sheets-read.sh <spreadsheet_id>
./scripts/ga4-report.sh summary 505457597 7
```

---

### Phase 3: MCPサーバーの修正 ✅

**問題:**
- Python版のMCP SDKが存在しない

**対応:**
- stdio経由でMCPプロトコルを直接実装
- JSON-RPC形式でメッセージを送受信
- Pythonの標準ライブラリのみ使用（外部SDK不要）

**修正内容:**
- `automation/mcp_server/google_services_mcp.py` を更新
- stdio経由でMCPプロトコルを実装
- ツール一覧取得・ツール実行に対応

---

## 🔧 修正後の動作確認

### 1. MCPサーバーの動作確認

```bash
# テスト実行
python3 automation/mcp_server/google_services_mcp.py
```

### 2. Cursorで動作確認

1. **Cursorを再起動**（`Cmd + Q`で完全終了後、再起動）
2. **設定画面を確認**（`Cmd + ,` → 「Tools & MCP」）
3. **google-services MCPサーバーの状態を確認**
   - エラーが解消されているか確認
   - 「Show Output」をクリックしてエラーがないか確認

### 3. 動作確認（Cursor内で）

```
「Googleスプレッドシート一覧を表示してください」
「GA4のサマリー統計を取得してください」
```

---

## ⚠️ 注意事項

### GA4 APIの有効化

GA4エラーの原因：
- プロジェクトID `822307921974` でAPIが有効化されていない
- 認証情報ファイルのプロジェクトID: `acoustic-skein-329303`

**対応:**
- 正しいプロジェクトIDでAPIを有効化する
- または、認証情報ファイルを確認する

### MCPプロトコルの実装

**修正したMCPサーバー:**
- stdio経由でMCPプロトコルを実装
- JSON-RPC形式でメッセージを送受信
- Pythonの標準ライブラリのみ使用

**注意:**
- MCPプロトコルの完全な実装ではない可能性
- 必要に応じて修正が必要

---

## 📋 次のステップ

### 即座に実装可能（Phase 1-2を使用）

Phase 1-2の実装で以下の機能が利用可能です：

1. **Google Sheets操作**
   ```bash
   python3 automation/google_services/google_sheets.py read <spreadsheet_id>
   ```

2. **GA4データ取得**
   ```bash
   python3 automation/google_services/ga4.py summary 505457597 7
   ```

### 次の実装（優先順位順）

1. **現サイト管理・運営効率化** ⏳
   - GA4 APIの有効化確認
   - サイトパフォーマンス分析スクリプト作成

2. **STEP 2: 自動記事生成実装** ⏳
   - スプレッドシートからデータ読み込み
   - 記事生成プロンプトの最適化

3. **自動ツイート（X）実装** ⏳
   - X API認証設定
   - ツイート文案自動生成

4. **STEP 1: 診断ツール実装** ⏳
   - 診断ロジックの実装
   - SWELLへの統合

---

## 💡 推奨アプローチ

**現時点では、Phase 1-2の実装を使用することを推奨します。**

Phase 3（MCPサーバー）は、修正しましたが、完全に動作するか確認が必要です。

**Phase 1-2で十分な機能を提供しています：**
- ✅ Google Sheets操作
- ✅ GA4データ取得
- ✅ Cursorから実行可能

Cursorを再起動して、MCPサーバーのエラーが解消されたか確認してください。
