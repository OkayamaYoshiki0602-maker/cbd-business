# MCP連携ステータス確認

## 🔍 現在の状況

### 確認結果
- ❌ **MCPリソースが検出されませんでした**
- ✅ **MCP設定ファイル**: 正しく設定されていることを確認済み
- ⚠️ **Node.js**: インストールされていない（前回確認時）

---

## 🔧 考えられる原因と対応

### 原因1: Node.jsがインストールされていない

**確認方法:**
```bash
node --version
npm --version
```

**対応:**
Node.jsをインストールする必要があります：

```bash
# Homebrewでインストール（推奨）
brew install node

# または公式サイトから
# https://nodejs.org/
```

インストール後、Cursorを再起動してください。

---

### 原因2: MCPサーバーパッケージが存在しない

**可能性:**
設定ファイルで使用しているパッケージ名（例: `@modelcontextprotocol/server-google-calendar`）が実際には存在しない可能性があります。

**確認方法:**
```bash
# Node.jsインストール後
npm search @modelcontextprotocol/server-google
```

**対応:**
実際に存在するパッケージ名に修正する必要があります。

公式のMCPサーバーリストを確認:
- https://github.com/modelcontextprotocol/servers

---

### 原因3: CursorのMCP設定でエラーが発生している

**確認方法:**
1. Cursorの設定を開く（`Cmd + ,`）
2. 「Features」→「MCP」セクションを確認
3. エラーメッセージがないか確認

**対応:**
エラーメッセージに基づいて対応してください。

---

### 原因4: 認証情報の問題

**確認方法:**
```bash
ls -la ~/.config/cursor/google-drive-credentials.json
cat ~/.config/cursor/google-drive-credentials.json | python3 -m json.tool
```

**対応:**
認証情報ファイルが正しく配置されているか、JSON形式が正しいか確認してください。

---

## 🚀 推奨対応手順

### STEP 1: Node.jsのインストール

```bash
# Homebrewがインストールされているか確認
brew --version

# Homebrewがインストールされていない場合
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"

# Node.jsをインストール
brew install node

# インストール確認
node --version
npm --version
npx --version
```

### STEP 2: Cursorを再起動

1. Cursorを完全に終了（`Cmd + Q`）
2. Cursorを再起動

### STEP 3: MCP設定を確認

1. Cursorの設定を開く（`Cmd + ,`）
2. 「Features」→「MCP」セクションを確認
3. エラーメッセージがないか確認

### STEP 4: 動作確認

Cursor再起動後、再度MCPリソースが検出されるか確認してください。

---

## 📋 チェックリスト

- [ ] Node.jsがインストールされているか確認
- [ ] npmがインストールされているか確認
- [ ] npxが利用可能か確認
- [ ] Cursorを再起動
- [ ] CursorのMCP設定でエラーがないか確認
- [ ] MCPリソースが検出されるか確認

---

## 💡 次のステップ

1. **Node.jsをインストール**（最優先）
2. **Cursorを再起動**
3. **再度MCPリソースを確認**
4. **エラーが続く場合は、実際のMCPサーバーパッケージ名を確認**

---

## 📝 参考

- [Node.js公式サイト](https://nodejs.org/)
- [Homebrew公式サイト](https://brew.sh/)
- [MCPサーバーリスト](https://github.com/modelcontextprotocol/servers)
