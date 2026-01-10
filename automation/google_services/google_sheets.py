#!/usr/bin/env python3
"""
Google Sheets操作スクリプト
Googleスプレッドシートからデータを読み込む
"""

import os
import sys
import json
from pathlib import Path
from google.oauth2 import service_account
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError


# 認証情報ファイルのパス
CREDENTIALS_FILE = os.path.expanduser("~/.config/cursor/google-drive-credentials.json")

# スコープ
SCOPES = [
    'https://www.googleapis.com/auth/spreadsheets.readonly',
    'https://www.googleapis.com/auth/drive.readonly'
]


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


def read_spreadsheet(spreadsheet_id, range_name='Sheet1!A1:Z1000'):
    """
    Googleスプレッドシートからデータを読み込む
    
    Args:
        spreadsheet_id: スプレッドシートID
        range_name: 読み込む範囲（例: 'Sheet1!A1:D10'）
    
    Returns:
        データのリスト
    """
    try:
        credentials = get_credentials()
        service = build('sheets', 'v4', credentials=credentials)
        
        result = service.spreadsheets().values().get(
            spreadsheetId=spreadsheet_id,
            range=range_name
        ).execute()
        
        values = result.get('values', [])
        return values
    
    except HttpError as error:
        print(f"エラーが発生しました: {error}")
        return None


def write_spreadsheet(spreadsheet_id, range_name, values):
    """
    Googleスプレッドシートにデータを書き込む
    
    Args:
        spreadsheet_id: スプレッドシートID
        range_name: 書き込む範囲（例: 'Sheet1!A1'）
        values: 書き込むデータ（2次元リスト）
    
    Returns:
        成功した場合はTrue
    """
    try:
        credentials = get_credentials()
        service = build('sheets', 'v4', credentials=credentials)
        
        body = {
            'values': values
        }
        
        result = service.spreadsheets().values().update(
            spreadsheetId=spreadsheet_id,
            range=range_name,
            valueInputOption='RAW',
            body=body
        ).execute()
        
        print(f"{result.get('updatedCells')} セルが更新されました")
        return True
    
    except HttpError as error:
        print(f"エラーが発生しました: {error}")
        return False


def create_sheet(spreadsheet_id, sheet_title):
    """
    スプレッドシートに新しいシートを作成
    
    Args:
        spreadsheet_id: スプレッドシートID
        sheet_title: 新しいシートのタイトル
    
    Returns:
        作成されたシートの情報
    """
    try:
        credentials = get_credentials()
        service = build('sheets', 'v4', credentials=credentials)
        
        request = {
            'requests': [{
                'addSheet': {
                    'properties': {
                        'title': sheet_title
                    }
                }
            }]
        }
        
        response = service.spreadsheets().batchUpdate(
            spreadsheetId=spreadsheet_id,
            body=request
        ).execute()
        
        added_sheet = response.get('replies', [])[0].get('addSheet', {}).get('properties', {})
        return added_sheet
    
    except HttpError as error:
        print(f"エラーが発生しました: {error}")
        return None


def list_sheets(spreadsheet_id):
    """
    スプレッドシート内のシート一覧を取得
    
    Args:
        spreadsheet_id: スプレッドシートID
    
    Returns:
        シート一覧
    """
    try:
        credentials = get_credentials()
        service = build('sheets', 'v4', credentials=credentials)
        
        spreadsheet = service.spreadsheets().get(
            spreadsheetId=spreadsheet_id
        ).execute()
        
        sheets = spreadsheet.get('sheets', [])
        return sheets
    
    except HttpError as error:
        print(f"エラーが発生しました: {error}")
        return None


def list_spreadsheets(query='', max_results=10):
    """
    Google Driveからスプレッドシート一覧を取得
    
    Args:
        query: 検索クエリ（例: "name contains 'CBD'")
        max_results: 最大取得件数
    
    Returns:
        スプレッドシート一覧
    """
    try:
        credentials = get_credentials()
        drive_service = build('drive', 'v3', credentials=credentials)
        
        query_string = "mimeType='application/vnd.google-apps.spreadsheet'"
        if query:
            query_string += f" and {query}"
        
        results = drive_service.files().list(
            q=query_string,
            pageSize=max_results,
            fields="files(id, name, createdTime, modifiedTime)"
        ).execute()
        
        files = results.get('files', [])
        return files
    
    except HttpError as error:
        print(f"エラーが発生しました: {error}")
        return []


def main():
    """メイン関数"""
    if len(sys.argv) < 2:
        print("使用方法:")
        print("  python google_sheets.py read <spreadsheet_id> [range]")
        print("  python google_sheets.py write <spreadsheet_id> <range> <data_json>")
        print("  python google_sheets.py list [query]")
        print("\n例:")
        print("  python google_sheets.py read 1BxiMVs0XRA5nFMdKvBdBZjgmUUqptlbs74OgvE2upms")
        print("  python google_sheets.py list \"name contains 'CBD'\"")
        sys.exit(1)
    
    command = sys.argv[1]
    
    if command == 'read':
        if len(sys.argv) < 3:
            print("エラー: スプレッドシートIDが必要です")
            sys.exit(1)
        
        spreadsheet_id = sys.argv[2]
        range_name = sys.argv[3] if len(sys.argv) > 3 else 'Sheet1!A1:Z1000'
        
        data = read_spreadsheet(spreadsheet_id, range_name)
        if data:
            print(json.dumps(data, ensure_ascii=False, indent=2))
    
    elif command == 'write':
        if len(sys.argv) < 5:
            print("エラー: スプレッドシートID、範囲、データが必要です")
            sys.exit(1)
        
        spreadsheet_id = sys.argv[2]
        range_name = sys.argv[3]
        data_json = sys.argv[4]
        
        try:
            values = json.loads(data_json)
            write_spreadsheet(spreadsheet_id, range_name, values)
        except json.JSONDecodeError:
            print("エラー: データがJSON形式ではありません")
            sys.exit(1)
    
    elif command == 'list':
        query = sys.argv[2] if len(sys.argv) > 2 else ''
        files = list_spreadsheets(query)
        
        if files:
            for file in files:
                print(f"{file['name']} ({file['id']})")
        else:
            print("スプレッドシートが見つかりませんでした")
    
    else:
        print(f"不明なコマンド: {command}")
        sys.exit(1)


if __name__ == '__main__':
    main()
