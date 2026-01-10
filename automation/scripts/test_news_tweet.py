#!/usr/bin/env python3
"""
CBDニュースのツイート生成テストスクリプト
"""

import os
import sys
from pathlib import Path
from dotenv import load_dotenv

# 親ディレクトリをパスに追加
sys.path.insert(0, str(Path(__file__).parent.parent))

from social_media.news_collector import collect_cbd_news
from social_media.news_tweet_generator import generate_news_tweet_with_ai
from social_media.article_detector import add_to_approval_queue
from social_media.line_notify import send_line_message

# .envファイルを読み込む
load_dotenv()

def test_news_tweet():
    """CBDニュースからのツイート生成テスト"""
    print("📰 CBDニュースからのツイート生成テスト\n")
    print("=" * 60)
    
    # 直近1か月のニュースを収集
    print("📝 CBD・大麻関連ニュースを収集中（直近1か月）...")
    cbd_news = collect_cbd_news(days=30, max_articles=5)
    
    if not cbd_news:
        print("⚠️ ニュースが見つかりませんでした")
        return
    
    # 最新のニュースを選択
    latest_news = cbd_news[0]
    print(f"\n📝 ニュース: {latest_news['title']}")
    print(f"   URL: {latest_news.get('url', 'なし')}")
    print(f"   要約: {latest_news.get('summary', 'なし')[:100]}...")
    
    # ツイート文案を生成
    print("\n📝 ツイート文案を生成中（AI活用）...")
    tweet_text = generate_news_tweet_with_ai(
        latest_news['title'],
        latest_news.get('summary', ''),
        latest_news.get('url', '')
    )
    
    if not tweet_text:
        print("⚠️ ツイート文案の生成に失敗しました")
        return
    
    print("\n" + "=" * 60)
    print("📝 生成されたツイート文案:")
    print("=" * 60)
    print(tweet_text)
    print("=" * 60)
    print(f"\n文字数: {len(tweet_text)}/280")
    
    # LINE通知でプレビュー送信
    print("\n📱 LINEにプレビューを送信中...")
    message = f"""📰 CBDニュースからのツイート案（テスト）

{tweet_text}

---
文字数: {len(tweet_text)}/280
"""
    send_line_message(message)
    print("✅ LINE通知を送信しました")
    
    # スプレッドシートに追加
    print("\n📊 スプレッドシートに追加中...")
    result = add_to_approval_queue(
        latest_news['title'],
        tweet_text,
        latest_news.get('url', ''),
        'news'
    )
    
    if result:
        print("✅ スプレッドシートに追加しました")
    else:
        print("⚠️ スプレッドシートへの追加をスキップしました（重複の可能性）")
    
    print("\n✅ テスト完了")


if __name__ == '__main__':
    test_news_tweet()
