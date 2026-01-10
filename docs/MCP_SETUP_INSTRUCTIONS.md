# MCP連携セットアップ手順

## 📍 設定ファイルの場所

### macOS (Cursor)
```
~/Library/Application Support/Cursor/User/globalStorage/saoudrizwan.claude-dev/settings/cline_mcp_settings.json
```

または Cursor設定内の `Features` → `MCP Settings` から直接編集可能

---

## 🔧 GitHub MCP連携

### 1. Personal Access Token (PAT) の取得

1. GitHubにログイン
2. 右上のプロフィールアイコン → `Settings`
3. 左メニューの `Developer settings` → `Personal access tokens` → `Tokens (classic)`
4. `Generate new token (classic)` をクリック
5. 以下を設定:
   - **Note:** `Cursor MCP Integration`
   - **Expiration:** 任意（90日、1年等）
   - **Select scopes:** 以下を選択
     - ✅ `repo` (すべてのリポジトリ)
     - ✅ `read:org` (組織情報の読み取り)
6. `Generate token` をクリック
7. **トークンをコピー**（一度しか表示されないので注意！）

### 2. CursorのMCP設定に追加

`mcp_settings_template.json` の内容を参考に、以下を設定：

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
        "GITHUB_TOKEN": "ghp_xxxxxxxxxxxxxxxxxxxx"  // ここに取得したPATを貼り付け
      }
    }
  }
}
```

### 3. 動作確認

Cursorを再起動後、以下をテスト：
- GitHubリポジトリ情報の読み込み
- Issue作成・参照
- PR管理

---

## 📁 Google Drive MCP連携

### 1. Google Cloud Console でプロジェクト作成

1. [Google Cloud Console](https://console.cloud.google.com/) にアクセス
2. 新しいプロジェクトを作成（例: `cbd-side-business`）
3. プロジェクトを選択

### 2. Google Drive API を有効化

1. `APIとサービス` → `ライブラリ` に移動
2. 「Google Drive API」を検索
3. `有効にする` をクリック

### 3. 認証情報（JSON）の取得

1. `APIとサービス` → `認証情報` に移動
2. `認証情報を作成` → `サービスアカウント` を選択
3. 以下を入力:
   - **サービスアカウント名:** `cursor-mcp`
   - **サービスアカウントID:** 自動生成
   - **説明:** `Cursor MCP Integration for Google Drive`
4. `作成して続行` をクリック
5. **ロール:** `エディター` または `閲覧者` を選択
6. `完了` をクリック
7. 作成したサービスアカウントをクリック
8. `キー` タブ → `キーを追加` → `JSONを作成`
9. **JSONファイルをダウンロード**

### 4. 認証情報ファイルの配置

```bash
mkdir -p ~/.config/cursor
mv ~/Downloads/your-project-xxxxx-xxxxxxxxxxxx.json ~/.config/cursor/google-drive-credentials.json
```

### 5. Google Driveの共有設定

1. Google Driveで共有したいスプレッドシートを開く
2. `共有` をクリック
3. サービスアカウントのメールアドレス（`cursor-mcp@your-project.iam.gserviceaccount.com`）を追加
4. 権限: `閲覧者` または `編集者` を選択

### 6. CursorのMCP設定に追加

```json
{
  "mcpServers": {
    "google-drive": {
      "command": "npx",
      "args": [
        "-y",
        "@modelcontextprotocol/server-google-drive"
      ],
      "env": {
        "GOOGLE_DRIVE_CREDENTIALS": "~/.config/cursor/google-drive-credentials.json"
      }
    }
  }
}
```

### 7. 動作確認

Cursorを再起動後、以下をテスト：
- スプレッドシートの読み込み
- データの参照

---

## 🎯 統合設定例（両方有効化）

`cline_mcp_settings.json` に以下を設定：

```json
{
  "mcpServers": {
    "google-drive": {
      "command": "npx",
      "args": [
        "-y",
        "@modelcontextprotocol/server-google-drive"
      ],
      "env": {
        "GOOGLE_DRIVE_CREDENTIALS": "~/.config/cursor/google-drive-credentials.json"
      }
    },
    "github": {
      "command": "npx",
      "args": [
        "-y",
        "@modelcontextprotocol/server-github"
      ],
      "env": {
        "GITHUB_TOKEN": "ghp_xxxxxxxxxxxxxxxxxxxx"
      }
    }
  }
}
```

---

## ⚠️ セキュリティ注意事項

1. ✅ **認証情報はローカルのみ保存**
   - `.gitignore` で除外済み（`*.json`, `.env`等）
   - GitHubには絶対にプッシュしない

2. ✅ **PATの権限は最小限に**
   - GitHub PATは必要なスコープのみ選択

3. ✅ **サービスアカウントの権限は最小限に**
   - Google Driveの共有は必要なファイルのみ

4. ✅ **定期的にトークンを更新**
   - GitHub PATは有効期限を設定
   - 定期的に確認・更新

---

## 🔍 トラブルシューティング

### MCPサーバーが動作しない場合

1. Cursorを再起動
2. MCP設定ファイルのJSON構文を確認（カンマ、引用符等）
3. 認証情報のパスが正しいか確認（`~` は展開されるか確認）
4. Node.jsがインストールされているか確認: `node --version`

### Google Drive API エラー

- スプレッドシートの共有設定を確認
- サービスアカウントのメールアドレスが正しく共有されているか確認
- APIが有効になっているか確認

### GitHub API エラー

- PATが有効か確認（GitHub Settings → Developer settings → Personal access tokens）
- 必要なスコープが付与されているか確認

---

## 📝 次のステップ

1. ✅ GitHub PATを取得 → MCP設定に追加
2. ✅ Google Drive API認証情報を取得 → MCP設定に追加
3. ✅ Cursor再起動 → 動作確認
4. ✅ テスト（スプレッドシート読み込み、GitHub操作）
