# WordPressアプリケーションパスワード設定ガイド

## 📋 概要

WordPress REST APIで記事を投稿するためのアプリケーションパスワードの設定方法です。

---

## ✅ 既存の「GitHub Sync」パスワードを使用する場合

**既に「GitHub Sync」という名前でアプリケーションパスワードを作成済みの場合、それを使用できます。**

### メリット
- ✅ 新しいパスワードを作成する必要がない
- ✅ 既存のパスワードをそのまま使用できる
- ✅ 複数のアプリケーションパスワードを管理する必要がない

### 注意点
- ⚠️ 既存のパスワードが分からない場合は、新しいパスワードを作成する必要があります
- ⚠️ アプリケーションパスワードは表示されないため、既存のパスワードが分からない場合は再生成が必要です

### 確認方法
1. WordPress管理画面にログイン
2. 「ユーザー」→「プロフィール」を開く
3. 「アプリケーションパスワード」セクションを開く
4. 既存の「GitHub Sync」パスワードを確認（パスワード自体は表示されません）

**既存のパスワードが分からない場合:** 新しいパスワードを作成するか、「GitHub Sync」パスワードを再生成してください。

---

## 🆕 新しいパスワードを使用する場合

新しいパスワード「Cursor Article Generator」（`dHGO JH2x DTnM zzj8 2KXd G7dj`）を使用する場合：

### .envファイルの設定

`.env`ファイルに以下を設定：

```env
WORDPRESS_USERNAME=yoshiki
WORDPRESS_APP_PASSWORD=dHGO JH2x DTnM zzj8 2KXd G7dj
```

**注意:**
- パスワードのスペースはそのまま含めてください（例: `dHGO JH2x DTnM zzj8 2KXd G7dj`）
- `.env`ファイルは`.gitignore`に含まれているため、GitHubにコミットされません

---

## 🔧 .envファイルの更新

### 方法1: エディタで直接編集

1. プロジェクトルートにある`.env`ファイルをエディタで開く
2. 以下の行を確認・更新：

```env
WORDPRESS_USERNAME=yoshiki
WORDPRESS_APP_PASSWORD=dHGO JH2x DTnM zzj8 2KXd G7dj
```

3. ファイルを保存

### 方法2: ターミナルで確認・更新

既存の設定を確認：

```bash
grep -E "WORDPRESS_USERNAME|WORDPRESS_APP_PASSWORD" .env
```

**実行結果例:**
```
WORDPRESS_USERNAME=yoshiki
WORDPRESS_APP_PASSWORD=u7X7oO2oyaGv80RJPbw84SUm
```

既存のパスワードを新しいパスワードに更新する場合：

```bash
# バックアップ（オプション）
cp .env .env.backup

# パスワードを更新（新しいパスワードを使用する場合）
# エディタで直接編集することを推奨
```

---

## ✅ 動作確認

### 1. .envファイルの設定確認

```bash
grep -E "WORDPRESS_USERNAME|WORDPRESS_APP_PASSWORD" .env
```

**期待される結果:**
```
WORDPRESS_USERNAME=yoshiki
WORDPRESS_APP_PASSWORD=dHGO JH2x DTnM zzj8 2KXd G7dj
```
または既存の「GitHub Sync」パスワード

### 2. テスト実行

記事生成スクリプトをテスト実行：

```bash
python automation/content/article_generator_v2.py
```

**実行結果:** エラーが表示されなければ成功です

---

## 🔄 既存の「GitHub Sync」パスワードを使う場合

### 既存のパスワードが分かる場合

1. `.env`ファイルに既存のパスワードを設定
2. `WORDPRESS_USERNAME=yoshiki`を設定
3. テスト実行して動作確認

### 既存のパスワードが分からない場合

#### オプション1: 新しいパスワードを作成（推奨）

新しいパスワード「Cursor Article Generator」を使用：

```env
WORDPRESS_USERNAME=yoshiki
WORDPRESS_APP_PASSWORD=dHGO JH2x DTnM zzj8 2KXd G7dj
```

#### オプション2: 既存のパスワードを再生成

1. WordPress管理画面にログイン
2. 「ユーザー」→「プロフィール」を開く
3. 「アプリケーションパスワード」セクションを開く
4. 既存の「GitHub Sync」パスワードを削除
5. 新しい「GitHub Sync」パスワードを作成
6. 生成されたパスワードを`.env`に設定

---

## 💡 推奨事項

### 複数のアプリケーションパスワードの使用

以下のように用途別にパスワードを分けることを推奨：

- **「GitHub Sync」**: GitHub ActionsでWordPressに同期する場合
- **「Cursor Article Generator」**: Cursor/AIで記事を生成・投稿する場合

**メリット:**
- ✅ 用途別に管理できる
- ✅ 必要に応じて個別に削除・再生成できる
- ✅ セキュリティが向上

---

## 🔍 トラブルシューティング

### エラー1: `401 Unauthorized`

**原因:** アプリケーションパスワードが正しくない

**解決方法:**
1. `.env`ファイルの`WORDPRESS_APP_PASSWORD`を確認
2. パスワードにスペースが含まれているか確認
3. パスワードが正しいかWordPress管理画面で確認
4. 必要に応じて新しいパスワードを作成して再設定

### エラー2: `403 Forbidden`

**原因:** ユーザーの権限が不足している

**解決方法:**
1. WordPress管理画面でユーザーの権限を確認（「管理者」権限が必要）
2. 必要に応じて権限を変更

### エラー3: `REST API is disabled`

**原因:** WordPress REST APIが無効になっている

**解決方法:**
1. WordPress管理画面で「設定」→「パーマリンク設定」を確認
2. パーマリンク設定を保存（REST APIが有効化される）

---

## 📋 チェックリスト

### 今すぐやること

- [ ] `.env`ファイルに`WORDPRESS_USERNAME=yoshiki`を設定
- [ ] `.env`ファイルに`WORDPRESS_APP_PASSWORD`を設定（既存の「GitHub Sync」パスワードまたは新しいパスワード）
- [ ] テスト実行して動作確認

---

**最終更新:** 2026-01-11
