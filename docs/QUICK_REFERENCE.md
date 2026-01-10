# クイックリファレンス

## ✅ Phase 1-2: すぐに使える（動作確認済み）

### Google Sheets操作

```bash
# Pythonスクリプト
python3 automation/google_services/google_sheets.py read <spreadsheet_id> [range]

# シェルスクリプト（簡易版）
./scripts/google-sheets-read.sh <spreadsheet_id> [range]

# スプレッドシート一覧取得
python3 automation/google_services/google_sheets.py list [query]
```

### GA4データ取得

```bash
# Pythonスクリプト
python3 automation/google_services/ga4.py summary 505457597 7

# シェルスクリプト（簡易版）
./scripts/ga4-report.sh summary 505457597 7
```

---

## ⚠️ Phase 3: MCPサーバー（修正済み、動作確認待ち）

### 現在の状態

- ✅ コード修正完了（stdio経由でMCPプロトコル実装）
- ⏳ Cursor再起動後の動作確認が必要

### 動作確認方法

1. **Cursorを再起動**（`Cmd + Q`で完全終了後、再起動）
2. **設定画面を確認**（`Cmd + ,` → 「Tools & MCP」）
3. **google-services MCPサーバーの状態を確認**
   - エラーが解消されているか確認
   - 「Show Output」をクリックしてエラーメッセージを確認

### エラーが続く場合

**Phase 1-2を使用してください**（完全に動作可能）：
- Pythonスクリプトまたはシェルスクリプトで実行
- Cursorから実行可能

---

## 🚀 次のステップ（優先順位順）

### 1. 現サイト管理・運営効率化 ⏳

**実装内容:**
- GA4データ取得の自動化
- サイトパフォーマンス分析スクリプト作成

**使用方法（Phase 1-2）:**
```bash
# GA4サマリー取得
python3 automation/google_services/ga4.py summary 505457597 7
```

### 2. STEP 2: 自動記事生成実装 ⏳

**実装内容:**
- スプレッドシートからデータ読み込み
- 記事生成プロンプトの最適化
- バッチ生成スクリプト作成

**使用方法（Phase 1-2）:**
```bash
# スプレッドシートからデータ読み込み
python3 automation/google_services/google_sheets.py read <spreadsheet_id> 'Sheet1!A1:D10'
```

### 3. 自動ツイート（X）実装 ⏳

**実装内容:**
- X API認証設定
- ツイート文案自動生成
- 予約投稿システム構築

### 4. STEP 1: 診断ツール実装 ⏳

**実装内容:**
- 診断ロジックの実装
- HTML/CSS/JavaScriptコード作成
- SWELLへの統合

---

## 📝 まとめ

**Phase 1-2は完全に動作可能**です。必要な機能をすぐに実装できます。

**Phase 3（MCPサーバー）は修正済み**ですが、Cursor再起動後の動作確認が必要です。

**エラーが続く場合は、Phase 1-2を使用してください。**
