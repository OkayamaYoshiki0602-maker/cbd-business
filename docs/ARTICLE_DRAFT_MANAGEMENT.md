# 記事下書き管理ガイド

## 📋 概要

新規作成した記事をすべて下書きとして保存し、添削後に公開するための管理方法です。

---

## 1. 下書き保存の自動化

### 1.1 記事作成スクリプトの動作

`complete_article_with_requirements.py`を実行すると、記事は自動的に**下書き（draft）**として保存されます。

```bash
# 記事を完成させる（自動的に下書きとして保存）
python3 automation/scripts/complete_article_with_requirements.py 1097 review
```

**保存される状態**:
- ✅ ステータス: `draft`（下書き）
- ✅ メタデータ: カテゴリー、タグ、ディスクリプション設定済み
- ✅ アイキャッチ画像: 設定済み（生成された場合）
- ✅ 記事本文: 改善済み

---

## 2. 下書き記事の確認方法

### 2.1 WordPress管理画面で確認

1. [WordPress管理画面](https://cbd-no-hito.com/wp-admin/)にログイン
2. 「投稿」→「投稿一覧」を選択
3. 「下書き」フィルターを選択
4. 新規作成した記事を確認

### 2.2 記事IDで直接確認

```
https://cbd-no-hito.com/wp-admin/post.php?post={記事ID}&action=edit
```

**例**:
- 記事ID 1097: https://cbd-no-hito.com/wp-admin/post.php?post=1097&action=edit
- 記事ID 1088: https://cbd-no-hito.com/wp-admin/post.php?post=1088&action=edit

---

## 3. 記事の公開方法

### 3.1 WordPress管理画面から公開

1. 下書き記事を開く
2. 内容を確認・添削
3. 右上の「公開」ボタンをクリック

### 3.2 スクリプトで一括公開

```bash
# 記事を公開
python3 automation/scripts/publish_article.py 1097
```

---

## 4. 下書き記事の一覧取得

### 4.1 スクリプトで一覧表示

```bash
# 下書き記事の一覧を表示
python3 automation/scripts/list_draft_articles.py
```

**出力例**:
```
📝 下書き記事一覧:

1. 記事ID: 1097
   タイトル: 【決定版】Naturecan(ネイチャーカン)の評判は？世界No.1と言われる3つの理由
   スラッグ: naturecan-review
   作成日: 2025-01-13
   URL: https://cbd-no-hito.com/wp-admin/post.php?post=1097&action=edit

2. 記事ID: 1088
   タイトル: 【2025年版】CBD市場はどう変わる？法改正の動きと失敗しないCBD製品の選び方
   スラッグ: cbd-market-trends-2025
   作成日: 2025-01-13
   URL: https://cbd-no-hito.com/wp-admin/post.php?post=1088&action=edit
```

---

## 5. 記事作成時の自動設定

### 5.1 自動的に下書きとして保存

記事作成スクリプト（`complete_article_with_requirements.py`）は、以下の設定で記事を作成します:

```python
update_data = {
    'status': 'draft',  # 下書きとして保存（添削後に公開）
    'featured_media': featured_media_id,  # アイキャッチ画像
    'categories': categories,  # カテゴリー
    'tags': tags,  # タグ
    'excerpt': excerpt,  # ディスクリプション
    'content': improved_content,  # 改善された記事本文
}
```

### 5.2 下書き保存の理由

- ✅ **添削のため**: 内容を確認してから公開
- ✅ **品質管理**: 公開前に最終チェック
- ✅ **SEO対策**: メタデータの確認

---

## 6. 記事公開前のチェックリスト

### 6.1 必須チェック項目

- [ ] タイトルが適切か
- [ ] ディスクリプションが適切か（120〜160文字）
- [ ] アイキャッチ画像が設定されているか
- [ ] カテゴリー・タグが適切か
- [ ] アフィリエイトリンクが正しく設定されているか
- [ ] 画像が正しく表示されているか
- [ ] 表が正しく表示されているか
- [ ] メリット・デメリットが明記されているか
- [ ] 「こんな人におすすめ」セクションがあるか

### 6.2 推奨チェック項目

- [ ] 見出し構造が適切か（H2: 3〜8個）
- [ ] 画像配置が適切か（300〜500文字ごとに1枚）
- [ ] 内部リンクが適切に配置されているか
- [ ] まとめセクションがあるか

---

## 7. 一括公開スクリプト

### 7.1 記事を公開

```bash
# 単一記事を公開
python3 automation/scripts/publish_article.py 1097

# 複数記事を一括公開
python3 automation/scripts/publish_article.py 1097 1088
```

### 7.2 公開前の確認

```bash
# 記事の内容を確認してから公開
python3 automation/scripts/publish_article.py 1097 --confirm
```

---

## 8. 関連ドキュメント

- [記事作成要件定義書](./ARTICLE_CREATION_REQUIREMENTS.md)
- [WordPress REST API連携要件](./WORDPRESS_SYNC_REQUIREMENTS.md)
