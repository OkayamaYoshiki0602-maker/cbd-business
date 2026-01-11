# WordPressからGitHubへの同期ガイド

## 📋 概要

WordPressに既に存在する投稿記事と固定ページのHTMLコンテンツを、GitHubリポジトリに同期する方法です。

---

## 🎯 機能

- WordPress REST APIを使用して投稿・固定ページを取得
- HTMLコンテンツを `wordpress/posts/` と `wordpress/pages/` に保存
- ファイル名はスラッグ（slug）を使用

---

## 🔧 必要な設定

### 環境変数の確認

`.env`ファイルに以下の設定があることを確認してください：

```env
WORDPRESS_URL=https://cbd-no-hito.com
WORDPRESS_USERNAME=yoshiki
WORDPRESS_APP_PASSWORD=Zn5jnUxjfP0DQNgB6fCbaUYy
```

---

## 📝 使用方法

### Step 1: スクリプトを実行

```bash
cd "/Users/okayamayoshiki/Library/CloudStorage/GoogleDrive-okayamayoshiki0602o@gmail.com/マイドライブ/cursor"
python3 automation/scripts/sync_from_wordpress.py
```

### Step 2: 結果を確認

スクリプトは以下を実行します：
- WordPressからすべての公開済み投稿を取得
- WordPressからすべての公開済み固定ページを取得
- `wordpress/posts/` ディレクトリに投稿を保存
- `wordpress/pages/` ディレクトリに固定ページを保存

### Step 3: Gitにコミット・プッシュ

```bash
# 変更を確認
git status

# ファイルを追加
git add wordpress/posts/ wordpress/pages/

# コミット
git commit -m "Sync posts and pages from WordPress"

# プッシュ
git push origin main
```

---

## 📂 ファイルの保存形式

### ファイル名

- **投稿**: `wordpress/posts/[スラッグ].html`
- **固定ページ**: `wordpress/pages/[スラッグ].html`

例：
- `wordpress/posts/cbd-pet-anxiety-dogs-cats-safe-use.html`
- `wordpress/pages/about.html`

### ファイル内容

- WordPress REST APIから取得したHTMLコンテンツをそのまま保存
- エディターで編集可能な形式

---

## ⚠️ 注意事項

### 既存ファイルとの競合

- 同じスラッグのファイルが既に存在する場合、上書きされます
- 重要な変更がある場合は、事前にバックアップを取ることをお勧めします

### 取得対象

- **公開済み（publish）**の投稿・固定ページのみを取得します
- 下書きや予約投稿は取得しません

### コンテンツの形式

- WordPress REST APIから取得したHTMLコンテンツをそのまま保存します
- ブロックエディターの形式で保存されます

---

## 🔄 今後の運用

### WordPressからGitHubへの同期

必要に応じて、このスクリプトを実行してWordPressの最新状態をGitHubに同期できます。

```bash
python3 automation/scripts/sync_from_wordpress.py
```

### GitHubからWordPressへの同期

既に実装済みの機能です。`wordpress/posts/` や `wordpress/pages/` のファイルを変更してGitHubにプッシュすると、自動的にWordPressに同期されます。

---

## 📝 トラブルシューティング

### エラー: 環境変数が設定されていません

`.env`ファイルに以下の設定があることを確認してください：

```env
WORDPRESS_URL=https://cbd-no-hito.com
WORDPRESS_USERNAME=yoshiki
WORDPRESS_APP_PASSWORD=Zn5jnUxjfP0DQNgB6fCbaUYy
```

### エラー: 403 Forbidden

WordPress REST APIへのアクセスがブロックされている可能性があります。以下のドキュメントを参照してください：

- `docs/CONOHA_WING_REST_API_403_SOLUTION.md`

### エラー: 接続タイムアウト

WordPressサーバーへの接続がタイムアウトしている可能性があります。ネットワーク接続を確認してください。

---

## 🔗 参考情報

- `automation/scripts/sync_from_wordpress.py` - 同期スクリプト
- `docs/WORDPRESS_GITHUB_SETUP_GUIDE.md` - WordPress-GitHub連携の設定ガイド
