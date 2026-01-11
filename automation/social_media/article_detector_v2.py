#!/usr/bin/env python3
"""
記事検知スクリプト（v2: 新しい方向性に合わせた改善版）
新しいスプレッドシート構造に対応（ペルソナ・引き付け期待列を追加）
"""

import os
import sys
from datetime import datetime
from pathlib import Path
from dotenv import load_dotenv

# 親ディレクトリをパスに追加
sys.path.insert(0, str(Path(__file__).parent.parent))

from google_services.google_sheets import read_spreadsheet, write_spreadsheet

# .envファイルを読み込む
load_dotenv()

APPROVAL_SPREADSHEET_ID = os.getenv('APPROVAL_SPREADSHEET_ID', '')


def add_to_approval_queue_v2(article_title, tweet_text, article_url=None, source='wordpress', content_type=None, persona=None, engagement=None):
    """
    承認待ちリストに追加（v2: 新しいスプレッドシート構造に対応）
    
    Args:
        article_title: 記事タイトル
        tweet_text: ツイート文案
        article_url: 記事URL
        source: ソース（wordpress / news / scheduled）
        content_type: コンテンツタイプ（data_analysis / lifestyle / other）
        persona: ペルソナ
        engagement: 引き付け期待（ゴール：サイト遷移）
    
    Returns:
        追加結果
    """
    if not APPROVAL_SPREADSHEET_ID:
        print("⚠️ APPROVAL_SPREADSHEET_IDが設定されていません。")
        return False
    
    try:
        # スプレッドシートを読み込む
        approval_data = read_spreadsheet(APPROVAL_SPREADSHEET_ID, 'シート1!A1:I1000')
        
        # ヘッダー行を確認
        headers = [
            'タイムスタンプ',
            'ステータス',
            '記事タイトル',
            'ツイート文案',
            'URL',
            'ソース',
            'コンテンツタイプ',
            'ペルソナ',
            '引き付け期待（ゴール：サイト遷移）'
        ]
        
        if not approval_data:
            # ヘッダー行を作成
            range_name = 'シート1!A1'
            write_spreadsheet(APPROVAL_SPREADSHEET_ID, range_name, [headers])
            approval_data = [headers]
        elif len(approval_data[0]) < 9:
            # ヘッダー行が不完全な場合は更新
            range_name = 'シート1!A1'
            write_spreadsheet(APPROVAL_SPREADSHEET_ID, range_name, [headers])
            approval_data[0] = headers
        
        # 重複チェック
        today = datetime.now().date().isoformat()
        if len(approval_data) > 1:
            for row in approval_data[1:]:
                if len(row) >= 3:
                    existing_timestamp = row[0] if row[0] else ''
                    existing_title = row[2] if len(row) > 2 else ''
                    existing_source = row[5] if len(row) > 5 else ''
                    
                    if existing_timestamp.startswith(today) and existing_title == article_title and existing_source == source:
                        print(f"⚠️ 重複エントリーを検出しました（スキップ）")
                        return False
        
        # 新しい行を追加
        new_row = [
            datetime.now().isoformat(),
            '下書き',
            article_title,
            tweet_text,
            article_url or '',
            source,
            content_type or '',
            persona or '',
            engagement or ''
        ]
        
        # スプレッドシートに書き込み
        next_row = len(approval_data) + 1
        range_name = f'シート1!A{next_row}'
        result = write_spreadsheet(APPROVAL_SPREADSHEET_ID, range_name, [new_row])
        
        if result:
            print(f"✅ 承認待ちリストに追加しました（行{next_row}）")
            return True
        else:
            print("❌ スプレッドシートへの書き込みに失敗しました")
            return False
    
    except Exception as e:
        print(f"❌ エラーが発生しました: {e}")
        import traceback
        traceback.print_exc()
        return False
