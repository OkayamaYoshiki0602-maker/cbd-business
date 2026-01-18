# ファイル整理・分類完全ガイド

**作成日**: 2026年1月17日  
**目的**: Pythonファイルの整理・不要な古いファイルの整理

---

## 🗂️ ファイル構造の最適化

### 推奨される最新構成

```
automation/
│
├── content/
│   ├── __init__.py
│   ├── article_generator_html_v2.py          ⭐【メイン】
│   ├── generate_title_options.py             ⭐【タイトル生成】
│   ├── related_articles_connector.py         ⭐【関連記事】
│   │
│   └── old/
│       ├── README.md (バージョン情報)
│       ├── article_generator_v2.py           (廃止: Markdown版)
│       ├── article_generator_html.py         (廃止: v1版)
│       └── markdown_to_swell_html.py         (廃止: 変換スクリプト)
│
├── scripts/
│   ├── __init__.py
│   ├── setup_title_options_columns.py        【初回セットアップ】
│   ├── setup_affiliate_sheet.py              【初回セットアップ】
│   ├── add_template_column.py                【初回セットアップ】
│   │
│   └── old/
│       └── README.md (廃止理由)
│
├── google_services/
│   ├── __init__.py
│   ├── google_sheets.py                      【Google Sheets API】
│   ├── ga4.py                                (今後用)
│   ├── gmail.py                              (今後用)
│   ├── google_calendar.py                    (今後用)
│   └── google_sheets_trigger.gs              (不使用)
│
└── social_media/
    ├── __init__.py
    ├── line_notify.py                        【LINE通知】
    └── ...
```

---

## 📁 ファイル整理手順

### ステップ 1: old フォルダを作成

```bash
mkdir -p automation/content/old
mkdir -p automation/scripts/old
```

### ステップ 2: 古いファイルを移動

```bash
# Markdown 関連の古いファイルを移動
mv automation/content/article_generator_v2.py automation/content/old/
mv automation/content/article_generator_html.py automation/content/old/
mv automation/content/markdown_to_swell_html.py automation/content/old/

# old フォルダに README を作成
cat > automation/content/old/README.md << 'EOF'
# 廃止ファイル一覧

このフォルダに入っているファイルは廃止版です。使用しないでください。

## article_generator_v2.py
- **廃止理由**: Markdown生成版（直接HTML生成に変更）
- **置き換え**: article_generator_html_v2.py
- **廃止日**: 2026-01-17

## article_generator_html.py
- **廃止理由**: v1版（v2で改修）
- **置き換え**: article_generator_html_v2.py
- **廃止日**: 2026-01-17

## markdown_to_swell_html.py
- **廃止理由**: Markdown→HTML変換スクリプト（直接生成に変更）
- **置き換え**: article_generator_html_v2.py内の関数
- **廃止日**: 2026-01-17

---

参考が必要な場合は Git の履歴から確認できます。
EOF
```

### ステップ 3: 使用中のファイルを確認

```bash
# 実行中のスクリプトを確認
grep -r "import.*article_generator" automation/
grep -r "import.*markdown_to_swell" automation/
grep -r "import.*related_articles" automation/

# 結果: 
# - article_generator_html_v2.py: 外部スクリプトなし（メイン実行）
# - generate_title_options.py: 外部スクリプトなし（独立実行）
# - article_generator_html_v2.py が related_articles_connector.py をインポート
```

---

## 📊 ファイル分類表

### 【毎日実行するファイル】

| ファイル | 実行頻度 | コマンド | 説明 |
|---------|--------|--------|------|
| `generate_title_options.py` | 1～5回/日 | `python3 automation/content/generate_title_options.py --generate` | タイトル候補を生成 |
| `article_generator_html_v2.py` | 1～10回/日 | `python3 automation/content/article_generator_html_v2.py` | 記事を生成・投稿 |

### 【初回のみ実行】

| ファイル | 実行時期 | コマンド | 説明 |
|---------|--------|--------|------|
| `setup_title_options_columns.py` | 初回のみ | `python3 automation/scripts/setup_title_options_columns.py` | Google Sheets K～P列追加 |
| `setup_affiliate_sheet.py` | 初回のみ | `python3 automation/scripts/setup_affiliate_sheet.py` | Affiliate_Management初期化 |
| `add_template_column.py` | 初回のみ | `python3 automation/scripts/add_template_column.py` | テンプレート列追加 |

### 【必要時に実行】

| ファイル | 実行時期 | 説明 |
|---------|--------|------|
| `generate_title_options.py --show` | 確認時 | タイトル候補を表示 |

### 【今後用】

| ファイル | 状態 | 説明 |
|---------|-----|------|
| `ga4.py` | 未使用 | Google Analytics 4 との連携 |
| `gmail.py` | 未使用 | Gmail との連携 |
| `google_calendar.py` | 未使用 | Google Calendar との連携 |

### 【廃止】

| ファイル | 廃止理由 | 置き換え | 廃止日 |
|---------|--------|--------|--------|
| `article_generator_v2.py` | Markdown版 | article_generator_html_v2.py | 2026-01-17 |
| `article_generator_html.py` | v1版 | article_generator_html_v2.py | 2026-01-17 |
| `markdown_to_swell_html.py` | 不要 | article_generator_html_v2.py | 2026-01-17 |

---

## 🔄 関数・モジュールの依存関係

```
【article_generator_html_v2.py】(メイン)
    ↓ インポート
    ├─ google_services.google_sheets
    │   ├─ read_spreadsheet()
    │   └─ write_spreadsheet()
    │
    ├─ related_articles_connector
    │   ├─ find_related_articles_by_ai()
    │   └─ generate_related_articles_section()
    │
    ├─ social_media.line_notify
    │   └─ send_line_message()
    │
    └─ google.generativeai (Gemini API)
        └─ GenerativeModel("gemini-2.5-flash")


【generate_title_options.py】(タイトル生成)
    ↓ インポート
    ├─ google_services.google_sheets
    │   ├─ read_spreadsheet()
    │   └─ write_spreadsheet()
    │
    └─ google.generativeai (Gemini API)
        └─ GenerativeModel("gemini-2.5-flash")


【related_articles_connector.py】(関連記事)
    ↓ インポート
    └─ google.generativeai (Gemini API)
        └─ GenerativeModel("gemini-2.5-flash")

※article_generator_html_v2.py から自動的に呼び出される
```

---

## ✅ ファイル整理チェックリスト

```
【整理前の確認】
□ Git で全ファイルをコミット（バックアップ）
□ 廃止ファイルが実際に不要かを確認

【実行】
□ old フォルダを作成
□ 廃止ファイルを移動
□ README を作成
□ スクリプトが正常に実行できることを確認

【確認】
□ article_generator_html_v2.py が正常に実行
□ generate_title_options.py が正常に実行
□ エラーログで廃止ファイルへのインポートがないか確認

【ドキュメント】
□ このファイルを保存
□ チーム内で共有
```

---

## 📚 参考資料

### ファイルの用途

- **article_generator_html_v2.py**: 記事生成のメインエンジン
  - Google Sheets から記事テーマを読み込み
  - タイトル・メタデータ・HTMLを生成
  - WordPress に投稿

- **generate_title_options.py**: タイトル候補の生成・管理
  - テーマからタイトル候補を生成
  - Google Sheets に自動入力
  - ユーザーが選択可能に

- **related_articles_connector.py**: 関連記事の自動推奨
  - 既存記事を検索
  - AI で最適な関連記事を判定
  - HTML セクションを生成

---

## 🎯 まとめ

### ファイル整理の効果

✅ **コードの明確性向上**  
✅ **メンテナンスの容易性**  
✅ **新しいチームメンバーの理解が簡単に**  
✅ **不要なインポートがなくなる**  
✅ **実行速度がわずかに向上**  

### 今後の推奨事項

1. **定期的な整理**
   - 3ヶ月ごとにファイル構造を見直す
   - 不要なファイルを old フォルダに移動

2. **ドキュメントの更新**
   - このファイルを最新の状態に保つ
   - 新しいファイルを追加したら記録

3. **バージョン管理**
   - Git で履歴を管理
   - old フォルダのファイルは削除せず保持

---

**実装日**: 2026年1月17日  
**最終更新**: 2026年1月17日

