#!/usr/bin/env python3
"""
記事作成検知・ツイート文案生成スクリプト
WordPress記事更新検知、CBDニュース取得、ツイート文案生成
"""

import os
import sys
import json
from datetime import datetime
from pathlib import Path
from dotenv import load_dotenv
import feedparser
import requests
from urllib.parse import urljoin

# 親ディレクトリをパスに追加
sys.path.insert(0, str(Path(__file__).parent.parent))

from social_media.line_notify import send_tweet_preview
from google_services.google_sheets import read_spreadsheet, write_spreadsheet, list_spreadsheets

# .envファイルを読み込む
load_dotenv()

# WordPress URL
WORDPRESS_URL = os.getenv('WORDPRESS_URL', 'https://cbd-no-hito.com')
WORDPRESS_RSS_URL = f"{WORDPRESS_URL}/feed/"

# スプレッドシートID（承認待ちリスト用）
APPROVAL_SPREADSHEET_ID = os.getenv('APPROVAL_SPREADSHEET_ID', '')


def generate_tweet_text(article_title, article_summary=None, article_url=None):
    """
    記事情報からツイート文案を生成
    
    Args:
        article_title: 記事タイトル
        article_summary: 記事要約（オプション）
        article_url: 記事URL（オプション）
    
    Returns:
        ツイート文案（280文字以内）
    """
    # 基本的なツイート文案を生成
    base_text = article_title
    
    if article_url:
        # URLを含める場合は、URLの長さ（23文字）を考慮
        url_text = f"\n\n{article_url}"
        max_title_length = 280 - len(url_text) - 10  # 余裕を持たせる
    else:
        url_text = ""
        max_title_length = 280
    
    # タイトルが長すぎる場合は短縮
    if len(base_text) > max_title_length:
        base_text = base_text[:max_title_length-3] + "..."
    
    # ハッシュタグを追加（余裕があれば）
    hashtags = "#CBD"
    if len(base_text) + len(url_text) + len(hashtags) + 2 <= 280:
        tweet_text = f"{base_text}{url_text}\n{hashtags}"
    else:
        tweet_text = f"{base_text}{url_text}"
    
    return tweet_text


def check_wordpress_rss(last_check_date=None):
    """
    WordPress RSSフィードをチェックして新着記事を検知
    
    Args:
        last_check_date: 最後にチェックした日時（ISO形式文字列）
    
    Returns:
        新着記事のリスト
    """
    try:
        feed = feedparser.parse(WORDPRESS_RSS_URL)
        
        if feed.bozo:
            print(f"⚠️ RSSフィードの解析エラー: {feed.bozo_exception}")
            return []
        
        new_articles = []
        
        for entry in feed.entries:
            # 公開日時を取得
            published_time = datetime(*entry.published_parsed[:6]) if hasattr(entry, 'published_parsed') else None
            
            # 最後のチェック日時と比較
            if last_check_date:
                last_check = datetime.fromisoformat(last_check_date.replace('Z', '+00:00'))
                if published_time and published_time <= last_check:
                    continue
            
            article_info = {
                'title': entry.title,
                'url': entry.link,
                'summary': entry.summary if hasattr(entry, 'summary') else None,
                'published': published_time.isoformat() if published_time else None,
            }
            new_articles.append(article_info)
        
        return new_articles
    
    except Exception as e:
        print(f"❌ エラーが発生しました: {e}")
        return []


def add_to_approval_queue(article_title, tweet_text, article_url=None, source='wordpress'):
    """
    承認待ちリストに追加（スプレッドシート）
    
    Args:
        article_title: 記事タイトル
        tweet_text: ツイート文案
        article_url: 記事URL
        source: ソース（wordpress / news / manual）
    
    Returns:
        追加結果
    """
    if not APPROVAL_SPREADSHEET_ID:
        print("⚠️ APPROVAL_SPREADSHEET_IDが設定されていません。")
        print("承認待ちリストのスプレッドシートIDを設定してください。")
        return False
    
    try:
        # 承認待ちリストを読み込む
        approval_data = read_spreadsheet(APPROVAL_SPREADSHEET_ID, '承認待ちリスト!A1:Z1000')
        
        # ヘッダー行を確認
        if not approval_data:
            # ヘッダー行を作成
            headers = ['タイムスタンプ', 'ステータス', '記事タイトル', 'ツイート文案', '記事URL', 'ソース']
            approval_data = [headers]
        elif len(approval_data[0]) < 6:
            # ヘッダー行が不完全な場合は補完
            headers = ['タイムスタンプ', 'ステータス', '記事タイトル', 'ツイート文案', '記事URL', 'ソース']
            approval_data[0] = headers
        
        # 新しい行を追加
        new_row = [
            datetime.now().isoformat(),
            '下書き',  # ステータス: 下書き → 承認済み → 投稿済み
            article_title,
            tweet_text,
            article_url or '',
            source
        ]
        
        approval_data.append(new_row)
        
        # スプレッドシートに書き込み
        range_name = f'承認待ちリスト!A{len(approval_data)}'
        result = write_spreadsheet(APPROVAL_SPREADSHEET_ID, range_name, [new_row])
        
        if result:
            print(f"✅ 承認待ちリストに追加しました")
            print(f"  記事タイトル: {article_title}")
            return True
        else:
            print("❌ 承認待ちリストへの追加に失敗しました")
            return False
    
    except Exception as e:
        print(f"❌ エラーが発生しました: {e}")
        return False


def detect_new_articles_and_notify():
    """
    新着記事を検知してLINE通知を送信
    """
    try:
        print("📰 新着記事をチェックしています...")
        
        # WordPress RSSフィードをチェック
        new_articles = check_wordpress_rss()
        
        if not new_articles:
            print("✅ 新着記事はありませんでした")
            return
        
        print(f"✅ {len(new_articles)}件の新着記事を検知しました")
        
        for article in new_articles:
            # ツイート文案を生成
            tweet_text = generate_tweet_text(
                article['title'],
                article.get('summary'),
                article['url']
            )
            
            print(f"\n📝 記事: {article['title']}")
            print(f"   ツイート文案: {tweet_text[:50]}...")
            
            # LINE通知でプレビュー送信
            print("📱 LINEにプレビューを送信しています...")
            send_tweet_preview(tweet_text)
            
            # 承認待ちリストに追加
            print("📊 承認待ちリストに追加しています...")
            add_to_approval_queue(
                article['title'],
                tweet_text,
                article['url'],
                'wordpress'
            )
            
            print(f"✅ 処理完了: {article['title']}")
        
        print(f"\n✅ すべての新着記事を処理しました")
    
    except Exception as e:
        print(f"❌ エラーが発生しました: {e}")
        import traceback
        traceback.print_exc()


def create_manual_tweet_request(article_title, tweet_text=None, article_url=None):
    """
    手動でツイート投稿リクエストを作成
    
    Args:
        article_title: 記事タイトル
        tweet_text: ツイート文案（Noneの場合は自動生成）
        article_url: 記事URL（オプション）
    
    Returns:
        作成結果
    """
    try:
        # ツイート文案を生成（指定がない場合）
        if not tweet_text:
            tweet_text = generate_tweet_text(article_title, None, article_url)
        
        print(f"📝 記事: {article_title}")
        print(f"   ツイート文案: {tweet_text}")
        
        # LINE通知でプレビュー送信
        print("📱 LINEにプレビューを送信しています...")
        send_tweet_preview(tweet_text)
        
        # 承認待ちリストに追加
        print("📊 承認待ちリストに追加しています...")
        result = add_to_approval_queue(
            article_title,
            tweet_text,
            article_url,
            'manual'
        )
        
        if result:
            print(f"✅ 承認待ちリストに追加しました")
            print(f"💡 LINEで確認してから、承認コマンドを実行してください")
            return True
        else:
            print("❌ 承認待ちリストへの追加に失敗しました")
            return False
    
    except Exception as e:
        print(f"❌ エラーが発生しました: {e}")
        return False


def main():
    """メイン関数"""
    if len(sys.argv) < 2:
        print("使用方法:")
        print("  python article_detector.py check")
        print("  python article_detector.py manual <記事タイトル> [ツイート文案] [記事URL]")
        print("\n例:")
        print("  python article_detector.py check")
        print("  python article_detector.py manual 'CBDとは？' 'CBDについて解説します #CBD' 'https://cbd-no-hito.com/article'")
        sys.exit(1)
    
    command = sys.argv[1]
    
    if command == 'check':
        # WordPress RSSフィードをチェック
        detect_new_articles_and_notify()
    
    elif command == 'manual':
        if len(sys.argv) < 3:
            print("エラー: 記事タイトルが必要です")
            sys.exit(1)
        
        article_title = sys.argv[2]
        tweet_text = sys.argv[3] if len(sys.argv) > 3 else None
        article_url = sys.argv[4] if len(sys.argv) > 4 else None
        
        create_manual_tweet_request(article_title, tweet_text, article_url)
    
    else:
        print(f"不明なコマンド: {command}")
        sys.exit(1)


if __name__ == '__main__':
    main()
