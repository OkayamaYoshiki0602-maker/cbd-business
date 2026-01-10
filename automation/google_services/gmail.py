#!/usr/bin/env python3
"""
Gmail操作スクリプト
Gmailのメールを確認・送信
"""

import os
import sys
import json
import base64
from pathlib import Path
from google.oauth2 import service_account
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError


# 認証情報ファイルのパス
CREDENTIALS_FILE = os.path.expanduser("~/.config/cursor/google-drive-credentials.json")

# スコープ
SCOPES = ['https://www.googleapis.com/auth/gmail.readonly']


def get_credentials():
    """認証情報を取得"""
    if not os.path.exists(CREDENTIALS_FILE):
        raise FileNotFoundError(
            f"認証情報ファイルが見つかりません: {CREDENTIALS_FILE}\n"
            "Google Cloud Consoleから認証情報を取得してください。"
        )
    
    credentials = service_account.Credentials.from_service_account_file(
        CREDENTIALS_FILE,
        scopes=SCOPES
    )
    return credentials


def list_messages(user_id='me', max_results=10, query=''):
    """
    Gmailからメール一覧を取得
    
    Args:
        user_id: ユーザーID（デフォルト: 'me'）
        max_results: 最大取得件数
        query: 検索クエリ（例: 'is:unread', 'from:example@gmail.com'）
    
    Returns:
        メール一覧
    """
    try:
        credentials = get_credentials()
        service = build('gmail', 'v1', credentials=credentials)
        
        results = service.users().messages().list(
            userId=user_id,
            maxResults=max_results,
            q=query
        ).execute()
        
        messages = results.get('messages', [])
        return messages
    
    except HttpError as error:
        print(f"エラーが発生しました: {error}")
        if '401' in str(error) or '403' in str(error):
            print("\n⚠️ 注意: Gmail APIはサービスアカウントでは直接使用できない可能性があります。")
            print("OAuth 2.0認証が必要な場合があります。")
        return None


def get_message(user_id='me', msg_id=''):
    """
    メールの詳細を取得
    
    Args:
        user_id: ユーザーID（デフォルト: 'me'）
        msg_id: メールID
    
    Returns:
        メールの詳細情報
    """
    try:
        credentials = get_credentials()
        service = build('gmail', 'v1', credentials=credentials)
        
        message = service.users().messages().get(
            userId=user_id,
            id=msg_id
        ).execute()
        
        return message
    
    except HttpError as error:
        print(f"エラーが発生しました: {error}")
        return None


def decode_message_body(message):
    """メール本文をデコード"""
    payload = message.get('payload', {})
    parts = payload.get('parts', [])
    
    body = ""
    for part in parts:
        if part.get('mimeType') == 'text/plain':
            data = part['body'].get('data')
            if data:
                body += base64.urlsafe_b64decode(data).decode('utf-8')
        elif part.get('mimeType') == 'text/html':
            data = part['body'].get('data')
            if data:
                body += base64.urlsafe_b64decode(data).decode('utf-8')
    
    # partsがない場合（シンプルなメール）
    if not parts and payload.get('body', {}).get('data'):
        data = payload['body']['data']
        body = base64.urlsafe_b64decode(data).decode('utf-8')
    
    return body


def main():
    """メイン関数"""
    if len(sys.argv) < 2:
        print("使用方法:")
        print("  python gmail.py list [max_results] [query]")
        print("  python gmail.py get <msg_id>")
        print("\n例:")
        print("  python gmail.py list 10")
        print("  python gmail.py list 10 'is:unread'")
        print("  python gmail.py get <msg_id>")
        sys.exit(1)
    
    command = sys.argv[1]
    
    if command == 'list':
        max_results = int(sys.argv[2]) if len(sys.argv) > 2 else 10
        query = sys.argv[3] if len(sys.argv) > 3 else ''
        
        messages = list_messages(max_results=max_results, query=query)
        
        if messages:
            print(f"📧 メール一覧（{len(messages)}件）:")
            for msg in messages:
                message = get_message(msg_id=msg['id'])
                if message:
                    headers = message.get('payload', {}).get('headers', [])
                    subject = next((h['value'] for h in headers if h['name'] == 'Subject'), '（件名なし）')
                    from_addr = next((h['value'] for h in headers if h['name'] == 'From'), '（送信者なし）')
                    date = next((h['value'] for h in headers if h['name'] == 'Date'), '（日付なし）')
                    print(f"  - {date} | {from_addr}")
                    print(f"    {subject}")
                    print(f"    ID: {msg['id']}")
        else:
            print("メールが見つかりませんでした")
    
    elif command == 'get':
        if len(sys.argv) < 3:
            print("エラー: メールIDが必要です")
            sys.exit(1)
        
        msg_id = sys.argv[2]
        message = get_message(msg_id=msg_id)
        
        if message:
            headers = message.get('payload', {}).get('headers', [])
            subject = next((h['value'] for h in headers if h['name'] == 'Subject'), '（件名なし）')
            from_addr = next((h['value'] for h in headers if h['name'] == 'From'), '（送信者なし）')
            date = next((h['value'] for h in headers if h['name'] == 'Date'), '（日付なし）')
            body = decode_message_body(message)
            
            print(f"📧 メール詳細:")
            print(f"件名: {subject}")
            print(f"送信者: {from_addr}")
            print(f"日付: {date}")
            print(f"\n本文:\n{body}")
        else:
            print("メールの取得に失敗しました")
    
    else:
        print(f"不明なコマンド: {command}")
        sys.exit(1)


if __name__ == '__main__':
    main()
