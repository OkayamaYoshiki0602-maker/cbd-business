# GitHub Actions実行状況の確認方法

## 📋 確認手順

### Step 1: GitHubリポジトリにアクセス

1. ブラウザで以下のURLにアクセス：
   ```
   https://github.com/OkayamaYoshiki0602-maker/cbd-business
   ```

### Step 2: Actionsタブを開く

1. リポジトリページの上部にある「**Actions**」タブをクリック

### Step 3: ワークフローの実行状況を確認

1. 左サイドバーで「**Sync to WordPress**」をクリック
2. 最近の実行履歴が表示されます
3. 各実行をクリックすると詳細が表示されます

---

## 🔍 確認ポイント

### ✅ 正常な場合

- 実行ステータスが「**✓（緑色のチェックマーク）**」になっている
- 「Sync to WordPress via REST API」ステップで以下のようなメッセージが表示される：
  ```
  ✅ 投稿を作成しました: CBDオイルの正しい選び方：安心して始めるための完全ガイド (ID: XXX)
  ✅ 同期処理が完了しました
  ```

### ❌ エラーの場合

- 実行ステータスが「**✗（赤色のX）**」になっている
- 「Sync to WordPress via REST API」ステップをクリックしてエラーメッセージを確認

---

## 🚨 よくあるエラー

### 403 Forbidden エラー

**エラーメッセージ例:**
```
403 Client Error: Forbidden for url: https://cbd-no-hito.com/wp-json/wp/v2/posts
```

**解決方法:**
→ `docs/WORDPRESS_403_ERROR_FIX.md` を参照

### 401 Unauthorized エラー

**エラーメッセージ例:**
```
401 Client Error: Unauthorized for url: https://cbd-no-hito.com/wp-json/wp/v2/posts
```

**解決方法:**
→ GitHub Secretsの設定を確認（`WORDPRESS_USERNAME`、`WORDPRESS_APP_PASSWORD`）

---

## 📝 手動実行の方法

GitHub Actionsは自動実行されますが、手動で実行することもできます：

1. GitHubリポジトリ → **Actions**タブ
2. 左サイドバーで「**Sync to WordPress**」をクリック
3. 右側の「**Run workflow**」ボタンをクリック
4. ブランチを選択（通常は`main`）
5. 「**Run workflow**」ボタンをクリック

---

## 🔄 最新の実行を確認

1. Actionsタブを開く
2. 最新の実行（一番上）をクリック
3. 「**sync**」ジョブをクリック
4. 「**Sync to WordPress via REST API**」ステップを展開
5. ログを確認
