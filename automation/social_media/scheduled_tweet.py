#!/usr/bin/env python3
"""
定期実行スクリプト（毎日決まったタイミング）
ツイート文案を自動生成してLINE通知・スプレッドシート記録
"""

import os
import sys
from datetime import datetime
from pathlib import Path
from dotenv import load_dotenv

# 親ディレクトリをパスに追加
sys.path.insert(0, str(Path(__file__).parent.parent))

from social_media.article_detector import check_wordpress_rss, add_to_approval_queue
from social_media.tweet_generator_v3 import generate_tweet_by_type, select_content_type, get_persona_and_engagement
from social_media.news_tweet_generator import generate_news_tweet_with_ai
from social_media.line_notify import send_line_message
from social_media.news_collector import collect_cbd_news, summarize_news_articles
from social_media.news_summarizer import summarize_news
from social_media.tweet_formatter import format_tweet
from social_media.buzz_analyzer import analyze_buzz_tweets, compare_accounts
from google_services.google_sheets import read_spreadsheet, write_spreadsheet

# .envファイルを読み込む
load_dotenv()

WORDPRESS_URL = os.getenv('WORDPRESS_URL', 'https://cbd-no-hito.com')
APPROVAL_SPREADSHEET_ID = os.getenv('APPROVAL_SPREADSHEET_ID', '')


def summarize_article_trends():
    """
    記事動向を要約（WordPress記事 + CBD・大麻関連ニュース）
    
    Returns:
        記事動向要約テキスト
    """
    try:
        summaries = []
        
        # 1. WordPress記事を取得
        wordpress_articles = check_wordpress_rss()
        if wordpress_articles:
            wp_summary = f"📝 WordPress記事（{len(wordpress_articles)}件）：\n\n"
            for i, article in enumerate(wordpress_articles[:3], 1):  # 最大3件
                title = article['title']
                url = article.get('url', '')
                wp_summary += f"{i}. {title}\n"
                if url:
                    wp_summary += f"   {url}\n"
                wp_summary += "\n"
            summaries.append(wp_summary)
        
        # 2. CBD・大麻関連ニュースを取得（直近1か月）
        print("📰 CBD・大麻関連ニュースを収集しています（直近1か月）...")
        cbd_news = collect_cbd_news(days=30, max_articles=10)
        
        if cbd_news:
            news_summary = f"📰 CBD・大麻関連ニュース（{len(cbd_news)}件）：\n\n"
            for i, news in enumerate(cbd_news[:3], 1):  # 最大3件
                title = news['title']
                url = news.get('url', '')
                summary_text = news.get('summary', '')
                
                # AI要約（可能な場合）
                if summary_text:
                    summarized = summarize_news(f"{title} {summary_text}", max_length=100, use_ai='auto')
                    if summarized and summarized != summary_text:
                        news_summary += f"{i}. {title}\n   {summarized}\n"
                    else:
                        news_summary += f"{i}. {title}\n"
                else:
                    news_summary += f"{i}. {title}\n"
                
                if url:
                    news_summary += f"   {url}\n"
                news_summary += "\n"
            summaries.append(news_summary)
        
        if not summaries:
            return "📰 記事動向：\n新着記事・ニュースはありません"
        
        return "\n---\n".join(summaries)
    
    except Exception as e:
        print(f"⚠️ 記事動向要約の取得に失敗: {e}")
        import traceback
        traceback.print_exc()
        return "📰 記事動向：\n取得に失敗しました"


def generate_daily_tweet():
    """
    毎日のツイート文案を自動生成（新しい方向性に合わせた改善版）
    
    Returns:
        (tweet_text, content_type, persona, engagement) のタプル
    """
    try:
        # コンテンツタイプを選択（投稿比率に基づく）
        content_type = select_content_type()
        
        # WordPress RSSフィードから新着記事を取得
        new_articles = check_wordpress_rss()
        
        # CBDニュースを取得
        cbd_news = collect_cbd_news(days=30, max_articles=5)
        
        tweet_text = None
        article_title = None
        article_url = None
        news_title = None
        news_url = None
        
        if new_articles:
            # 記事がある場合
            latest_article = new_articles[0]
            article_title = latest_article['title']
            article_url = latest_article.get('url')
            article_content = latest_article.get('summary', '')
            
            tweet_text = generate_tweet_by_type(
                content_type=content_type,
                article_title=article_title,
                article_content=article_content,
                article_url=article_url
            )
        elif cbd_news:
            # ニュースがある場合
            latest_news = cbd_news[0]
            news_title = latest_news['title']
            news_url = latest_news.get('url')
            news_content = latest_news.get('summary', '')
            
            tweet_text = generate_tweet_by_type(
                content_type=content_type,
                news_title=news_title,
                news_content=news_content,
                news_url=news_url
            )
        else:
            # コンテンツがない場合、フォールバック
            tweet_text = "【CBD情報】幅広く正確なCBDや大麻情報をお届けします。"
            content_type = 'other'
        
        # ペルソナと引き付け期待を取得
        persona, engagement = get_persona_and_engagement(content_type)
        
        return (tweet_text, content_type, persona, engagement, article_title or news_title, article_url or news_url)
    
    except Exception as e:
        print(f"⚠️ ツイート文案生成に失敗: {e}")
        import traceback
        traceback.print_exc()
        return ("【CBD情報】幅広く正確なCBDや大麻情報をお届けします。", 'other', '幅広い層', '最新情報の価値で興味を持ち、サイトで詳しい情報を確認したいと感じてもらう', None, None)


def send_daily_tweet_preview():
    """
    毎日のツイート案をLINE通知・スプレッドシート記録
    """
    try:
        print(f"📝 本日のツイート案を生成しています... ({datetime.now().strftime('%Y-%m-%d %H:%M')})")
        
        # ツイート文案を自動生成（新しい方向性に合わせて）
        result_tuple = generate_daily_tweet()
        if isinstance(result_tuple, tuple) and len(result_tuple) >= 4:
            tweet_text, content_type, persona, engagement = result_tuple[:4]
            article_title = result_tuple[4] if len(result_tuple) > 4 else None
            article_url = result_tuple[5] if len(result_tuple) > 5 else None
        else:
            # フォールバック（旧形式）
            tweet_text = result_tuple if isinstance(result_tuple, str) else "【CBD情報】幅広く正確なCBDや大麻情報をお届けします。"
            content_type = 'other'
            persona = '幅広い層'
            engagement = '最新情報の価値で興味を持ち、サイトで詳しい情報を確認したいと感じてもらう'
            article_title = f"本日のツイート案 ({datetime.now().strftime('%Y-%m-%d')})"
            article_url = None
        
        # 記事動向を要約
        article_summary = summarize_article_trends()
        
        # LINE通知でプレビュー送信
        message = f"""📝 本日のツイート案

{tweet_text}

---
{article_summary}

---
文字数: {len(tweet_text)}/280
コンテンツタイプ: {content_type}
ペルソナ: {persona}

承認待ちリスト: https://docs.google.com/spreadsheets/d/{APPROVAL_SPREADSHEET_ID}
"""
        
        print("📱 LINEにプレビューを送信しています...")
        send_line_message(message)
        
        # スプレッドシートに「下書き」として記録（新しい構造に対応）
        print("📊 スプレッドシートに下書きとして記録しています...")
        from social_media.article_detector_v2 import add_to_approval_queue_v2
        result = add_to_approval_queue_v2(
            article_title or f"本日のツイート案 ({datetime.now().strftime('%Y-%m-%d')})",
            tweet_text,
            article_url,
            'scheduled',
            content_type,
            persona,
            engagement
        )
        
        if result:
            print("✅ 処理完了")
            print(f"   ツイート文案: {tweet_text[:50]}...")
        else:
            print("⚠️ スプレッドシートへの記録に失敗しました")
    
    except Exception as e:
        print(f"❌ エラーが発生しました: {e}")
        import traceback
        traceback.print_exc()


def main():
    """メイン関数"""
    send_daily_tweet_preview()


if __name__ == '__main__':
    main()
