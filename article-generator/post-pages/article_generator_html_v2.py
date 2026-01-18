#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
CBD記事生成（HTML直接出力版 v2）
改修内容：
- 改行・文字量の改善（見た目は短く、実質2,500-3,500文字）
- タイトルのバリエーション（複数候補から選択）
- メタデータの自動埋め込み（ディスクリプション、カテゴリー、タグ）
- SEOフレンドリーなスラッグの自動生成
- テンプレート列の自動埋め込み
"""

import os
import sys
import re
from pathlib import Path
from datetime import datetime
from dotenv import load_dotenv
import json
import requests
from requests.auth import HTTPBasicAuth

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

# テンプレート定義（15個に拡張）
# カテゴリーは WordPress の確定済みカテゴリーから選択
TEMPLATES = {
    # 【商品・購入系】(6個) → CBDブランド
    1: {"name": "単一商品レビュー型", "require_product": True, "category": "CBDブランド"},
    2: {"name": "複数商品比較型", "require_product": True, "category": "CBDブランド"},
    3: {"name": "ブランド比較型", "require_product": True, "category": "CBDブランド"},
    4: {"name": "初心者向け商品ガイド型", "require_product": True, "category": "CBDブランド"},
    5: {"name": "上級者向け商品ガイド型", "require_product": True, "category": "CBDブランド"},
    6: {"name": "購入ガイド・コスパ型", "require_product": True, "category": "CBDブランド"},
    
    # 【知識・解説系】(5個) → 基礎知識（Basics）
    7: {"name": "基礎知識解説型", "require_product": False, "category": "基礎知識（Basics）"},
    8: {"name": "科学的根拠解説型", "require_product": False, "category": "基礎知識（Basics）"},
    9: {"name": "歴史・背景解説型", "require_product": False, "category": "基礎知識（Basics）"},
    10: {"name": "法律・規制解説型", "require_product": False, "category": "基礎知識（Basics）"},
    11: {"name": "業界トレンド解説型", "require_product": False, "category": "基礎知識（Basics）"},
    
    # 【課題解決系】(3個) → 摂取方法（Methods） / 課題別（Issues）
    12: {"name": "医学的課題解決型", "require_product": True, "category": "摂取方法（Methods）"},
    13: {"name": "日常的課題解決型", "require_product": True, "category": "課題別（Issues）"},
    14: {"name": "ビジネス・パフォーマンス型", "require_product": False, "category": "基礎知識（Basics）"},
    
    # 【コンテンツ系】(1個) → 課題別（Issues）
    15: {"name": "体験談型", "require_product": True, "category": "課題別（Issues）"},
}

# WordPress カテゴリー名 → ID マッピング（キャッシュ）
CATEGORY_NAME_TO_ID_CACHE = {}


def get_wordpress_category_id(category_name):
    """
    カテゴリー名から WordPress のカテゴリー ID を取得
    キャッシュがあればそれを使用、なければ API から取得
    """
    global CATEGORY_NAME_TO_ID_CACHE
    
    # キャッシュにあればそれを返す
    if category_name in CATEGORY_NAME_TO_ID_CACHE:
        return CATEGORY_NAME_TO_ID_CACHE[category_name]
    
    # API から取得
    try:
        url = f"{WORDPRESS_URL}/wp-json/wp/v2/categories?search={category_name}"
        response = requests.get(url, timeout=10)
        
        if response.status_code == 200:
            categories = response.json()
            if categories:
                category_id = categories[0]["id"]
                # キャッシュに保存
                CATEGORY_NAME_TO_ID_CACHE[category_name] = category_id
                return category_id
        
        print(f"⚠️ カテゴリー '{category_name}' が見つかりません。ID 1 (Uncategorized) を使用します。")
        CATEGORY_NAME_TO_ID_CACHE[category_name] = 1
        return 1
    
    except Exception as e:
        print(f"⚠️ カテゴリー取得エラー: {e}。ID 1 (Uncategorized) を使用します。")
        CATEGORY_NAME_TO_ID_CACHE[category_name] = 1
        return 1


def generate_title_variations(theme, template_id):
    """
    複数のタイトル候補を生成
    """
    model = genai.GenerativeModel("gemini-2.5-flash")
    current_year = datetime.now().year
    template_name = TEMPLATES.get(template_id, {}).get("name", "")
    
    prompt = f"""あなたはSEO最適化と読者の興味を引き出すプロのライターです。

【指定内容】
テーマ: {theme}
テンプレート: {template_name}
年号: {current_year}

【要件】
以下の5つのタイトル候補を生成してください。各タイトルは異なるアプローチで、読みたくなるようにしてください。

1. 数字を活用したタイトル（例：「3つの」「5つの理由」など）
2. 疑問形のタイトル（例：「○○って本当に効く？」）
3. 解決策を示すタイトル（例：「××を解決する方法は？」）
4. 権威性を持つタイトル（例：「【プロが選ぶ】」「【データで証明】」）
5. 希少性・最新性を活用したタイトル（例：「2026年最新」「知られざる」）

【禁止事項】
- 「【決定版】」を全てに付けない
- 同じ枕詞を複数使わない
- 説教的な表現は避ける
- 誇大広告のような表現は避ける

【出力形式】
JSON形式で、以下の構造で返してください：
{{
  "titles": [
    {{"number": 1, "title": "タイトル1", "approach": "アプローチ説明"}},
    {{"number": 2, "title": "タイトル2", "approach": "アプローチ説明"}},
    ...
  ]
}}

タイトルのみ返してください。前置きや説明は不要です。
"""
    
    try:
        response = model.generate_content(prompt)
        json_str = response.text.strip()
        
        # JSON部分を抽出
        json_match = re.search(r'\{.*\}', json_str, re.DOTALL)
        if json_match:
            data = json.loads(json_match.group())
            return [t["title"] for t in data.get("titles", [])]
    except Exception as e:
        print(f"⚠️ タイトル生成エラー: {e}")
    
    # フォールバック
    return [
        f"【2026年最新版】{theme}について完全解説",
        f"【データから分かる】{theme}の重要ポイント3つ",
        f"{theme}で失敗しないために知るべき真実",
        f"プロが解説：{theme}の本当の選び方",
        f"知られざる{theme}の実態と対策",
    ]


def generate_metadata(title, theme, template_id, keywords):
    """
    メタデータ（ディスクリプション、カテゴリー、タグ）を自動生成
    """
    model = genai.GenerativeModel("gemini-2.5-flash")
    template_name = TEMPLATES.get(template_id, {}).get("name", "")
    
    prompt = f"""あなたはSEO専門家です。以下の指定に従い、メタデータを生成してください。

【記事情報】
タイトル: {title}
テーマ: {theme}
テンプレート: {template_name}
キーワード: {keywords}

【要件】
以下のJSON形式で返してください：

{{
  "description": "160文字以内のメタディスクリプション。記事の要点を簡潔に、読者の興味を引くように",
  "category": "以下から選択: 商品紹介|初心者ガイド|悩み解決|ビジネス|比較|成分解説|体験談|ニュース|最適化|購入ガイド",
  "tags": "タグ1,タグ2,タグ3,タグ4,タグ5",
  "image_suggestions": [
    {{"position": "セクション1の後", "description": "提案する画像内容（例：比較表、グラフ等）"}},
    {{"position": "セクション3の後", "description": "提案する画像内容"}}
  ],
  "seo_keywords": ["キーワード1", "キーワード2", "キーワード3"]
}}

【ルール】
- ディスクリプションは160文字以内
- タグはカンマで区切った単語（スペース無し）を入力。記事の最重要キーワードから5個
- image_suggestions: 記事に挿入すべき画像を2つ提案（位置と内容）
- SEOキーワードは検索ボリュームが多そうなものを選択

JSONのみ返してください。前置きは不要です。
"""
    
    try:
        response = model.generate_content(prompt)
        json_str = response.text.strip()
        
        json_match = re.search(r'\{.*\}', json_str, re.DOTALL)
        if json_match:
            data = json.loads(json_match.group())
            
            # タグをカンマで分割（文字列から配列に変換）
            tags = data.get("tags", "")
            if isinstance(tags, list):
                tags_str = ",".join(tags)
            else:
                tags_str = tags
            
            return {
                "description": data.get("description", ""),
                "category": data.get("category", ""),
                "tags": tags_str,
                "image_suggestions": data.get("image_suggestions", []),
            }
    except Exception as e:
        print(f"⚠️ メタデータ生成エラー: {e}")
    
    # フォールバック
    return {
        "description": f"{title[:80]}について詳しく解説。CBD選びのポイントをプロが分かりやすく説明します。",
        "category": "CBD情報",
        "tags": "CBD,初心者,ガイド,情報,解説",
        "image_suggestions": [],
    }


def generate_seo_slug(title, theme):
    """
    SEOフレンドリーなスラッグを自動生成（英語）
    """
    model = genai.GenerativeModel("gemini-2.5-flash")
    
    prompt = f"""英語SEO最適化の専門家として、以下の記事用のURL スラッグを生成してください。

【記事情報】
タイトル: {title}
テーマ: {theme}

【要件】
- 英語のみ（日本語は絶対禁止）
- ハイフン区切り（スペースはハイフンに変換）
- 50文字以下
- SEOに強いキーワードを含める
- 記事内容を正確に反映
- 単語は3-5個程度
- 一般的で検索されやすいスラッグ

【例】
良い例：
- cbd-beginners-guide-2026
- how-to-choose-cbd-oil
- cbd-vs-thc-differences
- natural-anxiety-relief-cbd

悪い例：
- cbd-no-hito-article-1
- shishin-tool-2026 （日本語ローマ字化は禁止）
- article-2026-01-17 （日付は禁止）

スラッグのみ返してください。前置きや説明は不要です。
"""
    
    try:
        response = model.generate_content(prompt)
        slug = response.text.strip().lower()
        # ハイフン以外を削除
        slug = re.sub(r'[^a-z0-9-]', '', slug)
        slug = re.sub(r'-+', '-', slug).strip('-')
        if slug:
            return slug[:60]
    except Exception as e:
        print(f"⚠️ スラッグ生成エラー: {e}")
    
    # フォールバック：テーマから簡易生成
    fallback = theme.lower()
    fallback = re.sub(r'[^a-z0-9]+', '-', fallback)
    fallback = re.sub(r'-+', '-', fallback).strip('-')
    return fallback[:50] or "cbd-article"


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


def truncate_html_to_char_limit(html_content, target_chars=3500):
    """
    HTML内容を3500文字制限内に収める（セクション削除方式）
    最後のセクションから順に削除して調整
    """
    import re
    
    # タグを除いた実テキスト文字数を計算
    text_only = re.sub(r'<[^>]+>', '', html_content)
    current_chars = len(text_only)
    
    if current_chars <= target_chars:
        return html_content
    
    print(f"   ⚠️ 文字数超過: {current_chars}文字 → {target_chars}文字以内に削減")
    
    result = html_content
    
    # 繰り返し削除して3500字以内に収める
    max_iterations = 5
    iteration = 0
    
    while iteration < max_iterations:
        result_text = re.sub(r'<[^>]+>', '', result)
        final_chars = len(result_text)
        
        if final_chars <= target_chars:
            print(f"      削減後: {final_chars}文字 ✅")
            return result
        
        iteration += 1
        
        # 最後の<h3>セクションを削除
        last_h3_idx = result.rfind("<h3")
        if last_h3_idx > 0:
            result = result[:last_h3_idx]
            result = result.rstrip()
        else:
            # H3が見つからない場合は最後の段落を削除
            last_p_idx = result.rfind("<p")
            if last_p_idx > 0:
                result = result[:last_p_idx]
                result = result.rstrip()
            else:
                break
    
    result_text = re.sub(r'<[^>]+>', '', result)
    final_chars = len(result_text)
    print(f"      削減後: {final_chars}文字 ✅")
    
    return result


def generate_article_html_improved(theme, target, template_id, keywords, title):
    """
    改修版 v3：
    - 文字数厳密化（2000-5000文字 / 上限5000）
    - コンテンツ構造多様化（表・比較・チェックポイント等）
    - ビジュアル構成の最適化
    - 段落長・見出し頻度の厳密化
    - 生成後の文字数削減処理
    """
    model = genai.GenerativeModel("gemini-2.5-flash")
    current_year = datetime.now().year
    template_name = TEMPLATES.get(template_id, {}).get("name", "")
    require_product = TEMPLATES.get(template_id, {}).get("require_product", False)
    
    # テンプレートに応じたコンテンツ構造ガイダンス
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

【絶対に守るべき文字数ルール（v5.2 最終版 - シンプル化）】
★ 全体：3,500文字以内（超過厳禁）
★ 最小：2,000文字
★ 1見出し内：150文字以内（絶対上限、超過時はH4で細分化）
★ 1段落：50-80字目安（最大100字）
★ 段落の最大行数：2行（3行以上禁止、改行<br>を活用）
★ セクション数：3-5個推奨
★ 参考記事1097のシンプルさを実現

【構造と読みやすさルール（v5.2 最終版 - シンプル重視）】
★ 見出し（H3）の数：4-5個推奨（最大6個）
★ 各H3セクション：150文字以内（絶対）
★ 1段落は最大2行（改行で分割）
★ 1文が長い場合は改行<br>で分割
★ 参考記事1097のように短くシンプルに
★ ビジュアル（表・リスト・ボックス）で区切る
★ 詰まった印象を避ける

【ビジュアル・装飾ルール（v5.1 - 緑系統一）】
★ 色使いを緑系のみに統一（赤・オレンジ廃止）
  - 太字：<strong>重要な用語</strong>（色なし）
  - 緑下線：<span style="border-bottom: 3px solid #2d7a4c;">強調内容</span>
  - 青下線（オプション）：<span style="border-bottom: 3px solid #4a90e2;">ポイント</span>
  - マーカー：<span class="swl-marker mark_green">グリーン</span>のみ
★ 色数最小化：3-4色以内（赤・オレンジは使用禁止）
★ テキスト：30-40%、表・リスト：30-40%、ボックス・画像：20-30%

【Q&Aセクションの実装（v5.1 - 緑色統一）】
ダサくない、シンプルで洗練されたQ&Aに（参考サイト並み）：
```html
<div style="margin-bottom: 24px;">
  <p style="font-weight: bold; margin: 0 0 8px 0; font-size: 16px;">Q. 質問文</p>
  <p style="margin: 0; color: #2d7a4c; font-weight: bold;">A.</p>
  <p style="margin: 4px 0 0 0; color: #333; line-height: 1.6;">回答内容を簡潔に。重要な部分は<strong>太字</strong>で強調。</p>
</div>
```
★ ポイント：
  - 背景色なし（シンプル）
  - 左ボーダーなし
  - アイコン不要（「Q」「A」のテキストのみ）
  - Aは緑太字（#2d7a4c）で視覚的に区別
  - 複数Q&Aの場合は margin-bottom: 24px で余白確保
★ Q&A内で重要な部分は太字（<strong>）で強調
★ 参考サイト並みのシンプル・洗練されたデザイン

【商品紹介セクションのおしゃれな設計（v4改定）】
```html
<h3 class="wp-block-heading" style="border-left: 5px solid #2d7a4c; padding-left: 15px; margin-top: 24px;">
  ★ ブランド名：商品の1行説明
</h3>

<p>商品の特徴を簡潔に（150字以内）。<br />改行で読みやすく。</p>

<div style="background-color: #f9f9f9; border-radius: 8px; padding: 16px; margin: 16px 0; border-left: 4px solid #2d7a4c;">
  <p style="margin: 0 0 8px 0; font-weight: bold; color: #2d7a4c;">🔸 おすすめポイント</p>
  <ul style="margin: 8px 0; padding-left: 20px;">
    <li><span style="color: #2d7a4c; font-weight: bold;">メリット1</span></li>
    <li><span style="color: #2d7a4c; font-weight: bold;">メリット2</span></li>
  </ul>
  <p style="margin: 12px 0 0 0; font-size: 14px;"><span style="color: #ff6d4b; font-weight: bold;">💰 価格帯</span>：〇〇円 ～ 〇〇円</p>
</div>
```
★ 見出し（H3）に左ボーダー（5px #2d7a4c）で視覚的強調
★ グレー背景ボックスで情報をグループ化
★ 価格は赤太字で目立たせる
★ アイコン + 色分けで見やすさ向上

【コンテンツ構造を多様化してください】
{structure_guidance}

{product_instruction}

【生成時の重要な指示】

★ 段落の構成：
  - 1段落＝最大2行（3行以上は絶対禁止）
  - 改行<br>を活用して2行以内に収める
  - 1段落は50-80字が目安（最大100字）
  - 段落と段落の間は適度に余白を入れる

★ 1見出し内の文字数（厳密チェック）：
  - H3直後のテキスト：必ず150字以内
  - 150字を超えそうなら、H4で細分化するか、内容を削減
  - 生成後に文字数チェック：超過していたら該当セクションを削除

★ 参考記事1097のシンプルさを実現：
  - 短い文を意識
  - 詰まった印象を避ける
  - 改行で視覚的に区切る
  - 1段落1メッセージ

★ 参考リンク・エビデンス：
  - 必ず記事最下部に「参考リンク・エビデンス」セクションを追加
  - 3～5個のURL・参考資料を含める
  - 公式サイト、参考記事、論文など信頼できる出典を選ぶ

【装飾の使い分けルール】
- 太字強調：<strong>キーワード</strong>
- 赤太字：<span style="color: #ff0000; font-weight: bold;">特に重要</span>
- オレンジ下線：<span style="background-color: #ffa500; padding: 2px 4px;">アクセント</span>
- 背景色ボックス：is-style-big_icon_good（緑系）
- グレーボックス：style="background-color: #f5f5f5; border-radius: 8px; padding: 15px;"

【見出し内の文字数ルール（v5.2 - 厳密化）】
★ 絶対ルール：
  - H3（大見出し）の直後のテキスト：150文字以内（厳密）
  - 150字を超える場合：必ずH4で細分化
★ H4の使い分け：
  - 複数のステップ・ポイント → H4で細分化
  - 複数の商品紹介 → H4でブランド名
  - 複数のQ&A → 独自形式（H4は使用しない）

【参考リンク・エビデンスセクション（v5.2 新規追加）】
記事の最下部（まとめセクション直後、関連記事前）に配置：
```html
<div style="background-color: #f5f5f5; border-top: 2px solid #2d7a4c; padding: 16px; margin-top: 20px;">
  <p style="font-weight: bold; margin: 0 0 12px 0; color: #2d7a4c;">📚 参考リンク・エビデンス</p>
  <ul style="margin: 0; padding-left: 20px; font-size: 14px; line-height: 1.8;">
    <li><a href="URL1" target="_blank" style="color: #2d7a4c; text-decoration: none;">公式サイト：説明</a></li>
    <li><a href="URL2" target="_blank" style="color: #2d7a4c; text-decoration: none;">参考記事：説明</a></li>
    <li><a href="URL3" target="_blank" style="color: #2d7a4c; text-decoration: none;">論文・資料：説明</a></li>
  </ul>
</div>
```
★ ポイント：
  - グレー背景（#f5f5f5）
  - 上ボーダー（#2d7a4c）
  - リンクは緑色（#2d7a4c）で統一
  - 各記事に3～5個のURL・エビデンスを含める
  - 新しいタブで開くように target="_blank" を設定

【「この記事で分かること」セクション（v5.2 - コントラスト改善）】
導入段落の直後に以下の形式で配置（コンテンツの一部として機能）：
```html
<div style="background-color: #f0f7f0; border-left: 5px solid #2d7a4c; padding: 16px; margin: 20px 0;">
  <p style="font-weight: bold; margin: 0 0 12px 0; color: #333;">✓ この記事で分かること</p>
  <ul style="margin: 0; padding-left: 20px;">
    <li>ポイント1</li>
    <li>ポイント2</li>
    <li>ポイント3</li>
    <li>ポイント4</li>
  </ul>
</div>
```
★ ポイント：
  - 背景：薄緑（#f0f7f0）
  - 左ボーダー：濃い緑（#2d7a4c）
  - テキスト色：黒（#333）← 緑から変更（見やすく）
  - チェックマーク：✓で視覚的強調
  - リスト：番号なし（シンプル）

【見出し構成の最適化（v5改定）】
★ 見出し（H3）の数：3-5個（最大6個を超えない）
★ パターン例：
  - シンプル記事：見出し3個 + まとめ
  - 標準記事：見出し4個 + まとめ
  - 詳細記事：見出し5個 + まとめ
★ 各H3セクション：150-200文字を厳密に遵守
★ セクション内で150字を超える場合は H4 で細分化

【最終チェックリスト（v5.2 最終シンプル化版）】
□ 文字数：2,000-3,500文字（厳密に遵守）
□ 1見出し内：150文字以内（絶対、超過時はH4で細分化）
□ 1段落：50-80字目安（最大100字）
□ 段落の最大行数：2行（3行以上禁止）
□ 見出し数（H3）：4-5個推奨（最大6個）
□ 「この記事で分かること」：黒テキスト（#333）、コンテンツ統合
□ 参考リンク・エビデンス：最下部に配置（3-5個のURL）
□ Q&A：シンプル版、Aは緑色
□ 表：#2d7a4c（ヘッダー） + グレー/薄緑行
□ 装飾：太字のみ + 緑下線（赤・オレンジなし）
□ 色使い：緑系のみ（3-4色以内）
□ シンプルさ：参考記事1097並み
□ 記事が途中で終わらない（必ずまとめで完結）

出力はHTMLコードのみ。前置きや説明は不要です。
```html
から```の間にHTMLを記述してください。
"""
    
    try:
        response = model.generate_content(prompt)
        html_content = response.text.strip()
        
        # HTMLコード部分を抽出
        html_match = re.search(r'```html\s*(.*?)\s*```', html_content, re.DOTALL)
        if html_match:
            extracted_html = html_match.group(1).strip()
        else:
            extracted_html = html_content
        
        # ★ 文字数を3500以内に削減
        result_html = truncate_html_to_char_limit(extracted_html, target_chars=3500)
        
        return result_html
    except Exception as e:
        print(f"❌ HTML生成エラー: {e}")
        return None


def get_or_create_tags(tag_names, auth):
    """
    タグ名からタグIDを取得、なければ作成
    """
    import requests
    
    tag_ids = []
    for tag_name in tag_names:
        tag_name = tag_name.strip()
        if not tag_name:
            continue
        
        # 既存タグを検索
        search_url = f"{WORDPRESS_URL}/wp-json/wp/v2/tags?search={tag_name}"
        try:
            response = requests.get(search_url, auth=auth, timeout=10)
            if response.status_code == 200:
                tags = response.json()
                if tags:
                    tag_ids.append(tags[0]["id"])
                    continue
        except:
            pass
        
        # タグが見つからない場合は作成
        create_url = f"{WORDPRESS_URL}/wp-json/wp/v2/tags"
        try:
            response = requests.post(create_url, json={"name": tag_name}, auth=auth, timeout=10)
            if response.status_code == 201:
                tag_ids.append(response.json()["id"])
        except:
            pass
    
    return tag_ids


def post_to_wordpress(title, content, category="CBD", tags="CBD"):
    """
    WordPressに記事を投稿（下書き）
    """
    url = f"{WORDPRESS_URL}/wp-json/wp/v2/posts"
    
    auth = (WORDPRESS_USERNAME, WORDPRESS_PASSWORD)
    
    # タグ名からタグIDに変換
    tag_names = [t.strip() for t in tags.split(",")]
    tag_ids = get_or_create_tags(tag_names, auth)
    
    # カテゴリー名からカテゴリーIDに変換
    category_id = get_wordpress_category_id(category)
    
    payload = {
        "title": title,
        "content": content,
        "status": "draft",
        "categories": [category_id],
        "tags": tag_ids,
    }
    
    try:
        response = requests.post(url, json=payload, auth=auth, timeout=60)
        if response.status_code == 201:
            data = response.json()
            return data["id"], data["link"]
        else:
            print(f"❌ WordPress投稿エラー: {response.status_code} - {response.text}")
            return None, None
    except Exception as e:
        print(f"❌ WordPress投稿エラー: {e}")
        return None, None


def update_article_theme_sheet(row_index, template_id, title_used):
    """
    Article_Theme シートにテンプレートIDとタイトルを反映
    """
    try:
        # テンプレート列（J列）とタイトル列（C列）を更新
        write_spreadsheet(
            ARTICLE_SPREADSHEET_ID,
            f"{ARTICLE_SHEET_NAME}!C{row_index}",
            [[title_used]]
        )
        
        template_name = TEMPLATES.get(template_id, {}).get("name", "")
        write_spreadsheet(
            ARTICLE_SPREADSHEET_ID,
            f"{ARTICLE_SHEET_NAME}!J{row_index}",
            [[template_name]]
        )
        
        return True
    except Exception as e:
        print(f"⚠️ シート更新エラー: {e}")
        return False


def generate_articles_from_sheet():
    """
    Article_Theme シートから記事テーマを読込、記事を生成
    """
    print("📝 スプレッドシート『Article_Theme』から記事テーマを読み込み中...\n")
    
    try:
        # P列（選択されたタイトル）まで読み込む
        sheet_data = read_spreadsheet(ARTICLE_SPREADSHEET_ID, f"{ARTICLE_SHEET_NAME}!A:P")
    except Exception as e:
        print(f"❌ シート読込エラー: {e}")
        return
    
    if not sheet_data or len(sheet_data) < 2:
        print("⚠️ スプレッドシートにデータが見つかりません")
        return
    
    # ヘッダーをスキップ
    article_count = 0
    for row_idx, row in enumerate(sheet_data[1:], start=2):
        if len(row) < 9:
            continue
        
        timestamp = row[0] if len(row) > 0 else ""
        status = row[1] if len(row) > 1 else ""
        theme = row[2] if len(row) > 2 else ""
        template_str = row[3] if len(row) > 3 else ""
        target = row[4] if len(row) > 4 else ""
        tags_raw = row[5] if len(row) > 5 else ""
        description = row[6] if len(row) > 6 else ""
        slug = row[7] if len(row) > 7 else ""
        affiliate = row[8] if len(row) > 8 else ""
        
        # ユーザー選択タイトルを取得（P列、インデックス15）
        selected_title_from_user = row[15] if len(row) > 15 else ""
        
        # ステータスが「生成待ち」または「新規」のもののみ処理
        if status not in ["新規", "生成待ち"]:
            continue
        
        if not theme or not template_str:
            print(f"⚠️ 行{row_idx}: テーマまたはテンプレートが未入力")
            continue
        
        # テンプレートIDを取得
        template_id = None
        for tid, tinfo in TEMPLATES.items():
            if tinfo["name"] == template_str:
                template_id = tid
                break
        
        if not template_id:
            print(f"⚠️ 行{row_idx}: テンプレート '{template_str}' が見つかりません")
            continue
        
        print(f"📝 HTML形式で記事生成中: {target} / {template_str}\n")
        
        # ステップ1：タイトルを決定（ユーザー選択 or 自動生成）
        if selected_title_from_user:
            print("   📋 ユーザーが選択したタイトルを使用します")
            selected_title = selected_title_from_user
            print(f"      ✓ タイトル: {selected_title}")
        else:
            # ユーザー選択がない場合は、自動生成
            print("   📋 タイトル候補を生成中...")
            title_options = generate_title_variations(theme, template_id)
            print(f"      ✓ タイトル候補を生成しました（{len(title_options)}案）")
            print(f"      推奨タイトル: {title_options[0]}")
            
            selected_title = title_options[0]  # 最初のタイトルを採用
        
        # ステップ2：メタデータを生成
        print(f"   📋 メタデータを生成中...")
        metadata = generate_metadata(selected_title, theme, template_id, tags_raw)
        
        # テンプレートからカテゴリーを取得
        template_category = TEMPLATES.get(template_id, {}).get("category", "CBDブランド")
        metadata["category"] = template_category
        print(f"      ✓ メタデータを生成しました（カテゴリー: {template_category}）")
        
        # 画像提案を表示
        if metadata.get("image_suggestions"):
            print(f"   📸 推奨画像:")
            for img in metadata.get("image_suggestions", []):
                print(f"      • {img.get('position', '')}: {img.get('description', '')}")
        
        # ステップ3：SEOフレンドリーなスラッグを生成
        print(f"   📋 SEOスラッグを生成中...")
        seo_slug = generate_seo_slug(selected_title, theme)
        print(f"      ✓ スラッグ: {seo_slug}")
        
        # ステップ4：HTML記事を生成
        print(f"   📋 HTML記事を生成中...")
        html_content = generate_article_html_improved(
            theme, target, template_id, tags_raw, selected_title
        )
        
        if not html_content:
            print(f"❌ 記事生成に失敗しました")
            continue
        
        print(f"      ✓ HTML記事を生成しました（{len(html_content)}文字）")
        
        # ステップ4.5：関連記事を自動推奨
        print(f"   📋 関連記事を自動推奨中...")
        try:
            # Article_List から既存記事を取得
            all_articles = read_spreadsheet(ARTICLE_SPREADSHEET_ID, f"{ARTICLE_LIST_SHEET}!A:E")
            if all_articles and len(all_articles) > 1:
                related_articles = find_related_articles_by_ai(
                    selected_title, 
                    tags_raw if tags_raw else theme,
                    all_articles[1:]  # ヘッダーをスキップ
                )
                
                if related_articles:
                    print(f"      ✓ {len(related_articles)}件の関連記事を推奨しました")
                    # HTMLに関連記事セクションを注入
                    related_section = generate_related_articles_section(related_articles)
                    html_content = html_content.rstrip() + "\n" + related_section
                else:
                    print(f"      ℹ️ 関連記事は見つかりませんでした")
            else:
                print(f"      ℹ️ 既存記事データが不足しています")
        except Exception as e:
            print(f"      ⚠️ 関連記事推奨エラー: {e}")
        
        # ステップ5：WordPressに投稿
        print(f"   📋 WordPressに下書き投稿中...")
        post_id, post_url = post_to_wordpress(
            selected_title, html_content, 
            category=metadata.get("category", "CBD"),
            tags=metadata.get("tags", "CBD")
        )
        
        if post_id:
            print(f"✅ WordPressに投稿しました: {post_url}")
            print(f"   投稿ID: {post_id}")
            
            # ステップ6：Article_Theme シートを更新
            update_article_theme_sheet(row_idx, template_id, selected_title)
            
            # ステップ7：LINE通知
            line_message = f"""✅ 新記事が生成されました！

【タイトル】
{selected_title}

【ターゲット】
{target}

【テンプレート】
{template_str}

【メタディスクリプション】
{metadata.get('description', '')}

【スラッグ】
{seo_slug}

【WordPress下書きURL】
{post_url}

👉 WordPress で確認・編集してください
"""
            try:
                send_line_message(line_message)
                print(f"✅ LINE通知を送信しました")
            except Exception as e:
                print(f"⚠️ LINE通知エラー: {e}")
            
            article_count += 1
        else:
            print(f"❌ WordPress投稿に失敗しました")
        
        print()
    
    print(f"\n✅ {article_count}件の記事を生成しました")


if __name__ == '__main__':
    generate_articles_from_sheet()
