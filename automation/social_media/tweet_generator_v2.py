#!/usr/bin/env python3
"""
ツイート生成スクリプト（バズる要素を考慮した改善版）
"""

import os
import sys
import re
from datetime import datetime
from pathlib import Path
from dotenv import load_dotenv

# 親ディレクトリをパスに追加
sys.path.insert(0, str(Path(__file__).parent.parent))

from social_media.article_detector import check_wordpress_rss

# .envファイルを読み込む
load_dotenv()


def extract_key_info(text):
    """
    テキストから重要な情報を抽出
    
    Args:
        text: 抽出対象のテキスト
    
    Returns:
        抽出された情報（日付、数字、人物名など）
    """
    info = {
        'dates': [],
        'numbers': [],
        'names': [],
        'keywords': []
    }
    
    # 日付を抽出（YYYY-MM-DD、MM/DD、12/18など）
    date_patterns = [
        r'\d{4}[-/]\d{1,2}[-/]\d{1,2}',  # 2024-12-18, 2024/12/18
        r'\d{1,2}[-/]\d{1,2}',  # 12/18, 12-18
    ]
    for pattern in date_patterns:
        dates = re.findall(pattern, text)
        info['dates'].extend(dates)
    
    # 数字を抽出（パーセント、金額など）
    number_patterns = [
        r'\d+%',  # パーセント
        r'\d+億', r'\d+万',  # 金額（億、万）
        r'\d+件', r'\d+人',  # 件数、人数
    ]
    for pattern in number_patterns:
        numbers = re.findall(pattern, text)
        info['numbers'].extend(numbers)
    
    # 固有名詞を抽出（簡単な方法：大文字で始まる単語）
    # より高度な方法：自然言語処理ライブラリを使用
    
    return info


def generate_buzz_tweet(article_title, article_summary=None, article_url=None, source_text=None):
    """
    バズる要素を考慮したツイート文案を生成
    
    Args:
        article_title: 記事タイトル
        article_summary: 記事要約
        article_url: 記事URL
        source_text: 元のテキスト（ニュース本文など）
    
    Returns:
        ツイート文案（280文字以内）
    """
    # 情報を抽出
    full_text = f"{article_title} {article_summary or ''} {source_text or ''}"
    key_info = extract_key_info(full_text)
    
    # ツイート文案を生成
    tweet_parts = []
    
    # パート1: 具体的な出来事・結論
    if key_info['dates']:
        date_str = key_info['dates'][0]
        conclusion = f"{date_str}、{article_title}"
    else:
        conclusion = article_title
    
    # 280文字以内に収める
    max_length = 250  # URLと余裕を考慮
    if article_url:
        max_length -= 23  # URLの長さ
    
    if len(conclusion) > max_length - 50:  # 次のパートの余裕を考慮
        conclusion = conclusion[:max_length - 53] + "..."
    
    tweet_parts.append(conclusion)
    
    # パート2: 影響・意義
    if article_summary:
        # 要約から重要な部分を抽出
        impact = article_summary[:100]  # 簡潔に
        
        # 数字を含む場合は優先
        if key_info['numbers']:
            impact = f"最大の変化は、{key_info['numbers'][0]}に関わる変化です"
        
        remaining_length = max_length - len(tweet_parts[0]) - 10
        if len(impact) > remaining_length:
            impact = impact[:remaining_length - 3] + "..."
        
        if impact:
            tweet_parts.append(impact)
    
    # パート3: 価値の提示（余裕があれば）
    if article_url:
        value_statement = "歴史的転換点です"  # デフォルトの価値提示
        remaining_length = max_length - sum(len(p) for p in tweet_parts) - 10
        if remaining_length > 20:
            tweet_parts.append(value_statement)
    
    # ツイート文案を組み立て
    tweet_text = "\n\n".join(tweet_parts)
    
    # URLを追加
    if article_url:
        tweet_text += f"\n\n{article_url}"
    
    # ハッシュタグを追加（余裕があれば）
    hashtag = "#CBD"
    if len(tweet_text) + len(hashtag) + 1 <= 280:
        tweet_text += f"\n{hashtag}"
    
    # 最終チェック：280文字以内
    if len(tweet_text) > 280:
        # URLとハッシュタグ以外を短縮
        url_part = article_url if article_url else ""
        hashtag_part = f"\n{hashtag}" if hashtag else ""
        main_text = tweet_text.replace(url_part, "").replace(hashtag_part, "").strip()
        max_main_length = 280 - len(url_part) - len(hashtag_part) - 5
        if len(main_text) > max_main_length:
            main_text = main_text[:max_main_length - 3] + "..."
        tweet_text = f"{main_text}\n\n{url_part}{hashtag_part}" if url_part else f"{main_text}{hashtag_part}"
    
    return tweet_text


def generate_news_tweet(news_title, news_content, news_url=None):
    """
    ニュース型ツイートを生成
    
    Args:
        news_title: ニュースタイトル
        news_content: ニュース本文
        news_url: ニュースURL
    
    Returns:
        ツイート文案
    """
    # 情報を抽出
    key_info = extract_key_info(f"{news_title} {news_content}")
    
    tweet_parts = []
    
    # パート1: 具体的な出来事
    if key_info['dates']:
        date_str = key_info['dates'][0]
        event = f"{date_str}、{news_title}"
    else:
        event = news_title
    
    tweet_parts.append(event)
    
    # パート2: 最大の変化・影響
    if key_info['numbers'] or "最大" in news_content or "変化" in news_content:
        impact_line = None
        if key_info['numbers']:
            impact_line = f"最大の変化は、{key_info['numbers'][0]}に関わる変化です"
        elif "最大" in news_content:
            # 「最大」を含む文を抽出
            impact_lines = [line for line in news_content.split('\n') if "最大" in line]
            if impact_lines:
                impact_line = impact_lines[0][:80]
        
        if impact_line:
            tweet_parts.append(impact_line)
    
    # パート3: 価値の提示
    if any(keyword in news_content for keyword in ["歴史的", "転換点", "重要", "画期的"]):
        value_line = "歴史的転換点です"
        tweet_parts.append(value_line)
    
    # ツイート文案を組み立て
    tweet_text = "\n\n".join(tweet_parts)
    
    # URLを追加
    if news_url:
        if len(tweet_text) + len(news_url) + 2 <= 280:
            tweet_text += f"\n\n{news_url}"
    
    # ハッシュタグを追加
    hashtag = "#CBD"
    if len(tweet_text) + len(hashtag) + 1 <= 280:
        tweet_text += f"\n{hashtag}"
    
    # 280文字以内に収める
    if len(tweet_text) > 280:
        # URLとハッシュタグ以外を短縮
        url_part = news_url if news_url else ""
        hashtag_part = f"\n{hashtag}" if hashtag else ""
        main_text = tweet_text.replace(url_part, "").replace(hashtag_part, "").strip()
        max_main_length = 280 - len(url_part) - len(hashtag_part) - 5
        if len(main_text) > max_main_length:
            main_text = main_text[:max_main_length - 3] + "..."
        tweet_text = f"{main_text}\n\n{url_part}{hashtag_part}" if url_part else f"{main_text}{hashtag_part}"
    
    return tweet_text


def main():
    """メイン関数（テスト用）"""
    if len(sys.argv) < 2:
        print("使用方法:")
        print("  python tweet_generator_v2.py test")
        print("  python tweet_generator_v2.py news <ニュースタイトル> <ニュース本文> [URL]")
        sys.exit(1)
    
    command = sys.argv[1]
    
    if command == 'test':
        # テスト実行
        test_title = "米トランプ大統領が12/18、大麻を「スケジュールIII」へ再分類させる大統領令に署名"
        test_summary = "最大の変化は、企業を苦しめていた「280E条項(重税)」の撤廃です。浮いた資金が研究に回り、より安全で高品質なCBDが世界へ普及する"
        
        tweet = generate_buzz_tweet(
            test_title,
            test_summary,
            "https://example.com/article"
        )
        
        print("📝 生成されたツイート文案:")
        print("=" * 60)
        print(tweet)
        print("=" * 60)
        print(f"文字数: {len(tweet)}/280")
    
    elif command == 'news':
        if len(sys.argv) < 4:
            print("エラー: ニュースタイトルと本文が必要です")
            sys.exit(1)
        
        news_title = sys.argv[2]
        news_content = sys.argv[3]
        news_url = sys.argv[4] if len(sys.argv) > 4 else None
        
        tweet = generate_news_tweet(news_title, news_content, news_url)
        
        print("📝 生成されたツイート文案:")
        print("=" * 60)
        print(tweet)
        print("=" * 60)
        print(f"文字数: {len(tweet)}/280")
    
    else:
        print(f"不明なコマンド: {command}")
        sys.exit(1)


if __name__ == '__main__':
    main()
