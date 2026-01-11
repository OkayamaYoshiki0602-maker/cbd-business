#!/usr/bin/env python3
"""
新しい方向性に基づいたツイート案を生成してスプレッドシートに反映
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

# .envファイルを読み込む
load_dotenv()

SPREADSHEET_ID = "1-2L6C3NpF8vqnXxHWKP-Js3TMFKYE73tTtxdkZVPTaM"
SHEET_NAME = "シート1"


def get_headers():
    """
    スプレッドシートのヘッダーを取得
    """
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


def generate_sample_tweets():
    """
    サンプルツイート案を生成（各タイプから1件ずつ）
    """
    sample_tweets = []
    
    # サンプルデータ
    sample_articles = [
        {
            'title': 'CBDの選び方：1000件のレビューを分析した結果',
            'content': 'データコンサルタントとして、Amazonのレビュー1000件を分析しました。効果を実感した人の共通点は継続使用と目的に合った商品選びです。',
            'url': 'https://cbd-no-hito.com/cbd-selection-guide/',
            'type': 'data_analysis'
        },
        {
            'title': 'CBD初心者向け：選び方のコツ',
            'content': 'CBDを始めたいけど、何を選べばいいか分からない方向けに、選び方のコツをまとめました。ポイントは自分の目的に合った商品を選ぶことです。',
            'url': 'https://cbd-no-hito.com/cbd-beginner-guide/',
            'type': 'lifestyle'
        },
        {
            'title': 'CBD業界の最新ニュース',
            'content': '最新のCBD業界ニュースをお届けします。',
            'url': 'https://cbd-no-hito.com/news/',
            'type': 'other'
        }
    ]
    
    for article in sample_articles:
        content_type = article['type']
        tweet_text = generate_tweet_by_type(
            content_type=content_type,
            article_title=article['title'],
            article_content=article['content'],
            article_url=article['url']
        )
        
        persona, engagement = get_persona_and_engagement(content_type)
        
        sample_tweets.append({
            'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            'status': '下書き',
            'title': article['title'],
            'tweet_text': tweet_text,
            'url': article['url'],
            'source': 'sample',
            'content_type': content_type,
            'persona': persona,
            'engagement': engagement
        })
    
    return sample_tweets


def write_to_spreadsheet(tweets_data):
    """
    スプレッドシートにツイート案を書き込む
    """
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
    print("新しい方向性に基づいたツイート案生成")
    print("=" * 60)
    
    # サンプルツイートを生成
    print("\n📝 サンプルツイート案を生成中...")
    sample_tweets = generate_sample_tweets()
    
    print(f"\n✅ {len(sample_tweets)}件のサンプルツイート案を生成しました")
    
    # スプレッドシートに書き込み
    print("\n📊 スプレッドシートに書き込み中...")
    success = write_to_spreadsheet(sample_tweets)
    
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
