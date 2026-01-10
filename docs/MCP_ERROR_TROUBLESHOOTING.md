# MCPサーバーエラー対応ガイド

## 🔍 現在の状況

### ✅ 正常に動作しているMCPサーバー
- **GitHub MCP**: 26 tools enabled（正常動作）

### ❌ エラーが発生しているMCPサーバー
- **ga4**: Error
- **gmail**: Error
- **google-calendar**: Error
- **google-drive**: Error
- **google-sheets**: Error

---

## 🎯 原因の可能性

### 可能性1: MCPサーバーパッケージが存在しない

**問題:**
設定ファイルで使用しているパッケージ名（例: `@modelcontextprotocol/server-google-calendar`）が実際には存在しない可能性があります。

**確認方法:**
```bash
npm search @modelcontextprotocol/server-google
npx @modelcontextprotocol/server-google-calendar --version
```

### 可能性2: 認証情報の問題

**問題:**
- 認証情報ファイルのパスが間違っている
- サービスアカウントに権限がない
- APIが有効化されていない

**確認方法:**
```bash
ls -la ~/.config/cursor/google-drive-credentials.json
cat ~/.config/cursor/google-drive-credentials.json | python3 -m json.tool
```

### 可能性3: 環境変数の問題

**問題:**
環境変数名や値が正しく設定されていない可能性があります。

**確認方法:**
設定ファイル（`.cursor/mcp.json`）の環境変数名を確認

---

## 🔧 対応手順

### STEP 1: エラー出力を確認

1. **Cursorの設定画面で「Show Output」をクリック**
   - 各エラーがあるMCPサーバーの「Error - Show Output」をクリック
   - エラーメッセージを確認

2. **エラーメッセージの内容を記録**
   - 「Package not found」などのエラーか確認
   - 認証エラーか確認
   - その他のエラーか確認

### STEP 2: パッケージの存在確認

実際に利用可能なMCPサーバーパッケージを確認します。

**公式MCPサーバーリスト:**
- https://github.com/modelcontextprotocol/servers

**一般的なGoogle MCPサーバー:**
- Google Drive: `@modelcontextprotocol/server-google-drive`（存在確認済み）
- その他のGoogleサービス: 存在しない可能性

### STEP 3: 代替案の検討

#### 案1: 汎用のGoogle API MCPサーバーを使用

1つのMCPサーバーで複数のGoogleサービスにアクセスできるパッケージがある可能性があります。

#### 案2: Google Drive MCPのみを使用

Google Drive MCPは既に存在するため、以下の機能を活用：
- Google Drive: ファイル管理
- Googleスプレッドシート: Google Drive経由でアクセス可能

#### 案3: カスタムMCPサーバーを作成

必要に応じて、カスタムMCPサーバーを作成する可能性があります。

---

## 📋 確認チェックリスト

- [ ] 各MCPサーバーのエラー出力を確認
- [ ] エラーメッセージの内容を記録
- [ ] パッケージが実際に存在するか確認
- [ ] 認証情報が正しいか確認
- [ ] APIが有効化されているか確認

---

## 🚀 次のステップ

1. **エラー出力を確認**（最優先）
   - Cursorの設定画面で「Show Output」をクリック
   - エラーメッセージの内容を確認

2. **実際に存在するパッケージを確認**
   - npm searchで確認
   - 公式ドキュメントで確認

3. **必要に応じて設定を修正**
   - 正しいパッケージ名に修正
   - または、存在しないパッケージを削除

---

## 💡 推奨対応

まずは**エラー出力を確認**して、具体的なエラーメッセージを特定することが重要です。

エラーメッセージの内容に基づいて、適切な対応を行います。
