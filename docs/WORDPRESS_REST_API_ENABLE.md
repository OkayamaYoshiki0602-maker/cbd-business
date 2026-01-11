# WordPress REST API有効化ガイド

## 🎯 目的

403 Forbiddenエラーを解決するため、WordPress REST APIを有効化します。

---

## 🔍 確認事項

### Step 1: REST APIが有効か確認

ブラウザで以下にアクセスしてください：

**URL:** https://cbd-no-hito.com/wp-json/wp/v2/posts

**期待される結果:**
- ✅ **JSONが表示される** → REST APIは有効（他の原因を調査）
- ❌ **403 Forbidden** → REST APIがブロックされている（このガイドを参照）
- ❌ **404 Not Found** → REST APIが無効化されている

---

## 🔧 解決方法

### 方法1: SiteGuardプラグインの設定（推奨）

画像で「SiteGuard」プラグインが確認されています。

#### Step 1: SiteGuardの設定を開く

1. WordPress管理画面にログイン
2. 左メニューから **「SiteGuard」** をクリック

#### Step 2: REST APIの設定を確認

1. **「REST API」** または **「API」** の設定項目を探す
2. REST APIを許可する設定を**有効化**
3. 設定を保存

---

### 方法2: functions.phpでREST APIを有効化（上級者向け）

**注意:** テーマの`functions.php`を編集します。事前にバックアップを取ってください。

1. **WordPress管理画面 → 外観 → テーマファイルエディタ**
2. **「functions.php」** を選択
3. 以下のコードを追加：

```php
// REST APIを有効化
add_filter('rest_authentication_errors', function($result) {
    if (!empty($result)) {
        return $result;
    }
    if (!is_user_logged_in()) {
        return new WP_Error('rest_not_logged_in', 'You are not currently logged in.', array('status' => 401));
    }
    return $result;
});
```

4. **「ファイルを更新」** をクリック

---

### 方法3: .htaccessの確認（サーバー管理者向け）

**注意:** `.htaccess`の編集は慎重に行ってください。誤った設定はサイトを破壊する可能性があります。

1. WordPressのルートディレクトリの `.htaccess` を確認
2. REST APIをブロックするルールがないか確認
3. 必要に応じて、以下のルールを追加：

```apache
# REST APIを許可
<IfModule mod_rewrite.c>
RewriteEngine On
RewriteRule ^wp-json/(.*)$ wp-json/$1 [L]
</IfModule>
```

---

## ✅ 確認方法

### Step 1: REST APIにアクセス

ブラウザで以下にアクセス：
- https://cbd-no-hito.com/wp-json/wp/v2/posts

**期待される結果:**
- ✅ JSONが表示される

### Step 2: GitHub Actionsを再実行

1. GitHubリポジトリ → Actionsタブ
2. 「Sync to WordPress」ワークフロー → 「Run workflow」をクリック
3. エラーが解消されたか確認

---

## 📝 参考情報

- [WordPress REST API Handbook](https://developer.wordpress.org/rest-api/)
- [SiteGuardプラグイン](https://siteguard.jp/)
