# MCP設定ファイルの場所について

## 🔍 問題点

Cursorの設定画面に「No MCP Tools」と表示され、MCPサーバーが認識されていませんでした。

**原因:**
- Cursorは2つの場所でMCP設定を読み込みます：
  1. **グローバル設定**: `~/Library/Application Support/Cursor/User/globalStorage/saoudrizwan.claude-dev/settings/cline_mcp_settings.json`
  2. **プロジェクト設定**: `<project-root>/.cursor/mcp.json` ← **こちらも必要**

## ✅ 対応

### STEP 1: プロジェクトルートに`.cursor/mcp.json`を作成

プロジェクトルート（`cursor/`ディレクトリ）に`.cursor/mcp.json`を作成しました。

このファイルは、グローバル設定と同じ内容ですが、**プロジェクト固有の設定**として扱われます。

### STEP 2: Cursorを再起動

1. **Cursorを完全に終了**（`Cmd + Q`）
2. **Cursorを再起動**
3. **設定画面を確認**（`Cmd + ,` → 「Tools & MCP」）

## 📋 設定ファイルの場所

### グローバル設定
```
~/Library/Application Support/Cursor/User/globalStorage/saoudrizwan.claude-dev/settings/cline_mcp_settings.json
```
- 全プロジェクトで有効
- ユーザー全体の設定

### プロジェクト設定（新規追加）
```
.cursor/mcp.json
```
- このプロジェクトのみ有効
- プロジェクト固有の設定

**両方の設定が存在する場合、プロジェクト設定（`.cursor/mcp.json`）が優先されます。**

## 🔧 設定ファイルの内容

両方のファイルに、以下のMCPサーバーが設定されています：

1. **GitHub MCP** - GitHubリポジトリ情報
2. **Google Drive MCP** - Google Driveファイル
3. **Google Calendar MCP** - Googleカレンダー
4. **Gmail MCP** - Gmail
5. **Google Sheets MCP** - Googleスプレッドシート
6. **GA4 MCP** - Google Analytics 4

## ⚠️ 注意事項

### .gitignoreについて

`.cursor/mcp.json`は設定ファイルですが、認証情報を含まないため、Gitにコミット対象としました。

**認証情報（PATやJSON認証情報）は環境変数や別ファイルで管理**することを推奨しますが、現在の設定では：
- GitHub PATは設定ファイルに直接記載（`.gitignore`で除外済み）
- Google認証情報は`~/.config/cursor/google-drive-credentials.json`に保存（`.gitignore`で除外済み）

### Node.jsのインストール

MCPサーバーは`npx`経由で実行されるため、**Node.jsがインストールされている必要があります**。

```bash
# Homebrewでインストール（完了済み）
brew install node

# 確認
node --version
npm --version
npx --version
```

## 🚀 次のステップ

1. ✅ **Node.jsのインストール確認**（完了済み）
2. ✅ **`.cursor/mcp.json`の作成**（完了済み）
3. ⏳ **Cursorを再起動**
4. ⏳ **設定画面でMCPサーバーが表示されるか確認**

## 📝 トラブルシューティング

### MCPサーバーが表示されない場合

1. **`.cursor/mcp.json`が正しい場所にあるか確認**
   ```bash
   ls -la .cursor/mcp.json
   ```

2. **JSON形式が正しいか確認**
   ```bash
   cat .cursor/mcp.json | python3 -m json.tool
   ```

3. **Cursorを完全に再起動**
   - `Cmd + Q`で完全に終了
   - 再起動

4. **Node.jsがインストールされているか確認**
   ```bash
   node --version
   ```

5. **Cursorのログを確認**
   - Cursorの設定からログを確認
   - エラーメッセージがないか確認

### MCPサーバーがエラーになる場合

1. **パッケージが存在するか確認**
   ```bash
   npm search @modelcontextprotocol/server-github
   ```

2. **実際に利用可能なパッケージ名を確認**
   - https://github.com/modelcontextprotocol/servers

3. **認証情報が正しいか確認**
   - GitHub PAT
   - Google認証情報ファイルのパス
