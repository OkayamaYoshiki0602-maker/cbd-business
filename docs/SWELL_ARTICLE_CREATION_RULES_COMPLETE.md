# SWELL記事作成ルール（完全版）

## 概要
過去記事（1085、1097）の実際のHTMLコードを分析し、同じレベルの記事を誰でも作成できるルールを作成。

## 基本構造

### 1. 記事全体の構造
```html
<div class="wp-block-group cbd-aff-disclaimer">
  <div class="wp-block-group__inner-container">
    <p style="font-size:13px;opacity:.8">※当サイトはアフィリエイト広告を利用しています。価格・在庫・成分はリンク先の最新情報が正となります。</p>
  </div>
</div>

<h2 class="wp-block-heading is-style-default">【決定版】記事タイトル</h2>

<!-- 導入部分 -->
<p>CBD選びで、絶対に失敗したくない。<br />自分の体に入れるものだから、1ミリの不安も残したくない。<br />そう思うなら、結論は<span class="swl-marker mark_green">○○一択</span>です。</p>

<p>「なぜこれほど高いのか？」「なぜ世界中で売れているのか？」<br />その理由は、○○による「品質革命」と、異常なまでの「安全への執着」にありました。</p>

<!-- この記事で分かることボックス -->
<div class="wp-block-group is-style-big_icon_good">
  <div class="wp-block-group__inner-container">
    <p><strong>この記事で分かること</strong></p>
    <ul class="wp-block-list is-style-num_circle">
      <li>項目1</li>
      <li>項目2</li>
      <li>項目3</li>
      <li>項目4</li>
    </ul>
  </div>
</div>

<hr class="wp-block-separator has-css-opacity is-style-wide"/>

<!-- メインコンテンツ -->
<h3 class="wp-block-heading">セクション1</h3>
<!-- 内容 -->

<hr class="wp-block-separator has-css-opacity is-style-wide"/>

<h3 class="wp-block-heading">セクション2</h3>
<!-- 内容 -->
```

### 2. 導入部分のルール
- **必ず<br>タグで改行**
- **2-3段落、各段落は1-2文**
- **共感→問題提示→解決策の流れ**
- **断定的な表現**（「結論は○○一択です」）

```html
<p>CBD選びで、絶対に失敗したくない。<br />自分の体に入れるものだから、1ミリの不安も残したくない。<br />そう思うなら、結論は<span class="swl-marker mark_green">Naturecan（ネイチャーカン）一択</span>です。</p>

<p>「なぜこれほど高いのか？」「なぜ世界中で売れているのか？」<br />その理由は、フィットネス界の伝説による「品質革命」と、異常なまでの「安全への執着」にありました。</p>
```

### 3. 「この記事で分かること」ボックス
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

### 4. セクション区切り
**必ず各H3セクションの前に区切り線を入れる**
```html
<hr class="wp-block-separator has-css-opacity is-style-wide"/>
```

### 5. 段落の書き方
- **短い段落（1-2文）**
- **<br>タグで改行**
- **強調は<strong>タグ**
- **マーカーは<span class="swl-marker mark_green">**

```html
<p>Naturecanの創設者は、あの世界No.1プロテインブランド<strong>「Myprotein（マイプロテイン）」の元CEO</strong>、アンディ・ダックワース氏です。</p>

<p>彼はMyprotein時代、「高品質なサプリメントを、サプライチェーンの効率化によって適正価格で届ける」という革命を起こしました。<br />その彼が次に目をつけたのがCBDです。</p>
```

### 6. 情報ボックス（メリット・デメリット・おすすめ）

#### メリット（good_list）
```html
<div class="wp-block-group is-style-big_icon_good">
  <div class="wp-block-group__inner-container">
    <p><strong>CBDの特徴</strong></p>
    <ul class="wp-block-list is-style-good_list">
      <li><span class="swl-marker mark_green">ハイにならない</span>（精神作用なし）</li>
      <li><span class="swl-marker mark_green">依存性がない</span>（WHO報告）</li>
      <li><span class="swl-marker mark_green">日本で合法</span>（THCが含まれていない場合）</li>
    </ul>
  </div>
</div>
```

#### デメリット（bad_list）
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

#### 通常のリスト（メリット・デメリット）
```html
<p><strong>メリット</strong>：</p>
<ul class="wp-block-list is-style-good_list">
  <li><span class="swl-marker mark_green">世界基準の安全性と透明性</span></li>
  <li>全ロットの成分表（COA）を公開</li>
  <li>日本公式サイトでサポート充実</li>
</ul>

<p><strong>デメリット</strong>：</p>
<ul class="wp-block-list is-style-bad_list">
  <li>価格がやや高め（通常価格8,000円）</li>
  <li>初心者には少し濃度が高い場合がある</li>
</ul>

<p><strong>こんな人におすすめ</strong>：</p>
<ul class="wp-block-list">
  <li>ブランドへの信頼を重視する方</li>
  <li>成分表の透明性を重視する方</li>
  <li>日中〜夜まで幅広く使いたい方</li>
</ul>
```

### 7. テーブル（商品情報）
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
      <tr>
        <td>容量</td>
        <td>10mL</td>
      </tr>
    </tbody>
  </table>
</figure>
```

### 8. 画像
```html
<figure class="wp-block-image size-large">
  <img decoding="async" src="画像URL" alt="画像の説明" />
  <figcaption style="font-size:13px;opacity:.8">キャプション</figcaption>
</figure>

<!-- 商品画像（小さめ） -->
<figure class="wp-block-image size-thumbnail">
  <img decoding="async" src="商品画像URL" alt="商品名 商品画像" />
</figure>
```

### 9. アフィリエイトボタン
```html
<div class="swell-block-button is-style-btn_normal">
  <a href="アフィリエイトURL" target="_blank" rel="noopener noreferrer" class="swell-block-button__link">
    <span>公式で詳細・成分表を見る（Naturecan）</span>
  </a>
</div>
```

### 10. FAQ（よくある質問）
```html
<dl class="swell-block-faq" data-a="col-text" data-q="col-text">
  <div class="swell-block-faq__item">
    <dt class="faq_q"><strong>CBDは安全ですか？</strong></dt>
    <dd class="faq_a">
      <p>WHO（世界保健機関）は「CBDは依存や乱用のリスクが低く、安全性が高い」と評価しています。</p>
    </dd>
  </div>
</dl>
```

### 11. まとめセクション
```html
<div class="wp-block-group is-style-big_icon_good">
  <div class="wp-block-group__inner-container">
    <p><strong>Naturecanがおすすめな人</strong></p>
    <ul class="wp-block-list is-style-check_list">
      <li>多少高くても、<strong>世界最高レベルの安全性</strong>が欲しい人</li>
      <li><strong>THCフリー</strong>が科学的に証明されていないと怖い人</li>
      <li>「安物買いの銭失い」をしたくない、本物志向の人</li>
    </ul>
  </div>
</div>

<p>👉 <strong>Naturecanは「安全をお金で買う」という意味で、これ以上の選択肢はありません。</strong></p>
```

## Markdownからの変換ルール

### 1. 見出し変換
```markdown
# タイトル → <h2 class="wp-block-heading is-style-default">タイトル</h2>
### セクション → <h3 class="wp-block-heading">セクション</h3>
#### サブセクション → <h4 class="wp-block-heading">サブセクション</h4>
```

### 2. 段落変換
```markdown
段落1<br>
段落2

→

<p>段落1<br />段落2</p>
```

### 3. リスト変換
```markdown
メリット:
- 項目1
- 項目2

→

<p><strong>メリット</strong>：</p>
<ul class="wp-block-list is-style-good_list">
  <li><span class="swl-marker mark_green">項目1</span></li>
  <li>項目2</li>
</ul>
```

### 4. テーブル変換
```markdown
| 項目 | 内容 |
|------|------|
| 商品名 | Naturecan |
| 価格 | 8,000円 |

→

<figure class="wp-block-table is-style-regular">
  <table>
    <thead><tr><th>項目</th><th>内容</th></tr></thead>
    <tbody>
      <tr><td>商品名</td><td>Naturecan</td></tr>
      <tr><td>価格</td><td>8,000円</td></tr>
    </tbody>
  </table>
</figure>
```

### 5. 画像変換
```markdown
![商品名](画像URL)

→

<figure class="wp-block-image size-thumbnail">
  <img decoding="async" src="画像URL" alt="商品名" />
</figure>
```

### 6. アフィリエイトリンク変換
```markdown
[公式で詳細を見る（ブランド名）](URL)

→

<div class="swell-block-button is-style-btn_normal">
  <a href="URL" target="_blank" rel="noopener noreferrer" class="swell-block-button__link">
    <span>公式で詳細を見る（ブランド名）</span>
  </a>
</div>
```

## 文字数・構成ルール

### 1. 全体構成
- **導入**: 100-150文字（2-3段落、各段落1-2文）
- **この記事で分かること**: 3-4項目
- **メインセクション**: 3-4セクション（各150-300文字）
- **まとめ**: 100-150文字
- **全体**: 2,500-3,500文字

### 2. 段落ルール
- **1段落 = 1-2文**
- **<br>タグで改行**
- **段落間に空行**
- **長い説明は複数段落に分割**

### 3. 見出し階層
```
H1: 記事タイトル（WordPressで自動生成）
H2: メインタイトル（記事冒頭）
H3: メインセクション（3-4個）
H4: サブセクション（必要に応じて）
```

### 4. 必須要素
1. **アフィリエイト免責事項**（記事冒頭）
2. **導入**（共感→問題→解決策）
3. **この記事で分かること**ボックス
4. **区切り線**（各セクション前）
5. **商品情報テーブル**
6. **メリット・デメリット**リスト
7. **アフィリエイトボタン**
8. **まとめ**セクション

## 実装時の注意点

### 1. SWELL固有クラス
- `is-style-big_icon_good`: 緑アイコンボックス
- `is-style-big_icon_bad`: 赤アイコンボックス
- `is-style-good_list`: 緑チェックリスト
- `is-style-bad_list`: 赤バツリスト
- `is-style-check_list`: チェックリスト
- `is-style-num_circle`: 番号付きリスト
- `swl-marker mark_green`: 緑マーカー
- `swl-marker mark_orange`: オレンジマーカー

### 2. レスポンシブ対応
- テーブルは自動でレスポンシブ
- 画像は`size-large`または`size-thumbnail`
- ボタンは自動で幅調整

### 3. SEO対策
- H2タイトルにキーワード含める
- 画像のalt属性を適切に設定
- 内部リンクを適切に配置
- メタディスクリプション120文字以内

この完全版ルールに従えば、過去記事（1085、1097）と同レベルの記事を誰でも作成できます。