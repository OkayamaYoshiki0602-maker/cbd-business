# GitHubへのプッシュ方法

## 🎯 概要

ローカルにコミット済みのコードをGitHubリポジトリ（https://github.com/OkayamaYoshiki0602-maker/cbd-business）にプッシュする方法です。

---

## 📋 実行場所

**ターミナル（Terminal）アプリ**で実行します。

macOSの場合：
- `アプリケーション` → `ユーティリティ` → `ターミナル`
- または、Spotlight検索で「ターミナル」と入力

---

## 🚀 方法1: GitHub CLIを使用（推奨）

### Step 1: GitHub CLIをインストール（未インストールの場合）

```bash
brew install gh
```

### Step 2: GitHub CLIで認証（初回のみ）

```bash
gh auth login
```

**実行時の選択肢:**
1. **What account do you want to log into?** → `GitHub.com` を選択
2. **What is your preferred protocol for Git operations?** → `HTTPS` を選択
3. **Authenticate Git with your GitHub credentials?** → `Yes` を選択
4. **How would you like to authenticate GitHub CLI?** → `Login with a web browser` を選択
5. 表示されたコードをコピー
6. ブラウザで https://github.com/login/device にアクセス
7. コードを入力して認証

### Step 3: GitHubにプッシュ

```bash
cd "/Users/okayamayoshiki/Library/CloudStorage/GoogleDrive-okayamayoshiki0602o@gmail.com/マイドライブ/cursor"
git push origin main
```

---

## 🚀 方法2: 通常のGitコマンドを使用

### Step 1: 認証情報を設定（初回のみ）

GitHubへの認証には、**Personal Access Token**が必要です。

#### Personal Access Tokenの作成

1. **GitHubにログイン**
2. **Settings → Developer settings → Personal access tokens → Tokens (classic)**
3. **Generate new token → Generate new token (classic)**
4. **Note**: `cbd-business-push` など適当な名前を入力
5. **Expiration**: `90 days` または `No expiration` を選択
6. **Select scopes**: `repo` にチェックを入れる
7. **Generate token** をクリック
8. **トークンをコピー**（一度しか表示されません！）

#### Git認証情報を設定

```bash
# macOSの場合は、Keychainに保存されます
git config --global credential.helper osxkeychain

# プッシュ時に認証情報を入力
git push origin main
# Username: OkayamaYoshiki0602-maker
# Password: （Personal Access Tokenを貼り付け）
```

---

## 🚀 方法3: GitHub Desktopを使用（GUIで簡単）

### Step 1: GitHub Desktopをインストール

1. https://desktop.github.com/ にアクセス
2. **Download for macOS** をクリック
3. インストール

### Step 2: GitHub Desktopでリポジトリを開く

1. **GitHub Desktop**を起動
2. **File → Add Local Repository**
3. **Choose...** をクリック
4. `/Users/okayamayoshiki/Library/CloudStorage/GoogleDrive-okayamayoshiki0602o@gmail.com/マイドライブ/cursor` を選択
5. **Add repository** をクリック

### Step 3: GitHubにプッシュ

1. 変更内容を確認
2. **Push origin** ボタンをクリック
3. GitHubに認証情報を入力（初回のみ）

---

## ✅ プッシュ完了後の確認

### 1. GitHubリポジトリを確認

1. https://github.com/OkayamaYoshiki0602-maker/cbd-business にアクセス
2. ファイルが反映されているか確認
   - `wordpress/posts/cbd-oil-howto.html`
   - `.github/workflows/sync-wordpress.yml`
   - `.github/scripts/sync_to_wordpress.py`

### 2. GitHub Actionsの実行を確認

1. **GitHubリポジトリ → Actionsタブ**
2. 「Sync to WordPress」ワークフローが実行されているか確認
3. ✅ 緑色のチェックマーク = 成功
4. ⚠️ 黄色/赤色 = エラー（ログを確認）

### 3. WordPressサイトを確認

1. https://cbd-no-hito.com/wp-admin/
2. **投稿 → 投稿一覧**で記事が反映されているか確認

---

## 🔧 トラブルシューティング

### エラー: "fatal: could not read Username"

**原因:** 認証情報が設定されていない

**解決方法:**
- GitHub CLIを使用: `gh auth login`
- Personal Access Tokenを使用: トークンを作成して設定

---

### エラー: "Permission denied"

**原因:** リポジトリへのアクセス権限がない

**解決方法:**
1. GitHubでリポジトリのオーナーかどうか確認
2. 別のアカウントでログインしている場合は、正しいアカウントで認証

---

### エラー: "remote origin already exists"

**原因:** リモートリポジトリが既に設定されている

**解決方法:**
```bash
# リモートのURLを確認
git remote -v

# 必要に応じてURLを更新
git remote set-url origin https://github.com/OkayamaYoshiki0602-maker/cbd-business.git
```

---

## 📝 参考

### コマンドの説明

- `git push origin main` - `main`ブランチを`origin`（GitHub）にプッシュ
- `git status` - 現在の状態を確認
- `git log --oneline` - コミット履歴を確認
