# WordPress 403 Forbidden エラー対策

## ⚠️ エラー内容

```
403 Client Error: Forbidden for url: ***/wp-json/wp/v2/posts
```

**意味:** WordPress REST APIへのアクセスが拒否されています。

---

## 🔍 原因

403エラーは、認証（401）ではなく**認可（403）**の問題です。
- 認証情報は正しい（401ではない）
- しかし、アクセス権限がない

---

## 🔧 解決方法

### 方法1: WordPress REST APIが有効か確認

1. **ブラウザでREST APIにアクセス**
   - https://cbd-no-hito.com/wp-json/wp/v2/posts
   - JSONが表示されればOK
   - 403エラーが表示されれば、REST APIがブロックされています

---

### 方法2: セキュリティプラグインを確認

WordPressに以下のようなセキュリティプラグインがインストールされていませんか？

- **SiteGuard**（画像で確認済み）
- **Wordfence**
- **iThemes Security**
- その他のセキュリティプラグイン

**解決方法:**
1. WordPress管理画面 → プラグイン
2. セキュリティプラグインの設定を確認
3. REST APIを許可する設定を有効化

---

### 方法3: SiteGuardプラグインの設定

画像で「SiteGuard」が確認されています。

1. **WordPress管理画面 → SiteGuard**
2. **「REST API」または「API」の設定を確認**
3. **REST APIを許可する設定を有効化**

---

### 方法4: .htaccessの確認

サーバーレベルでREST APIがブロックされている可能性があります。

**確認方法:**
1. WordPressのルートディレクトリの `.htaccess` を確認
2. REST APIをブロックするルールがないか確認

**注意:** `.htaccess` の編集は慎重に行ってください。

---

### 方法5: アプリケーションパスワードの権限を確認

アプリケーションパスワードに適切な権限が付与されているか確認してください。

**確認方法:**
1. WordPress管理画面 → ユーザー → プロフィール
2. アプリケーションパスワードの一覧を確認
3. 必要に応じて新しいパスワードを作成

---

## 🎯 推奨手順

### Step 1: REST APIが有効か確認

ブラウザで以下にアクセス：
- https://cbd-no-hito.com/wp-json/wp/v2/posts

**結果:**
- ✅ JSONが表示される → REST APIは有効
- ❌ 403エラー → REST APIがブロックされている

---

### Step 2: SiteGuardプラグインの設定を確認

1. WordPress管理画面 → **SiteGuard**
2. REST APIの設定を確認
3. REST APIを許可する設定を有効化

---

### Step 3: テスト

GitHub Actionsを再実行（または手動実行）して、エラーが解消されたか確認してください。

---

## 📝 参考情報

- [WordPress REST API Handbook](https://developer.wordpress.org/rest-api/)
- [SiteGuardプラグインのドキュメント](https://siteguard.jp/)
