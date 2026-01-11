# ConoHa WING REST API設定ガイド

## 📋 状況

- ConoHa WINGサーバーを使用中
- ConoHa WINGコントロールパネルプラグインが有効化されている
- WordPress REST APIがGitHub Actionsから403エラー

→ **ConoHa WINGのサーバーレベルのセキュリティ設定が原因の可能性が高い**

---

## 🔍 確認手順

### 方法1: WordPress管理画面からConoHa WINGの設定を確認

1. WordPress管理画面にログイン
2. 左メニューから **「ConoHa WING」** を探す
   - または、**「設定」** → **「ConoHa WING」**
3. セキュリティ設定やアクセス制限の項目を確認
4. REST APIやAPIアクセスに関する設定を確認

---

### 方法2: ConoHa WINGのコントロールパネルから確認

1. ConoHa WINGのコントロールパネルにログイン
   - https://cp.conoha.jp/
2. **「サーバー管理」** → **「サーバー一覧」** から該当サーバーを選択
3. **「セキュリティ」** または **「アクセス制限」** の項目を確認
4. 以下のような設定を確認：
   - REST APIブロック設定
   - APIアクセス制限
   - .htaccess設定
   - アクセス制限ルール

---

## 🔧 一般的な解決方法

### 1. .htaccessファイルの確認

ConoHa WINGでは、サーバーレベルの`.htaccess`設定がREST APIをブロックしている可能性があります。

**確認方法:**
1. ConoHa WINGのコントロールパネル → **「ファイルマネージャー」**
2. WordPressのルートディレクトリ（通常は`/home/[ユーザー名]/[ドメイン]/`）にアクセス
3. `.htaccess`ファイルを開く
4. 以下のようなルールがないか確認：

```apache
# REST APIをブロックする可能性のあるルール
<FilesMatch "wp-json">
    Order Allow,Deny
    Deny from all
</FilesMatch>

# または
RewriteRule ^wp-json - [F,L]
```

---

### 2. ConoHa WINGのセキュリティ設定を確認

ConoHa WINGには、サーバーレベルのセキュリティ設定がある場合があります。

**確認すべき設定:**
- REST APIアクセスの許可
- APIアクセス制限の無効化
- アクセス制限ルールの確認

---

### 3. ConoHa WINGのサポートに問い合わせ

上記の方法で解決しない場合、ConoHa WINGのサポートに問い合わせることをお勧めします。

**問い合わせ時に伝える情報:**
1. WordPressのバージョン
2. 問題の詳細（GitHub ActionsからREST APIにアクセスできない）
3. エラーメッセージ（403 Forbidden）
4. ブラウザからのアクセスは成功する（REST API自体は有効）
5. サーバーログの内容（あれば）

---

## 🎯 推奨手順

### Step 1: WordPress管理画面からConoHa WINGの設定を確認

1. WordPress管理画面 → 左メニューから **「ConoHa WING」** を探す
2. セキュリティ設定やアクセス制限の項目を確認
3. REST API関連の設定を確認

---

### Step 2: .htaccessファイルを確認

1. ConoHa WINGのコントロールパネル → **「ファイルマネージャー」**
2. WordPressのルートディレクトリにアクセス
3. `.htaccess`ファイルをバックアップ
4. `.htaccess`ファイルを開いて確認
5. REST APIをブロックするルールがないか確認

---

### Step 3: ConoHa WINGのコントロールパネルから確認

1. ConoHa WINGのコントロールパネルにログイン
2. **「サーバー管理」** → **「サーバー一覧」**
3. 該当サーバーを選択
4. **「セキュリティ」** または **「アクセス制限」** を確認

---

### Step 4: サーバーログを確認

1. ConoHa WINGのコントロールパネル → **「ログ」** または **「アクセスログ」**
2. 403エラーの詳細を確認
3. どのルールがブロックしているかを特定

---

## 🔗 参考情報

- [ConoHa WING公式サイト](https://www.conoha.jp/conoha/)
- [ConoHa WINGサポート](https://support.conoha.jp/)
- [WordPress REST API Handbook](https://developer.wordpress.org/rest-api/)

---

## ⚠️ 注意事項

- `.htaccess`ファイルの編集は慎重に行ってください
- 編集前に必ずバックアップを取ってください
- 誤った設定はサイトを破壊する可能性があります
- 本番環境でのテストは、バックアップを取ってから実施してください
