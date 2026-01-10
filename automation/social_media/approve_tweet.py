#!/usr/bin/env python3
"""
承認済みツイートを投稿するスクリプト
スプレッドシートから承認済みツイートを読み込んで投稿
"""

import os
import sys
from pathlib import Path
from dotenv import load_dotenv

# 親ディレクトリをパスに追加
sys.path.insert(0, str(Path(__file__).parent.parent))

from social_media.x_twitter import tweet
from social_media.line_notify import send_tweet_result
from social_media.approval_manager import get_approved_tweets, approve_tweet as update_status_to_approved
from google_services.google_sheets import write_spreadsheet

# .envファイルを読み込む
load_dotenv()

APPROVAL_SPREADSHEET_ID = os.getenv('APPROVAL_SPREADSHEET_ID', '')


def post_approved_tweets(auto_mode=False):
    """
    承認済みツイートを投稿
    
    Args:
        auto_mode: 自動モード（定期実行時はTrue）
    """
    if not APPROVAL_SPREADSHEET_ID:
        print("⚠️ APPROVAL_SPREADSHEET_IDが設定されていません。")
        return
    
    try:
        # 承認済みツイートを取得
        approved = get_approved_tweets()
        
        if not approved:
            if auto_mode:
                # 自動モードの場合は何もしない（ログも出力しない）
                return
            print("📋 投稿待ちの承認済みツイートはありません")
            return
        
        print(f"📋 {len(approved)}件の承認済みツイートを投稿します")
        
        for item in approved:
            tweet_text = item['tweet_text']
            article_title = item['title']
            row_number = item['row']
            
            print(f"\n📝 投稿中: {article_title}")
            print(f"   ツイート文案: {tweet_text[:50]}...")
            
            # ツイート投稿
            result = tweet(tweet_text)
            
            if result:
                # 投稿結果をLINEで通知
                send_tweet_result(result['id'], tweet_text, success=True)
                
                # ステータスを「投稿済み」に更新
                range_name = f'承認待ちリスト!B{row_number}'
                write_spreadsheet(APPROVAL_SPREADSHEET_ID, range_name, [['投稿済み']])
                
                print(f"✅ ツイート投稿完了: {result['id']}")
            else:
                # エラーをLINEで通知
                send_tweet_result(None, tweet_text, success=False)
                print(f"❌ ツイート投稿失敗: {article_title}")
        
        print(f"\n✅ すべての承認済みツイートを処理しました")
    
    except Exception as e:
        print(f"❌ エラーが発生しました: {e}")
        import traceback
        traceback.print_exc()


def main():
    """メイン関数"""
    if len(sys.argv) >= 2 and sys.argv[1] == 'list':
        # 承認済みリストを表示
        from social_media.approval_manager import get_approved_tweets
        
        approved = get_approved_tweets()
        
        if not approved:
            print("📋 投稿待ちの承認済みツイートはありません")
        else:
            print(f"📋 投稿待ちの承認済みツイート（{len(approved)}件）:")
            print("=" * 60)
            for item in approved:
                print(f"\n行{item['row']}: {item['title']}")
                print(f"  ツイート文案: {item['tweet_text']}")
                print(f"  URL: {item['url']}")
    elif len(sys.argv) >= 2 and sys.argv[1] == 'auto':
        # 自動モード（定期実行時）
        post_approved_tweets(auto_mode=True)
    else:
        # 承認済みツイートを投稿
        post_approved_tweets()


if __name__ == '__main__':
    main()
