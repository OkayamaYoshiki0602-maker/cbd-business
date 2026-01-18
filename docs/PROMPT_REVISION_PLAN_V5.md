# 記事生成プロンプト修正プラン v5 - 設計段階での改善

## 🔍 ユーザーの指摘内容

### 指摘1: 見出し内の文字数超過
- ❌ 1見出し内が150字を超えている箇所が複数
- ✅ 改善案：150字以内に収めるか、見出しを下げてさらに細分化

### 指摘2: 表のデザイン
- ❌ 赤塗りの表は「醜い」「怖い」印象
- ✅ 改善案：赤塗りを廃止、グレー/緑系の落ち着いた色に変更

### 指摘3: Q&Aの見た目
- ❌ デザイン修正後も「結局ださい」
- ✅ 改善案：参考サイト並みのシンプル・洗練されたデザインに

### 指摘4: 免責事項ボックス
- ❌ 長くて、赤塗りが「怖い」
- ✅ 改善案：短縮 + 色を薄いグレーや青系に変更

---

## 📝 修正アプローチ：「設計優先」

ユーザーの指摘通り、**AIがいきなり記事を描き始めるのではなく**、以下の順序で進めるべきです：

```
1️⃣ テーマ・キーワード分析
   ↓
2️⃣ 「伝えるべきメッセージ」の明確化
   ↓
3️⃣ 必要な見出し数・セクション構成の設計
   ↓
4️⃣ 3,500字以内に収めるための調整
   ↓
5️⃣ 画像挿入ポイントの提案
   ↓
6️⃣ HTML生成
```

---

## 🎨 デザイン修正案

### 修正1: 表のカラー設計

**❌ 現在の赤塗り表:**
```html
<table>
  <tr style="background-color: red; color: white;">
    <th>誤解</th>
    <th>真実</th>
  </tr>
</table>
```
→ 「怖い」「メディカル」な印象で不適切

**✅ 改修案：グレー/グリーン配色**
```html
<table style="border-collapse: collapse; width: 100%;">
  <tr style="background-color: #2d7a4c; color: white;">
    <th style="padding: 12px; border: 1px solid #ddd; text-align: left;">❌ よくある誤解</th>
    <th style="padding: 12px; border: 1px solid #ddd; text-align: left;">✅ 正しい知識</th>
  </tr>
  <tr>
    <td style="padding: 12px; border: 1px solid #ddd; background-color: #f9f9f9;">誤解内容</td>
    <td style="padding: 12px; border: 1px solid #ddd; background-color: #f0f7f0;">正しい説明</td>
  </tr>
</table>
```

**特徴:**
- ヘッダー：落ち着いた緑（#2d7a4c）
- 誤解列：ライトグレー（#f9f9f9）
- 正しい列：薄緑（#f0f7f0）
- アイコン使用（❌✅）で視覚的強調

---

### 修正2: Q&Aのデザイン再検討

**❌ 現在の実装：複雑で装飾が多い**
```html
<div style="background-color: #f9f9f9; border-radius: 8px; padding: 16px; margin: 16px 0; border-left: 4px solid #4a90e2;">
  <p style="margin: 0 0 8px 0; font-weight: bold; color: #4a90e2;">❓ Q: 質問文</p>
  <p style="margin: 0; font-size: 14px; color: #333;">✓ <span style="color: #e74c3c; font-weight: bold;">重要な回答部分</span>をここで強調します。</p>
</div>
```
→ 要素が多すぎて「ダサい」という指摘

**✅ 改修案：シンプルで洗練されたデザイン**

参考サイト（on-clinic、shiawase-wine等）の分析：
- Q/Aが背景色で区別
- 装飾は最小限
- 左ボーダーのみ
- 背景色は薄い

```html
<!-- シンプル版 -->
<div style="background-color: #f9f9f9; border-left: 4px solid #2d7a4c; padding: 16px; margin: 16px 0;">
  <p style="font-weight: bold; margin: 0 0 8px 0;">Q: 質問文</p>
  <p style="margin: 0;">回答を簡潔に。<br />重要な部分は <strong>太字</strong> で強調。</p>
</div>
```

**特徴:**
- 背景色 + 左ボーダーのみ（装飾最小化）
- アイコン不要（記号「Q:」「A:」のみ）
- 色は落ち着いた緑系
- 回答は太字のみで強調

---

### 修正3: 免責事項ボックス

**❌ 現在の実装：長くて赤塗り**
```html
<div class="wp-block-group cbd-aff-disclaimer">
  <div class="wp-block-group__inner-container">
    <p style="font-size:13px;opacity:.8;background-color: red; color: white; padding: 12px;">
      ※当サイトはアフィリエイト広告を利用しています。価格・在庫・成分はリンク先の最新情報が正となります。
    </p>
  </div>
</div>
```
→ 「赤塗りは怖い」という指摘

**✅ 改修案：短縮 + 薄いグレーに**
```html
<p style="font-size: 12px; color: #666; background-color: #f5f5f5; padding: 8px 12px; border-radius: 4px; margin-bottom: 16px;">
  ※アフィリエイト広告を含みます。最新情報はリンク先をご確認ください。
</p>
```

**特徴:**
- 文字数：大幅短縮（1行）
- 色：薄いグレー（#f5f5f5）
- 枠線不要
- 重要度：低（デザイン上目立たない）

---

## 📊 見出し構成の設計例

### THC記事の場合：

**伝えるべきメッセージ（優先度順）:**
1. THCが違法？合法？（最重要）
2. CBDとの違い（重要）
3. 具体的な規制内容（高）
4. Q&A（補足）
5. 注意事項（参考）

**見出し数の調整:**
```
【導入】
  ↓
【見出し1】THCの法的ステータス（150-200字）
  ↓
【見出し2】CBDとTHCの違い（150-200字）
  ↓
【見出し3】日本の現行規制（150-200字）
  ↓
【見出し4】Q&A（各質問150字以内）
  ↓
【見出し5】注意事項（150-200字）
  ↓
【まとめ】
```

**特徴:**
- 見出し5個で「多いほど読みやすい」を実現
- 各セクション150-200字で「1見出し = 1メッセージ」を厳密化
- 全体で3,500字以内に収まる

---

## 🔧 プロンプト内での「設計フェーズ」の追加

修正後のプロンプトでは、以下の順序を明示します：

```markdown
【生成手順】

Step1: テーマ分析
- キーワード抽出
- ターゲット層確認
- テンプレート特性の理解

Step2: メッセージ設計
- 伝えるべきこと（3-5個のポイント）を優先度順に列挙
- 不要な情報は削除（3,500字制限のため）

Step3: 見出し構成設計
- 必要な見出し数を決定（通常3-5個、最大6個）
- 各セクションの内容をブレインストーミング

Step4: 文字数配分
- 全体3,500字を見出し数で逆算
- 各セクション150-200字の目安を設定

Step5: ビジュアル配置
- 表・リスト・ボックスの配置位置を決定
- 画像挿入ポイント提案

Step6: HTML生成
- 上記設計に基づいてHTMLを生成
```

---

## 📋 最終的なデザイン指定

### Q&Aセクション（最終版）
```html
<!-- シンプル・洗練版 -->
<div style="background-color: #f9f9f9; border-left: 4px solid #2d7a4c; padding: 16px; margin: 16px 0;">
  <p style="font-weight: bold; margin: 0 0 8px 0;">Q: 質問文</p>
  <p style="margin: 0;">回答内容。<br /><strong>重要な部分</strong>は太字で。</p>
</div>
```

### 表のデザイン（最終版）
```html
<table style="width: 100%; border-collapse: collapse; margin: 16px 0;">
  <tr style="background-color: #2d7a4c; color: white;">
    <th style="padding: 12px; text-align: left; border: 1px solid #ddd;">❌ よくある誤解</th>
    <th style="padding: 12px; text-align: left; border: 1px solid #ddd;">✅ 正しい知識</th>
  </tr>
  <tr>
    <td style="padding: 12px; border: 1px solid #ddd; background-color: #f9f9f9;">誤解</td>
    <td style="padding: 12px; border: 1px solid #ddd; background-color: #f0f7f0;">正しい知識</td>
  </tr>
</table>
```

### 免責事項（最終版）
```html
<p style="font-size: 12px; color: #666; background-color: #f5f5f5; padding: 8px 12px; border-radius: 4px; margin-bottom: 16px;">
  ※アフィリエイト広告を含みます。最新情報はリンク先をご確認ください。
</p>
```

---

## ✅ チェックリスト（修正前の確認）

実装時に以下を確認してください：

- [ ] 免責事項：短縮（1行）+ グレー背景
- [ ] 表：赤塗り廃止、グリーン系に変更
- [ ] Q&A：シンプル設計、装飾最小化
- [ ] 見出し内：150字以上を全て分割
- [ ] 全体文字数：3,500字以内確認
- [ ] 見出し数：3-5個（最大6個）

