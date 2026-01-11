# アフィリエイトリンクサンプルデータ追加完了

## ✅ 完了したこと

### 1. スプレッドシートにサンプルデータを追加 ✅

記事（https://cbd-no-hito.com/cbd-oil-howto/）から抽出したアフィリエイトリンクを3件追加しました：

| 商品ID | 商品名 | アフィリエイトサービス | アフィリエイトURL |
|--------|--------|----------------------|------------------|
| cbd-oil-naturecan-001 | （NATURECAN）CBDオイル 10% | A8 | https://px.a8.net/svt/ejp?... |
| cbd-oil-roun-001 | roun（ラウン）CBN＋CBDオイル | 楽天 | （通常URLのみ） |
| cbd-oil-cannatech-001 | （CannaTech）CBDオイル 36% | A8 | https://a.r10.to/h5wCf4 |

---

## 📋 スプレッドシート

**URL:** https://docs.google.com/spreadsheets/d/1vRrHmqF04QPhpuZY0wdFO8vvwj4AIBatHGEZ5zVBi7g/edit?gid=0#gid=0

**確認事項:**
- [x] ヘッダー行が設定されている
- [x] サンプルデータが3件追加されている
- [x] 商品ID、商品名、アフィリエイトサービス、アフィリエイトURLが入力されている

---

## 🎯 次のステップ

### Step 2: WordPressプラグインの実装

次は、WordPressプラグインを実装して、スプレッドシートからデータを読み込んでショートコードでアフィリエイトリンクを表示できるようにします。

---

## 📝 WordPressとGitHubの連携について

記事コードをGitHubで管理する方法については、`docs/WORDPRESS_GITHUB_SYNC.md` を参照してください。

### 簡単な方法（推奨）

1. **GitHubリポジトリを作成**
2. **記事コードをGitHubにコミット**
   - ファイル: `wordpress/posts/cbd-oil-howto.html`
   - 既にローカルに保存済み

3. **必要に応じてWordPressに手動で同期**
   - WordPress管理画面 → 投稿 → 新規追加
   - コードエディタに切り替え
   - 記事コードを貼り付け

---

## ✅ 確認事項

スプレッドシートを確認して、以下が正しく追加されているか確認してください：

- [ ] ヘッダー行（1行目）が設定されている
- [ ] サンプルデータ（2-4行目）が追加されている
- [ ] 商品IDがユニークか確認
- [ ] アフィリエイトURLが正しく入力されているか確認
