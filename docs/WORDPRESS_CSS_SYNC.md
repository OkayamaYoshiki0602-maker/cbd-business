# WordPress追加CSSのGitHub管理ガイド

## 📋 概要

WordPressの「外観」→「カスタマイズ」→「追加CSS」のCSSコードをGitHubで管理する方法です。

---

## 🎯 実装方法

### 方法1: ファイルとして保存（推奨）⭐⭐

WordPressの追加CSSを `wordpress/custom-css.css` ファイルとして保存し、GitHubで管理します。

#### メリット
- ✅ GitHubでバージョン管理ができる
- ✅ 編集履歴を追跡できる
- ✅ 他の開発者と共有しやすい
- ✅ バックアップが自動的に取れる

#### デメリット
- ⚠️ WordPress側に手動でコピー＆ペーストする必要がある（またはスクリプトで自動化）

---

### 方法2: WordPress REST APIで自動同期（将来実装可能）

WordPress REST APIを使用してCSSを自動的に同期する方法です。

#### 現状
- WordPress REST APIには、テーマのカスタマイザー設定（追加CSS含む）を直接取得/更新するエンドポイントが標準で提供されていない
- カスタムプラグインまたはテーマ機能が必要

---

## 📝 推奨実装（方法1）

### Step 1: CSSファイルを作成

1. `wordpress/custom-css.css` ファイルを作成
2. WordPressの「追加CSS」からコードをコピー
3. ファイルに貼り付け

```bash
# ファイルを作成
touch wordpress/custom-css.css
```

### Step 2: CSSコードをコピー

1. WordPress管理画面 → **「外観」** → **「カスタマイズ」**
2. **「追加CSS」** を開く
3. CSSコードをすべてコピー
4. `wordpress/custom-css.css` ファイルに貼り付け

### Step 3: Gitで管理

```bash
# ファイルを追加
git add wordpress/custom-css.css

# コミット
git commit -m "Add WordPress custom CSS"

# プッシュ
git push origin main
```

---

## 🔄 運用フロー

### CSSを更新する場合

1. `wordpress/custom-css.css` ファイルを編集
2. Gitにコミット・プッシュ
3. WordPress管理画面 → **「外観」** → **「カスタマイズ」** → **「追加CSS」**
4. 更新したCSSコードをコピー＆ペースト

---

## 📂 ファイル構造

```
wordpress/
├── custom-css.css          # WordPress追加CSS
├── posts/                  # 投稿記事
│   └── *.html
└── pages/                  # 固定ページ
    └── *.html
```

---

## 🔍 WordPress追加CSSの取得方法

### 手動でコピー

1. WordPress管理画面にログイン
2. **「外観」** → **「カスタマイズ」**
3. **「追加CSS」** セクションを開く
4. CSSコードをすべて選択してコピー
5. `wordpress/custom-css.css` ファイルに貼り付け

---

## 🔗 参考情報

- `docs/WORDPRESS_TO_GITHUB_SYNC.md` - WordPressからGitHubへの同期ガイド
- [WordPress Codex: 追加CSS](https://wordpress.org/support/article/appearance-customize-screen/#additional-css)

---

## ⚠️ 注意事項

### CSSファイルの編集

- CSSファイルを編集する際は、WordPress側にも同じ変更を反映する必要があります
- または、将来スクリプトで自動化することも可能です

### バックアップ

- Gitで管理しているため、GitHubに自動的にバックアップされます
- WordPress側の追加CSSも定期的にバックアップすることをお勧めします

---

## 🚀 将来の拡張

将来的に、以下のような自動同期機能を実装することも可能です：

1. WordPress REST APIを使用したCSS取得（カスタムエンドポイントが必要）
2. WordPress CLIを使用したCSS同期（SSHアクセスが必要）
3. GitHub Actionsで自動的にWordPressに同期（カスタムプラグインが必要）

現時点では、手動でのコピー＆ペーストが最も簡単で確実な方法です。
