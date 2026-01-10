#!/usr/bin/env python3
"""
承認待ちリスト管理スクリプト
スプレッドシートで承認待ちリストを管理
"""

import os
import sys
import json
from datetime import datetime
from pathlib import Path
from dotenv import load_dotenv

# 親ディレクトリをパスに追加
sys.path.insert(0, str(Path(__file__).parent.parent))

from google_services.google_sheets import read_spreadsheet, write_spreadsheet

# .envファイルを読み込む
load_dotenv()

# スプレッドシートID
APPROVAL_SPREADSHEET_ID = os.getenv('APPROVAL_SPREADSHEET_ID', '')


def list_pending_approvals():
    """
    承認待ちリストを取得
    
    Returns:
        承認待ちリスト
    """
    if not APPROVAL_SPREADSHEET_ID:
        print("⚠️ APPROVAL_SPREADSHEET_IDが設定されていません。")
        return []
    
    try:
        # 承認待ちリストを読み込む（シート名は「シート1」を使用）
        data = read_spreadsheet(APPROVAL_SPREADSHEET_ID, 'シート1!A2:Z1000')
        
        if not data:
            return []
        
        pending = []
        for i, row in enumerate(data, start=2):
            if len(row) >= 6 and row[1] in ['下書き', '承認待ち']:  # 下書きと承認待ちの両方を表示
                pending.append({
                    'row': i,
                    'timestamp': row[0] if len(row) > 0 else '',
                    'status': row[1] if len(row) > 1 else '',
                    'title': row[2] if len(row) > 2 else '',
                    'tweet_text': row[3] if len(row) > 3 else '',
                    'url': row[4] if len(row) > 4 else '',
                    'source': row[5] if len(row) > 5 else '',
                })
        
        return pending
    
    except Exception as e:
        print(f"❌ エラーが発生しました: {e}")
        return []


def approve_tweet(row_number):
    """
    承認待ちリストのステータスを「承認済み」に変更
    
    Args:
        row_number: 行番号
    
    Returns:
        更新結果
    """
    if not APPROVAL_SPREADSHEET_ID:
        print("⚠️ APPROVAL_SPREADSHEET_IDが設定されていません。")
        return False
    
    try:
        # ステータスを「承認済み」に更新（シート名は「シート1」を使用）
        range_name = f'シート1!B{row_number}'
        result = write_spreadsheet(APPROVAL_SPREADSHEET_ID, range_name, [['承認済み']])
        
        if result:
            print(f"✅ 行{row_number}を承認済みに更新しました")
            return True
        else:
            print("❌ ステータスの更新に失敗しました")
            return False
    
    except Exception as e:
        print(f"❌ エラーが発生しました: {e}")
        return False


def get_approved_tweets():
    """
    承認済みツイートを取得
    
    Returns:
        承認済みツイートのリスト
    """
    if not APPROVAL_SPREADSHEET_ID:
        print("⚠️ APPROVAL_SPREADSHEET_IDが設定されていません。")
        return []
    
    try:
        # 承認待ちリストを読み込む（シート名は「シート1」を使用）
        data = read_spreadsheet(APPROVAL_SPREADSHEET_ID, 'シート1!A2:Z1000')
        
        if not data:
            return []
        
        approved = []
        for i, row in enumerate(data, start=2):
            if len(row) >= 6 and row[1] == '承認済み':
                approved.append({
                    'row': i,
                    'timestamp': row[0] if len(row) > 0 else '',
                    'status': row[1] if len(row) > 1 else '',
                    'title': row[2] if len(row) > 2 else '',
                    'tweet_text': row[3] if len(row) > 3 else '',
                    'url': row[4] if len(row) > 4 else '',
                    'source': row[5] if len(row) > 5 else '',
                })
        
        return approved
    
    except Exception as e:
        print(f"❌ エラーが発生しました: {e}")
        return []


def main():
    """メイン関数"""
    if len(sys.argv) < 2:
        print("使用方法:")
        print("  python approval_manager.py list")
        print("  python approval_manager.py approve <行番号>")
        print("  python approval_manager.py approved")
        print("\n例:")
        print("  python approval_manager.py list")
        print("  python approval_manager.py approve 2")
        print("  python approval_manager.py approved")
        sys.exit(1)
    
    command = sys.argv[1]
    
    if command == 'list':
        # 承認待ちリストを表示
        pending = list_pending_approvals()
        
        if not pending:
            print("📋 承認待ちリストは空です")
        else:
            print(f"📋 承認待ちリスト（{len(pending)}件）:")
            print("=" * 60)
            for item in pending:
                print(f"\n行{item['row']}: {item['title']}")
                print(f"  ツイート文案: {item['tweet_text'][:50]}...")
                print(f"  URL: {item['url']}")
                print(f"  ソース: {item['source']}")
                print(f"  タイムスタンプ: {item['timestamp']}")
    
    elif command == 'approve':
        if len(sys.argv) < 3:
            print("エラー: 行番号が必要です")
            sys.exit(1)
        
        row_number = int(sys.argv[2])
        approve_tweet(row_number)
    
    elif command == 'approved':
        # 承認済みリストを表示
        approved = get_approved_tweets()
        
        if not approved:
            print("📋 承認済みリストは空です")
        else:
            print(f"📋 承認済みリスト（{len(approved)}件）:")
            print("=" * 60)
            for item in approved:
                print(f"\n行{item['row']}: {item['title']}")
                print(f"  ツイート文案: {item['tweet_text'][:50]}...")
                print(f"  URL: {item['url']}")
                print(f"  タイムスタンプ: {item['timestamp']}")
    
    else:
        print(f"不明なコマンド: {command}")
        sys.exit(1)


if __name__ == '__main__':
    main()
