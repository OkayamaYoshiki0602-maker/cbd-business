# セットアップ実行プラン

## 📋 優先順位と実行手順

### 🔴 最優先（今すぐ実行）

#### 1. Gitリポジトリ初期化とGitHub連携
**目的:** コード管理の基盤確立、承認制ワークフロー実現  
**時間:** 5-10分  
**影響:** すべての開発作業の前提条件

**実行手順:**
1. Git初期化
2. `.gitignore` で個人情報を除外（✅ 作成済み）
3. GitHubリポジトリ作成
4. 初期コミット・プッシュ

#### 2. .gitignore適用
**目的:** 認証情報や個人情報の誤コミット防止  
**時間:** 1分  
**影響:** セキュリティ確保

**実行手順:**
- ✅ `.gitignore` 作成済み
- Git初期化時に自動適用

---

### 🟡 次優先（STEP 1実装前）

#### 3. Google Drive MCP連携
**目的:** 記事自動生成（STEP 2）の基盤  
**時間:** 15-30分（API認証取得含む）  
**影響:** スプレッドシートからのデータ読み込み

**実行手順:**
1. Google Cloud Consoleでプロジェクト作成
2. Google Drive API有効化
3. 認証情報（JSON）取得
4. CursorのMCP設定に追加
5. 動作確認（テストスプレッドシート読み込み）

---

### 🟢 将来的に（STEP 2-3実装時）

#### 4. GitHub MCP連携（オプション）
**目的:** コード管理の自動化  
**時間:** 10分  
**影響:** GitHub操作の自動化

#### 5. その他のMCP連携（Slack等）
**目的:** 通知・連携の自動化  
**時間:** 各10-15分  
**影響:** ワークフロー効率化

---

## 🚀 今すぐ実行する内容

### ステップ1: Git初期化

**コマンド（承認後に実行）:**
```bash
cd "/Users/okayamayoshiki/Library/CloudStorage/GoogleDrive-okayamayoshiki0602o@gmail.com/マイドライブ/cursor"
git init
git add .
git commit -m "初期セットアップ: Cursor最適化ルールとプロジェクト計画"
```

### ステップ2: GitHubリポジトリ作成

**手順:**
1. GitHubで新規リポジトリ作成（`cbd-side-business` など）
2. リモート追加:
```bash
git remote add origin https://github.com/[あなたのユーザー名]/cbd-side-business.git
git branch -M main
git push -u origin main
```

### ステップ3: MCP設定確認

**CursorのMCP設定場所（macOS）:**
- `~/Library/Application Support/Cursor/User/globalStorage/saoudrizwan.claude-dev/settings/cline_mcp_settings.json`
- または Cursor設定内の `MCP Settings` から

**確認事項:**
- [ ] MCP機能が有効か
- [ ] 現在のMCPサーバー一覧
- [ ] Google Drive MCPの設定状況

---

## 📊 実行前チェックリスト

### Git・GitHub
- [ ] GitHubアカウント持っている？
- [ ] GitHubユーザー名は？
- [ ] リポジトリ名の希望は？（例: `cbd-side-business`）

### MCP連携
- [ ] Google Cloud Consoleアカウント持っている？
- [ ] 既にプロジェクト作成済み？
- [ ] API認証情報は既に取得済み？

### 開発環境
- [ ] Gitコマンド使える？（Xcode開発ツール必要）
- [ ] Node.jsインストール済み？（MCP用）
- [ ] Python環境整備済み？（自動化スクリプト用）

---

## ⚠️ 注意事項

### セキュリティ
- ✅ `.gitignore` で認証情報（`.json`, `.env`等）を除外
- ⚠️ GitHubにプッシュする前に個人情報がないか確認
- ⚠️ MCP認証情報はローカルにのみ保存

### パス問題
- Google Driveのパスにスペースがあるため、コマンド実行時に注意
- 必要に応じて引用符で囲む

---

## 🎯 次のステップ

**承認いただけたら:**
1. ✅ Git初期化を実行
2. ✅ GitHubリポジトリ作成・連携
3. ✅ 初期コミット・プッシュ
4. ✅ MCP設定状況を確認
5. ✅ Google Drive MCP設定（必要に応じて）

**完了後の確認:**
- GitHubリポジトリが正常に作成・連携されているか
- `.gitignore` が正しく機能しているか
- MCP連携が動作するか（テスト読み込み）

---

## 💡 質問事項

実行前に確認させてください：

1. **GitHubリポジトリ名:** `cbd-side-business` で良いですか？他に希望はありますか？

2. **GitHubユーザー名:** 教えていただけますか？（リモートURL用）

3. **Xcode開発ツール:** インストールされていますか？未インストールの場合、Gitコマンドが使えません（必要ならインストール案内します）

4. **Google Drive MCP:** 今すぐ設定しますか？それともGit連携後にしますか？

**承認いただければ、すぐに実行開始します！** 🚀
