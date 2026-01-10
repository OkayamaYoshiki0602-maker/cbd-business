#!/usr/bin/env python3
"""
X (Twitter) API操作スクリプト（LINE通知連携版）
ツイート投稿時にLINE通知を送信
"""

import os
import sys
from dotenv import load_dotenv
from x_twitter import tweet, get_user_info
from line_notify import send_tweet_preview, send_tweet_result

# .envファイルを読み込む
load_dotenv()


def tweet_with_line_notification(text, media_path=None, confirm=True):
    """
    LINE通知付きでツイートを投稿
    
    Args:
        text: ツイート本文（280文字以内）
        media_path: メディアファイルのパス（オプション）
        confirm: 投稿前にLINE通知で確認するか（デフォルト: True）
    
    Returns:
        投稿されたツイートの情報
    """
    try:
        # 投稿前プレビューをLINEで送信
        if confirm:
            print("📱 LINEに投稿プレビューを送信しています...")
            preview_sent = send_tweet_preview(text, media_path)
            if preview_sent:
                print("✅ LINEにプレビューを送信しました")
                print("💡 LINEで確認してから、手動でツイートを投稿してください")
                
                # ここで確認を待つ（手動で実行する場合）
                # または、自動投稿する場合は confirm=False にする
                response = input("\nこのツイートを投稿しますか？ (y/n): ")
                if response.lower() != 'y':
                    print("❌ ツイート投稿をキャンセルしました")
                    return None
        
        # ツイート投稿
        print("\n📝 ツイートを投稿しています...")
        result = tweet(text, media_ids=None)
        
        if result:
            # 投稿結果をLINEで通知
            print("📱 LINEに投稿結果を送信しています...")
            send_tweet_result(result['id'], text, success=True)
            print("✅ ツイート投稿完了！")
            return result
        else:
            # エラーをLINEで通知
            print("📱 LINEにエラー通知を送信しています...")
            send_tweet_result(None, text, success=False)
            print("❌ ツイート投稿失敗")
            return None
    
    except Exception as e:
        print(f"❌ エラーが発生しました: {e}")
        # エラーをLINEで通知
        send_tweet_result(None, text, success=False)
        return None


def main():
    """メイン関数"""
    if len(sys.argv) < 2:
        print("使用方法:")
        print("  python x_twitter_with_line.py tweet <ツイート本文> [--no-confirm]")
        print("  python x_twitter_with_line.py tweet-preview <ツイート本文>")
        print("\n例:")
        print("  python x_twitter_with_line.py tweet 'ツイート内容'")
        print("  python x_twitter_with_line.py tweet 'ツイート内容' --no-confirm")
        print("  python x_twitter_with_line.py tweet-preview 'ツイート内容'")
        sys.exit(1)
    
    command = sys.argv[1]
    
    if command == 'tweet':
        if len(sys.argv) < 3:
            print("エラー: ツイート本文が必要です")
            sys.exit(1)
        
        text = sys.argv[2]
        confirm = '--no-confirm' not in sys.argv
        
        result = tweet_with_line_notification(text, confirm=confirm)
        
        if result:
            print(f"\n✅ ツイート投稿完了！")
            print(f"ツイートID: {result['id']}")
            print(f"ツイートURL: https://twitter.com/user/status/{result['id']}")
    
    elif command == 'tweet-preview':
        if len(sys.argv) < 3:
            print("エラー: ツイート本文が必要です")
            sys.exit(1)
        
        text = sys.argv[2]
        send_tweet_preview(text)
    
    else:
        print(f"不明なコマンド: {command}")
        sys.exit(1)


if __name__ == '__main__':
    main()
