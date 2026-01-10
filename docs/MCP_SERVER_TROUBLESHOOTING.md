# MCPサーバーエラートラブルシューティング

## 🔍 エラーの原因と対応

### エラーが発生している場合

Cursorの設定画面で「Error - Show Output」をクリックして、エラーメッセージを確認してください。

### よくあるエラーと対応

#### エラー1: ImportError

**症状:**
```
Error importing Google services modules: No module named 'google_services'
```

**原因:**
- Pythonパスの問題
- モジュールのインポートエラー

**対応:**
1. スクリプトのパスを確認
2. モジュールのインポートパスを修正

#### エラー2: 認証エラー

**症状:**
```
Error: 認証情報ファイルが見つかりません
```

**原因:**
- 認証情報ファイルのパスが間違っている
- 認証情報ファイルが存在しない

**対応:**
1. 認証情報ファイルのパスを確認: `~/.config/cursor/google-drive-credentials.json`
2. ファイルが存在するか確認

#### エラー3: MCPプロトコルエラー

**症状:**
```
Method not found: initialize
```

**原因:**
- MCPプロトコルの実装が不完全

**対応:**
- スクリプトを修正（完了済み）

---

## 🔧 動作確認方法

### 手動テスト

```bash
# 1. 初期化メッセージのテスト
echo '{"jsonrpc": "2.0", "method": "initialize", "params": {}, "id": 1}' | python3 automation/mcp_server/google_services_mcp.py

# 2. ツール一覧取得のテスト
echo '{"jsonrpc": "2.0", "method": "tools/list", "params": {}, "id": 2}' | python3 automation/mcp_server/google_services_mcp.py
```

### Cursorでの確認

1. **Cursorを再起動**（`Cmd + Q`で完全終了後、再起動）
2. **設定画面を確認**（`Cmd + ,` → 「Tools & MCP」）
3. **「Error - Show Output」をクリック**
4. **エラーメッセージを確認**

---

## 📋 推奨対応

### 現時点では、Phase 1-2を使用

**Phase 1-2は完全に動作可能**です：

```bash
# Google Sheets操作
python3 automation/google_services/google_sheets.py read <spreadsheet_id>

# GA4データ取得
python3 automation/google_services/ga4.py summary 505457597 7

# シェルスクリプト版（簡易）
./scripts/google-sheets-read.sh <spreadsheet_id>
./scripts/ga4-report.sh summary 505457597 7
```

### Phase 3（MCPサーバー）について

**現時点では、Phase 1-2で十分な機能を提供しています。**

Phase 3は将来的に実装することを推奨します：
- Node.js版のMCPサーバーを作成
- または、Python版のMCP SDKが公開されたら移行

---

## 🚀 次のステップ

**エラーが続く場合、Phase 1-2を使用して実装を進めることを推奨します。**

次の実装（優先順位順）：
1. 現サイト管理・運営効率化（Phase 1-2を使用）
2. STEP 2: 自動記事生成実装（Phase 1-2を使用）
3. 自動ツイート（X）実装
4. STEP 1: 診断ツール実装
