#!/usr/bin/env python3
"""
X (Twitter) API操作スクリプト
ツイート投稿・メディアアップロード・スケジュール投稿
"""

import os
import sys
import json
from datetime import datetime
from pathlib import Path
from dotenv import load_dotenv
import tweepy

# .envファイルを読み込む
load_dotenv()

# 認証情報（環境変数から取得）
X_API_KEY = os.getenv('X_API_KEY')
X_API_SECRET_KEY = os.getenv('X_API_SECRET_KEY')
X_ACCESS_TOKEN = os.getenv('X_ACCESS_TOKEN')
X_ACCESS_TOKEN_SECRET = os.getenv('X_ACCESS_TOKEN_SECRET')
X_BEARER_TOKEN = os.getenv('X_BEARER_TOKEN')


def get_twitter_client():
    """
    X (Twitter) API クライアントを取得
    """
    if not all([X_API_KEY, X_API_SECRET_KEY, X_ACCESS_TOKEN, X_ACCESS_TOKEN_SECRET]):
        raise ValueError(
            "X API認証情報が設定されていません。\n"
            ".envファイルに以下を設定してください:\n"
            "- X_API_KEY\n"
            "- X_API_SECRET_KEY\n"
            "- X_ACCESS_TOKEN\n"
            "- X_ACCESS_TOKEN_SECRET"
        )
    
    client = tweepy.Client(
        bearer_token=X_BEARER_TOKEN,
        consumer_key=X_API_KEY,
        consumer_secret=X_API_SECRET_KEY,
        access_token=X_ACCESS_TOKEN,
        access_token_secret=X_ACCESS_TOKEN_SECRET,
        wait_on_rate_limit=True
    )
    
    return client


def tweet(text, media_ids=None, reply_to_tweet_id=None):
    """
    ツイートを投稿
    
    Args:
        text: ツイート本文（280文字以内）
        media_ids: メディアIDのリスト（画像・動画）
        reply_to_tweet_id: リプライ先のツイートID
    
    Returns:
        投稿されたツイートの情報
    """
    try:
        client = get_twitter_client()
        
        # 文字数チェック
        if len(text) > 280:
            raise ValueError(f"ツイート本文が280文字を超えています: {len(text)}文字")
        
        # ツイート投稿
        tweet_params = {
            'text': text
        }
        
        if media_ids:
            tweet_params['media_ids'] = media_ids
        
        if reply_to_tweet_id:
            tweet_params['in_reply_to_tweet_id'] = reply_to_tweet_id
        
        response = client.create_tweet(**tweet_params)
        
        if response.data:
            print(f"✅ ツイートを投稿しました: {response.data['id']}")
            print(f"ツイート内容: {text[:50]}...")
            return response.data
        else:
            print("❌ ツイート投稿に失敗しました")
            return None
    
    except tweepy.TooManyRequests:
        print("❌ レート制限に達しました。しばらく待ってから再試行してください。")
        return None
    except tweepy.Unauthorized:
        print("❌ 認証エラー: API認証情報を確認してください。")
        return None
    except Exception as e:
        print(f"❌ エラーが発生しました: {e}")
        return None


def upload_media(media_path):
    """
    メディア（画像・動画）をアップロード
    
    Args:
        media_path: メディアファイルのパス
    
    Returns:
        メディアID
    """
    try:
        # API v1.1を使用してメディアアップロード
        auth = tweepy.OAuth1UserHandler(
            X_API_KEY,
            X_API_SECRET_KEY,
            X_ACCESS_TOKEN,
            X_ACCESS_TOKEN_SECRET
        )
        api_v1 = tweepy.API(auth)
        
        media = api_v1.media_upload(media_path)
        print(f"✅ メディアをアップロードしました: {media.media_id}")
        return media.media_id
    
    except Exception as e:
        print(f"❌ メディアアップロードエラー: {e}")
        return None


def get_user_info(username='me'):
    """
    ユーザー情報を取得
    
    Args:
        username: ユーザー名（'me' で認証ユーザー）
    
    Returns:
        ユーザー情報
    """
    try:
        client = get_twitter_client()
        
        if username == 'me':
            user = client.get_me()
        else:
            user = client.get_user(username=username)
        
        if user.data:
            print(f"✅ ユーザー情報を取得しました: @{user.data.username}")
            return user.data
        else:
            print("❌ ユーザー情報の取得に失敗しました")
            return None
    
    except Exception as e:
        print(f"❌ エラーが発生しました: {e}")
        return None


def main():
    """メイン関数"""
    if len(sys.argv) < 2:
        print("使用方法:")
        print("  python x_twitter.py tweet <ツイート本文>")
        print("  python x_twitter.py tweet-with-media <ツイート本文> <メディアパス>")
        print("  python x_twitter.py user <ユーザー名>")
        print("\n例:")
        print("  python x_twitter.py tweet 'こんにちは！'")
        print("  python x_twitter.py tweet-with-media '画像付きツイート' image.jpg")
        print("  python x_twitter.py user me")
        sys.exit(1)
    
    command = sys.argv[1]
    
    if command == 'tweet':
        if len(sys.argv) < 3:
            print("エラー: ツイート本文が必要です")
            sys.exit(1)
        
        text = sys.argv[2]
        result = tweet(text)
        
        if result:
            print(f"\nツイートID: {result['id']}")
            print(f"ツイートURL: https://twitter.com/user/status/{result['id']}")
    
    elif command == 'tweet-with-media':
        if len(sys.argv) < 4:
            print("エラー: ツイート本文とメディアパスが必要です")
            sys.exit(1)
        
        text = sys.argv[2]
        media_path = sys.argv[3]
        
        media_id = upload_media(media_path)
        if media_id:
            result = tweet(text, media_ids=[media_id])
            
            if result:
                print(f"\nツイートID: {result['id']}")
                print(f"ツイートURL: https://twitter.com/user/status/{result['id']}")
    
    elif command == 'user':
        username = sys.argv[2] if len(sys.argv) > 2 else 'me'
        user = get_user_info(username)
        
        if user:
            print(f"\nユーザー名: @{user.username}")
            print(f"表示名: {user.name}")
            print(f"ID: {user.id}")
    
    else:
        print(f"不明なコマンド: {command}")
        sys.exit(1)


if __name__ == '__main__':
    main()
