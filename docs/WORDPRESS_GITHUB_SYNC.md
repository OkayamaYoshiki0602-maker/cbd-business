# WordPressとGitHubの連携

## 🎯 目的

1. **WordPressの記事コードをGitHubで管理**
2. **GitHubからWordPressに記事を同期**

---

## 📋 方法の比較

### 方法A: WordPress REST API + GitHub Actions（推奨）

#### メリット
- ✅ 完全自動化可能
- ✅ コードレビューが可能
- ✅ バージョン管理が可能
- ✅ プルリクエストでレビュー可能

#### デメリット
- ⚠️ 設定が複雑
- ⚠️ WordPress REST APIの認証が必要

---

### 方法B: 手動でGitHubにコミット（シンプル）

#### メリット
- ✅ 設定が簡単
- ✅ コードレビューが可能
- ✅ バージョン管理が可能

#### デメリット
- ⚠️ 手動でコミットが必要
- ⚠️ WordPressへの同期は手動

---

### 方法C: WordPressプラグイン（WP Sync）を使用

#### メリット
- ✅ WordPress管理画面から操作可能
- ✅ 設定が簡単

#### デメリット
- ⚠️ プラグインの費用がかかる場合がある
- ⚠️ カスタマイズの自由度が低い

---

## 🚀 推奨アプローチ：方法A（WordPress REST API + GitHub Actions）

### Phase 1: WordPress REST APIの設定（30分）

#### Step 1: アプリケーションパスワードを作成

1. **WordPress管理画面にログイン**
   - URL: https://cbd-no-hito.com/wp-admin/

2. **ユーザー → プロフィール**
   - 「アプリケーションパスワード」セクションを探す

3. **新しいアプリケーションパスワードを作成**
   - 名前: `GitHub Sync`
   - 「新しいパスワードを追加」をクリック
   - パスワードをコピー（一度しか表示されません）

---

### Phase 2: GitHubリポジトリの作成（15分）

1. **GitHubで新しいリポジトリを作成**
   - 名前: `cbd-wordpress-content`
   - 説明: `CBDサイトのWordPress記事コード`

2. **ローカルにリポジトリをクローン**
   ```bash
   git clone https://github.com/YOUR_USERNAME/cbd-wordpress-content.git
   cd cbd-wordpress-content
   ```

3. **ディレクトリ構造を作成**
   ```
   cbd-wordpress-content/
   ├── posts/
   │   ├── cbd-oil-howto.html
   │   ├── cbd-gummy-howto.html
   │   └── ...
   ├── pages/
   │   └── ...
   └── README.md
   ```

---

### Phase 3: 記事コードをGitHubに追加（15分）

1. **記事コードをファイルに保存**
   - ファイル名: `posts/cbd-oil-howto.html`
   - 内容: 提供されたWordPressブロックエディタコード

2. **GitHubにコミット**
   ```bash
   git add posts/cbd-oil-howto.html
   git commit -m "Add: CBDオイルの選び方記事"
   git push origin main
   ```

---

### Phase 4: GitHub Actionsの設定（1時間）

#### Step 1: GitHub Actionsワークフローファイルを作成

`.github/workflows/sync-to-wordpress.yml`

```yaml
name: Sync to WordPress

on:
  push:
    branches:
      - main
    paths:
      - 'posts/**'
      - 'pages/**'
  workflow_dispatch:

jobs:
  sync:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      
      - name: Sync to WordPress
        uses: YOUR_ACTION
        with:
          wordpress_url: ${{ secrets.WORDPRESS_URL }}
          wordpress_username: ${{ secrets.WORDPRESS_USERNAME }}
          wordpress_password: ${{ secrets.WORDPRESS_APP_PASSWORD }}
          file_path: ${{ github.event.head_commit.modified }}
```

#### Step 2: GitHub Secretsを設定

1. **GitHubリポジトリ → Settings → Secrets and variables → Actions**
2. **New repository secret**をクリック
3. **以下のシークレットを追加:**
   - `WORDPRESS_URL`: `https://cbd-no-hito.com`
   - `WORDPRESS_USERNAME`: WordPressのユーザー名
   - `WORDPRESS_APP_PASSWORD`: アプリケーションパスワード

---

## 🔧 より簡単な方法：手動同期（方法B）

### Step 1: 記事コードをGitHubに保存

1. **GitHubリポジトリに記事コードをコミット**
   - ファイル名: `posts/cbd-oil-howto.html`
   - 内容: WordPressブロックエディタコード

2. **README.mdに使用方法を記載**

---

### Step 2: WordPressに手動で同期

1. **GitHubから記事コードを取得**
2. **WordPress管理画面 → 投稿 → 新規追加**
3. **コードエディタに切り替え（右上の「...」→「コードエディタ」）**
4. **記事コードを貼り付け**
5. **公開**

---

## 📝 実装ファイル

### 1. GitHubリポジトリ構造

```
cbd-wordpress-content/
├── .github/
│   └── workflows/
│       └── sync-to-wordpress.yml
├── posts/
│   ├── cbd-oil-howto.html
│   ├── cbd-gummy-howto.html
│   └── cbd-vape-howto.html
├── pages/
│   └── ...
└── README.md
```

### 2. 記事ファイルの例

`posts/cbd-oil-howto.html`

```html
<!-- WordPressブロックエディタコード -->
<!-- wp:heading -->
<h2 class="wp-block-heading">CBDオイルの正しい選び方：安心して始めるための完全ガイド</h2>
<!-- /wp:heading -->
...
```

---

## ✅ 次のアクション

### まずは手動同期から始める（推奨）

1. **GitHubリポジトリを作成**
2. **記事コードをGitHubにコミット**
3. **必要に応じてWordPressに手動で同期**

### 自動化が必要になったら

1. **WordPress REST APIの設定**
2. **GitHub Actionsの設定**
3. **自動同期のテスト**

---

## 📚 参考情報

### WordPress REST API
- [WordPress REST API Handbook](https://developer.wordpress.org/rest-api/)

### GitHub Actions
- [GitHub Actions Documentation](https://docs.github.com/en/actions)

### WordPressブロックエディタ
- [WordPress Block Editor Handbook](https://developer.wordpress.org/block-editor/)
