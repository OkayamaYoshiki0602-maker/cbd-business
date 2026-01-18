# WordPress REST API連携 要件定義書

## 📋 施策概要

**施策名**: WordPress REST API連携

**目的**: WordPress REST APIからコンテンツを取得・同期する仕組みを構築

**実施日**: 2026-01-11

**ステータス**: ✅ 完了

---

## 🎯 目標

### 定量的目標
- 全投稿記事・全固定ページの同期完了
- 同期の自動化

### 定性的目標
- コンテンツ管理の効率化
- バージョン管理の容易化
- コンテンツの一元管理

---

## 📊 現状分析

### 現状の問題点

1. **コンテンツの分散管理**
   - WordPressとGitHubでコンテンツが分散
   - 同期の手動実施が必要

2. **バージョン管理の困難**
   - WordPressのコンテンツの変更履歴が追跡困難
   - バックアップの取得が手動

---

## 🎯 要件

### 必須要件

1. **WordPress REST APIからの取得**
   - 投稿記事を取得
   - 固定ページを取得
   - HTML形式で保存

2. **GitHubへの同期**
   - 取得したコンテンツをGitHubに保存
   - ファイル名はスラッグベース

3. **認証の実装**
   - WordPress REST APIの認証
   - アプリケーションパスワードの使用

### 推奨要件

1. **自動同期**
   - 定期的な自動同期
   - 変更検知時の自動同期

2. **差分管理**
   - 変更の差分を記録
   - 変更履歴の管理

---

## 🔧 実装内容

### 1. WordPress REST API連携スクリプト（取得）

**ファイル**: `automation/scripts/sync_from_wordpress.py`

**機能**:
- WordPress REST APIから投稿記事・固定ページを取得
- HTML形式で保存
- GitHubに同期

**認証方法**:
- WordPressアプリケーションパスワードを使用
- Basic認証でAPIにアクセス

### 2. WordPress REST API連携スクリプト（送信）

**ファイル**: `.github/scripts/sync_to_wordpress.py`

**機能**:
- GitHubのHTMLファイルをWordPress REST APIに送信
- 投稿記事・固定ページを作成または更新
- タイトルをHTMLから自動抽出

**認証方法**:
- WordPressアプリケーションパスワードを使用
- Basic認証でAPIにアクセス

### 3. GitHub Actions自動同期

**ファイル**: `.github/workflows/sync-wordpress.yml`

**機能**:
- `wordpress/posts/`または`wordpress/pages/`のファイルが変更されると自動実行
- GitHub Secretsから認証情報を取得
- WordPress REST APIに自動同期

**トリガー**:
- `push`イベント（`main`ブランチ、`wordpress/posts/**`または`wordpress/pages/**`のパス）
- `workflow_dispatch`（手動実行）

**必要なGitHub Secrets**:
- `WORDPRESS_URL` - WordPressのURL（例: `https://cbd-no-hito.com`）
- `WORDPRESS_USERNAME` - WordPressのユーザー名
- `WORDPRESS_APP_PASSWORD` - WordPressのアプリケーションパスワード

### 4. 同期結果

**保存先**:
- `wordpress/posts/` - 投稿記事
- `wordpress/pages/` - 固定ページ

**ファイル形式**:
- HTML形式
- ファイル名はスラッグベース（例: `cbd-oil-howto.html`）

---

## 📈 期待される効果

### 定量的効果
- 全投稿記事・全固定ページの同期完了
- 同期の自動化

### 定性的効果
- コンテンツ管理の効率化
- バージョン管理の容易化

---

## 📝 実装手順

### WordPressからGitHubへの同期（取得）

1. **WordPress REST APIの有効化**
   - WordPress管理画面でREST APIを有効化
   - アプリケーションパスワードを生成

2. **環境変数の設定**
   - `.env`ファイルに以下を設定:
     - `WORDPRESS_URL`
     - `WORDPRESS_USERNAME`
     - `WORDPRESS_APP_PASSWORD`

3. **同期スクリプトの実行**
   ```bash
   python3 automation/scripts/sync_from_wordpress.py
   ```

4. **同期結果の確認**
   - `wordpress/posts/`と`wordpress/pages/`を確認
   - コンテンツが正しく取得されているか確認

### GitHubからWordPressへの同期（送信・自動化）

1. **GitHub Secretsの設定**
   - GitHubリポジトリの「Settings」→「Secrets and variables」→「Actions」
   - 以下のSecretsを追加:
     - `WORDPRESS_URL` - WordPressのURL
     - `WORDPRESS_USERNAME` - WordPressのユーザー名
     - `WORDPRESS_APP_PASSWORD` - WordPressのアプリケーションパスワード

2. **自動同期の確認**
   - `wordpress/posts/`または`wordpress/pages/`のファイルを変更
   - GitHubにプッシュすると、自動的にWordPressに同期される
   - GitHub Actionsの「Actions」タブで実行状況を確認

3. **手動実行（オプション）**
   - GitHub Actionsの「Actions」タブから「Sync to WordPress」ワークフローを選択
   - 「Run workflow」ボタンをクリックして手動実行

---

## 🔗 関連ドキュメント

- [WordPress REST API設定ガイド](./WORDPRESS_REST_API_ENABLE.md)
- [WordPressコンテンツ同期完了](./WORDPRESS_CONTENT_SYNC_COMPLETE.md)

---

## ⚠️ 注意事項

- WordPress REST APIの認証情報は安全に管理
- 同期スクリプトの実行は、定期的に実施
- コンテンツの変更は、WordPressとGitHubで同期を保つ

---

## 📊 実装結果

**実施日**: 2026-01-11（取得）、2026-01-12（送信・自動化）

**結果**:
- ✅ WordPress REST API連携スクリプト（取得）作成完了
- ✅ 20件の投稿記事、13件の固定ページを同期完了
- ✅ WordPress REST API連携スクリプト（送信）作成完了
- ✅ GitHub Actions自動同期設定完了
- ✅ GitHubからWordPressへの自動同期が正常に動作

**実装済み機能**:
- WordPressからGitHubへの同期（手動実行）
- GitHubからWordPressへの同期（自動実行）
- ファイル変更時の自動同期
- 手動実行機能（workflow_dispatch）

**次のステップ**:
- 定期的な自動同期（cron）の実装（将来実装）
