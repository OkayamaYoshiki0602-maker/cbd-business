#!/usr/bin/env python3
"""
CBD・大麻関連ニュース収集スクリプト
RSSフィードから最新ニュースを収集
"""

import os
import sys
from datetime import datetime, timedelta
from pathlib import Path
from dotenv import load_dotenv
import feedparser

# 親ディレクトリをパスに追加
sys.path.insert(0, str(Path(__file__).parent.parent))

# .envファイルを読み込む
load_dotenv()


# CBD・大麻関連RSSフィード（推奨）
CBD_RSS_FEEDS = [
    # 国際的なニュースサイト
    'https://hempindustrydaily.com/feed/',
    'https://www.leafly.com/news/rss',
    'https://www.cannabisbusinesstimes.com/rss/',
    'https://mjbizdaily.com/feed/',
    
    # Google News RSS（検索クエリ: CBD marijuana cannabis）
    'https://news.google.com/rss/search?q=CBD+marijuana+cannabis&hl=ja&gl=JP&ceid=JP:ja',
    
    # 日本のニュースサイト（RSSがある場合）
    # 追加してください
]

# キーワードフィルター（日本語・英語）
CBD_KEYWORDS = [
    'CBD', 'cannabidiol', 'cannabis', 'marijuana', '大麻', 'ヘンプ', 'hemp',
    'THC', 'カンナビノイド', 'cannabinoid', '医療大麻', 'medical marijuana',
    '合法化', 'legalization', '規制緩和', 'regulatory'
]


def collect_cbd_news(hours=24, days=30, max_articles=10):
    """
    CBD・大麻関連ニュースを収集
    
    Args:
        hours: 過去何時間のニュースを取得するか（daysが指定されている場合は無視）
        days: 過去何日間のニュースを取得するか（デフォルト: 30日）
        max_articles: 最大記事数
    
    Returns:
        ニュース記事のリスト
    """
    all_articles = []
    # daysが指定されている場合、hoursを無視してdaysを使用
    if days:
        cutoff_time = datetime.now() - timedelta(days=days)
    else:
        cutoff_time = datetime.now() - timedelta(hours=hours)
    
    for feed_url in CBD_RSS_FEEDS:
        try:
            print(f"📰 RSSフィードを取得中: {feed_url}")
            feed = feedparser.parse(feed_url)
            
            if feed.bozo:
                print(f"⚠️ RSSフィードの解析エラー: {feed.bozo_exception}")
                continue
            
            for entry in feed.entries[:max_articles]:  # 各フィードから最大10件
                # 公開日時を取得
                published_time = None
                if hasattr(entry, 'published_parsed') and entry.published_parsed:
                    published_time = datetime(*entry.published_parsed[:6])
                elif hasattr(entry, 'updated_parsed') and entry.updated_parsed:
                    published_time = datetime(*entry.updated_parsed[:6])
                
                # 時間フィルター
                if published_time and published_time < cutoff_time:
                    continue
                
                # キーワードフィルター
                title = entry.title if hasattr(entry, 'title') else ''
                summary = entry.summary if hasattr(entry, 'summary') else ''
                full_text = f"{title} {summary}".lower()
                
                if not any(keyword.lower() in full_text for keyword in CBD_KEYWORDS):
                    continue
                
                article = {
                    'title': title,
                    'url': entry.link if hasattr(entry, 'link') else '',
                    'summary': summary,
                    'published': published_time.isoformat() if published_time else None,
                    'source': feed_url
                }
                
                all_articles.append(article)
                
        except Exception as e:
            print(f"⚠️ RSSフィード取得エラー: {feed_url}, {e}")
            continue
    
    # 公開日時でソート（新しい順）
    all_articles.sort(key=lambda x: x['published'] or '', reverse=True)
    
    # 重複を除去（URLで判定）
    seen_urls = set()
    unique_articles = []
    for article in all_articles:
        url = article['url']
        if url and url not in seen_urls:
            seen_urls.add(url)
            unique_articles.append(article)
    
    return unique_articles[:max_articles]


def summarize_news_articles(articles, use_ai=True):
    """
    ニュース記事を要約
    
    Args:
        articles: ニュース記事のリスト
        use_ai: AI要約を使用するか（デフォルト: True、未実装時はFalse）
    
    Returns:
        要約テキスト
    """
    if not articles:
        return "📰 記事動向：\n新着ニュースはありません"
    
    summary = f"📰 CBD・大麻関連ニュース（{len(articles)}件）:\n\n"
    
    for i, article in enumerate(articles, 1):
        title = article['title']
        url = article.get('url', '')
        
        summary += f"{i}. {title}\n"
        if url:
            summary += f"   {url}\n"
        summary += "\n"
    
    return summary


def main():
    """メイン関数"""
    if len(sys.argv) < 2:
        print("使用方法:")
        print("  python news_collector.py collect [hours] [max_articles]")
        print("  python news_collector.py summary [hours]")
        print("\n例:")
        print("  python news_collector.py collect 24 10")
        print("  python news_collector.py summary 24")
        sys.exit(1)
    
    command = sys.argv[1]
    
    if command == 'collect':
        hours = int(sys.argv[2]) if len(sys.argv) > 2 else 24
        max_articles = int(sys.argv[3]) if len(sys.argv) > 3 else 10
        
        articles = collect_cbd_news(hours, max_articles)
        
        print(f"\n✅ {len(articles)}件のニュースを収集しました\n")
        for i, article in enumerate(articles, 1):
            print(f"{i}. {article['title']}")
            print(f"   {article['url']}")
            print()
    
    elif command == 'summary':
        hours = int(sys.argv[2]) if len(sys.argv) > 2 else 24
        
        articles = collect_cbd_news(hours)
        summary = summarize_news_articles(articles)
        
        print(summary)
    
    else:
        print(f"不明なコマンド: {command}")
        sys.exit(1)


if __name__ == '__main__':
    main()
