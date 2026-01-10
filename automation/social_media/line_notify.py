#!/usr/bin/env python3
"""
LINE通知機能
投稿前確認・通知送信
"""

import os
import sys
import json
from pathlib import Path
from dotenv import load_dotenv
import requests

# .envファイルを読み込む
load_dotenv()

# LINE Messaging API の認証情報（環境変数から取得）
LINE_CHANNEL_ACCESS_TOKEN = os.getenv('LINE_CHANNEL_ACCESS_TOKEN')
LINE_USER_ID = os.getenv('LINE_USER_ID')  # 通知を送信するユーザーID（任意）


def send_line_message(message, user_id=None):
    """
    LINEにメッセージを送信
    
    Args:
        message: 送信するメッセージ
        user_id: 送信先のユーザーID（Noneの場合はプッシュ通知で送信）
    
    Returns:
        送信結果
    """
    if not LINE_CHANNEL_ACCESS_TOKEN:
        print("⚠️ LINE_CHANNEL_ACCESS_TOKENが設定されていません。")
        print("LINE Messaging API の Channel Access Token を設定してください。")
        return False
    
    try:
        url = 'https://api.line.me/v2/bot/message/push' if user_id else 'https://api.line.me/v2/bot/message/broadcast'
        
        headers = {
            'Content-Type': 'application/json',
            'Authorization': f'Bearer {LINE_CHANNEL_ACCESS_TOKEN}'
        }
        
        payload = {
            'messages': [{
                'type': 'text',
                'text': message
            }]
        }
        
        if user_id:
            payload['to'] = user_id
        
        response = requests.post(url, headers=headers, json=payload)
        
        if response.status_code == 200:
            print(f"✅ LINE通知を送信しました")
            return True
        else:
            print(f"❌ LINE通知送信エラー: {response.status_code}")
            print(f"レスポンス: {response.text}")
            return False
    
    except Exception as e:
        print(f"❌ エラーが発生しました: {e}")
        return False


def send_tweet_preview(tweet_text, media_path=None):
    """
    ツイート投稿前のプレビューをLINEで送信
    
    Args:
        tweet_text: ツイート本文
        media_path: メディアパス（オプション）
    
    Returns:
        送信結果
    """
    preview_message = f"""📝 ツイート投稿予定

{tweet_text}

---
文字数: {len(tweet_text)}/280
"""
    
    if media_path:
        preview_message += f"📎 メディア: {media_path}\n"
    
    preview_message += "\nこのツイートを投稿しますか？"
    
    return send_line_message(preview_message, user_id=LINE_USER_ID)


def send_tweet_result(tweet_id, tweet_text, success=True):
    """
    ツイート投稿結果をLINEで通知
    
    Args:
        tweet_id: ツイートID
        tweet_text: ツイート本文
        success: 成功/失敗
    
    Returns:
        送信結果
    """
    if success:
        message = f"""✅ ツイート投稿完了

{tweet_text}

ツイートID: {tweet_id}
URL: https://twitter.com/user/status/{tweet_id}
"""
    else:
        message = f"""❌ ツイート投稿失敗

{tweet_text}

エラーが発生しました。
"""
    
    return send_line_message(message, user_id=LINE_USER_ID)


def main():
    """メイン関数"""
    if len(sys.argv) < 2:
        print("使用方法:")
        print("  python line_notify.py send <メッセージ>")
        print("  python line_notify.py preview <ツイート本文> [メディアパス]")
        print("\n例:")
        print("  python line_notify.py send 'テストメッセージ'")
        print("  python line_notify.py preview 'ツイート内容' image.jpg")
        sys.exit(1)
    
    command = sys.argv[1]
    
    if command == 'send':
        if len(sys.argv) < 3:
            print("エラー: メッセージが必要です")
            sys.exit(1)
        
        message = sys.argv[2]
        send_line_message(message)
    
    elif command == 'preview':
        if len(sys.argv) < 3:
            print("エラー: ツイート本文が必要です")
            sys.exit(1)
        
        tweet_text = sys.argv[2]
        media_path = sys.argv[3] if len(sys.argv) > 3 else None
        
        send_tweet_preview(tweet_text, media_path)
    
    else:
        print(f"不明なコマンド: {command}")
        sys.exit(1)


if __name__ == '__main__':
    main()
