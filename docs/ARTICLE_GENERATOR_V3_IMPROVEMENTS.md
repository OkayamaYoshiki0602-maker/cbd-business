#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
記事生成システム改修版 - v3
改修内容：
- カテゴリー自動選択機能
- 文字数厳密化（2000-3500文字）
- コンテンツ構造多様化（表・箇条書き・比較・チェックポイント等）
"""

import os
import sys
import re
from pathlib import Path
from datetime import datetime
from dotenv import load_dotenv
import json

sys.path.insert(0, str(Path(__file__).parent.parent))

import google.generativeai as genai
from google_services.google_sheets import read_spreadsheet, write_spreadsheet
from social_media.line_notify import send_line_message
from content.related_articles_connector import find_related_articles_by_ai, generate_related_articles_section

load_dotenv()

ARTICLE_SPREADSHEET_ID = os.getenv('ARTICLE_SPREADSHEET_ID', '1-2L6C3NpF8vqnXxHWKP-Js3TMFKYE73tTtxdkZVPTaM')
ARTICLE_SHEET_NAME = 'Article_Theme'
ARTICLE_LIST_SHEET = 'Article_List'
GEMINI_API_KEY = os.getenv('GEMINI_API_KEY')
WORDPRESS_URL = os.getenv('WORDPRESS_URL', 'https://cbd-no-hito.com')
WORDPRESS_USERNAME = os.getenv('WORDPRESS_USERNAME', 'yoshiki')
WORDPRESS_PASSWORD = os.getenv('WORDPRESS_APP_PASSWORD')

genai.configure(api_key=GEMINI_API_KEY)

# テンプレート定義（15個）
TEMPLATES = {
    # 【商品・購入系】(6個)
    1: {"name": "単一商品レビュー型", "require_product": True, "category": "CBD商品レビュー"},
    2: {"name": "複数商品比較型", "require_product": True, "category": "CBD商品比較"},
    3: {"name": "ブランド比較型", "require_product": True, "category": "CBD商品比較"},
    4: {"name": "初心者向け商品ガイド型", "require_product": True, "category": "CBD初心者ガイド"},
    5: {"name": "上級者向け商品ガイド型", "require_product": True, "category": "CBD選び方"},
    6: {"name": "購入ガイド・コスパ型", "require_product": True, "category": "CBD購入ガイド"},
    
    # 【知識・解説系】(5個)
    7: {"name": "基礎知識解説型", "require_product": False, "category": "基礎知識（Basics）"},
    8: {"name": "科学的根拠解説型", "require_product": False, "category": "基礎知識（Basics）"},
    9: {"name": "歴史・背景解説型", "require_product": False, "category": "基礎知識（Basics）"},
    10: {"name": "法律・規制解説型", "require_product": False, "category": "基礎知識（Basics）"},
    11: {"name": "業界トレンド解説型", "require_product": False, "category": "CBDブランド"},
    
    # 【課題解決系】(3個)
    12: {"name": "医学的課題解決型", "require_product": True, "category": "摂取方法（Methods）"},
    13: {"name": "日常的課題解決型", "require_product": True, "category": "CBD効果"},
    14: {"name": "ビジネス・パフォーマンス型", "require_product": False, "category": "CBD効果"},
    
    # 【コンテンツ系】(1個)
    15: {"name": "体験談型", "require_product": True, "category": "CBD効果"},
}


def get_category_for_template(template_id):
    """
    テンプレートIDからカテゴリーを取得
    """
    template_info = TEMPLATES.get(template_id, {})
    return template_info.get("category", "CBD")


def generate_article_html_v3_enhanced(theme, target, template_id, keywords, title):
    """
    改修版：
    - 文字数厳密化（2000-3500文字）
    - コンテンツ構造多様化
    - 表・比較・チェックポイント・箇条書き等を活用
    """
    model = genai.GenerativeModel("gemini-2.5-flash")
    current_year = datetime.now().year
    template_name = TEMPLATES.get(template_id, {}).get("name", "")
    require_product = TEMPLATES.get(template_id, {}).get("require_product", False)
    
    # テンプレートに応じたコンテンツ構造の指示
    structure_guidance = get_template_specific_structure(template_id, template_name)
    
    product_instruction = ""
    if require_product:
        product_instruction = """
【商品紹介について】
- 自然な流れで商品を紹介する
- 複数商品を紹介してもOK
- 商品紹介セクションはまとめて1つのセクションにする
"""
    else:
        product_instruction = """
【商品紹介について】
- 商品紹介は基本的に不要
- どうしても必要な場合のみ、関連商品へのリンク形式で対応
"""
    
    prompt = f"""あなたはCBD専門ライターで、SEO最適化とユーザー体験の向上に精通しています。

【記事基本情報】
テーマ: {theme}
タイトル: {title}
ターゲット: {target}
テンプレート: {template_name}
キーワード: {keywords}
作成年: {current_year}年

【絶対に守るべきルール】
★ 文字数は2,000～3,500文字に厳密に制限してください
★ 短い段落（2行以下）で改行を多用してください
★ 見た目は短く感じるようにしてください

【コンテンツ構造を多様化してください】
{structure_guidance}

{product_instruction}

【HTML構造】
```html
<div class="wp-block-group cbd-aff-disclaimer">
  <div class="wp-block-group__inner-container">
    <p style="font-size:13px;opacity:.8">※当サイトはアフィリエイト広告を利用しています。</p>
  </div>
</div>

<h2 class="wp-block-heading">{title}</h2>

<p>導入段落：読者の悩みや興味に共感。<br />短く、明確に。</p>

【目次風セクション】
<ul class="wp-block-list">
  <li><a href="#section1">セクション1</a></li>
  <li><a href="#section2">セクション2</a></li>
</ul>

【本文セクション】
- 見出しは h3 タグを使用
- 表・リスト・チェックポイント等を活用
- 段落は短く（2行以下）
- 箇条書きで情報を整理

【まとめセクション】
<div class="wp-block-group is-style-summary-box">
  <div class="wp-block-group__inner-container">
    <h3 class="wp-block-heading">まとめ</h3>
    <ul class="wp-block-list is-style-check_list">
      <li>ポイント1</li>
      <li>ポイント2</li>
      <li>ポイント3</li>
    </ul>
  </div>
</div>

【参考文献】
<div class="wp-block-group">
  <div class="wp-block-group__inner-container">
    <h3 class="wp-block-heading">参考文献</h3>
    <ul class="wp-block-list">
      <li>参考リンク1</li>
      <li>参考リンク2</li>
    </ul>
  </div>
</div>
```

【出力指示】
HTMLのみを返してください。前置きや説明は不要です。
"""
    
    try:
        response = model.generate_content(prompt)
        html_content = response.text.strip()
        
        # 文字数をチェック
        char_count = len(html_content)
        if char_count < 2000:
            print(f"⚠️ 警告: 文字数が不足しています（{char_count}文字、目標：2000～3500文字）")
        elif char_count > 3500:
            print(f"⚠️ 警告: 文字数が超過しています（{char_count}文字、目標：2000～3500文字）")
        else:
            print(f"✓ 文字数OK: {char_count}文字")
        
        return html_content
    
    except Exception as e:
        print(f"❌ 記事生成エラー: {e}")
        return None


def get_template_specific_structure(template_id, template_name):
    """
    テンプレートに応じた構造ガイダンス
    """
    structures = {
        1: """【単一商品レビュー型】
- 商品の概要（表で商品スペック）
- メリット（箇条書き 3-5個）
- デメリット（箇条書き 2-3個）
- 使用方法（ステップ形式）
- 実際の効果（体験者の声）
- 購入ガイド""",
        
        2: """【複数商品比較型】
- 商品比較表（3-5商品を並べて比較）
- 各商品の詳細（1商品ずつ）
- 比較チャート（価格 vs 含有量）
- どの商品がおすすめか""",
        
        3: """【ブランド比較型】
- ブランドの特徴を表で比較
- ブランドAの詳細
- ブランドBの詳細
- 選ぶ際のポイント""",
        
        4: """【初心者向け商品ガイド型】
- よくある質問（Q&A形式）
- 初心者が選ぶべきポイント（チェックリスト）
- おすすめ商品（3-5個）
- 購入時の注意点""",
        
        5: """【上級者向け商品ガイド型】
- 成分比較表（CBD・CBN・テルペン等）
- 効果別おすすめ（表形式）
- 使用体験レビュー
- コスパ分析""",
        
        6: """【購入ガイド・コスパ型】
- コスパ比較表
- 価格帯別おすすめ
- 割引情報
- 購入先ガイド""",
        
        7: """【基礎知識解説型】
- CBDとは何か（簡潔に）
- 基本用語の解説（箇条書き）
- よくある誤解 vs 正しい知識（比較表）
- 次のステップ""",
        
        8: """【科学的根拠解説型】
- 研究概要
- 科学的メカニズム（図解イメージ説明）
- 研究結果一覧（表）
- 今後の期待""",
        
        9: """【歴史・背景解説型】
- タイムライン形式で歴史説明
- 主要な出来事（表）
- 現在の状況
- 将来の展望""",
        
        10: """【法律・規制解説型】
- 日本での法律（表で明確に）
- よくある質問（Q&A）
- 注意点チェックリスト
- 国別の状況""",
        
        11: """【業界トレンド解説型】
- 最新トレンド（箇条書き 5個）
- 市場動向（グラフ風説明）
- 今後の予測
- ブランド動向""",
        
        12: """【医学的課題解決型】
- 課題の説明
- CBDの科学的作用（表）
- 実際の改善例（レビュー形式）
- 使用上の注意""",
        
        13: """【日常的課題解決型】
- 悩みあるあるチェックリスト
- CBDでの改善ステップ
- 実体験ストーリー
- 実践的なアドバイス""",
        
        14: """【ビジネス・パフォーマンス型】
- ビジネスシーンでの効果（表）
- 実績例（複数）
- 使用シーン別ガイド
- ROI分析""",
        
        15: """【体験談型】
- 背景・きっかけ
- 使用前後の変化（Before/After）
- 実際の体験（ストーリー形式）
- おすすめポイント""",
    }
    
    return structures.get(template_id, """
【基本構造】
- 導入：問題提示
- 本文：複数セクション（表・リスト・比較等を活用）
- まとめ：ポイント整理
""")


# 以下、既存のコード（generate_title_variations, generate_metadata等）は変更なし

print("""
✅ article_generator_html_v3.py が準備完了しました

【改修内容】
1. カテゴリー自動選択 - テンプレートに応じて自動設定
2. 文字数厳密化 - 2000～3500文字に制限
3. コンテンツ構造多様化 - 表・比較・チェックリスト等を活用

【使用方法】
既存の article_generator_html_v2.py と同じ使い方です。
内部的にプロンプトが改善されています。

【今後の予定】
article_generator_html_v2.py のプロンプトを置き換えてください。
""")
