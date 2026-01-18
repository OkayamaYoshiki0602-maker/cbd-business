# 記事デザイン改善ルール v4

## 📊 修正ポイント

### 1. ビジュアルの改善 - Q&Aとボックス

#### ❌ ダサいQ&A例：
```
Q1: CBDは違法ではないですか?
A1: いいえ、日本ではCBDは合法です。ただし、THCを含まないことが条件です。
```

#### ✅ おしゃれなQ&A例：
```html
<div class="wp-block-group is-style-FAQ_style">
  <div class="wp-block-group__inner-container">
    <div class="swell-block-faq">
      <div class="swell-faq-item">
        <div class="swell-faq-question">
          <p><span class="swl-marker mark_blue">Q</span> CBDは違法ではないですか？</p>
        </div>
        <div class="swell-faq-answer">
          <p>いいえ、日本ではCBDは合法です。<br />
          <span style="color: #E85D75; font-weight: bold;">ただし、THCを含まないことが必須条件</span>となります。</p>
        </div>
      </div>
    </div>
  </div>
</div>
```

### 2. ボックスデザインの改善

#### ❌ 古い背景色ボックス：
```html
<div class="wp-block-group is-style-big_icon_good">
  <p><strong>ポイント</strong></p>
  <ul>...</ul>
</div>
```

#### ✅ モダンな背景色ボックス：
```html
<!-- グリーン背景（重要情報） -->
<div class="wp-block-group" style="background-color: #f0f7f0; border-left: 4px solid #2d7a4c; padding: 16px; margin: 16px 0;">
  <p style="margin: 0; color: #2d7a4c; font-weight: bold;">📌 重要なポイント</p>
  <ul style="margin-top: 12px; padding-left: 20px;">
    <li><span style="color: #2d7a4c; font-weight: bold;">チェック項目1</span>：詳細説明</li>
    <li>チェック項目2：詳細説明</li>
  </ul>
</div>

<!-- オレンジ背景（注意・警告） -->
<div class="wp-block-group" style="background-color: #fff5f0; border-left: 4px solid #ff6d4b; padding: 16px; margin: 16px 0;">
  <p style="margin: 0; color: #ff6d4b; font-weight: bold;">⚠️ 注意事項</p>
  <p style="margin-top: 8px; font-size: 14px;">THCを含む製品は違法です。必ずCOA（成分分析結果）を確認してください。</p>
</div>

<!-- 青背景（情報） -->
<div class="wp-block-group" style="background-color: #f0f5ff; border-left: 4px solid #4a90e2; padding: 16px; margin: 16px 0;">
  <p style="margin: 0; color: #4a90e2; font-weight: bold;">ℹ️ 情報</p>
  <p style="margin-top: 8px;">参考情報や補足説明</p>
</div>
```

### 3. 文字数・構造ルール

#### 文字数制限：
- **全体：3,500文字以内（絶対）**
- **1セクション（見出し下）：150-200文字以内**
- セクション数：最大6個（見出しが多い = 読みやすい）

#### 各セクションの構成：
```
【見出し】
├ 導入：50-80文字（何を説明するか）
├ ビジュアル（表・リスト・ボックス）
└ まとめ：50-100文字（要点、アクション）
```

#### 記事が途中で終わらないルール：
- セクション削除は最終手段
- むしろ **「1見出し = 1メッセージ」をより厳密に**
- 表の行数を減らす、リストを絞る、説明を簡潔にしてスペースを確保

### 4. 視覚的メリハリの強調ルール

#### 強調スタイル：

**① 太字**
```html
<strong>重要な用語</strong>
```

**② 赤太字**
```html
<span style="color: #e74c3c; font-weight: bold;">強調したい内容</span>
```

**③ オレンジ下線**
```html
<span style="border-bottom: 3px solid #ff9800;">強調ポイント</span>
```

**④ 背景ハイライト**
```html
<span class="swl-marker mark_orange">オレンジマーカー</span>
<span class="swl-marker mark_green">グリーンマーカー</span>
<span class="swl-marker mark_blue">ブルーマーカー</span>
```

#### 使い分け：
- **赤太字**：危険性・注意が必要
- **オレンジ下線**：特に重要な情報
- **マーカー**：キーワード・定義
- **太字**：一般的な強調

---

## 🎨 テンプレート別デザイン例

### 商品紹介テンプレート
```html
<h3>おすすめ商品</h3>

<!-- 商品情報ボックス -->
<div style="background-color: #f9f9f9; border-radius: 8px; padding: 16px; margin: 16px 0;">
  <p style="margin: 0 0 8px 0; font-weight: bold;">【商品名】</p>
  <p style="margin: 0; font-size: 14px;">🔸 <span style="color: #2d7a4c; font-weight: bold;">メリット</span>：簡潔に</p>
  <p style="margin: 8px 0; font-size: 14px;">🔹 <span style="color: #ff6d4b; font-weight: bold;">注意点</span>：簡潔に</p>
</div>

<!-- ボタン -->
<div style="text-align: center; margin: 16px 0;">
  <a href="URL" style="display: inline-block; background-color: #2d7a4c; color: white; padding: 12px 24px; border-radius: 6px; text-decoration: none; font-weight: bold;">詳細を見る</a>
</div>
```

### Q&Aテンプレート
```html
<h3>よくある質問</h3>

<div style="background-color: #f9f9f9; border-radius: 8px; padding: 16px; margin: 12px 0; border-left: 4px solid #4a90e2;">
  <p style="margin: 0 0 8px 0; font-weight: bold; color: #4a90e2;">❓ Q1: 質問文</p>
  <p style="margin: 0; font-size: 14px; color: #333;">✓ <span style="font-weight: bold;">重要な回答部分</span>をここで強調します。</p>
</div>
```

---

## 📋 実装チェックリスト

- [ ] ボックスのデザイン：グリーン/オレンジ/ブルーで色分け
- [ ] Q&Aの見た目：背景色 + 左ボーダー + アイコン
- [ ] 文字数：全体3,500以内、1セクション150-200以内
- [ ] 記事の最後：必ずまとめか関連記事で終わる
- [ ] 強調スタイル：赤太字 × 3-5個、オレンジ下線 × 2-3個を使用
- [ ] 表の行数：最大5行
- [ ] 見出し数：3-6個

