#!/usr/bin/env python3
"""
スプレッドシートにツイート案を生成して書き込むスクリプト
サイト記事パターン5件 + CBDニュース5件 = 合計10件
"""

import os
import sys
from pathlib import Path
from datetime import datetime
from dotenv import load_dotenv

# 親ディレクトリをパスに追加
sys.path.insert(0, str(Path(__file__).parent.parent))

from google_services.google_sheets import write_spreadsheet, read_spreadsheet
from social_media.tweet_generator_v3 import generate_tweet_by_type, select_content_type, get_persona_and_engagement
from social_media.article_detector import check_wordpress_rss
from social_media.news_collector import collect_cbd_news
from social_media.article_summarizer import summarize_article_with_highlights

# .envファイルを読み込む
load_dotenv()

SPREADSHEET_ID = "1-2L6C3NpF8vqnXxHWKP-Js3TMFKYE73tTtxdkZVPTaM"
SHEET_NAME = "シート1"


def get_headers():
    """スプレッドシートのヘッダーを取得"""
    return [
        'タイムスタンプ',
        'ステータス',
        '記事タイトル',
        'ツイート文案',
        'URL',
        'ソース',
        'コンテンツタイプ',
        'ペルソナ',
        '引き付け期待（ゴール：サイト遷移）'
    ]


def generate_article_tweets(num_samples=5):
    """WordPress記事からツイート案を生成"""
    print(f"📝 WordPress記事から{num_samples}件のツイート案を生成中...")
    
    # WordPress RSSフィードから記事を取得
    articles = check_wordpress_rss()
    
    if not articles:
        print("⚠️ WordPress記事が見つかりませんでした")
        return []
    
    tweets = []
    for i, article in enumerate(articles[:num_samples], 1):
        print(f"  [{i}/{num_samples}] {article['title'][:50]}...")
        
        # コンテンツタイプを選択（実体験×データ分析型: 60%, ライフスタイル型: 30%）
        # 記事の場合は、データ分析型またはライフスタイル型を使用
        import random
        rand = random.random()
        if rand < 0.6:
            content_type = 'data_analysis'
        elif rand < 0.9:
            content_type = 'lifestyle'
        else:
            content_type = 'data_analysis'  # 記事の場合はデータ分析型を優先
        
        # 記事内容を取得
        article_url = article.get('url', '')
        article_title = article['title']
        article_content = article.get('summary', '')
        
        # 記事本文を取得（要約用）
        # 記事要約はツイート生成時に含まれるので、ここでは基本情報のみを使用
        # 記事要約機能はツイート生成ロジック内で呼び出される
        
        # ツイートを生成
        try:
            tweet_text = generate_tweet_by_type(
                content_type=content_type,
                article_title=article_title,
                article_content=article_content,
                article_url=article_url
            )
            
            persona, engagement = get_persona_and_engagement(content_type)
            
            tweets.append({
                'timestamp': datetime.now().isoformat(),
                'status': '下書き',
                'title': article_title,
                'tweet_text': tweet_text,
                'url': article_url,
                'source': 'wordpress',
                'content_type': content_type,
                'persona': persona,
                'engagement': engagement
            })
            
            print(f"    ✅ 生成完了（{len(tweet_text)}文字）")
        except Exception as e:
            print(f"    ❌ エラー: {e}")
            import traceback
            traceback.print_exc()
    
    return tweets


def generate_news_tweets(num_samples=5):
    """CBDニュースからツイート案を生成"""
    print(f"\n📰 CBDニュースから{num_samples}件のツイート案を生成中...")
    
    # CBDニュースを取得（直近1ヶ月）
    news_list = collect_cbd_news(days=30, max_articles=num_samples * 2)  # 多めに取得
    
    if not news_list:
        print("⚠️ CBDニュースが見つかりませんでした")
        return []
    
    tweets = []
    for i, news in enumerate(news_list[:num_samples], 1):
        print(f"  [{i}/{num_samples}] {news['title'][:50]}...")
        
        # ニュースの場合は「その他」タイプ（10%）またはデータ分析型（60%）を使用
        import random
        rand = random.random()
        if rand < 0.1:
            content_type = 'other'
        elif rand < 0.7:
            content_type = 'data_analysis'
        else:
            content_type = 'data_analysis'
        
        news_title = news['title']
        news_content = news.get('summary', '')
        news_url = news.get('url', '')
        
        # ツイートを生成
        try:
            tweet_text = generate_tweet_by_type(
                content_type=content_type,
                news_title=news_title,
                news_content=news_content,
                news_url=news_url
            )
            
            persona, engagement = get_persona_and_engagement(content_type)
            
            tweets.append({
                'timestamp': datetime.now().isoformat(),
                'status': '下書き',
                'title': news_title,
                'tweet_text': tweet_text,
                'url': news_url,
                'source': 'news',
                'content_type': content_type,
                'persona': persona,
                'engagement': engagement
            })
            
            print(f"    ✅ 生成完了（{len(tweet_text)}文字）")
        except Exception as e:
            print(f"    ❌ エラー: {e}")
            import traceback
            traceback.print_exc()
    
    return tweets


def write_to_spreadsheet(tweets_data):
    """スプレッドシートにツイート案を書き込む"""
    try:
        # 既存のデータを確認
        existing_data = read_spreadsheet(SPREADSHEET_ID, f"{SHEET_NAME}!A1:I1")
        
        # ヘッダーを書き込み（既にある場合はスキップ）
        headers = get_headers()
        if not existing_data or existing_data[0] != headers:
            write_spreadsheet(SPREADSHEET_ID, f"{SHEET_NAME}!A1", [headers])
            print("✅ ヘッダーを書き込みました")
        else:
            print("✅ ヘッダーは既に存在します")
        
        # 既存のデータを確認して、次の行を決定
        all_data = read_spreadsheet(SPREADSHEET_ID, f"{SHEET_NAME}!A2:I1000")
        next_row = len(all_data) + 2 if all_data else 2
        
        # データを書き込み
        for i, tweet_data in enumerate(tweets_data):
            row_data = [
                tweet_data['timestamp'],
                tweet_data['status'],
                tweet_data['title'],
                tweet_data['tweet_text'],
                tweet_data['url'],
                tweet_data['source'],
                tweet_data['content_type'],
                tweet_data['persona'],
                tweet_data['engagement']
            ]
            
            range_name = f"{SHEET_NAME}!A{next_row + i}"
            write_spreadsheet(SPREADSHEET_ID, range_name, [row_data])
            print(f"✅ [{i+1}/{len(tweets_data)}] ツイート案を書き込みました: {tweet_data['title'][:30]}...")
        
        print(f"\n✅ {len(tweets_data)}件のツイート案をスプレッドシートに書き込みました")
        print(f"📋 スプレッドシート: https://docs.google.com/spreadsheets/d/{SPREADSHEET_ID}/edit")
        
        return True
    
    except Exception as e:
        print(f"❌ エラーが発生しました: {e}")
        import traceback
        traceback.print_exc()
        return False


def main():
    """メイン関数"""
    print("=" * 60)
    print("ツイート案生成（サイト記事5件 + CBDニュース5件）")
    print("=" * 60)
    
    all_tweets = []
    
    # 1. WordPress記事から5件生成
    article_tweets = generate_article_tweets(num_samples=5)
    all_tweets.extend(article_tweets)
    
    # 2. CBDニュースから5件生成
    news_tweets = generate_news_tweets(num_samples=5)
    all_tweets.extend(news_tweets)
    
    print(f"\n✅ 合計{len(all_tweets)}件のツイート案を生成しました")
    print(f"   - サイト記事: {len(article_tweets)}件")
    print(f"   - CBDニュース: {len(news_tweets)}件")
    
    # スプレッドシートに書き込み
    print("\n📊 スプレッドシートに書き込み中...")
    success = write_to_spreadsheet(all_tweets)
    
    if success:
        print("\n" + "=" * 60)
        print("✅ 処理完了")
        print("=" * 60)
    else:
        print("\n" + "=" * 60)
        print("❌ 処理失敗")
        print("=" * 60)


if __name__ == '__main__':
    main()
