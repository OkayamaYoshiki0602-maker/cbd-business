# ConoHa WING .htaccessファイル確認ガイド

## 📋 現在の状況

- ✅ ConoHa WINGのREST-API設定は「利用」（有効）
- ❌ GitHub Actionsから403エラー
- 🔍 `.htaccess`ファイルを確認する必要がある

---

## 🔍 .htaccessファイルの確認手順

### Step 1: ファイルマネージャーでWordPressのルートディレクトリを開く

1. ConoHa WINGのコントロールパネルにログイン
   - https://cp.conoha.jp/
2. **「ファイルマネージャー」**を開く
3. 左側のフォルダーツリーで **`public_html`** フォルダーを探す
4. **`public_html`** フォルダーをクリックして開く
   - 通常、WordPressのファイルは`public_html`内にあります

---

### Step 2: .htaccessファイルを探す

**`.htaccess`ファイルの特徴:**
- ファイル名が **`.htaccess`**（ドットで始まる）
- 通常、隠しファイルなので、表示設定で「隠しファイルを表示」を有効にする必要がある場合があります

**確認方法:**
1. `public_html`フォルダー内のファイル一覧を確認
2. **`.htaccess`**という名前のファイルを探す
3. 見つからない場合：
   - ファイルマネージャーの「表示オプション」や「設定」から「隠しファイルを表示」を有効化
   - または、WordPressがサブディレクトリにインストールされている場合、そのディレクトリ内を確認

---

### Step 3: .htaccessファイルを開く

1. **`.htaccess`**ファイルを右クリック
2. **「編集」**または**「開く」**を選択
3. ファイルの内容を確認

---

## 🔍 確認すべき内容

`.htaccess`ファイルの中で、以下のようなルールがないか確認してください：

### REST APIをブロックする可能性のあるルール

```apache
# パターン1: wp-jsonをブロック
<FilesMatch "wp-json">
    Order Allow,Deny
    Deny from all
</FilesMatch>

# パターン2: RewriteRuleでブロック
RewriteRule ^wp-json - [F,L]

# パターン3: mod_rewriteでブロック
<IfModule mod_rewrite.c>
    RewriteEngine On
    RewriteRule ^wp-json/(.*)$ - [F,L]
</IfModule>
```

---

## 📝 .htaccessファイルが見つからない場合

`.htaccess`ファイルが見つからない場合、以下の可能性があります：

1. **WordPressがサブディレクトリにインストールされている**
   - `public_html/[ディレクトリ名]/`内を確認

2. **.htaccessファイルが存在しない**
   - WordPressが正しくインストールされていない可能性
   - または、WordPressがパーマリンク設定をまだ行っていない

3. **隠しファイルが表示されていない**
   - ファイルマネージャーの設定で「隠しファイルを表示」を有効化

---

## 🔧 その他の確認事項

### 1. WordPressのfunctions.phpを確認

`.htaccess`ファイルに問題がない場合、WordPressテーマの`functions.php`ファイルを確認します。

**確認方法:**
1. ファイルマネージャーで以下のパスを開く：
   - `public_html/wp-content/themes/[テーマ名]/functions.php`
2. `functions.php`ファイルを開く
3. REST APIをブロックするコードがないか確認

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

---

### 2. サーバーログを確認

ConoHa WINGのコントロールパネルからサーバーログを確認します。

**確認方法:**
1. ConoHa WINGのコントロールパネル → **「ログ」** または **「アクセスログ」**
2. 403エラーの詳細を確認
3. どのルールがブロックしているかを特定

---

## 🆘 次のステップ

1. **`.htaccess`ファイルを確認**
   - REST APIをブロックするルールがないか確認
   
2. **問題のあるルールが見つかった場合**
   - 該当するルールを削除またはコメントアウト
   - バックアップを取ってから編集
   
3. **問題が見つからない場合**
   - `functions.php`を確認
   - サーバーログを確認
   - ConoHa WINGのサポートに問い合わせ

---

## ⚠️ 注意事項

- `.htaccess`ファイルや`functions.php`ファイルの編集は慎重に行ってください
- **編集前に必ずバックアップを取ってください**
- 誤った設定はサイトを破壊する可能性があります
- 本番環境でのテストは、バックアップを取ってから実施してください

---

## 🔗 参考情報

- `docs/WORDPRESS_403_ALTERNATIVE_CAUSES.md` - その他の原因の詳細
- `docs/CONOHA_WING_REST_API_SETUP.md` - ConoHa WINGの設定ガイド
