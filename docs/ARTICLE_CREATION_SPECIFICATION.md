# 記事作成要件定義書

## 📋 概要

CBD情報サイト（https://cbd-no-hito.com/）の記事作成に関する要件定義書です。
参考記事のスタイルとHTML構造に基づいて、記事生成の仕様を定義します。

---

## 📚 参考記事

### 1. Naturecanレビュー記事
- **URL:** https://cbd-no-hito.com/wp-admin/post.php?post=1097&action=edit
- **ファイル:** `wordpress/posts/naturecan-review-complete.html`
- **特徴:** 商品紹介記事のテンプレート

### 2. その他の参考記事
- **URL:** https://cbd-no-hito.com/wp-admin/post.php?post=1085&action=edit
- **特徴:** その他の記事タイプのテンプレート

---

## 🎨 HTML構造・デザイン仕様

### 1. アフィリエイト免責事項（必須・記事冒頭）

```html
<div class="wp-block-group cbd-aff-disclaimer">
<div class="wp-block-group__inner-container">
<p style="font-size:13px;opacity:.8">※当サイトはアフィリエイト広告を利用しています。価格・在庫・成分はリンク先の最新情報が正となります。</p>
</div>
</div>
```

### 2. 記事タイトル（H2）

```html
<h2 class="wp-block-heading is-style-default">【決定版】記事タイトル</h2>
```

**要件:**
- H2タグを使用（H1はWordPressが自動生成）
- `class="wp-block-heading is-style-default"`を付与
- 【決定版】などの強調表現を含める

### 3. 導入パラグラフ

```html
<p>CBD選びで、絶対に失敗したくない。<br />自分の体に入れるものだから、1ミリの不安も残したくない。<br />そう思うなら、結論は<span class="swl-marker mark_green">Naturecan（ネイチャーカン）一択</span>です。</p>
```

**要件:**
- `<br />`で改行
- `<span class="swl-marker mark_green">`で重要な部分を強調
- ターゲットの悩みに共感する内容

### 4. 「この記事で分かること」ボックス

```html
<div class="wp-block-group is-style-big_icon_good">
<div class="wp-block-group__inner-container">
<p><strong>この記事で分かること</strong></p>
<ul class="wp-block-list is-style-num_circle">
<li>項目1</li>
<li>項目2</li>
<li>項目3</li>
</ul>
</div>
</div>
```

**要件:**
- 記事冒頭に配置（導入パラグラフの後）
- 3-5項目の箇条書き
- `is-style-num_circle`クラスで番号付きリスト

### 5. 区切り線

```html
<hr class="wp-block-separator has-css-opacity is-style-wide"/>
```

**要件:**
- 主要セクションの区切りに使用

### 6. 見出し階層

**H3見出し:**
```html
<h3 class="wp-block-heading">セクション見出し</h3>
```

**H4見出し:**
```html
<h4 class="wp-block-heading">① サブセクション見出し</h4>
```

**要件:**
- H2: 記事タイトル（1つのみ）
- H3: 主要セクション（3-5セクション）
- H4: サブセクション（必要に応じて）
- 絵文字（🥇🥈🥉）を使用してランキングを表現

### 7. テーブル（商品情報など）

```html
<figure class="wp-block-table is-style-regular">
<table>
<thead>
<tr>
<th>項目</th>
<th>内容</th>
</tr>
</thead>
<tbody>
<tr>
<td>項目名</td>
<td>内容</td>
</tr>
</tbody>
</table>
</figure>
```

**要件:**
- 商品情報を表形式で整理
- `wp-block-table is-style-regular`クラスを使用

### 8. リスト

**メリットリスト:**
```html
<p><strong>メリット</strong>：</p>
<ul class="wp-block-list is-style-good_list">
<li><span class="swl-marker mark_green">重要なメリット</span></li>
<li>メリット1</li>
<li>メリット2</li>
</ul>
```

**デメリットリスト:**
```html
<p><strong>デメリット</strong>：</p>
<ul class="wp-block-list is-style-bad_list">
<li>デメリット1</li>
<li>デメリット2</li>
</ul>
```

**おすすめリスト:**
```html
<p><strong>こんな人におすすめ</strong>：</p>
<ul class="wp-block-list">
<li>ターゲット1</li>
<li>ターゲット2</li>
</ul>
```

**要件:**
- `is-style-good_list`: メリット用
- `is-style-bad_list`: デメリット用
- 通常のリスト: その他

### 9. アフィリエイトボタン

```html
<div class="swell-block-button is-style-btn_normal">
<a href="アフィリエイトURL" target="_blank" rel="noopener noreferrer" class="swell-block-button__link">
<span>ボタンテキスト（例: 公式で詳細・成分表を見る（Naturecan））</span>
</a>
</div>
```

**要件:**
- 商品紹介の後に配置
- `swell-block-button is-style-btn_normal`クラスを使用
- A8.netなどのアフィリエイトURLを使用

### 10. 画像

```html
<figure class="wp-block-image size-large">
<img decoding="async" src="画像URL" alt="代替テキスト" />
<figcaption style="font-size:13px;opacity:.8">キャプション</figcaption>
</figure>
```

**要件:**
- `wp-block-image size-large`または`size-thumbnail`
- キャプションを付ける（オプション）

### 11. まとめボックス

```html
<div class="wp-block-group is-style-big_icon_good">
<div class="wp-block-group__inner-container">
<p><strong>Naturecanがおすすめな人</strong></p>
<ul class="wp-block-list is-style-check_list">
<li>ターゲット1</li>
<li>ターゲット2</li>
</ul>
</div>
</div>
```

**要件:**
- 記事の最後に配置
- `is-style-big_icon_good`クラスを使用
- `is-style-check_list`でチェックリスト表示

---

## 📝 記事構成の要件

### 1. 記事タイプ別の構成

#### 商品紹介記事

**構成:**
1. アフィリエイト免責事項
2. 記事タイトル（H2）
3. 導入パラグラフ（ターゲットの悩みに共感）
4. 「この記事で分かること」ボックス
5. 区切り線
6. ブランド背景・特徴（H3）
   - サブセクション（H4）
   - テーブル（商品情報）
7. 区切り線
8. おすすめ商品セクション（H3）
   - 商品1（H4）
     - 商品画像
     - 商品情報テーブル
     - メリットリスト
     - デメリットリスト
     - おすすめリスト
     - アフィリエイトボタン
   - 商品2（同様の構成）
9. 区切り線
10. まとめ（H3）
    - まとめボックス
    - 最終的なメッセージ

#### 悩み解決記事

**構成:**
1. アフィリエイト免責事項
2. 記事タイトル（H2）
3. 導入パラグラフ（悩みに共感）
4. 「この記事で分かること」ボックス
5. 区切り線
6. 悩みの原因・解説（H3）
7. CBDの効果・エビデンス（H3）
8. 解決方法・実践的なアドバイス（H3）
9. おすすめ商品（必要に応じて）
10. まとめ

#### 経済・ビジネス記事

**構成:**
1. アフィリエイト免責事項（オプション）
2. 記事タイトル（H2）
3. 導入パラグラフ
4. 「この記事で分かること」ボックス
5. 区切り線
6. 市場動向・トレンド（H3）
7. 具体的なデータ・数値（テーブル）
8. ビジネス事例（H3）
9. 将来予測・展望（H3）
10. まとめ

---

## 🎯 タイトル・スラッグ・タグの要件

### 1. タイトル

**要件:**
- SEOキーワードを含む
- 読者の興味を引く表現
- 【決定版】【保存版】などの強調表現を使用
- 例: 「【決定版】Naturecan(ネイチャーカン)の評判は？世界No.1と言われる3つの理由」

### 2. スラッグ

**要件:**
- SEOを意識した英語と日本語のハイフン区切り
- タイトルから自動生成
- 例: `naturecan-review-world-no1-reasons-2026`

**現在の問題点:**
- シンプルすぎる（例: `article-20250111`）
- SEO的にも魅力的ではない

**改善案:**
- キーワードを含む
- 年号を含める（2026年以上）
- 例: `cbd-beginners-guide-best-products-2026`

### 3. タグ

**要件:**
- 記事タイプに応じて自動振り分け
- カテゴリ別のタグ体系を定義

**タグ体系:**

**商品紹介:**
- `CBD商品`, `CBDオイル`, `CBDグミ`, `CBDベイプ`, `商品レビュー`, `おすすめ商品`

**悩み解決:**
- `睡眠`, `ストレス`, `リラックス`, `健康`, `美容`, `ダイエット`, `集中力`

**経済・ビジネス:**
- `CBD市場`, `ビジネス`, `経済`, `投資`, `法規制`, `トレンド`

**その他:**
- `初心者向け`, `比較`, `使い方`, `効果`, `副作用`

---

## 🔗 アフィリエイトリンクの要件

### 1. アフィリエイトリンクの配置

**配置ポイント:**
1. 商品紹介セクション内（各商品の後に配置）
2. まとめセクション前（最終的な行動を促す）

**配置形式:**
```html
<div class="swell-block-button is-style-btn_normal">
<a href="アフィリエイトURL" target="_blank" rel="noopener noreferrer" class="swell-block-button__link">
<span>ボタンテキスト</span>
</a>
</div>
```

### 2. アフィリエイトリンクの管理（シート3：アフィリエイト管理）

**Google Sheets（シート3）で商品ごとに一元管理:**

詳細は `ARTICLE_GOOGLESHEETS_STRUCTURE.md` を参照してください。

**管理内容:**
- 商品ID、商品名、ブランド、カテゴリ
- アフィリエイトURL、ボタンテキスト
- **使用記事ID**（複数記事で同じ商品を再利用可能）
- **使用記事数**、CV数、売上など成績追跡

---

## 📊 メタデータの要件

### 1. メタディスクリプション

**要件:**
- 150文字以内
- SEOキーワードを含む
- 記事の要約と価値の提示

**例:**
```
Naturecan（ネイチャーカン）の評判を徹底解説。世界No.1と言われる3つの理由と、初心者が買うべき「後悔しない」2品を紹介。安全性と透明性を重視する方におすすめ。
```

### 2. カテゴリ

**要件:**
- 記事タイプに応じて自動設定
- WordPressのカテゴリ体系に合わせる

**カテゴリ体系:**
- `CBD商品`
- `CBD基礎知識`
- `CBD効果・使い方`
- `CBD市場・ビジネス`
- `CBDニュース`

### 3. タグ

**要件:**
- 上記「タグの要件」を参照

---

## 📝 記事作成フロー（v4）

### シート構成の更新（2026-01-17）
- **シート1:** `記事一覧` （旧シート1） - 生成した記事の管理
- **シート2:** `記事テーマ` （旧シート2） - 記事生成の入力
- **シート3:** `アフィリエイト管理` （新規） - **商品ごと**のリンク管理

詳細は `ARTICLE_GOOGLESHEETS_STRUCTURE.md` を参照

### 1. 記事生成（毎朝8:00）

1. Google Sheets（`記事テーマ`）から記事テーマを読み込み
2. Gemini APIでHTML記事を直接生成
3. WordPressに下書きとして投稿
4. スプレッドシート（シート1 / シート3）にメタデータを反映

### 2. 承認・投稿

1. WordPressの下書きを確認・添削
2. スプレッドシート（シート2）で「承認済み」に変更
3. 承認済み記事を検出（13時、18時、21時に実行）
4. WordPressに公開投稿
5. ステータスを「投稿済み」に更新

---

## 🎨 デザインガイドライン

### 1. トーン・スタイル

- **専門的でありながら親しみやすい**
- **データコンサルタントの視点**（数字・エビデンス重視）
- **少しユーモアも含める**（ポーカー・マラソン・お酒のエピソードを適度に）

### 2. 文字数

- **本文: 2,000-3,000文字**
- **見出し・リストを含めて全体で3,000-4,000文字**

### 3. 信頼性

- **公的な研究結果、論文、エビデンスを引用**
- **推測や憶測は避ける**
- **医療効果の断定的表現は避ける（薬機法遵守）**

---

## ✅ チェックリスト

### 記事生成時

- [ ] アフィリエイト免責事項が記事冒頭にある
- [ ] タイトルがSEOキーワードを含む
- [ ] 「この記事で分かること」ボックスがある
- [ ] 見出し階層（H2/H3/H4）が適切
- [ ] テーブル（商品情報）が適切に配置されている
- [ ] リスト（メリット・デメリット）が適切に使用されている
- [ ] アフィリエイトボタンが適切な位置に配置されている
- [ ] 区切り線が主要セクションの区切りに使用されている
- [ ] まとめボックスがある

### メタデータ

- [ ] メタディスクリプションが150文字以内
- [ ] スラッグがSEOを意識した形式
- [ ] タグが適切に振り分けられている

---

**作成日:** 2026-01-11  
**最終更新:** 2026-01-17
