# WordPress自動同期のトラブルシューティング

## ⚠️ 問題: GitHub Actionsは実行されたが、WordPressに記事が反映されない

### 確認事項

1. **GitHub Actionsのログを確認**
   - GitHubリポジトリ → Actionsタブ
   - 「Sync to WordPress」ワークフローをクリック
   - 「sync」ジョブをクリック
   - 「Sync to WordPress via REST API」ステップを展開
   - エラーメッセージを確認

---

## 🔍 よくある原因と解決方法

### 原因1: WordPress REST APIの認証エラー（401 Unauthorized）

**エラーメッセージ例:**
```
401 Unauthorized
```

**解決方法:**
1. GitHub Secretsの設定を確認
   - `WORDPRESS_USERNAME`: `yoshiki`
   - `WORDPRESS_APP_PASSWORD`: `Zn5jnUxjfP0DQNgB6fCbaUYy`（スペースなし）
2. WordPressのアプリケーションパスワードを再確認
   - WordPress管理画面 → ユーザー → プロフィール
   - アプリケーションパスワードが正しいか確認

---

### 原因2: WordPress URLが間違っている（404 Not Found）

**エラーメッセージ例:**
```
404 Not Found
```

**解決方法:**
1. GitHub Secretsの `WORDPRESS_URL` を確認
   - 正しい値: `https://cbd-no-hito.com`（末尾の`/`は不要）
2. WordPress REST APIが有効か確認
   - https://cbd-no-hito.com/wp-json/wp/v2/posts にアクセス
   - JSONが表示されればOK

---

### 原因3: スクリプトのロジックエラー

**エラーメッセージ例:**
```
⚠️ 同期するファイルがありません
```

**原因:**
- `wordpress/posts/` ディレクトリが正しく検知されていない
- ファイルパスが間違っている

**解決方法:**
1. スクリプトのログを確認
2. ファイルパスを確認
3. スクリプトを修正

---

### 原因4: 記事の作成は成功したが、スラッグが異なる

**確認方法:**
1. WordPress管理画面 → 投稿 → 投稿一覧
2. すべての投稿を確認
3. スラッグが `cbd-oil-howto` でない可能性

**解決方法:**
- スクリプトのロジックを確認
- スラッグの生成方法を確認

---

## 🛠️ スクリプトの改善が必要な可能性

現在のスクリプト（`.github/scripts/sync_to_wordpress.py`）は、基本的な実装ですが、以下の改善が必要な可能性があります：

1. **エラーハンドリングの強化**
2. **ログ出力の詳細化**
3. **ファイルパスの検証**
4. **スラッグの生成ロジックの改善**

---

## 📋 次のステップ

1. **GitHub Actionsのログを確認**
   - エラーメッセージを特定
2. **エラーに応じて対応**
   - 上記の解決方法を試す
3. **スクリプトを改善（必要に応じて）**
   - エラーハンドリングを強化
   - ログ出力を詳細化
