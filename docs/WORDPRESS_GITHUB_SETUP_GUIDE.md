# WordPressとGitHub自動連携セットアップガイド

## 🎯 概要

**コードエディタを触らずに**、GitHubにプッシュしただけでWordPressに記事が自動反映される仕組みです。

---

## ✅ 実装済みの機能

- ✅ GitHub Actionsワークフロー（`.github/workflows/sync-wordpress.yml`）
- ✅ WordPress同期スクリプト（`.github/scripts/sync_to_wordpress.py`）
- ✅ 記事コードの保存（`wordpress/posts/cbd-oil-howto.html`）

---

## 🚀 セットアップ手順（約20分）

### Step 1: WordPress側の設定（10分）

#### 1.1 アプリケーションパスワードを作成

1. **WordPress管理画面にログイン**
   - URL: https://cbd-no-hito.com/wp-admin/

2. **ユーザー → プロフィール**
   - ページを下にスクロールして「アプリケーションパスワード」セクションを探す

3. **新しいアプリケーションパスワードを作成**
   - **名前**: `GitHub Sync` と入力
   - **「新しいパスワードを追加」**ボタンをクリック
   - **パスワードをコピー**（一度しか表示されません！）
   - 例: `xxxx xxxx xxxx xxxx xxxx xxxx`（スペース区切り）

---

### Step 2: GitHub Secretsの設定（5分）

1. **GitHubリポジトリを開く**
   - https://github.com/OkayamaYoshiki0602-maker/cbd-business

2. **Settings → Secrets and variables → Actions**

3. **New repository secret**をクリック

4. **以下の3つのシークレットを追加:**

   | Name | Value | 説明 |
   |------|-------|------|
   | `WORDPRESS_URL` | `https://cbd-no-hito.com` | WordPressサイトのURL（末尾の`/`は不要） |
   | `WORDPRESS_USERNAME` | WordPressのユーザー名 | WordPressにログインする際のユーザー名 |
   | `WORDPRESS_APP_PASSWORD` | アプリケーションパスワード | Step 1.1で作成したパスワード（**スペースを削除**） |

   **重要:** アプリケーションパスワードは、スペースを削除して入力してください。
   - 例: `xxxx-xxxx-xxxx-xxxx-xxxx-xxxx`

---

### Step 3: GitHubへのプッシュ（5分）

現在、ローカルにコミット済みですが、GitHubへのプッシュが必要です。

#### 方法A: GitHub CLIを使用（推奨）

```bash
cd "/Users/okayamayoshiki/Library/CloudStorage/GoogleDrive-okayamayoshiki0602o@gmail.com/マイドライブ/cursor"

# GitHub CLIで認証（初回のみ）
gh auth login

# プッシュ
git push origin main
```

#### 方法B: 手動でプッシュ

1. **GitHub Desktop**を使用する
2. または、ターミナルで以下を実行：
   ```bash
   git push origin main
   ```
   （認証情報を求められたら、GitHubのユーザー名とPersonal Access Tokenを入力）

---

## 📋 使用方法（通常の運用）

### 1. 記事コードを編集

```bash
# wordpress/posts/cbd-oil-howto.html を編集
```

### 2. GitHubにプッシュ

```bash
git add wordpress/posts/cbd-oil-howto.html
git commit -m "Update: CBDオイル記事を更新"
git push origin main
```

### 3. 自動同期完了 ✅

- GitHub Actionsが自動実行（約1-2分）
- WordPressに記事が自動反映
- **コードエディタは触る必要なし！**

---

## 🔍 動作確認

### GitHub Actionsの確認

1. **GitHubリポジトリ → Actionsタブ**
2. 「Sync to WordPress」ワークフローの実行状況を確認
3. ✅ 緑色のチェックマーク = 成功

### WordPressサイトの確認

1. https://cbd-no-hito.com/wp-admin/
2. **投稿 → 投稿一覧**で記事が反映されているか確認

---

## 🔧 トラブルシューティング

### エラー: "Unauthorized" または "401"

**原因:** アプリケーションパスワードが間違っている

**解決方法:**
1. WordPressで新しいアプリケーションパスワードを作成
2. GitHub Secretsの `WORDPRESS_APP_PASSWORD` を更新

---

### エラー: "Not Found" または "404"

**原因:** REST APIが無効、またはURLが間違っている

**解決方法:**
1. https://cbd-no-hito.com/wp-json/wp/v2/posts にアクセス
2. JSONが表示されるか確認
3. GitHub Secretsの `WORDPRESS_URL` を確認（末尾の `/` は不要）

---

### エラー: 記事が作成されない

**原因:** スクリプトのエラー

**解決方法:**
1. GitHub Actionsのログを確認
2. `.github/scripts/sync_to_wordpress.py` のエラーメッセージを確認

---

## 📝 参考情報

### 作成されたファイル

- `.github/workflows/sync-wordpress.yml` - GitHub Actionsワークフロー
- `.github/scripts/sync_to_wordpress.py` - WordPress同期スクリプト
- `wordpress/posts/cbd-oil-howto.html` - 記事コード

### ドキュメント

- `docs/WORDPRESS_GITHUB_AUTO_SYNC.md` - 詳細な技術説明
- `docs/WORDPRESS_GITHUB_SYNC.md` - 元の連携方法の説明

---

## 🎯 次のステップ

1. ✅ WordPress側の設定（アプリケーションパスワード作成）
2. ✅ GitHub Secretsの設定
3. ✅ GitHubへのプッシュ
4. ✅ テスト実行
5. ✅ 自動同期の確認

完了後、今後は**GitHubにプッシュするだけでWordPressに自動反映**されます！
