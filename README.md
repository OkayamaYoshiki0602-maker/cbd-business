# CBD Business - WordPress/SWELL 自動化プロジェクト

CBD Side Businessの記事生成・WordPress自動化・Google連携システム一式

## 📁 ディレクトリ構造

```
cbd-business/
├── article-generator/           # 記事自動生成ツール
│   ├── core/                   # コア機能（変換・生成エンジン）
│   │   ├── markdown_to_swell_html.py
│   │   └── article_generator_html.py
│   ├── post-pages/             # 投稿ページ生成
│   │   ├── article_generator_v2.py
│   │   └── article_generator_html_v2.py
│   ├── fixed-pages/            # 固定ページ生成（今後）
│   └── utilities/              # 補助ツール・CSS
│       ├── generate_title_options.py
│       ├── related_articles_connector.py
│       ├── github_article_publisher.py
│       ├── wordpress_publisher.py
│       └── swell-additional-styles.css  # 追加CSS
│
├── wordpress/                  # WordPress関連ファイル
│   ├── pages/                 # 固定ページHTML
│   ├── posts/                 # 投稿ページHTML
│   └── plugins/               # WordPress プラグイン
│
├── google-services/            # Google API連携
│   ├── google_sheets.py
│   ├── google_calendar.py
│   ├── gmail.py
│   ├── ga4.py
│   ├── google_sheets_trigger_direct.py
│   └── __init__.py
│
└── docs/                       # ドキュメント（記事・WordPress関連）
```

## 🎯 主要機能

### 記事生成
- Gemini APIを使用した自動記事生成
- Markdown → SWELL HTML変換
- Google Sheets連携で記事テーマを管理
- WordPress REST APIで自動投稿

### WordPress関連
- 固定ページ・投稿ページHTMLテンプレート
- SWELL専用プラグイン（アフィリエイト管理）
- CSS管理（responsive design対応）

### Google連携
- Google Sheets：記事テーマ・メタデータ管理
- Google Calendar：発行スケジュール
- Gmail：通知・連携
- GA4：分析データ

## 🚀 セットアップ

```bash
# 依存関係インストール
pip install -r requirements.txt

# 環境変数設定
cp .env.example .env
# .envにGemini API Key、WordPress認証情報などを記入

# 記事生成実行
python article-generator/post-pages/article_generator_v2.py
```

## 📝 使用方法

詳細は各ディレクトリの`README.md`を参照

---

**Owner:** OkayamaYoshiki0602-maker  
**Last Updated:** 2026-01-18
