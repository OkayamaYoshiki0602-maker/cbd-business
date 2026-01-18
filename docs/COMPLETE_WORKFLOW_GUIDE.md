# CBD記事生成システム - 実行フロー完全ガイド

**更新日**: 2026年1月17日  
**ステータス**: ✅ 最新版

---

## 📋 全体フロー図

```
【Google Sheets 準備】
    ↓
Article_Theme に記事テーマ入力
 ├─ A列: タイムスタンプ（自動）
 ├─ B列: ステータス「新規」
 ├─ C列: 記事タイトル（テーマ）
 ├─ D列: 記事の分類（15個のテンプレート）
 ├─ E列: ターゲット
 ├─ F列: タグ（カンマ区切り）
 └─ その他: 自動入力項目
    ↓
【Step 1】タイトル候補を生成
    python3 automation/content/generate_title_options.py --generate
    ├─ K～O列: 5つのタイトル候補が自動入力
    ├─ B列: ステータス「タイトル選択待ち」に変更
    └─ ユーザー: P列に選択したタイトルを入力
    ↓
【Step 2】ステータスを更新
    ├─ B列: 「生成待ち」に変更
    └─ P列: 選択したタイトルが入力されている
    ↓
【Step 3】記事を生成
    python3 automation/content/article_generator_html_v2.py
    ├─ P列から選択されたタイトルを読み込み
    ├─ テンプレートから最適な構造を選択
    ├─ HTML 記事を生成
    ├─ メタデータを自動生成
    ├─ 関連記事を自動推奨
    ├─ WordPress に下書き投稿
    ├─ Article_List を更新
    └─ LINE で通知
    ↓
【Step 4】WordPress で確認・編集・公開
    ├─ 下書きタブから記事を確認
    ├─ 必要に応じて編集
    └─ 公開をクリック
```

---

## 🐍 Pythonファイル分類

### 【メイン実行ファイル】- 常時使用

```
automation/content/
├── article_generator_html_v2.py ⭐【メイン】
│   ├── 記事生成のメインスクリプト
│   ├── 実行: python3 automation/content/article_generator_html_v2.py
│   ├── 機能:
│   │   ├─ Google Sheets から「生成待ち」のテーマを読み込み
│   │   ├─ P列から選択されたタイトルを優先的に使用
│   │   ├─ 15個のテンプレートから最適なものを選択
│   │   ├─ HTML 記事を生成（2,500-3,500文字）
│   │   ├─ メタデータを自動生成
│   │   ├─ SEO スラッグを自動生成
│   │   ├─ 関連記事を自動推奨（3件）
│   │   ├─ WordPress に下書き投稿
│   │   └─ LINE で通知
│   │
│   └── 実装版: ✅ v2（最新版）
│
├── generate_title_options.py ⭐【タイトル生成】
│   ├── 説明: タイトル候補を生成・管理
│   ├── 実行:
│   │   ├─ python3 generate_title_options.py --generate
│   │   │  └─ タイトル候補を生成し Google Sheets に入力
│   │   └─ python3 generate_title_options.py --show
│   │      └─ タイトル候補を表示
│   │
│   └── 実装版: ✅ 最新版（優先度5で作成）
│
└── related_articles_connector.py ⭐【関連記事】
    ├── 説明: 関連記事の自動推奨
    ├── 使用場所: article_generator_html_v2.py 内で自動呼び出し
    ├── 機能:
    │   ├─ 既存記事からキーワード抽出
    │   ├─ AI による関連記事推奨
    │   └─ HTML セクション自動生成
    │
    └── 実装版: ✅ 最新版（優先度4で作成）
```

### 【セットアップファイル】- 初回のみ使用

```
automation/scripts/
├── setup_title_options_columns.py 🔧【初回セットアップ】
│   ├── 説明: Google Sheets に新しい列を追加
│   ├── 実行: python3 automation/scripts/setup_title_options_columns.py
│   ├── 実行時期: 初回のみ（K～P列を追加）
│   └── 実装版: ✅ 最新版（優先度5で作成）
│
├── setup_affiliate_sheet.py 🔧【アフィリエイト管理セットアップ】
│   ├── 説明: Affiliate_Management シートの初期化
│   ├── 実行: python3 automation/scripts/setup_affiliate_sheet.py
│   ├── 実行時期: 初回のみ
│   └── 実装版: ✅ 最新版
│
└── add_template_column.py 🔧【テンプレート列追加】
    ├── 説明: Article_Theme に「使用テンプレート」列を追加
    ├── 実行: python3 automation/scripts/add_template_column.py
    ├── 実行時期: 初回のみ
    └── 実装版: ✅ 最新版
```

### 【Google Sheets 連携】- ユーティリティ

```
automation/google_services/
├── google_sheets.py
│   ├── 説明: Google Sheets API のラッパー
│   ├── 関数:
│   │   ├─ read_spreadsheet(spreadsheet_id, range)
│   │   └─ write_spreadsheet(spreadsheet_id, range, values)
│   │
│   └── 使用場所: 全Pythonファイルで使用
│
├── ga4.py
│   ├── 説明: Google Analytics 4 API
│   └── 現在: 未使用（今後の拡張向け）
│
├── gmail.py
│   ├── 説明: Gmail API
│   └── 現在: 未使用（今後の拡張向け）
│
├── google_calendar.py
│   ├── 説明: Google Calendar API
│   └── 現在: 未使用（今後の拡張向け）
│
└── google_sheets_trigger.gs
    ├── 説明: Google Apps Script
    └── 現在: 未使用
```

### 【古いファイル】- old/ フォルダに移動対象

```
old/
├── article_generator_v2.py
│   └── Markdown 生成版（直接HTMLに変わったため不要）
│
├── article_generator_html.py
│   └── v1版（v2で改修されたため不要）
│
├── markdown_to_swell_html.py
│   └── Markdown→HTML変換（直接生成に変わったため不要）
│
└── その他古いスクリプト
```

---

## 🔄 ワークフロー詳細

### ステップ 0: 初回セットアップ（1回のみ）

```bash
# Google Sheets に新しい列を追加
$ python3 automation/scripts/setup_title_options_columns.py

# Affiliate_Management シートを初期化
$ python3 automation/scripts/setup_affiliate_sheet.py

# Article_Theme に「使用テンプレート」列を追加
$ python3 automation/scripts/add_template_column.py
```

**確認**: Google Sheets で以下の列が追加されているか確認
- Article_Theme: K～P列（タイトル候補と選択）
- Affiliate_Management: A～H列（商品情報）

---

### ステップ 1: 記事テーマを入力

**Google Sheets → Article_Theme シート**

```
1. 新しい行を追加
2. 以下を入力:
   
   A列: （自動 - タイムスタンプ）
   B列: 新規
   C列: 記事のテーマ
        例: 「CBD とコーヒーの相性」
   D列: テンプレート選択（15個から選択）
        例: 「基礎知識解説型」
   E列: ターゲット
        例: 「CBD ユーザー・コーヒー愛好家」
   F列: タグ（カンマ区切り）
        例: 「CBD,カフェイン,相性,効果」
   G列: メタディスクリプション（空白でOK - 自動生成）
   H列: スラッグ（空白でOK - 自動生成）
   I列: アフィリエイトリンク（商品ID, 複数の場合はカンマ区切り）
        例: 「prod_001,prod_002」
   J列: 使用テンプレート（自動入力 - 編集不要）
```

---

### ステップ 2: タイトル候補を生成

**コマンド実行**

```bash
$ python3 automation/content/generate_title_options.py --generate
```

**処理内容**:
1. Article_Theme から「新規」ステータスの行を取得
2. テーマとテンプレートから5つのタイトル候補を AI で生成
3. K～O列に自動入力
4. ステータスを「タイトル選択待ち」に変更

**Google Sheets での確認**:
```
K列: タイトル候補1
L列: タイトル候補2
M列: タイトル候補3
N列: タイトル候補4
O列: タイトル候補5
P列: （空白 - ユーザーが入力）
B列: 「タイトル選択待ち」に変更
```

---

### ステップ 3: ユーザーがタイトルを選択

**Google Sheets で手動操作**

```
1. K～O列のタイトル候補を確認
2. 最適だと思うタイトルを P列にコピー&ペースト
3. B列を「生成待ち」に変更
```

**例**:
```
K1: 「CBD×コーヒーでカフェイン効果を最大化！知っておくべき3つの組み合わせ法」
L1: 「CBDとコーヒー、本当に効く？気になる疑問を徹底解説」
M1: 「カフェインの「ピークと落ち込み」を解消！」
N1: 「【科学的アプローチ】CBD...」
O1: 「2026年最新！CBD コーヒーで...」

↓ ユーザーが K1 を選択

P1: 「CBD×コーヒーでカフェイン効果を最大化！知っておくべき3つの組み合わせ法」
B1: 「生成待ち」
```

---

### ステップ 4: 記事を自動生成

**コマンド実行**

```bash
$ python3 automation/content/article_generator_html_v2.py
```

**処理フロー**:

```
1. Article_Theme から「生成待ち」の行を取得
   ↓
2. P列から選択されたタイトルを読み込み
   ↓
3. テンプレートから記事構造を選択
   ├─ 15個のテンプレートから最適なものを自動選択
   └─ 記事の構造と内容を最適化
   ↓
4. HTML 記事を生成
   ├─ 2,500-3,500文字
   ├─ 改行を活用した読みやすい構成
   ├─ SWELL互換の HTML
   └─ 見出し・リスト・テーブルを活用
   ↓
5. メタデータを自動生成
   ├─ メタディスクリプション
   ├─ カテゴリー
   └─ タグ
   ↓
6. SEO スラッグを自動生成
   ├─ 英語に統一
   ├─ キーワードベース
   └─ SEO 最適化
   ↓
7. 関連記事を自動推奨
   ├─ 既存記事を検索
   ├─ AI が最適な関連記事を判定
   └─ 最大3件を HTML に追加
   ↓
8. WordPress に投稿
   ├─ ステータス: 下書き
   ├─ タイトル・本文・メタデータを設定
   └─ 投稿ID を取得
   ↓
9. Google Sheets を更新
   ├─ B列: ステータスを「完了」に変更
   ├─ J列: 使用テンプレートを記入
   └─ Article_List に記事情報を追加
   ↓
10. LINE で通知
    └─ 記事情報と WordPress リンクを送信
```

**出力例**:
```
📝 スプレッドシート『Article_Theme』から記事テーマを読み込み中...

📝 HTML形式で記事生成中: CBD ユーザー・コーヒー愛好家 / 基礎知識解説型

   📋 ユーザーが選択したタイトルを使用します
      ✓ タイトル: CBD×コーヒーでカフェイン効果を最大化！...
   📋 メタデータを生成中...
      ✓ メタデータを生成しました
   📋 SEOスラッグを生成中...
      ✓ スラッグ: cbd-coffee-synergy-alertness
   📋 HTML記事を生成中...
      ✓ HTML記事を生成しました（7517文字）
   📋 関連記事を自動推奨中...
      ✓ 3件の関連記事を推奨しました
   📋 WordPressに下書き投稿中...
✅ WordPressに投稿しました: https://cbd-no-hito.com/?p=1187
   投稿ID: 1187

✅ 1件の記事を生成しました
```

---

### ステップ 5: WordPress で確認・編集・公開

**WordPress 管理画面**

```
1. 投稿 → 下書き
2. 投稿ID 1187 の記事を確認
3. 必要に応じて編集
   ├─ 画像を追加
   ├─ リンクをカスタマイズ
   └─ 改行を調整
4. 公開をクリック
```

---

## 📊 15個のテンプレート一覧

```
【商品・購入系】(6個)
1. 単一商品レビュー型
   └─ 1つの商品を詳しく紹介
   
2. 複数商品比較型
   └─ 3～5個の商品を比較
   
3. ブランド比較型
   └─ ブランド間の比較
   
4. 初心者向け商品ガイド型
   └─ 初心者向けの選び方
   
5. 上級者向け商品ガイド型
   └─ 上級者向けの選び方
   
6. 購入ガイド・コスパ型
   └─ コスパ重視の選び方

【知識・解説系】(5個)
7. 基礎知識解説型
   └─ 初心者向けの基本知識
   
8. 科学的根拠解説型
   └─ 研究に基づいた解説
   
9. 歴史・背景解説型
   └─ 歴史や背景の解説
   
10. 法律・規制解説型
    └─ 法律や規制の解説
   
11. 業界トレンド解説型
    └─ 業界の最新動向

【課題解決系】(3個)
12. 医学的課題解決型
    └─ 医学的根拠のある解決策
   
13. 日常的課題解決型
    └─ 日常的な悩みの解決
   
14. ビジネス・パフォーマンス型
    └─ ビジネスパフォーマンス向上

【コンテンツ系】(1個)
15. 体験談型
    └─ 個人の体験に基づいた記事
```

---

## 🗂️ ファイル分類・まとめ提案

### 推奨される構成

```
automation/
├── content/ ⭐【記事生成関連 - メイン】
│   ├── article_generator_html_v2.py      【実行】
│   ├── generate_title_options.py         【実行】
│   ├── related_articles_connector.py     【自動呼び出し】
│   ├── __init__.py
│   └── old/ 【古いファイル】
│       ├── article_generator_v2.py       (Markdown 版)
│       ├── article_generator_html.py     (v1版)
│       └── markdown_to_swell_html.py     (変換スクリプト)
│
├── scripts/ 🔧【セットアップ・ユーティリティ】
│   ├── setup_title_options_columns.py    【初回のみ】
│   ├── setup_affiliate_sheet.py          【初回のみ】
│   ├── add_template_column.py            【初回のみ】
│   ├── __init__.py
│   └── old/ 【古いファイル】
│       ├── ...
│       └── ...
│
├── google_services/ 🔌【Google API連携】
│   ├── google_sheets.py                  【共通ユーティリティ】
│   ├── ga4.py                            (未使用)
│   ├── gmail.py                          (未使用)
│   ├── google_calendar.py                (未使用)
│   └── __init__.py
│
└── social_media/ 📱【SNS連携】
    ├── line_notify.py                    【LINE 通知】
    └── ...
```

---

## ✅ 実行チェックリスト

### 【毎回】

```
□ Google Sheets に記事テーマを入力
□ python3 generate_title_options.py --generate
□ Google Sheets でタイトルを選択・ステータス更新
□ python3 article_generator_html_v2.py
□ WordPress で確認・編集・公開
```

### 【初回のみ】

```
□ python3 setup_title_options_columns.py
□ python3 setup_affiliate_sheet.py
□ python3 add_template_column.py
```

---

## 📞 トラブルシューティング

| 問題 | 原因 | 解決方法 |
|------|------|--------|
| タイトル候補が表示されない | Google Sheets API の問題 | API キー確認、クォータ確認 |
| テンプレートが認識されない | TEMPLATES 辞書に登録なし | article_generator_html_v2.py のテンプレートを確認 |
| 関連記事が推奨されない | Article_List に記事が少ない | 既存記事を確認（最低3件以上） |
| WordPress に投稿できない | 認証情報エラー | WORDPRESS_USERNAME, WORDPRESS_PASSWORD を確認 |

---

## 🎯 最後に

このフロー図とファイル分類を使用することで：

✅ 記事生成の流れが明確になる  
✅ 不要なファイルが整理される  
✅ 新しいメンバーもすぐに理解できる  
✅ メンテナンスが容易になる  

**定期的にこのドキュメントを更新してください！**
