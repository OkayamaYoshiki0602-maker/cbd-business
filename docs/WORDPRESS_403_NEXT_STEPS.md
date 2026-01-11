# WordPress 403エラー 次のステップ

## 📋 現在の状況まとめ

- ✅ ブラウザからREST APIにアクセスできる
- ❌ GitHub Actionsから403エラー
- ✅ SiteGuardのダッシュボードにREST API関連の設定項目がない
- ✅ ConoHa WINGのREST-API設定は「利用」（有効）
- 🔍 `.htaccess`ファイルを確認する必要がある

---

## 🎯 次の調査ステップ（優先順）

### 1. .htaccessファイルを確認 ⭐⭐⭐（最重要）

ConoHa WINGのファイルマネージャーで`.htaccess`ファイルを確認してください。

**確認手順:**
1. ConoHa WINGのコントロールパネル → **「ファイルマネージャー」**
2. `public_html`フォルダーを開く
3. **`.htaccess`**ファイルを探す（隠しファイルなので表示設定を確認）
4. `.htaccess`ファイルを開いて内容を確認

**確認すべきルール:**
```apache
# REST APIをブロックする可能性のあるルール
<FilesMatch "wp-json">
    Order Allow,Deny
    Deny from all
</FilesMatch>

# または
RewriteRule ^wp-json - [F,L]
```

**詳細な手順:** `docs/CONOHA_WING_HTACCESS_CHECK.md`を参照

---

### 2. WordPressのfunctions.phpを確認 ⭐⭐

`.htaccess`ファイルに問題がない場合、テーマの`functions.php`ファイルを確認します。

**確認方法:**
1. ファイルマネージャーで以下を開く：
   - `public_html/wp-content/themes/[テーマ名]/functions.php`
   - SWELLテーマを使用している場合：`public_html/wp-content/themes/swell/functions.php`
2. REST APIをブロックするコードがないか確認

---

### 3. サーバーログを確認 ⭐

ConoHa WINGのコントロールパネルからサーバーログを確認します。

**確認方法:**
1. ConoHa WINGのコントロールパネル → **「ログ」** または **「アクセスログ」**
2. 403エラーの詳細を確認
3. どのルールがブロックしているかを特定

---

### 4. ConoHa WINGのサポートに問い合わせ ⭐

上記の方法で原因が特定できない場合、ConoHa WINGのサポートに問い合わせることをお勧めします。

**問い合わせ時に伝える情報:**
1. WordPressのバージョン
2. 問題の詳細（GitHub ActionsからREST APIにアクセスできない）
3. エラーメッセージ（403 Forbidden）
4. ブラウザからのアクセスは成功する（REST API自体は有効）
5. ConoHa WINGのREST-API設定は「利用」（有効）になっている
6. `.htaccess`ファイルの内容（あれば）
7. サーバーログの内容（あれば）

---

## 📝 調査結果の記録

以下の情報を記録しておくと、サポートに問い合わせる際に役立ちます：

- [ ] `.htaccess`ファイルの内容（REST API関連のルール）
- [ ] `functions.php`の内容（REST API関連のコード）
- [ ] サーバーログの内容（403エラーの詳細）

---

## 🔗 参考ドキュメント

- `docs/CONOHA_WING_HTACCESS_CHECK.md` - .htaccessファイル確認の詳細手順
- `docs/WORDPRESS_403_ALTERNATIVE_CAUSES.md` - その他の原因の詳細
- `docs/WORDPRESS_403_INVESTIGATION_CHECKLIST.md` - 調査チェックリスト
