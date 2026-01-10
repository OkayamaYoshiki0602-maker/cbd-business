# GitHubリポジトリ作成手順

## 📋 リポジトリ情報

- **リポジトリ名:** `cbd-business`
- **ユーザー名:** `OkayamaYoshiki0602-maker`
- **メールアドレス:** `okayamayoshiki0602@icloud.com`

---

## 🚀 リポジトリ作成方法（2通り）

### 方法1: Web UIで作成（推奨・簡単）

1. **GitHubにログイン**
   - https://github.com/OkayamaYoshiki0602-maker にアクセス

2. **新規リポジトリ作成**
   - 右上の `+` → `New repository` をクリック
   - 以下を入力:
     - **Repository name:** `cbd-business`
     - **Description:** `CBD Side Business Ecosystem - WordPress/SWELL自動化プロジェクト`
     - **Visibility:** `Private` または `Public`（お好みで）
     - ✅ **Add a README file** は**チェックしない**（既にローカルにファイルがあるため）
     - ✅ **Add .gitignore** は**チェックしない**（既に作成済み）
     - ✅ **Choose a license** は任意

3. **Create repository** をクリック

4. **リモート追加・プッシュ**
   リポジトリ作成後、表示される手順に従って以下を実行：
   ```bash
   git remote add origin https://github.com/OkayamaYoshiki0602-maker/cbd-business.git
   git branch -M main
   git push -u origin main
   ```

---

### 方法2: GitHub CLIで作成（自動化・効率的）

#### 1. GitHub CLIのインストール（未インストールの場合）

```bash
# Homebrewでインストール（推奨）
brew install gh

# 認証
gh auth login
# → ブラウザで認証
# → HTTPS/Git を選択
# → GitHub.com を選択
# → 認証方法を選択（ブラウザ推奨）
```

#### 2. リポジトリ作成

```bash
cd "/Users/okayamayoshiki/Library/CloudStorage/GoogleDrive-okayamayoshiki0602o@gmail.com/マイドライブ/cursor"
gh repo create cbd-business --private --source=. --remote=origin --push
# または Public の場合:
# gh repo create cbd-business --public --source=. --remote=origin --push
```

**オプション説明:**
- `--private`: プライベートリポジトリ（`--public` で公開）
- `--source=.`: 現在のディレクトリをソースとして使用
- `--remote=origin`: リモート名を `origin` に設定
- `--push`: 作成後、自動的にプッシュ

---

## ✅ リモート追加・プッシュ（方法1の場合）

GitHubリポジトリ作成後、以下を実行：

```bash
cd "/Users/okayamayoshiki/Library/CloudStorage/GoogleDrive-okayamayoshiki0602o@gmail.com/マイドライブ/cursor"
git remote add origin https://github.com/OkayamaYoshiki0602-maker/cbd-business.git
git branch -M main
git push -u origin main
```

**認証方法:**
- HTTPSの場合、GitHubのユーザー名とPAT（Personal Access Token）が求められます
- PATはパスワードの代わりに使用します

---

## 🔐 GitHub認証（HTTPSでプッシュする場合）

### Personal Access Token (PAT) の取得

1. GitHub Settings → Developer settings → Personal access tokens → Tokens (classic)
2. `Generate new token (classic)` をクリック
3. 以下を設定:
   - **Note:** `Git push access`
   - **Expiration:** 任意
   - **Select scopes:** ✅ `repo` を選択
4. `Generate token` をクリック
5. **トークンをコピー**（`ghp_xxxxxxxxxxxxxxxxxxxx`）

### Git Credential Helperの設定（推奨）

```bash
# macOS Keychainを使用（推奨）
git config --global credential.helper osxkeychain

# または、Git Credential Managerを使用
# brew install git-credential-manager
# git config --global credential.helper manager
```

**初回プッシュ時:**
- **Username:** `OkayamaYoshiki0602-maker`
- **Password:** PAT（`ghp_xxxxxxxxxxxxxxxxxxxx`）を貼り付け

---

## 🔍 動作確認

プッシュ後、以下を確認：

```bash
# リモート設定を確認
git remote -v

# ブランチを確認
git branch -a

# リモートとの同期状態を確認
git status
```

GitHub上で以下を確認：
- ✅ すべてのファイルがプッシュされているか
- ✅ `.gitignore` が正しく機能しているか（認証情報などが除外されているか）

---

## 📝 次のステップ

リポジトリ作成後：
1. ✅ GitHub MCP連携を設定（`MCP_SETUP_INSTRUCTIONS.md` を参照）
2. ✅ Google Drive MCP連携を設定（STEP 2実装前に必須）
3. ✅ 診断ツール実装開始（STEP 1）

---

## ⚠️ 注意事項

- ✅ `.gitignore` で認証情報（`.json`, `.env`等）を除外済み
- ⚠️ GitHubにプッシュする前に、個人情報が含まれていないか確認
- ⚠️ 認証情報（PAT、API keys等）は絶対にコミットしない
