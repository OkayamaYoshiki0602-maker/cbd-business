# WordPress同期 403エラー 詳細トラブルシューティング

## 📋 状況

- **ブラウザでアクセス**: ✅ 成功（`https://cbd-no-hito.com/wp-json/wp/v2/posts` で投稿が表示される）
- **GitHub Actionsからアクセス**: ❌ 403 Forbidden エラー

この状況は、**サーバー側のセキュリティ設定がGitHub Actionsからのアクセスをブロックしている**ことを示しています。

---

## 🔍 考えられる原因

### 1. SiteGuardプラグイン（最も可能性が高い）

SiteGuardプラグインがREST APIへのアクセスを制限している可能性があります。

**確認方法:**
1. WordPress管理画面 → **プラグイン** → **SiteGuard** の設定を開く
2. **「REST API」** または **「API」** の設定セクションを確認
3. REST APIへのアクセスが制限されていないか確認

**解決方法:**
- SiteGuardの設定でREST APIを許可する
- または、特定のIPアドレス（GitHub ActionsのIP範囲）を許可リストに追加

---

### 2. User-Agentベースのブロック

サーバーが特定のUser-Agentをブロックしている可能性があります。

**現在の設定:**
- スクリプトは `User-Agent: WordPress-GitHub-Sync/1.0` を送信
- サーバーがこのUser-Agentをブロックしている可能性

**解決方法:**
- サーバー側でこのUser-Agentを許可する
- または、ブラウザのUser-Agentに変更する（推奨しない）

---

### 3. IPアドレスベースのブロック

GitHub ActionsのIPアドレスがブロックされている可能性があります。

**GitHub ActionsのIP範囲:**
- GitHub Actionsは動的IPアドレスを使用
- 特定のIP範囲を許可リストに追加するのは困難

**解決方法:**
- SiteGuardなどのセキュリティプラグインで「REST API」へのアクセスを許可する設定を有効化
- IPベースのブロックを無効化する

---

### 4. .htaccessによるブロック

`.htaccess`ファイルがREST APIへのアクセスをブロックしている可能性があります。

**確認方法:**
1. WordPressのルートディレクトリ（`/wp-content/`の一つ上の階層）の `.htaccess` を確認
2. `wp-json` へのアクセスをブロックするルールがないか確認

**注意:** `.htaccess`の編集は慎重に行ってください。バックアップを取ってから編集してください。

---

### 5. アプリケーションパスワードの権限

アプリケーションパスワードに適切な権限が付与されていない可能性があります。

**確認方法:**
1. WordPress管理画面 → **ユーザー** → **プロフィール**
2. **「アプリケーションパスワード」**セクションを確認
3. 作成したパスワードが有効か確認
4. 必要に応じて新しいパスワードを作成

---

## 🎯 推奨解決手順

### Step 1: SiteGuardプラグインの設定を確認

1. WordPress管理画面にログイン
2. 左メニューから **「SiteGuard」** を選択
3. **「設定」** または **「REST API」** のセクションを探す
4. REST APIへのアクセスが許可されているか確認
5. 必要に応じて、REST APIを許可する設定を有効化

**SiteGuardの設定項目（一般的な例）:**
- 「REST API を有効にする」
- 「REST API へのアクセスを許可する」
- 「外部からのREST APIアクセスを許可する」

---

### Step 2: セキュリティプラグインの一時的な無効化（テスト用）

**注意:** 本番環境では慎重に実施してください。

1. WordPress管理画面 → **プラグイン**
2. SiteGuardプラグインを一時的に無効化
3. GitHub Actionsを再実行
4. エラーが解消された場合、SiteGuardが原因と確定
5. SiteGuardを再度有効化し、設定を調整

---

### Step 3: サーバーログの確認

サーバーのアクセスログを確認して、403エラーの詳細を確認します。

**確認したい情報:**
- リクエストヘッダー（User-Agent、Authorizationなど）
- エラーメッセージの詳細
- どのルールがブロックしているか

**ログの場所（一般的な例）:**
- `/var/log/apache2/access.log` (Apache)
- `/var/log/nginx/access.log` (Nginx)
- ホスティングサービスの管理画面から確認

---

### Step 4: WordPressのデバッグモードを有効化

WordPressのデバッグモードを有効化して、より詳細なエラー情報を取得します。

**注意:** デバッグモードは本番環境では推奨されません。テスト後に無効化してください。

1. `wp-config.php` を編集
2. 以下を追加または変更：

```php
define('WP_DEBUG', true);
define('WP_DEBUG_LOG', true);
define('WP_DEBUG_DISPLAY', false);
```

3. GitHub Actionsを再実行
4. `/wp-content/debug.log` を確認

---

## 🔧 代替解決策

### 方法A: SSH経由でWordPress CLIを使用

GitHub ActionsからSSH経由でWordPress CLIを使用する方法です。

**メリット:**
- REST APIの制限を回避できる
- サーバー側で直接実行できる

**デメリット:**
- SSHアクセスが必要
- サーバー設定が必要
- セキュリティリスクが高い

---

### 方法B: カスタムエンドポイントの作成

WordPressプラグインを作成して、カスタムエンドポイントを提供する方法です。

**メリット:**
- REST APIの制限を回避できる
- カスタマイズ可能

**デメリット:**
- 開発が必要
- メンテナンスが必要

---

## 📝 次のステップ

1. **SiteGuardプラグインの設定を確認**
   - REST APIを許可する設定を有効化
   
2. **GitHub Actionsを再実行**
   - エラーが解消されたか確認

3. **まだエラーが出る場合**
   - サーバーログを確認
   - ホスティングサービスのサポートに問い合わせ

---

## 🔗 参考リンク

- [WordPress REST API Handbook](https://developer.wordpress.org/rest-api/)
- [SiteGuardプラグインのドキュメント](https://siteguard.jp/)
- [WordPress Application Passwords](https://make.wordpress.org/core/2020/11/05/application-passwords-integration-guide/)

---

## ⚠️ 注意事項

- セキュリティプラグインの設定変更は慎重に行ってください
- 本番環境でのテストは、バックアップを取ってから実施してください
- 一時的な無効化は、テスト後すぐに元に戻してください
