# WordPress 403エラー 調査チェックリスト

## 📋 現在の状況

- ✅ ブラウザからREST APIにアクセスできる
- ❌ GitHub Actionsから403エラー
- ✅ SiteGuardのダッシュボードにREST API関連の設定項目がない

→ **SiteGuardが原因ではない可能性が高い**

---

## 🔍 調査手順（優先順）

### 1. 他のセキュリティプラグインを確認 ⭐⭐⭐

**確認方法:**
1. WordPress管理画面 → **プラグイン**
2. **有効化されているプラグイン**の一覧を確認
3. 以下のようなセキュリティプラグインがないか確認：

**確認すべきプラグイン:**
- Wordfence Security
- iThemes Security（旧Better WP Security）
- All In One WP Security
- BulletProof Security
- Security Ninja
- WP Security
- その他のセキュリティプラグイン

**対処方法:**
- 各プラグインの設定画面を開く
- REST API関連の設定を探す
- REST APIを許可する設定を有効化

---

### 2. .htaccessファイルを確認 ⭐⭐⭐

WordPressのルートディレクトリの`.htaccess`ファイルがREST APIをブロックしている可能性があります。

**確認方法:**
1. FTPやファイルマネージャーでWordPressのルートディレクトリにアクセス
   - 通常は `/wp-content/` の一つ上の階層
2. `.htaccess`ファイルをバックアップ（重要！）
3. `.htaccess`ファイルを開く
4. 以下のようなルールがないか確認：

**ブロックしている可能性のあるルール:**
```apache
# REST APIをブロックする可能性のあるルール
<FilesMatch "wp-json">
    Order Allow,Deny
    Deny from all
</FilesMatch>

# または
RewriteRule ^wp-json - [F,L]

# または
<IfModule mod_rewrite.c>
    RewriteEngine On
    RewriteRule ^wp-json/(.*)$ - [F,L]
</IfModule>
```

**対処方法:**
- 該当するルールを削除またはコメントアウト
- または、REST APIを許可するルールを追加

**注意:** `.htaccess`の編集は慎重に行ってください。誤った設定はサイトを破壊する可能性があります。

---

### 3. ホスティングサービスのセキュリティ設定を確認 ⭐⭐

ホスティングサービス（ロリポップ、エックスサーバー、さくらのレンタルサーバーなど）のセキュリティ設定がREST APIをブロックしている可能性があります。

**確認方法:**
1. ホスティングサービスの管理画面にログイン
2. セキュリティ設定やアクセス制限の項目を確認
3. 以下のような設定を確認：
   - APIアクセス制限
   - REST APIブロック
   - アクセス制限ルール
   - WAF設定

**対処方法:**
- REST APIを許可する設定を有効化
- または、ホスティングサービスのサポートに問い合わせ

---

### 4. WordPressのfunctions.phpを確認 ⭐

テーマの`functions.php`ファイルでREST APIがブロックされている可能性があります。

**確認方法:**
1. WordPress管理画面 → **外観** → **テーマファイルエディタ**
2. **「functions.php」**を選択
3. 以下のようなコードがないか確認：

**ブロックしている可能性のあるコード:**
```php
// REST APIを無効化するコード
add_filter('rest_authentication_errors', function($result) {
    return new WP_Error('rest_disabled', 'REST API is disabled.', array('status' => 403));
});

// または
remove_action('rest_api_init', 'rest_api_default_filters');

// または
add_filter('rest_enabled', '__return_false');
```

**対処方法:**
- 該当するコードを削除またはコメントアウト

**注意:** `functions.php`の編集は慎重に行ってください。誤ったコードはサイトを破壊する可能性があります。

---

### 5. サーバーログを確認 ⭐

サーバーのアクセスログやエラーログを確認して、403エラーの詳細を確認します。

**確認方法:**
1. ホスティングサービスの管理画面からログを確認
2. または、FTPでサーバーにアクセスしてログファイルを確認

**ログの場所（一般的な例）:**
- `/var/log/apache2/access.log` (Apache)
- `/var/log/apache2/error.log` (Apache)
- `/var/log/nginx/access.log` (Nginx)
- `/var/log/nginx/error.log` (Nginx)
- ホスティングサービスの管理画面から確認

**確認したい情報:**
- リクエストヘッダー（User-Agent、Authorizationなど）
- エラーメッセージの詳細
- どのルールがブロックしているか

---

### 6. 一時的にプラグインを無効化（テスト用） ⭐⭐

**注意:** 本番環境では慎重に実施してください。テスト後すぐに有効化してください。

**手順:**
1. WordPress管理画面 → **プラグイン**
2. 有効化されているセキュリティプラグインを一時的に無効化
   - 一つずつ無効化してテスト
3. GitHub Actionsを再実行
4. エラーが解消された場合、そのプラグインが原因と確定
5. プラグインを再度有効化し、設定を調整

---

## 📝 調査結果の記録

以下の情報を記録しておくと、サポートに問い合わせる際に役立ちます：

- [ ] 有効化されているプラグインの一覧
- [ ] `.htaccess`ファイルの内容（REST API関連のルール）
- [ ] `functions.php`の内容（REST API関連のコード）
- [ ] サーバーログの内容（403エラーの詳細）
- [ ] ホスティングサービスの情報（サービス名、プランなど）

---

## 🆘 原因が特定できない場合

上記の手順で原因が特定できない場合、以下の方法を検討してください：

1. **ホスティングサービスのサポートに問い合わせ**
   - 上記の調査結果をまとめて問い合わせ

2. **代替解決策を検討**
   - SSH経由でWordPress CLIを使用
   - カスタムエンドポイントを作成
   - REST APIエンドポイントを変更

---

## 🔗 参考ドキュメント

- `docs/WORDPRESS_403_ALTERNATIVE_CAUSES.md` - その他の原因の詳細
- `docs/WORDPRESS_SYNC_403_TROUBLESHOOTING.md` - 詳細なトラブルシューティングガイド
