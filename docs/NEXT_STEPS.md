# 次のステップ - 完了状況と実行手順

## ✅ 完了した作業

1. ✅ **Git初期化とコミット**
   - Gitユーザー設定（名前・メール）
   - リポジトリ初期化
   - 全ファイルをコミット（3回のコミット）
   
2. ✅ **開発環境ファイル作成**
   - `.cursorrules`: Cursor最適化ルール
   - `.gitignore`: Git除外設定
   - `README.md`: プロジェクト概要
   - `PROJECT_PLAN.md`: 詳細計画
   - `WORKFLOW.md`: ワークフロー
   - `DIAGNOSIS_LOGIC_PROPOSAL.md`: 診断ロジック案
   - `SETUP_GUIDE.md`: セットアップガイド
   - `SETUP_ACTION_PLAN.md`: 実行プラン
   - `MCP_INTEGRATION_PLAN.md`: MCP連携プラン
   - `MCP_SETUP_INSTRUCTIONS.md`: MCP設定手順
   - `mcp_settings_template.json`: MCP設定テンプレート
   - `GITHUB_REPO_SETUP.md`: GitHubリポジトリ作成手順

---

## 🚀 次に実行すべきこと

### 1. GitHubリポジトリ作成とプッシュ（最優先）

**方法A: Web UIで作成（簡単・推奨）**

1. https://github.com/new にアクセス
2. **Repository name:** `cbd-business`
3. **Visibility:** `Private` または `Public`
4. ✅ **Add a README file** は**チェックしない**
5. ✅ **Add .gitignore** は**チェックしない**
6. `Create repository` をクリック
7. 表示される手順に従って以下を実行：

```bash
cd "/Users/okayamayoshiki/Library/CloudStorage/GoogleDrive-okayamayoshiki0602o@gmail.com/マイドライブ/cursor"
git remote add origin https://github.com/OkayamaYoshiki0602-maker/cbd-business.git
git push -u origin main
```

**方法B: GitHub CLIで作成（自動化）**

```bash
# GitHub CLIをインストール（未インストールの場合）
brew install gh

# 認証
gh auth login

# リポジトリ作成とプッシュ（一括実行）
cd "/Users/okayamayoshiki/Library/CloudStorage/GoogleDrive-okayamayoshiki0602o@gmail.com/マイドライブ/cursor"
gh repo create cbd-business --private --source=. --remote=origin --push
```

詳細は `GITHUB_REPO_SETUP.md` を参照。

---

### 2. MCP連携設定（STEP 2実装前に必須）

#### 2-1. GitHub MCP連携

1. **Personal Access Token (PAT) を取得**
   - GitHub Settings → Developer settings → Personal access tokens → Tokens (classic)
   - `Generate new token (classic)` をクリック
   - スコープ: ✅ `repo`, ✅ `read:org`
   - トークンをコピー（一度しか表示されない）

2. **CursorのMCP設定に追加**
   - 設定ファイル: `~/Library/Application Support/Cursor/User/globalStorage/saoudrizwan.claude-dev/settings/cline_mcp_settings.json`
   - `mcp_settings_template.json` を参考に設定
   - Cursorを再起動

詳細は `MCP_SETUP_INSTRUCTIONS.md` を参照。

#### 2-2. Google Drive MCP連携（STEP 2実装前に必須）

1. **Google Cloud Console でプロジェクト作成**
2. **Google Drive API を有効化**
3. **認証情報（JSON）を取得**
4. **認証情報ファイルを配置**
   ```bash
   mkdir -p ~/.config/cursor
   mv ~/Downloads/your-project-xxxxx.json ~/.config/cursor/google-drive-credentials.json
   ```
5. **Google Driveスプレッドシートの共有設定**
   - サービスアカウントのメールアドレスを追加
6. **CursorのMCP設定に追加**
   - `MCP_SETUP_INSTRUCTIONS.md` を参照

詳細は `MCP_SETUP_INSTRUCTIONS.md` を参照。

---

### 3. 診断ツール実装（STEP 1）

**診断ロジック案の選定:**
- `DIAGNOSIS_LOGIC_PROPOSAL.md` を確認
- **案2: 緊急度×シチュエーション特化型** を推奨（CVR見込み: 12-15%）

**承認後:**
1. 詳細仕様書作成
2. HTML/CSS/JavaScriptプロトタイプコード作成
3. SWELLでの動作確認

---

## 📊 進捗状況

### 基盤整備 ✅ 完了
- [x] Git初期化
- [x] 開発環境ファイル作成
- [ ] GitHubリポジトリ作成 ← **今ここ**
- [ ] GitHub MCP連携
- [ ] Google Drive MCP連携

### STEP 1: 診断ツール実装 ⏳ 待機中
- [ ] 診断ロジック選定
- [ ] プロトタイプ作成
- [ ] SWELL統合

### STEP 2: 自動記事生成 ⏳ 待機中
- [ ] スプレッドシートテンプレート作成
- [ ] MCP連携確認
- [ ] 記事生成ロジック作成

### STEP 3: X自動投稿 ⏳ 待機中
- [ ] X API認証
- [ ] 自動投稿スクリプト作成
- [ ] 予約投稿システム構築

---

## 🎯 今すぐやること

1. **GitHubリポジトリ作成** ← **最優先**
   - Web UIまたはGitHub CLIで作成
   - リモート追加・プッシュ

2. **GitHub MCP連携設定** ← **効率化**
   - PAT取得
   - CursorのMCP設定に追加

3. **Google Drive MCP連携設定** ← **STEP 2実装前に必須**
   - API認証情報取得
   - CursorのMCP設定に追加

4. **診断ツール実装開始** ← **STEP 1**
   - 診断ロジック選定
   - プロトタイプ作成

---

## 💡 参考ドキュメント

- `GITHUB_REPO_SETUP.md`: GitHubリポジトリ作成手順
- `MCP_SETUP_INSTRUCTIONS.md`: MCP連携設定手順
- `DIAGNOSIS_LOGIC_PROPOSAL.md`: 診断ロジック案比較
- `PROJECT_PLAN.md`: 詳細プロジェクト計画
- `WORKFLOW.md`: ワークフロー・自動化手順
