#!/usr/bin/env python3
"""
記事のツイート生成テストスクリプト
"""

import os
import sys
from pathlib import Path
from dotenv import load_dotenv

# 親ディレクトリをパスに追加
sys.path.insert(0, str(Path(__file__).parent.parent))

from social_media.article_detector import check_wordpress_rss, generate_tweet_text, add_to_approval_queue
from social_media.line_notify import send_line_message

# .envファイルを読み込む
load_dotenv()

def test_article_tweet():
    """WordPress記事からのツイート生成テスト"""
    print("📰 WordPress記事からのツイート生成テスト\n")
    print("=" * 60)
    
    # WordPress RSSフィードから新着記事を取得
    print("📝 新着記事を取得中...")
    new_articles = check_wordpress_rss()
    
    if not new_articles:
        print("⚠️ 新着記事が見つかりませんでした")
        print("   テスト用に最新の記事を使用します")
        # 最新の記事を取得（last_check_dateなし）
        all_articles = check_wordpress_rss(last_check_date=None)
        if all_articles:
            new_articles = [all_articles[0]]
    
    if not new_articles:
        print("❌ 記事が見つかりませんでした")
        return
    
    # 最新記事からツイート文案を生成
    latest_article = new_articles[0]
    print(f"\n📝 記事: {latest_article['title']}")
    print(f"   URL: {latest_article.get('url', 'なし')}")
    
    print("\n📝 ツイート文案を生成中...")
    tweet_text = generate_tweet_text(
        latest_article['title'],
        latest_article.get('summary'),
        latest_article.get('url')
    )
    
    print("\n" + "=" * 60)
    print("📝 生成されたツイート文案:")
    print("=" * 60)
    print(tweet_text)
    print("=" * 60)
    print(f"\n文字数: {len(tweet_text)}/280")
    
    # LINE通知でプレビュー送信
    print("\n📱 LINEにプレビューを送信中...")
    message = f"""📝 記事からのツイート案（テスト）

{tweet_text}

---
文字数: {len(tweet_text)}/280
"""
    send_line_message(message)
    print("✅ LINE通知を送信しました")
    
    # スプレッドシートに追加
    print("\n📊 スプレッドシートに追加中...")
    result = add_to_approval_queue(
        latest_article['title'],
        tweet_text,
        latest_article.get('url'),
        'wordpress'
    )
    
    if result:
        print("✅ スプレッドシートに追加しました")
    else:
        print("⚠️ スプレッドシートへの追加をスキップしました（重複の可能性）")
    
    print("\n✅ テスト完了")


if __name__ == '__main__':
    test_article_tweet()
