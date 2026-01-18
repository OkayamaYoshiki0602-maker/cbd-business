# 記事生成プロンプト修正 v5 - 最終設計確定

## 📋 ユーザー指示の確定内容

### 1️⃣ Q&Aのデザイン（添付イメージを参照）

**✅ 採用デザイン:**
```html
<div style="background-color: transparent; border-left: none; padding: 16px 0; margin: 16px 0;">
  <p style="font-weight: bold; margin: 0 0 8px 0; font-size: 16px;">Q. 質問文</p>
  <p style="margin: 0; color: #e74c3c; font-weight: bold;">A.</p>
  <p style="margin: 4px 0 0 0; color: #333; line-height: 1.6;">回答内容を簡潔に記載します。重要な部分は太字で強調します。</p>
</div>
```

**特徴:**
- ❌ アイコン（❓✓）不要 - 「Q」「A」のテキストのみ
- ✅ Q：太字で黒
- ✅ A：太字で赤（#e74c3c）
- ✅ 背景色なし（シンプル）
- ✅ 左ボーダーなし
- ✅ 参考サイト並みのシンプルさ

**複数Q&Aの場合:**
```html
<!-- Q1 -->
<div style="margin-bottom: 24px;">
  <p style="font-weight: bold; margin: 0 0 8px 0; font-size: 16px;">Q. 質問1</p>
  <p style="margin: 0; color: #e74c3c; font-weight: bold;">A.</p>
  <p style="margin: 4px 0 0 0; color: #333; line-height: 1.6;">回答1</p>
</div>

<!-- Q2 -->
<div style="margin-bottom: 24px;">
  <p style="font-weight: bold; margin: 0 0 8px 0; font-size: 16px;">Q. 質問2</p>
  <p style="margin: 0; color: #e74c3c; font-weight: bold;">A.</p>
  <p style="margin: 4px 0 0 0; color: #333; line-height: 1.6;">回答2</p>
</div>
```

---

### 2️⃣ 見出し内文字数超過の対応

**✅ 対応方法: H4で細分化**

**❌ 例（150字超過）:**
```html
<h3>CBD製品選びの3ステップと安全な選び方</h3>
<p>ステップ1は目的を明確にすること。自分がなぜCBDを使いたいのか、睡眠なのか、リラックスなのか、集中力なのかを明確にすることが重要です。ステップ2は情報収集で、信頼できる情報源から正確な情報を集めることが大切です。ステップ3は実際に購入する際に成分表を確認することです。</p>
```

**✅ 改修後（H4で細分化）:**
```html
<h3>CBD製品選びの3ステップ</h3>

<h4>ステップ1：目的を明確にする</h4>
<p>自分がなぜCBDを使いたいのかを明確にしましょう。睡眠、リラックス、集中力のサポートなど、目的によって選ぶべき製品が異なります。</p>

<h4>ステップ2：信頼できる情報を収集</h4>
<p>正確な情報源から、成分やブランドについて調べることが重要です。信頼できるサイトやコミュニティの情報を参考にしましょう。</p>

<h4>ステップ3：成分表で安全性を確認</h4>
<p>購入前に必ずCOA（成分分析表）を確認し、THCが検出されていないことを確認しましょう。安全性が最優先です。</p>
```

**特徴:**
- ✅ H3で大見出し
- ✅ H4でそれぞれのステップを細分化
- ✅ 各H4セクション：150字以内
- ✅ 「1見出し = 1メッセージ」を厳密に守る

---

### 3️⃣ 表のカラー設計

**✅ 採用デザイン:**
```html
<table style="width: 100%; border-collapse: collapse; margin: 16px 0;">
  <thead>
    <tr style="background-color: #2d7a4c; color: white;">
      <th style="padding: 12px 16px; text-align: left; border: 1px solid #ddd; font-weight: bold;">よくある誤解</th>
      <th style="padding: 12px 16px; text-align: left; border: 1px solid #ddd; font-weight: bold;">正しい知識</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td style="padding: 12px 16px; border: 1px solid #ddd; background-color: #f5f5f5;">誤解の内容</td>
      <td style="padding: 12px 16px; border: 1px solid #ddd; background-color: #f0f7f0;">正しい説明</td>
    </tr>
    <tr>
      <td style="padding: 12px 16px; border: 1px solid #ddd; background-color: #f5f5f5;">誤解の内容</td>
      <td style="padding: 12px 16px; border: 1px solid #ddd; background-color: #f0f7f0;">正しい説明</td>
    </tr>
  </tbody>
</table>
```

**色設定:**
- ✅ ヘッダー背景：#2d7a4c（緑）
- ✅ ヘッダーテキスト：白
- ✅ 誤解列背景：#f5f5f5（ライトグレー）
- ✅ 正しい列背景：#f0f7f0（薄緑）
- ✅ 枠線：#ddd（薄いグレー）
- ✅ 赤塗り廃止

---

### 4️⃣ 見出し数の最適化

**✅ 確定内容：3-5個（最大6個）**

```
【導入段落】
  ↓
【見出し1（H3）】 ~ 150-200字
  ↓
【見出し2（H3）】 ~ 150-200字
  [※ 必要に応じてH4で細分化]
  ↓
【見出し3（H3）】 ~ 150-200字
  ↓
【見出し4（H3）】 ~ 150-200字（Q&Aなど）
  ↓
【見出し5（H3）】 ~ 150-200字（注意事項など）
  ↓
【まとめ】
```

**パターン例:**
- シンプル記事：見出し3個 + まとめ
- 標準記事：見出し4個 + まとめ
- 詳細記事：見出し5個 + まとめ
- 最大6個を超えない

---

## 🎯 プロンプトの改修ポイント

修正後の `article_generator_html_v2.py` プロンプトに以下を含める：

### 1. Q&Aテンプレート（新版）
```
【Q&Aセクションの実装】
各Q&Aは以下の形式で実装してください：

<div style="margin-bottom: 24px;">
  <p style="font-weight: bold; margin: 0 0 8px 0; font-size: 16px;">Q. 質問文</p>
  <p style="margin: 0; color: #e74c3c; font-weight: bold;">A.</p>
  <p style="margin: 4px 0 0 0; color: #333; line-height: 1.6;">回答内容。重要な部分は<strong>太字</strong>で強調。</p>
</div>

★ ポイント：
- Q/Aは背景色なし（シンプル）
- アイコンは不要（QとAのテキストのみ）
- Aは赤太字（#e74c3c）で視覚的に区別
- 複数Q&Aの場合は margin-bottom: 24px で余白確保
```

### 2. 表のカラー指定（新版）
```
【表のカラー設計】
比較表・一覧表は以下の色設定で統一：

- ヘッダー背景：#2d7a4c（緑）+ 白テキスト
- 列1背景：#f5f5f5（ライトグレー）
- 列2以降背景：#f0f7f0（薄緑）
- 枠線：#ddd（薄いグレー）

❌ 赤塗りは絶対に使用しない
✅ 落ち着いた緑系・グレー系で統一
```

### 3. 見出し細分化ルール（新版）
```
【見出し内の文字数ルール】

★ 絶対ルール：
- H3（大見出し）の直後のテキスト：150-200字以内
- 150字を超える場合：H4で細分化

★ 例：
❌ H3 見出し（内容が250字以上）

✅ H3 見出し
   ├ H4 サブ見出し1（150字以内）
   ├ H4 サブ見出し2（150字以内）
   └ H4 サブ見出し3（150字以内）

★ H4の使い分け：
- 複数のステップ・ポイント → H4で番号付け
- 複数の商品紹介 → H4でブランド名
- 複数のQ&A → H4で質問文（ただしQ&Aセクションは独自形式）
```

### 4. 免責事項（既定版）
```
【免責事項ボックス】

<p style="font-size: 12px; color: #666; background-color: #f5f5f5; padding: 8px 12px; border-radius: 4px; margin-bottom: 16px;">
  ※アフィリエイト広告を含みます。最新情報はリンク先をご確認ください。
</p>

★ ポイント：
- 1行に短縮
- グレー背景（#f5f5f5）
- 赤塗り不要
```

---

## ✅ 実装チェックリスト

修正実装時に確認する項目：

- [ ] Q&Aのアイコン削除（「Q」「A」のみ）
- [ ] Q&Aの背景色・左ボーダー廃止
- [ ] Aの色を赤（#e74c3c）に統一
- [ ] 表のヘッダー色を#2d7a4cに変更
- [ ] 表の赤塗り廃止
- [ ] H3の直後が150字超過している場合はH4で細分化
- [ ] 見出し数：3-5個（最大6個）
- [ ] 免責事項：グレー背景、1行に短縮
- [ ] 全体文字数：3,500字以内

---

## 🚀 次のステップ

確認事項：
1. ✅ Q&Aデザイン：確定（添付イメージ参照）
2. ✅ H4細分化：確定
3. ✅ 表の色設計：確定（#2d7a4c + グレー/薄緑）
4. ✅ 見出し数：確定（3-5個）

**実装予定：** `article_generator_html_v2.py` のプロンプト全体を修正

