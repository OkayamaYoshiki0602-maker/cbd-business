# SWELL記事作成ルール（完全版）

> **作成日:** 2026-01-11  
> **目的:** 過去記事の分析とSWELLブロックの使い方を学習し、最適な記事作成ルールを定義  
> **対象:** 自動記事生成スクリプト、手動作成時の参考

---

## 📋 目次

1. [記事全体構成](#記事全体構成)
2. [HTML構造パターン](#html構造パターン)
3. [SWELLブロックの使い方](#swellブロックの使い方)
4. [見出しの使い方](#見出しの使い方)
5. [リストとテーブル](#リストとテーブル)
6. [アフィリエイトリンク配置ルール](#アフィリエイトリンク配置ルール)
7. [SEO・メタ情報](#seoメタ情報)
8. [コンテンツ品質基準](#コンテンツ品質基準)
9. [自動生成時のチェックリスト](#自動生成時のチェックリスト)

---

## 記事全体構成

### 基本構造（必須要素の順序）

```html
1. アフィリエイト免責事項（冒頭）
2. H2見出し（タイトル）
3. 導入文（1-2段落）
4. 「この記事で分かること」ボックス
5. 区切り線（<hr>）
6. H3見出し（メインコンテンツ開始）
7. 本文（H3/H4見出しで区切る）
8. 区切り線（各セクション間）
9. 商品紹介セクション（H3/H4 + テーブル + ボタン）
10. まとめセクション
11. 区切り線
12. 最終CTA・関連記事リンク（任意）
```

### セクション構成の目安

| セクション | 説明 | 必須度 |
|---|---|---|
| アフィリエイト免責事項 | 記事冒頭に配置 | ✅ 必須 |
| 導入文 | 読者の悩み・課題に共感 | ✅ 必須 |
| 「この記事で分かること」 | 目次的な役割 | ✅ 推奨 |
| 本文（H3見出し） | 3-5セクション | ✅ 必須 |
| 商品紹介 | アフィリエイトリンク含む | ✅ 必須（商品紹介記事の場合） |
| まとめ | 記事の結論・行動喚起 | ✅ 必須 |

---

## HTML構造パターン

### 1. アフィリエイト免責事項（冒頭）

```html
<div class="wp-block-group cbd-aff-disclaimer">
<div class="wp-block-group__inner-container">
<p style="font-size:13px;opacity:.8">※当サイトはアフィリエイト広告を利用しています。価格・在庫・成分はリンク先の最新情報が正となります。</p>
</div>
</div>
```

**配置位置:** 記事の最上部（H2見出しより前）

---

### 2. H2見出し（タイトル）

```html
<h2 class="wp-block-heading is-style-default">【決定版】Naturecan(ネイチャーカン)の評判は？世界No.1と言われる3つの理由</h2>
```

**ルール:**
- クラス: `is-style-default` を使用
- タイトルにはキーワードを含める
- 【】でキャッチコピーを追加（例：【決定版】【2025年版】【完全版】）

---

### 3. 導入文

```html
<p>CBD選びで、絶対に失敗したくない。<br />自分の体に入れるものだから、1ミリの不安も残したくない。<br />そう思うなら、結論は<span class="swl-marker mark_green">Naturecan（ネイチャーカン）一択</span>です。</p>

<p>「なぜこれほど高いのか？」「なぜ世界中で売れているのか？」<br />その理由は、フィットネス界の伝説による「品質革命」と、異常なまでの「安全への執着」にありました。</p>
```

**ルール:**
- 1-2段落で構成
- 読者の悩み・課題に共感する
- 重要なキーワードは `<span class="swl-marker mark_green">` で強調
- `<br />` で読みやすく改行

---

### 4. 「この記事で分かること」ボックス

```html
<div class="wp-block-group is-style-big_icon_good">
<div class="wp-block-group__inner-container">
<p><strong>この記事で分かること</strong></p>
<ul class="wp-block-list is-style-num_circle">
<li>Naturecanが世界No.1と言われる3つの理由</li>
<li>「やりすぎ」と言われる6段階テストの詳細</li>
<li>初心者が買うべき「後悔しない」2品</li>
<li>誰におすすめなのか（メリット・デメリット）</li>
</ul>
</div>
</div>
```

**ルール:**
- クラス: `is-style-big_icon_good` を使用
- リストスタイル: `is-style-num_circle` を使用
- 3-5項目で構成
- 導入文の直後に配置

---

### 5. 区切り線（セクション間）

```html
<hr class="wp-block-separator has-css-opacity is-style-wide"/>
```

**ルール:**
- 各H3見出しの前後に配置
- 重要なセクション切り替え時に使用

---

## SWELLブロックの使い方

### 強調ボックス

#### 良い情報・重要ポイント

```html
<div class="wp-block-group is-style-big_icon_good">
<div class="wp-block-group__inner-container">
<p><strong>創設者の信念</strong></p>
<p>「家族に安心して勧められるCBDがないなら、自分で作るしかない」</p>
</div>
</div>
```

#### 注意・警告情報

```html
<div class="wp-block-group is-style-big_icon_bad">
<div class="wp-block-group__inner-container">
<p><strong>THCとの違い</strong></p>
<ul class="wp-block-list is-style-bad_list">
<li><span class="swl-marker mark_orange">THC（テトラヒドロカンナビノール）</span>：精神活性あり／日本では違法</li>
<li><span class="swl-marker mark_green">CBD（カンナビジオール）</span>：精神作用なし／日本で合法</li>
</ul>
</div>
</div>
```

---

### マーカー（強調）

```html
<!-- グリーン（良い情報・おすすめ） -->
<span class="swl-marker mark_green">世界基準の安全性と透明性</span>

<!-- オレンジ（注意・警告） -->
<span class="swl-marker mark_orange">THC（テトラヒドロカンナビノール）</span>

<!-- レッド（悪い情報・危険） -->
<span class="swl-marker mark_red">違法成分が含まれる</span>

<!-- ブルー（情報・補足） -->
<span class="swl-marker mark_blue">エビデンスに基づく</span>
```

**使い分け:**
- `mark_green`: 良い情報、おすすめ、結論
- `mark_orange`: 注意喚起、比較情報
- `mark_red`: 悪い情報、危険、禁止事項
- `mark_blue`: 補足情報、エビデンス

---

### リストスタイル

#### メリットリスト（✅）

```html
<ul class="wp-block-list is-style-good_list">
<li><span class="swl-marker mark_green">世界基準の安全性と透明性</span></li>
<li>全ロットの成分表（COA）を公開</li>
<li>日本公式サイトでサポート充実</li>
</ul>
```

#### デメリットリスト（❌）

```html
<ul class="wp-block-list is-style-bad_list">
<li>価格がやや高め（通常価格8,000円）</li>
<li>初心者には少し濃度が高い場合がある</li>
</ul>
```

#### チェックリスト（✓）

```html
<ul class="wp-block-list is-style-check_list">
<li>多少高くても、<strong>世界最高レベルの安全性</strong>が欲しい人</li>
<li><strong>THCフリー</strong>が科学的に証明されていないと怖い人</li>
</ul>
```

#### 番号付きリスト（🔢）

```html
<ul class="wp-block-list is-style-num_circle">
<li>Naturecanが世界No.1と言われる3つの理由</li>
<li>「やりすぎ」と言われる6段階テストの詳細</li>
</ul>
```

#### 通常リスト（デフォルト）

```html
<ul class="wp-block-list">
<li>ブランドへの信頼を重視する方</li>
<li>成分表の透明性を重視する方</li>
</ul>
```

---

### テーブル

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
<td>商品名</td>
<td>Naturecan CBDオイル 10%</td>
</tr>
<tr>
<td>価格</td>
<td>8,000円（セール時は5,000円台）</td>
</tr>
</tbody>
</table>
</figure>
```

**ルール:**
- クラス: `is-style-regular` を使用
- 商品情報、比較情報に使用
- 商品紹介セクションで必須

---

### ボタン（アフィリエイトリンク）

```html
<div class="swell-block-button is-style-btn_normal">
<a href="https://px.a8.net/svt/ejp?a8mat=..." target="_blank" rel="noopener noreferrer" class="swell-block-button__link">
<span>公式で詳細・成分表を見る（Naturecan）</span>
</a>
</div>
```

**ルール:**
- クラス: `is-style-btn_normal` を使用
- `target="_blank"` と `rel="noopener noreferrer"` を必須で付与
- テキスト: 「公式で詳細・成分表を見る（ブランド名）」形式
- 商品紹介セクションの最後に配置

---

### 関連記事リンク

```html
<div class="swell-block-postLink" data-id="1097">
<a href="/naturecan-review/">詳細レビューとエビデンスを見る</a>
</div>
```

**ルール:**
- 内部リンクで関連記事を誘導
- `data-id` に記事IDを指定

---

## 見出しの使い方

### 階層構造

```
H2（タイトル）: is-style-default
  └─ H3（大セクション）
      └─ H4（小セクション）
          └─ H4（小セクション）
```

**例:**
```html
<h2 class="wp-block-heading is-style-default">【決定版】Naturecan(ネイチャーカン)の評判は？世界No.1と言われる3つの理由</h2>

<h3 class="wp-block-heading">ブランドの背景：プロテイン界の伝説が作った「本物」</h3>

<h4 class="wp-block-heading">① オレゴン州産の厳選ヘンプ</h4>
```

**ルール:**
- H2: タイトルのみ（`is-style-default`）
- H3: メインセクション（スタイルなし）
- H4: サブセクション（スタイルなし）
- 見出しレベルを飛ばさない（H2→H3→H4の順）

---

## 商品紹介セクションのテンプレート

### 基本構造

```html
<h4 class="wp-block-heading">🥇 CBDオイル 10%（8,000円）</h4>

<figure class="wp-block-image size-thumbnail">
<img decoding="async" src="https://..." alt="商品画像" />
</figure>

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
<td>商品名</td>
<td>Naturecan CBDオイル 10%</td>
</tr>
<tr>
<td>価格</td>
<td>8,000円（セール時は5,000円台）</td>
</tr>
<!-- 他の項目 -->
</tbody>
</table>
</figure>

<p><strong>メリット</strong>：</p>
<ul class="wp-block-list is-style-good_list">
<li><span class="swl-marker mark_green">世界基準の安全性と透明性</span></li>
<li>全ロットの成分表（COA）を公開</li>
</ul>

<p><strong>デメリット</strong>：</p>
<ul class="wp-block-list is-style-bad_list">
<li>価格がやや高め（通常価格8,000円）</li>
</ul>

<p><strong>こんな人におすすめ</strong>：</p>
<ul class="wp-block-list">
<li>ブランドへの信頼を重視する方</li>
</ul>

<div class="swell-block-button is-style-btn_normal">
<a href="..." target="_blank" rel="noopener noreferrer" class="swell-block-button__link">
<span>公式で詳細・成分表を見る（Naturecan）</span>
</a>
</div>

<hr class="wp-block-separator has-css-opacity is-style-wide"/>
```

---

## アフィリエイトリンク配置ルール

### 配置位置

1. **冒頭免責事項**（必須）
   - 記事の最上部に配置

2. **商品紹介セクション**（必須）
   - 各商品の情報の後にボタンとして配置
   - テーブル → メリット/デメリット → おすすめ → ボタンの順

3. **まとめセクション**（推奨）
   - 記事の結論後に再度CTAを配置

### リンクテキスト

- 「公式で詳細・成分表を見る（ブランド名）」
- 「公式サイトで在庫を見る（ブランド名）」
- 「公式で詳細・在庫を見る（ブランド名）」

---

## SEO・メタ情報

### タイトル

- **形式:** 【キャッチコピー】キーワード + 疑問文・数字
- **例:** 【決定版】Naturecan(ネイチャーカン)の評判は？世界No.1と言われる3つの理由

### スラッグ

- 英数字のみ（日本語不可）
- ハイフン区切り（例: `naturecan-review-complete`）
- 30文字以内

### メタディスクリプション

- **文字数:** 120文字程度
- **内容:** キーワード + 記事の要約 + 読者へのメリット

### タグ

- 5-10個程度
- キーワード、商品名、用途、ターゲットを含める
- 例: `CBD`, `初心者`, `おすすめ`, `Naturecan`, `睡眠`, `リラックス`

---

## コンテンツ品質基準

### 文字数

- **本文:** 3,000-5,000文字
- **段落:** 3-4行程度で区切る
- **1文:** 40文字以内

### 見出し構造

- H2: 1つ（タイトル）
- H3: 3-5セクション
- H4: 必要に応じて使用

### 画像

- **アイキャッチ:** 必須
- **商品画像:** 各商品に1枚（`size-thumbnail`）
- **ALTテキスト:** 必須

### リスト・テーブル

- 情報を整理する際に積極的に使用
- メリット/デメリットは必ずリスト化

---

## 自動生成時のチェックリスト

### HTML構造チェック

- [ ] アフィリエイト免責事項が冒頭にある
- [ ] H2見出しに `is-style-default` が付いている
- [ ] 「この記事で分かること」ボックスがある（`is-style-big_icon_good` + `is-style-num_circle`）
- [ ] 区切り線（`is-style-wide`）がセクション間に配置されている
- [ ] 見出しレベルが正しい（H2→H3→H4の順）

### SWELLブロックチェック

- [ ] リストスタイルが適切（`is-style-good_list`, `is-style-bad_list`, `is-style-num_circle`など）
- [ ] マーカーが適切に使用されている（`mark_green`, `mark_orange`など）
- [ ] テーブルに `is-style-regular` が付いている
- [ ] ボタンに `is-style-btn_normal` が付いている
- [ ] ボタンのリンクに `target="_blank"` と `rel="noopener noreferrer"` がある

### アフィリエイトリンクチェック

- [ ] 冒頭免責事項がある
- [ ] 各商品紹介にボタンがある
- [ ] リンクテキストが分かりやすい

### SEOチェック

- [ ] タイトルにキーワードが含まれている
- [ ] スラッグが英数字のみで適切な長さ
- [ ] メタディスクリプションが120文字程度
- [ ] タグが5-10個設定されている

### コンテンツ品質チェック

- [ ] 本文が3,000文字以上
- [ ] H3見出しが3-5セクションある
- [ ] 商品紹介にテーブル、メリット/デメリット、ボタンがある
- [ ] まとめセクションがある

---

## 参考記事

- `wordpress/posts/naturecan-review-complete.html` - 商品紹介記事のテンプレート
- `wordpress/posts/cbd-beginners-guide-complete.html` - ガイド記事のテンプレート
- `wordpress/posts/cbd-market-trends-2025-complete.html` - ニュース・トレンド記事のテンプレート

---

**作成日:** 2026-01-11  
**最終更新:** 2026-01-11
