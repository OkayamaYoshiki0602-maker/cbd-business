#!/usr/bin/env python3
"""
毎日の定期実行スクリプト
毎日決まったタイミングでツイート案生成・承認済みツイート投稿を実行
"""

import os
import sys
import schedule
import time
from pathlib import Path
from datetime import datetime
from dotenv import load_dotenv

# 親ディレクトリをパスに追加
sys.path.insert(0, str(Path(__file__).parent.parent))

from social_media.scheduled_tweet import send_daily_tweet_preview
from social_media.approve_tweet import post_approved_tweets

# .envファイルを読み込む
load_dotenv()

# 実行時刻（環境変数から取得、デフォルトは9:00と18:00）
TWEET_GENERATION_TIME = os.getenv('TWEET_GENERATION_TIME', '09:00')
TWEET_POSTING_TIME = os.getenv('TWEET_POSTING_TIME', '09:30')


def daily_tweet_generation_job():
    """
    毎日のツイート案生成ジョブ
    """
    print(f"\n{'='*60}")
    print(f"📝 本日のツイート案生成開始 ({datetime.now().strftime('%Y-%m-%d %H:%M:%S')})")
    print(f"{'='*60}\n")
    
    try:
        send_daily_tweet_preview()
    except Exception as e:
        print(f"❌ エラーが発生しました: {e}")
        import traceback
        traceback.print_exc()
    
    print(f"\n{'='*60}\n")


def daily_tweet_posting_job():
    """
    毎日の承認済みツイート投稿ジョブ
    """
    print(f"\n{'='*60}")
    print(f"📤 承認済みツイート投稿開始 ({datetime.now().strftime('%Y-%m-%d %H:%M:%S')})")
    print(f"{'='*60}\n")
    
    try:
        post_approved_tweets(auto_mode=True)
    except Exception as e:
        print(f"❌ エラーが発生しました: {e}")
        import traceback
        traceback.print_exc()
    
    print(f"\n{'='*60}\n")


def main():
    """メイン関数"""
    print("🚀 毎日の定期実行スクリプトを開始します")
    print(f"📝 ツイート案生成時刻: {TWEET_GENERATION_TIME}")
    print(f"📤 ツイート投稿時刻: {TWEET_POSTING_TIME}")
    print("\n終了するには Ctrl+C を押してください\n")
    
    # スケジュール設定
    schedule.every().day.at(TWEET_GENERATION_TIME).do(daily_tweet_generation_job)
    schedule.every().day.at(TWEET_POSTING_TIME).do(daily_tweet_posting_job)
    
    # 初回実行（オプション）
    # daily_tweet_generation_job()
    
    # メインループ
    while True:
        schedule.run_pending()
        time.sleep(60)  # 1分ごとにチェック


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n👋 定期実行スクリプトを終了します")
        sys.exit(0)
