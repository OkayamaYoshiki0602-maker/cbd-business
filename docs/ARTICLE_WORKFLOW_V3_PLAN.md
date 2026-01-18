# 記事ワークフロー v3 実装計画

## 📋 要件整理

### 1. ワークフロー順番の変更

**現在:**
```
Google Sheets → 記事生成 → WordPress下書き → スプレッドシート反映 → 承認 → GitHub → 投稿
```

**変更後:**
```
Google Sheets → 記事生成 → GitHub（Markdown保存）→ WordPress下書き → スプレッドシート反映 → 承認 → 投稿（13時/18時/21時）
```

---

### 2. スラッグ生成の改善

**問題点:**
- 現在のスラッグ生成がシンプルすぎる
- SEO的にも魅力的ではない

**改善案:**
- タイトルからSEOを意識したスラッグを生成
- キーワードを含む魅力的なスラッグ
- 例: `cbd-初心者-おすすめ-商品5選` → `cbd-beginners-guide-best-products-2025`

---

### 3. タグの振り分け

**問題点:**
- タグが適切に振り分けられていない

**改善案:**
- 記事タイプ、ターゲット、キーワードから自動的にタグを生成
- カテゴリ別のタグ体系を定義
  - 商品紹介: `CBD商品`, `CBDオイル`, `商品レビュー`
  - 悩み解決: `睡眠`, `ストレス`, `リラックス`, `健康`
  - 経済・ビジネス: `CBD市場`, `ビジネス`, `経済`

---

### 4. 記事デザインの改善

**問題点:**
- 下書き時点で全くデザインされていない
- 参考記事（Naturecanレビュー）のようなHTMLブロック構造が適用されていない

**必要なHTML構造:**
- `<div class="wp-block-group cbd-aff-disclaimer">` - アフィリエイト免責事項
- `<h2 class="wp-block-heading is-style-default">` - 見出し
- `<div class="wp-block-group is-style-big_icon_good">` - 「この記事で分かること」ボックス
- `<ul class="wp-block-list is-style-num_circle">` - 番号付きリスト
- `<figure class="wp-block-table is-style-regular">` - テーブル
- `<ul class="wp-block-list is-style-good_list">` - メリットリスト
- `<ul class="wp-block-list is-style-bad_list">` - デメリットリスト
- `<div class="swell-block-button is-style-btn_normal">` - アフィリエイトボタン
- `<hr class="wp-block-separator has-css-opacity is-style-wide"/>` - 区切り線

---

### 5. アフィリエイトリンクの作成＆管理

**必要な機能:**
- アフィリエイトリンクのデータベース管理（Google SheetsまたはJSON）
- 記事タイプ・ターゲットに応じたアフィリエイトリンクの自動選択
- アフィリエイトリンクのHTML生成（`swell-block-button`形式）

**管理方法:**
- Google Sheetsにアフィリエイトリンクデータを管理
- 列構成: 商品名、ブランド、URL、A8.net ID、説明、対象記事タイプ

---

### 6. 承認済み記事の定期投稿（13時/18時/21時）

**必要な機能:**
- スプレッドシートで「承認済み」の記事を検出
- 指定時刻（13時、18時、21時）に自動投稿
- Launch Agentまたはcronで定期実行

---

## 🔄 実装順序

### Phase 1: 記事デザインの改善（最優先）
1. Markdown → WordPress HTML変換機能の強化
2. 参考記事のHTMLブロック構造を適用
3. アフィリエイト免責事項、リスト、テーブル、ボタンの生成

### Phase 2: ワークフロー順番の変更
1. GitHubへのMarkdown保存を先に実行
2. WordPress下書きへの投稿
3. スプレッドシートへの反映

### Phase 3: スラッグ・タグの改善
1. SEOを意識したスラッグ生成
2. タグの自動振り分け機能

### Phase 4: アフィリエイトリンク管理
1. アフィリエイトリンクデータベースの作成
2. 記事タイプに応じたリンク選択機能
3. アフィリエイトリンクHTML生成

### Phase 5: 承認済み記事の定期投稿
1. 承認済み記事の検出機能
2. 指定時刻（13時、18時、21時）の投稿機能
3. Launch Agent設定

---

## 📝 実装詳細

### 1. 記事デザインの改善

**ファイル:** `automation/content/markdown_to_wordpress_html.py`（新規作成）

**機能:**
- Markdown → WordPress HTML変換
- 参考記事のHTMLブロック構造を適用
- アフィリエイト免責事項の自動挿入
- リスト、テーブル、ボタンの適切なHTML生成

### 2. ワークフロー順番の変更

**ファイル:** `automation/content/article_generator_v3.py`（新規作成）

**変更点:**
1. Google Sheetsから記事テーマを読み込み
2. Gemini APIで記事生成
3. **GitHubにMarkdownとして保存**
4. WordPressに下書きとして投稿（HTML変換済み）
5. スプレッドシートにメタデータを反映

### 3. スラッグ・タグの改善

**スラッグ生成:**
- SEOキーワードを含む
- 英語と日本語のハイフン区切り
- 例: `cbd-beginners-guide-2025`

**タグ生成:**
- 記事タイプ、ターゲット、キーワードから自動生成
- カテゴリ別のタグ体系を定義

### 4. アフィリエイトリンク管理

**ファイル:** `automation/content/affiliate_manager.py`（新規作成）

**機能:**
- Google Sheetsからアフィリエイトリンクを読み込み
- 記事タイプに応じたリンク選択
- WordPress用HTML生成（`swell-block-button`形式）

### 5. 承認済み記事の定期投稿

**ファイル:** `automation/content/scheduled_publisher.py`（新規作成）

**機能:**
- スプレッドシートで「承認済み」記事を検出
- 指定時刻（13時、18時、21時）に投稿
- Launch Agent設定

---

## ⚠️ 注意事項

1. **既存のワークフローとの互換性**
   - 既存の`article_generator_v2.py`は残す
   - 新しい`article_generator_v3.py`を作成

2. **アフィリエイトリンクデータベース**
   - Google Sheetsで管理（`CBD関連/アフィリエイトリンク管理.gsheet`を活用）
   - または、JSONファイル（`affiliate_links_data.json`）を活用

3. **HTML変換の精度**
   - 参考記事のHTML構造を正確に再現
   - SWELLテーマのブロック構造に対応

---

**作成日:** 2026-01-11
