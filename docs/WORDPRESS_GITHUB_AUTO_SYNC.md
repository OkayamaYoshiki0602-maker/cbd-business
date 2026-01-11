# WordPressとGitHubの自動連携（コードエディタ不要）

## 🎯 目的

**コードエディタを触らずに**、GitHubにプッシュしただけでWordPressに記事が自動反映される仕組みを構築します。

---

## ✅ 実現可能な方法

### 方法A: GitHub Actions + WordPress REST API（推奨）⭐⭐⭐⭐⭐

#### メリット
- ✅ **完全自動化**（コードエディタ不要）
- ✅ **無料**（GitHub Actionsの無料枠で十分）
- ✅ **バージョン管理可能**
- ✅ **プルリクエストでレビュー可能**

#### デメリット
- ⚠️ 初期設定が必要（約30分）
- ⚠️ WordPress REST APIの認証が必要

#### 動作の流れ

```
1. GitHubに記事コードをプッシュ
   ↓
2. GitHub Actionsが自動実行
   ↓
3. WordPress REST APIで記事を投稿/更新
   ↓
4. WordPressサイトに自動反映 ✅
```

---

## 🚀 実装手順

### Step 1: WordPress側の設定（10分）

#### 1.1 アプリケーションパスワードを作成

1. **WordPress管理画面にログイン**
   - URL: https://cbd-no-hito.com/wp-admin/

2. **ユーザー → プロフィール**
   - 「アプリケーションパスワード」セクションを探す

3. **新しいアプリケーションパスワードを作成**
   - **名前**: `GitHub Sync`
   - **「新しいパスワードを追加」**をクリック
   - **パスワードをコピー**（一度しか表示されません！）
   - 例: `xxxx xxxx xxxx xxxx xxxx xxxx`

#### 1.2 REST APIが有効か確認

- WordPress 5.6以降では標準で有効
- 確認: https://cbd-no-hito.com/wp-json/wp/v2/posts にアクセス
- JSONが表示されればOK ✅

---

### Step 2: GitHub Secretsの設定（5分）

1. **GitHubリポジトリを開く**
   - https://github.com/OkayamaYoshiki0602-maker/cbd-business

2. **Settings → Secrets and variables → Actions**

3. **New repository secret**をクリック

4. **以下のシークレットを追加:**

   | Name | Value |
   |------|-------|
   | `WORDPRESS_URL` | `https://cbd-no-hito.com` |
   | `WORDPRESS_USERNAME` | WordPressのユーザー名 |
   | `WORDPRESS_APP_PASSWORD` | ステップ1.1で作成したパスワード（スペースは削除） |

   **注意:** アプリケーションパスワードはスペースを削除して入力（例: `xxxx-xxxx-xxxx-xxxx-xxxx-xxxx`）

---

### Step 3: GitHub Actionsワークフローの確認（5分）

既に `.github/workflows/sync-wordpress.yml` を作成済みです。

**確認事項:**
- [x] `.github/workflows/sync-wordpress.yml` が存在する
- [x] `.github/scripts/sync_to_wordpress.py` が存在する

---

### Step 4: テスト実行（10分）

1. **記事コードをコミット・プッシュ**

   ```bash
   git add wordpress/posts/cbd-oil-howto.html
   git commit -m "Add: CBDオイル記事（自動同期テスト）"
   git push origin main
   ```

2. **GitHub Actionsの実行を確認**
   - GitHubリポジトリ → **Actions** タブ
   - 「Sync to WordPress」ワークフローの実行状況を確認
   - ✅ 緑色のチェックマーク = 成功

3. **WordPressサイトを確認**
   - https://cbd-no-hito.com/ にアクセス
   - 記事が自動反映されているか確認

---

## 📋 使用方法

### 通常の運用フロー

1. **ローカルで記事コードを編集**
   ```bash
   # wordpress/posts/cbd-oil-howto.html を編集
   ```

2. **GitHubにプッシュ**
   ```bash
   git add wordpress/posts/cbd-oil-howto.html
   git commit -m "Update: CBDオイル記事を更新"
   git push origin main
   ```

3. **自動同期完了** ✅
   - GitHub Actionsが自動実行
   - WordPressに記事が自動反映
   - **コードエディタは触る必要なし！**

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

## 📝 ファイル構成

```
.github/
├── workflows/
│   └── sync-wordpress.yml          # GitHub Actionsワークフロー
└── scripts/
    └── sync_to_wordpress.py        # WordPress同期スクリプト

wordpress/
├── posts/
│   └── cbd-oil-howto.html          # 記事コード
└── pages/
    └── ...
```

---

## 🎯 次のステップ

1. ✅ WordPress側の設定（アプリケーションパスワード作成）
2. ✅ GitHub Secretsの設定
3. ✅ テスト実行
4. ✅ 自動同期の確認

---

## 📚 参考情報

### WordPress REST API
- [WordPress REST API Handbook](https://developer.wordpress.org/rest-api/)
- [Application Passwords](https://wordpress.org/support/article/application-passwords/)

### GitHub Actions
- [GitHub Actions Documentation](https://docs.github.com/en/actions)
- [GitHub Secrets](https://docs.github.com/en/actions/security-guides/encrypted-secrets)
