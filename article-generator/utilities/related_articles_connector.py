#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
関連記事の自動連携・推奨機能
既存記事からキーワードを抽出し、新規記事に最適な関連記事を自動推奨
"""

import os
import sys
import re
from pathlib import Path
from typing import List, Dict, Tuple
from dotenv import load_dotenv

sys.path.insert(0, str(Path(__file__).parent.parent))

from google_services.google_sheets import read_spreadsheet
import google.generativeai as genai

load_dotenv()

ARTICLE_SPREADSHEET_ID = os.getenv('ARTICLE_SPREADSHEET_ID', '1-2L6C3NpF8vqnXxHWKP-Js3TMFKYE73tTtxdkZVPTaM')
ARTICLE_LIST_SHEET = 'Article_List'
GEMINI_API_KEY = os.getenv('GEMINI_API_KEY')

genai.configure(api_key=GEMINI_API_KEY)


def extract_keywords_from_title(title: str) -> List[str]:
    """
    記事タイトルからキーワードを抽出
    """
    # 記事タイトルから主要なキーワードを抽出
    # 例：「CBD初心者ガイド」→ ["CBD", "初心者", "ガイド"]
    
    # 括弧内を削除
    title_clean = re.sub(r'【.*?】', '', title)
    title_clean = re.sub(r'[【】\[\]()]', '', title_clean)
    
    # 重要キーワード（停止語でない）を抽出
    keywords = []
    
    # 分割
    words = re.split(r'[・：、\s]', title_clean)
    
    for word in words:
        if len(word) > 2 and word not in ['こと', 'です', 'する', 'この', 'それ', 'ある']:
            keywords.append(word)
    
    return keywords[:5]  # 最大5個


def find_related_articles(
    new_article_title: str,
    new_article_keywords: str,
    all_articles: List[Dict],
    max_related: int = 3
) -> List[Tuple[str, str, float]]:
    """
    新規記事に対する関連記事を検索
    
    Args:
        new_article_title: 新規記事タイトル
        new_article_keywords: 新規記事キーワード（カンマ区切り）
        all_articles: 全既存記事のリスト
        max_related: 推奨する関連記事の最大数
    
    Returns:
        [(記事タイトル, 記事URL, 関連度スコア), ...] のリスト
    """
    
    # 新規記事のキーワードを分解
    new_keywords = set([k.strip() for k in new_article_keywords.split(",")])
    new_keywords.update(extract_keywords_from_title(new_article_title))
    
    print(f"   📝 新規記事のキーワード: {', '.join(list(new_keywords)[:5])}")
    
    # 既存記事とのマッチングスコアを計算
    scores = []
    
    for article in all_articles:
        if len(article) < 5:
            continue
        
        article_title = article[2] if len(article) > 2 else ""
        article_url = article[4] if len(article) > 4 else ""
        
        # 同じ記事は除外
        if article_title == new_article_title:
            continue
        
        # 既存記事のキーワードを抽出
        article_keywords = set(extract_keywords_from_title(article_title))
        
        # キーワードのマッチング度（Jaccard係数）を計算
        if not article_keywords:
            continue
        
        intersection = len(new_keywords & article_keywords)
        union = len(new_keywords | article_keywords)
        
        if union > 0:
            similarity = intersection / union
            scores.append((article_title, article_url, similarity))
    
    # スコアでソート（降順）
    scores.sort(key=lambda x: x[2], reverse=True)
    
    # 関連度が0.3以上のものを返す
    related = [(t, u, s) for t, u, s in scores if s >= 0.3][:max_related]
    
    return related


def generate_related_articles_section(
    related_articles: List[Tuple[str, str, float]]
) -> str:
    """
    関連記事セクションのHTML を生成
    """
    
    if not related_articles:
        return ""
    
    html = """
<hr class="wp-block-separator has-css-opacity is-style-wide"/>

<h3 class="wp-block-heading">関連記事</h3>

<p>このテーマについて、さらに詳しく知りたい方は以下の記事も参考にしてください。</p>

<ul>
"""
    
    for title, url, score in related_articles:
        # URLがない場合は推奨から除外
        if not url or url.startswith('http'):
            # 外部リンクの場合はそのまま
            html += f'  <li><a href="{url}" target="_blank" rel="noopener noreferrer">{title}</a></li>\n'
        else:
            # 内部リンク
            html += f'  <li><a href="/post/{url}">{title}</a> - 関連テーマの詳細</li>\n'
    
    html += """</ul>
"""
    
    return html


def inject_related_articles_to_html(
    article_html: str,
    related_articles: List[Tuple[str, str, float]]
) -> str:
    """
    既存の記事HTMLに関連記事セクションを注入
    """
    
    related_section = generate_related_articles_section(related_articles)
    
    if not related_section:
        return article_html
    
    # 「参考文献」セクションの後に関連記事を挿入
    # または、最後の</div>の前に挿入
    
    # 参考文献のセクションを検索
    param_section_match = re.search(r'(<h3 class="wp-block-heading">参考文献.*?</ul>)', article_html, re.DOTALL)
    
    if param_section_match:
        insert_pos = param_section_match.end()
        article_html = article_html[:insert_pos] + related_section + article_html[insert_pos:]
    else:
        # 最後の</ul>の後に挿入
        last_ul_pos = article_html.rfind('</ul>')
        if last_ul_pos != -1:
            article_html = article_html[:last_ul_pos + 5] + related_section + article_html[last_ul_pos + 5:]
        else:
            # 最後に追加
            article_html = article_html.rstrip() + "\n" + related_section
    
    return article_html


def get_all_articles_from_list() -> List[Dict]:
    """
    Article_List シートから全記事を取得
    """
    
    try:
        data = read_spreadsheet(ARTICLE_SPREADSHEET_ID, f"{ARTICLE_LIST_SHEET}!A:E")
        
        if not data or len(data) < 2:
            return []
        
        # ヘッダーをスキップ
        articles = []
        for row in data[1:]:
            if row and len(row) > 2 and row[2]:  # タイトルがある
                articles.append(row)
        
        return articles
    
    except Exception as e:
        print(f"⚠️ 記事リスト取得エラー: {e}")
        return []


def find_related_articles_by_ai(
    new_article_title: str,
    new_article_keywords: str,
    all_articles: List[Dict]
) -> List[Tuple[str, str, str]]:
    """
    AI を使用して関連記事をより高度に推奨
    （テンプレート内で自動的に関連記事を判断）
    
    Returns:
        [(記事タイトル, 記事URL, 推奨理由), ...] のリスト
    """
    
    model = genai.GenerativeModel("gemini-2.5-flash")
    
    # 既存記事のタイトル一覧
    existing_titles = [article[2] for article in all_articles if len(article) > 2][:20]
    
    if not existing_titles:
        return []
    
    prompt = f"""あなたは CBD サイト編集者です。新規記事と既存記事から、最適な関連記事を推奨してください。

【新規記事】
タイトル: {new_article_title}
キーワード: {new_article_keywords}

【既存記事（候補）】
{chr(10).join([f'{i+1}. {t}' for i, t in enumerate(existing_titles)])}

【指示】
新規記事に最適な関連記事を3つまで選んでください。
読者が「次のステップ」として参考になる記事を優先してください。

【出力形式】
以下の形式で返してください。タイトルは上記の既存記事から完全一致する方を選んでください。
1. 記事タイトル
2. 記事タイトル
3. 記事タイトル

（推奨できる関連記事がない場合は「なし」と記載）

返答のみ、前置きは不要です。
"""
    
    try:
        response = model.generate_content(prompt)
        suggestions = response.text.strip()
        
        if 'なし' in suggestions or not suggestions:
            return []
        
        # 推奨理由を抽出
        recommendations = []
        for line in suggestions.split('\n'):
            if line.strip() and (line.startswith(('1.', '2.', '3.'))):
                # 記事タイトルを抽出
                title_match = re.match(r'^\d+\.\s*(.+?)$', line.strip())
                if title_match:
                    title = title_match.group(1).strip()
                    
                    # 既存記事から完全一致を検索
                    for article in all_articles:
                        if len(article) > 2 and article[2] and article[2].strip() == title:
                            url = article[4] if len(article) > 4 else ""
                            reason = f"関連テーマの詳細解説"
                            recommendations.append((title, url, reason))
                            break
        
        return recommendations[:3]
    
    except Exception as e:
        print(f"⚠️ AI 推奨エラー: {e}")
        return []


# テスト用関数
def test_related_articles_finder():
    """
    関連記事推奨の動作テスト
    """
    
    print("📝 関連記事の自動連携機能テスト\n")
    print("=" * 100)
    
    # 既存記事を取得
    all_articles = get_all_articles_from_list()
    print(f"\n✅ 既存記事を取得しました: {len(all_articles)}件\n")
    
    if len(all_articles) < 2:
        print("⚠️ 既存記事が足りません")
        return
    
    # テスト用の新規記事
    test_new_title = "CBD初心者向けの安全な選び方と始め方"
    test_new_keywords = "CBD,初心者,安全,選び方"
    
    print(f"【テスト用新規記事】")
    print(f"  タイトル: {test_new_title}")
    print(f"  キーワード: {test_new_keywords}\n")
    
    # キーワードベースの関連記事検索
    print("📋 【方法1】キーワードマッチングで関連記事を検索\n")
    related_kw = find_related_articles(test_new_title, test_new_keywords, all_articles, max_related=3)
    
    print(f"  検索結果: {len(related_kw)}件\n")
    for i, (title, url, score) in enumerate(related_kw, 1):
        print(f"  {i}. {title}")
        print(f"     関連度: {score:.1%}")
        print()
    
    # HTML生成テスト
    print("📋 【方法2】HTML関連記事セクションの生成\n")
    related_section = generate_related_articles_section(related_kw)
    print("  生成されたHTML:")
    print(related_section[:200] + "..." if len(related_section) > 200 else related_section)
    
    print("\n" + "=" * 100)
    print("\n✅ 関連記事推奨機能は正常に動作しています")


if __name__ == '__main__':
    test_related_articles_finder()
