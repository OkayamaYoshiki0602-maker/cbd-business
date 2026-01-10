# 開発環境セットアップガイド

## 現在の状態

- ✅ `.cursorrules` - Cursor最適化ルール（設定済み）
- ❌ Gitリポジトリ - 未初期化
- ❌ MCP連携 - 未設定（Google Drive等）
- ❌ `.gitignore` - 未作成
- ❌ GitHub連携 - 未設定

## セットアップ手順

### 1. Gitリポジトリ初期化とGitHub連携

#### 1-1. Git初期化
```bash
cd "/Users/okayamayoshiki/Library/CloudStorage/GoogleDrive-okayamayoshiki0602o@gmail.com/マイドライブ/cursor"
git init
```

#### 1-2. GitHubリポジトリ作成（推奨）
1. GitHubで新規リポジトリ作成: `cbd-side-business` など
2. リモート追加:
```bash
git remote add origin https://github.com/[あなたのユーザー名]/cbd-side-business.git
```

#### 1-3. 初期コミット
```bash
git add .
git commit -m "初期セットアップ: Cursor最適化ルールとプロジェクト計画"
git branch -M main
git push -u origin main
```

### 2. MCP連携設定（Google Drive）

#### 2-1. CursorのMCP設定確認
1. Cursor設定を開く（`Cmd + ,` または `Settings`）
2. `Features` → `MCP` を確認
3. Google Drive MCPサーバーを有効化

#### 2-2. Google Drive MCP設定手順
1. Cursor設定ファイルを開く
   - macOS: `~/Library/Application Support/Cursor/User/globalStorage/saoudrizwan.claude-dev/settings/cline_mcp_settings.json`
   - または Cursor設定内の `MCP Settings` から

2. 以下を追加（例）:
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
        "GOOGLE_DRIVE_CREDENTIALS": "/path/to/credentials.json"
      }
    }
  }
}
```

#### 2-3. Google Drive認証情報取得
1. Google Cloud Consoleでプロジェクト作成
2. Google Drive APIを有効化
3. 認証情報（JSON）をダウンロード
4. 上記のパスに配置

**参考:**
- [MCP Google Drive Server](https://github.com/modelcontextprotocol/servers/tree/main/src/google-drive)
- [Google Drive API セットアップ](https://developers.google.com/drive/api/quickstart/js)

### 3. その他のMCP連携（オプション）

#### 3-1. GitHub MCP（コード管理用）
```json
{
  "github": {
    "command": "npx",
    "args": [
      "-y",
      "@modelcontextprotocol/server-github"
    ],
    "env": {
      "GITHUB_PERSONAL_ACCESS_TOKEN": "your_token_here"
    }
  }
}
```

#### 3-2. Slack MCP（通知用、将来的に）
```json
{
  "slack": {
    "command": "npx",
    "args": [
      "-y",
      "@modelcontextprotocol/server-slack"
    ],
    "env": {
      "SLACK_BOT_TOKEN": "your_token_here"
    }
  }
}
```

### 4. 開発環境のセットアップ

#### 4-1. 必要なツールの確認
- [ ] Git（コマンドライン開発ツール）
- [ ] Node.js（MCPサーバー用、必要に応じて）
- [ ] Python（自動化スクリプト用、必要に応じて）

#### 4-2. Node.jsインストール（MCP用）
```bash
# Homebrewでインストール（推奨）
brew install node

# または公式サイトから
# https://nodejs.org/
```

#### 4-3. Python環境（自動化スクリプト用）
```bash
# Homebrewでインストール（推奨）
brew install python3

# 仮想環境作成（将来的に）
python3 -m venv venv
source venv/bin/activate
```

### 5. プロジェクト構成の整備

#### 5-1. ディレクトリ構成
```
cursor/
├── .cursorrules              # Cursor最適化ルール
├── .gitignore                # Git除外設定
├── README.md                 # プロジェクト概要
├── SETUP_GUIDE.md           # このファイル
├── PROJECT_PLAN.md          # 詳細計画
├── WORKFLOW.md              # ワークフロー
├── DIAGNOSIS_LOGIC_PROPOSAL.md  # 診断ロジック案
├── identity.md              # ユーザープロフィール
└── [将来的に]
    ├── diagnosis-tools/     # 診断ツール関連
    ├── automation/          # 自動化スクリプト
    └── wordpress-theme/     # WordPressテーマ
```

## 優先順位

### 最優先（今すぐ）
1. ✅ **Git初期化とGitHub連携**
   - コード管理の基盤
   - 承認制のワークフロー確立
   
2. ✅ **.gitignore作成**
   - 個人情報や認証情報を除外
   - 不要ファイルの管理

### 次優先（STEP 1実装前）
3. ✅ **Google Drive MCP連携**
   - 記事自動生成（STEP 2）に必要
   - 診断ロジックの管理に活用可能

### 将来的に（STEP 2-3実装時）
4. GitHub MCP連携（オプション）
5. その他のMCP連携（Slack等）

## セットアップチェックリスト

- [ ] Gitリポジトリ初期化
- [ ] GitHubリポジトリ作成・連携
- [ ] .gitignore作成
- [ ] 初期コミット・プッシュ
- [ ] Google Drive MCP設定
- [ ] Google Drive API認証情報取得
- [ ] MCP動作確認（スプレッドシート読み込みテスト）
- [ ] Node.js/Python環境整備（必要に応じて）

## 次のステップ

1. **今すぐ実行:** Git初期化とGitHub連携
2. **承認後:** Google Drive MCP設定
3. **設定完了後:** 診断ツール実装開始（STEP 1）
