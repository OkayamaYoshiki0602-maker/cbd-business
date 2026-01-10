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

from social_media.article_detector import check_wordpress_rss, generate_tweet_text, add_to_approval_queue
from social_media.line_notify import send_line_message
from google_services.google_sheets import read_spreadsheet

# .envファイルを読み込む
load_dotenv()

WORDPRESS_URL = os.getenv('WORDPRESS_URL', 'https://cbd-no-hito.com')
APPROVAL_SPREADSHEET_ID = os.getenv('APPROVAL_SPREADSHEET_ID', '')


def summarize_article_trends():
    """
    記事動向を要約
    
    Returns:
        記事動向要約テキスト
    """
    try:
        # WordPress RSSフィードから新着記事を取得
        new_articles = check_wordpress_rss()
        
        if not new_articles:
            return "📰 記事動向：\n新着記事はありません"
        
        # 記事動向を要約
        summary = f"📰 記事動向（{len(new_articles)}件の新着記事）：\n\n"
        
        for i, article in enumerate(new_articles[:5], 1):  # 最大5件
            title = article['title']
            url = article.get('url', '')
            summary += f"{i}. {title}\n"
            if url:
                summary += f"   {url}\n"
            summary += "\n"
        
        if len(new_articles) > 5:
            summary += f"...他 {len(new_articles) - 5}件\n"
        
        return summary
    
    except Exception as e:
        print(f"⚠️ 記事動向要約の取得に失敗: {e}")
        return "📰 記事動向：\n取得に失敗しました"


def generate_daily_tweet():
    """
    毎日のツイート文案を自動生成
    
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
            # 最新記事からツイート文案を生成
            latest_article = new_articles[0]
            tweet_text = generate_tweet_text(
                latest_article['title'],
                latest_article.get('summary'),
                latest_article['url']
            )
        
        return tweet_text
    
    except Exception as e:
        print(f"⚠️ ツイート文案生成に失敗: {e}")
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
