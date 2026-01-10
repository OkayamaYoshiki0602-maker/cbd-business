#!/usr/bin/env python3
"""
Google Calendar操作スクリプト
Googleカレンダーにイベントを作成・参照・更新・削除
"""

import os
import sys
import json
from datetime import datetime, timedelta
from pathlib import Path
from google.oauth2 import service_account
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError


# 認証情報ファイルのパス
CREDENTIALS_FILE = os.path.expanduser("~/.config/cursor/google-drive-credentials.json")

# スコープ
SCOPES = ['https://www.googleapis.com/auth/calendar']


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


def create_event(calendar_id='primary', summary='', start_time=None, end_time=None, description='', location=''):
    """
    Googleカレンダーにイベントを作成
    
    Args:
        calendar_id: カレンダーID（デフォルト: 'primary'）
        summary: イベントのタイトル
        start_time: 開始時刻（datetime または ISO形式文字列）
        end_time: 終了時刻（datetime または ISO形式文字列）
        description: 説明
        location: 場所
    
    Returns:
        作成されたイベントの情報
    """
    try:
        credentials = get_credentials()
        service = build('calendar', 'v3', credentials=credentials)
        
        # 時刻の変換
        if isinstance(start_time, str):
            start_time = datetime.fromisoformat(start_time.replace('Z', '+00:00'))
        if isinstance(end_time, str):
            end_time = datetime.fromisoformat(end_time.replace('Z', '+00:00'))
        
        if not start_time:
            start_time = datetime.now()
        if not end_time:
            end_time = start_time + timedelta(hours=1)
        
        event = {
            'summary': summary,
            'description': description,
            'location': location,
            'start': {
                'dateTime': start_time.isoformat(),
                'timeZone': 'Asia/Tokyo',
            },
            'end': {
                'dateTime': end_time.isoformat(),
                'timeZone': 'Asia/Tokyo',
            },
        }
        
        created_event = service.events().insert(
            calendarId=calendar_id,
            body=event
        ).execute()
        
        return created_event
    
    except HttpError as error:
        print(f"エラーが発生しました: {error}")
        return None


def list_events(calendar_id='primary', max_results=10, time_min=None, time_max=None):
    """
    Googleカレンダーからイベント一覧を取得
    
    Args:
        calendar_id: カレンダーID（デフォルト: 'primary'）
        max_results: 最大取得件数
        time_min: 開始時刻（ISO形式文字列）
        time_max: 終了時刻（ISO形式文字列）
    
    Returns:
        イベント一覧
    """
    try:
        credentials = get_credentials()
        service = build('calendar', 'v3', credentials=credentials)
        
        if not time_min:
            time_min = datetime.utcnow().isoformat() + 'Z'
        
        events_result = service.events().list(
            calendarId=calendar_id,
            timeMin=time_min,
            timeMax=time_max,
            maxResults=max_results,
            singleEvents=True,
            orderBy='startTime'
        ).execute()
        
        events = events_result.get('items', [])
        return events
    
    except HttpError as error:
        print(f"エラーが発生しました: {error}")
        return None


def list_calendars():
    """
    利用可能なカレンダー一覧を取得
    
    Returns:
        カレンダー一覧
    """
    try:
        credentials = get_credentials()
        service = build('calendar', 'v3', credentials=credentials)
        
        calendars_result = service.calendarList().list().execute()
        calendars = calendars_result.get('items', [])
        
        return calendars
    
    except HttpError as error:
        print(f"エラーが発生しました: {error}")
        return None


def main():
    """メイン関数"""
    if len(sys.argv) < 2:
        print("使用方法:")
        print("  python google_calendar.py create <summary> [start_time] [end_time] [description] [location]")
        print("  python google_calendar.py list [calendar_id] [max_results]")
        print("  python google_calendar.py calendars")
        print("\n例:")
        print("  python google_calendar.py create '会議' '2025-01-11T14:00:00' '2025-01-11T15:00:00'")
        print("  python google_calendar.py list primary 10")
        print("  python google_calendar.py calendars")
        sys.exit(1)
    
    command = sys.argv[1]
    
    if command == 'create':
        summary = sys.argv[2] if len(sys.argv) > 2 else '新しいイベント'
        start_time = sys.argv[3] if len(sys.argv) > 3 else None
        end_time = sys.argv[4] if len(sys.argv) > 4 else None
        description = sys.argv[5] if len(sys.argv) > 5 else ''
        location = sys.argv[6] if len(sys.argv) > 6 else ''
        
        event = create_event(
            summary=summary,
            start_time=start_time,
            end_time=end_time,
            description=description,
            location=location
        )
        
        if event:
            print(f"✅ イベントを作成しました: {event.get('summary')}")
            print(f"開始時刻: {event.get('start', {}).get('dateTime')}")
            print(f"終了時刻: {event.get('end', {}).get('dateTime')}")
            print(f"イベントID: {event.get('id')}")
            print(json.dumps(event, ensure_ascii=False, indent=2))
    
    elif command == 'list':
        calendar_id = sys.argv[2] if len(sys.argv) > 2 else 'primary'
        max_results = int(sys.argv[3]) if len(sys.argv) > 3 else 10
        
        events = list_events(calendar_id=calendar_id, max_results=max_results)
        
        if events:
            print(f"📅 イベント一覧（{len(events)}件）:")
            for event in events:
                start = event['start'].get('dateTime', event['start'].get('date'))
                print(f"  - {start} | {event.get('summary', 'タイトルなし')}")
        else:
            print("イベントが見つかりませんでした")
    
    elif command == 'calendars':
        calendars = list_calendars()
        
        if calendars:
            print("📅 利用可能なカレンダー:")
            for calendar in calendars:
                print(f"  - {calendar['summary']} ({calendar['id']})")
        else:
            print("カレンダーが見つかりませんでした")
    
    else:
        print(f"不明なコマンド: {command}")
        sys.exit(1)


if __name__ == '__main__':
    main()
