# WordPress 403エラー その他の原因調査

## 📋 状況

- SiteGuardのダッシュボードにREST API関連の設定項目がない
- ブラウザからはREST APIにアクセスできる
- GitHub Actionsからは403エラー

→ **SiteGuardが原因ではない可能性が高い**

---

## 🔍 その他の考えられる原因

### 1. .htaccessファイルによるブロック

WordPressのルートディレクトリ（`/wp-content/`の一つ上の階層）の`.htaccess`ファイルがREST APIをブロックしている可能性があります。

**確認方法:**
1. FTPやファイルマネージャーでWordPressのルートディレクトリにアクセス
2. `.htaccess`ファイルを開く
3. `wp-json`や`REST`をブロックするルールがないか確認

**ブロックしている可能性のあるルール:**
```apache
# このようなルールがあるとREST APIがブロックされる
<FilesMatch "wp-json">
    Order Allow,Deny
    Deny from all
</FilesMatch>

# または
RewriteRule ^wp-json - [F,L]
```

---

### 2. サーバーレベル（ホスティングサービス）のセキュリティ設定

ホスティングサービス（ロリポップ、エックスサーバーなど）のセキュリティ設定がREST APIをブロックしている可能性があります。

**確認方法:**
1. ホスティングサービスの管理画面にログイン
2. セキュリティ設定やアクセス制限の項目を確認
3. REST APIやAPIアクセスに関する設定を確認

---

### 3. 他のセキュリティプラグイン

SiteGuard以外のセキュリティプラグインがREST APIをブロックしている可能性があります。

**確認方法:**
1. WordPress管理画面 → **プラグイン**
2. 有効化されているプラグインを確認
3. 以下のようなセキュリティプラグインがないか確認：
   - **Wordfence Security**
   - **iThemes Security**
   - **All In One WP Security**
   - **BulletProof Security**
   - その他のセキュリティプラグイン

**対処方法:**
1. 各セキュリティプラグインの設定を確認
2. REST API関連の設定を探す
3. REST APIを許可する設定を有効化

---

### 4. WordPressのfunctions.phpによるブロック

テーマの`functions.php`ファイルでREST APIがブロックされている可能性があります。

**確認方法:**
1. WordPress管理画面 → **外観** → **テーマファイルエディタ**
2. **「functions.php」**を選択
3. REST APIをブロックするコードがないか確認

**ブロックしている可能性のあるコード:**
```php
// このようなコードがあるとREST APIがブロックされる
add_filter('rest_authentication_errors', function($result) {
    return new WP_Error('rest_disabled', 'REST API is disabled.', array('status' => 403));
});

// または
remove_action('rest_api_init', 'rest_api_default_filters');
```

---

### 5. サーバーのmod_security（WAF）

サーバーのmod_security（Web Application Firewall）がREST APIへのアクセスをブロックしている可能性があります。

**確認方法:**
1. サーバーログを確認（`/var/log/apache2/error.log`など）
2. mod_securityによるブロックのログを確認
3. ホスティングサービスのサポートに問い合わせ

---

### 6. IPアドレスベースのブロック

GitHub ActionsのIPアドレスがサーバー側でブロックされている可能性があります。

**問題:**
- GitHub ActionsのIPアドレスは動的で、範囲が広い
- 特定のIPアドレスを許可リストに追加するのは困難

**対処方法:**
- IPベースのブロックを無効化する
- または、ホスティングサービスのサポートに相談

---

## 🎯 推奨調査手順

### Step 1: 他のセキュリティプラグインを確認

1. WordPress管理画面 → **プラグイン**
2. 有効化されているプラグインの一覧を確認
3. セキュリティ関連のプラグインを特定
4. 各プラグインの設定を確認

---

### Step 2: .htaccessファイルを確認

1. FTPやファイルマネージャーでWordPressのルートディレクトリにアクセス
2. `.htaccess`ファイルをバックアップ
3. `.htaccess`ファイルを開いて確認
4. `wp-json`やREST APIをブロックするルールがないか確認

**注意:** `.htaccess`の編集は慎重に行ってください。誤った設定はサイトを破壊する可能性があります。

---

### Step 3: サーバーログを確認

1. ホスティングサービスの管理画面からログを確認
2. 403エラーの詳細を確認
3. どのルールがブロックしているかを特定

---

### Step 4: 一時的にセキュリティプラグインを無効化（テスト用）

**注意:** 本番環境では慎重に実施してください。テスト後すぐに有効化してください。

1. 有効化されているセキュリティプラグインを一時的に無効化
2. GitHub Actionsを再実行
3. エラーが解消された場合、そのプラグインが原因と確定
4. プラグインを再度有効化し、設定を調整

---

### Step 5: ホスティングサービスのサポートに問い合わせ

上記の方法で原因が特定できない場合、ホスティングサービスのサポートに問い合わせることをお勧めします。

**問い合わせ時に伝える情報:**
1. WordPressのバージョン
2. 問題の詳細（GitHub ActionsからREST APIにアクセスできない）
3. エラーメッセージ（403 Forbidden）
4. ブラウザからのアクセスは成功する（REST API自体は有効）
5. サーバーログの内容（あれば）

---

## 🔧 代替解決策

### 方法A: REST APIエンドポイントを変更

WordPressのREST APIのエンドポイント（`/wp-json/wp/v2/`）を変更することで、ブロックを回避できる可能性があります。

**注意:** この方法は複雑で、プラグインやテーマとの互換性に影響する可能性があります。

---

### 方法B: カスタムエンドポイントを作成

WordPressプラグインを作成して、カスタムエンドポイントを提供する方法です。

**メリット:**
- REST APIの制限を回避できる
- カスタマイズ可能

**デメリット:**
- 開発が必要
- メンテナンスが必要

---

### 方法C: SSH経由でWordPress CLIを使用

GitHub ActionsからSSH経由でWordPress CLIを使用する方法です。

**メリット:**
- REST APIの制限を回避できる
- サーバー側で直接実行できる

**デメリット:**
- SSHアクセスが必要
- サーバー設定が必要
- セキュリティリスクが高い

---

## 📝 次のステップ

1. **他のセキュリティプラグインを確認**
2. **.htaccessファイルを確認**
3. **サーバーログを確認**
4. **必要に応じてホスティングサービスのサポートに問い合わせ**

---

## 🔗 参考情報

- [WordPress REST API Handbook](https://developer.wordpress.org/rest-api/)
- [.htaccess ファイルの編集方法](https://wordpress.org/support/article/htaccess/)
