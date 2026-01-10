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
from social_media.tweet_generator_v2 import generate_buzz_tweet
from social_media.news_tweet_generator import generate_news_tweet_with_ai, generate_news_tweet
from social_media.line_notify import send_line_message
from social_media.news_collector import collect_cbd_news, summarize_news_articles
from social_media.news_summarizer import summarize_news
from google_services.google_sheets import read_spreadsheet

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
    毎日のツイート文案を自動生成（バズる要素を考慮した改善版）
    
    Returns:
        ツイート文案
    """
    try:
        # WordPress RSSフィードから新着記事を取得
        new_articles = check_wordpress_rss()
        
        if not new_articles:
            # 新着記事がない場合、一般的なツイート文案を生成
            tweet_text = "CBDに関する最新情報をお届けします 🌿 #CBD"
        else:
            # 最新記事からツイート文案を生成（改善版）
            latest_article = new_articles[0]
            tweet_text = generate_buzz_tweet(
                latest_article['title'],
                latest_article.get('summary'),
                latest_article.get('url'),
                latest_article.get('summary')  # 元のテキストとして使用
            )
        
        return tweet_text
    
    except Exception as e:
        print(f"⚠️ ツイート文案生成に失敗: {e}")
        import traceback
        traceback.print_exc()
        return "CBDに関する最新情報をお届けします 🌿 #CBD"


def send_daily_tweet_preview():
    """
    毎日のツイート案をLINE通知・スプレッドシート記録
    """
    try:
        print(f"📝 本日のツイート案を生成しています... ({datetime.now().strftime('%Y-%m-%d %H:%M')})")
        
        # ツイート文案を自動生成
        tweet_text = generate_daily_tweet()
        
        # 記事動向を要約
        article_summary = summarize_article_trends()
        
        # LINE通知でプレビュー送信
        message = f"""📝 本日のツイート案

{tweet_text}

---
{article_summary}

---
文字数: {len(tweet_text)}/280

承認待ちリスト: https://docs.google.com/spreadsheets/d/{APPROVAL_SPREADSHEET_ID}
"""
        
        print("📱 LINEにプレビューを送信しています...")
        send_line_message(message)
        
        # スプレッドシートに「下書き」として記録
        print("📊 スプレッドシートに下書きとして記録しています...")
        result = add_to_approval_queue(
            f"本日のツイート案 ({datetime.now().strftime('%Y-%m-%d')})",
            tweet_text,
            None,
            'scheduled'
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
