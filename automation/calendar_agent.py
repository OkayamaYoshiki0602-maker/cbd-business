#!/usr/bin/env python3
"""
予定・TODO管理エージェント
Googleカレンダーと連携して、予定やTODOを管理し、ユーザーをマネージメントします。
"""

import os
import sys
import json
import re
from datetime import datetime, timedelta
from typing import Optional, List, Dict, Any
from pathlib import Path

# 既存のGoogleカレンダー機能をインポート
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from google_services.google_calendar import (
    create_event,
    list_events,
    list_calendars
)


class CalendarAgent:
    """予定・TODO管理エージェント"""
    
    def __init__(self, calendar_id=None, user_email='okayamayoshiki0602o@gmail.com'):
        """
        初期化
        
        Args:
            calendar_id: 使用するカレンダーID（Noneの場合は自動検出）
            user_email: ユーザーのメールアドレス
        """
        self.user_email = user_email
        self.todo_file = Path.home() / '.config' / 'cursor' / 'todos.json'
        self.todo_file.parent.mkdir(parents=True, exist_ok=True)
        self._load_todos()
        
        # カレンダーIDの設定
        if calendar_id:
            self.calendar_id = calendar_id
        else:
            # ユーザーのメールアドレスをカレンダーIDとして使用
            # サービスアカウントが共有されたカレンダーにアクセスする場合
            # 共有設定が完了していれば、メールアドレスがカレンダーIDとして機能する
            self.calendar_id = user_email
    
    def _load_todos(self):
        """TODOリストを読み込む"""
        if self.todo_file.exists():
            with open(self.todo_file, 'r', encoding='utf-8') as f:
                self.todos = json.load(f)
        else:
            self.todos = []
    
    def _save_todos(self):
        """TODOリストを保存する"""
        with open(self.todo_file, 'w', encoding='utf-8') as f:
            json.dump(self.todos, f, ensure_ascii=False, indent=2)
    
    def parse_datetime(self, text: str) -> Optional[Dict[str, Any]]:
        """
        自然言語から日時を解析
        
        Args:
            text: 日時を含むテキスト（例: "今月31日の午前中"、"来週の月曜日10時"）
        
        Returns:
            {'start': datetime, 'end': datetime} または None
        """
        now = datetime.now()
        text = text.strip()
        
        # パターン1: "今月X日" または "X月X日"
        match = re.search(r'今月(\d+)日|(\d+)月(\d+)日', text)
        if match:
            if match.group(1):  # 今月X日
                day = int(match.group(1))
                start = now.replace(day=day, hour=9, minute=0, second=0, microsecond=0)
            else:  # X月X日
                month = int(match.group(2))
                day = int(match.group(3))
                year = now.year
                if month < now.month:
                    year += 1
                start = datetime(year, month, day, 9, 0, 0)
            
            # 午前中、午後、夜などの判定
            if '午前' in text or '午前中' in text:
                start = start.replace(hour=9, minute=0)
                end = start.replace(hour=12, minute=0)
            elif '午後' in text:
                start = start.replace(hour=13, minute=0)
                end = start.replace(hour=17, minute=0)
            elif '夜' in text or '夕方' in text:
                start = start.replace(hour=18, minute=0)
                end = start.replace(hour=21, minute=0)
            else:
                # デフォルト: 1時間
                end = start + timedelta(hours=1)
            
            return {'start': start, 'end': end}
        
        # パターン2: "来週のX曜日"
        weekdays = ['月', '火', '水', '木', '金', '土', '日']
        match = re.search(r'来週の([月火水木金土日])曜日', text)
        if match:
            target_weekday = weekdays.index(match.group(1))
            days_ahead = target_weekday - now.weekday() + 7
            start = now + timedelta(days=days_ahead)
            start = start.replace(hour=10, minute=0, second=0, microsecond=0)
            end = start + timedelta(hours=1)
            return {'start': start, 'end': end}
        
        # パターン3: "X時" または "X時X分"
        match = re.search(r'(\d+)時(?:(\d+)分)?', text)
        if match:
            hour = int(match.group(1))
            minute = int(match.group(2)) if match.group(2) else 0
            start = now.replace(hour=hour, minute=minute, second=0, microsecond=0)
            if start < now:
                start += timedelta(days=1)
            end = start + timedelta(hours=1)
            return {'start': start, 'end': end}
        
        # パターン4: "明日"、"明後日"
        if '明日' in text:
            start = (now + timedelta(days=1)).replace(hour=10, minute=0, second=0, microsecond=0)
            end = start + timedelta(hours=1)
            return {'start': start, 'end': end}
        
        if '明後日' in text:
            start = (now + timedelta(days=2)).replace(hour=10, minute=0, second=0, microsecond=0)
            end = start + timedelta(hours=1)
            return {'start': start, 'end': end}
        
        return None
    
    def find_user_calendar(self) -> Optional[str]:
        """
        ユーザーのカレンダーIDを検索
        
        Returns:
            カレンダーID、見つからない場合はNone
        """
        try:
            calendars = list_calendars()
            if calendars:
                # ユーザーのメールアドレスに一致するカレンダーを探す
                for calendar in calendars:
                    if calendar.get('id') == self.user_email:
                        return calendar['id']
                    # summaryにユーザー名が含まれている場合
                    if 'summary' in calendar and self.user_email.split('@')[0] in calendar['summary'].lower():
                        return calendar['id']
                # 見つからない場合は最初のカレンダーを返す
                return calendars[0].get('id')
        except Exception as e:
            print(f"カレンダー検索エラー: {e}")
        return None
    
    def add_event(self, summary: str, datetime_text: Optional[str] = None, 
                  description: str = '', location: str = '') -> Dict[str, Any]:
        """
        予定を追加
        
        Args:
            summary: 予定のタイトル
            datetime_text: 日時を表す自然言語（例: "今月31日の午前中"）
            description: 説明
            location: 場所
        
        Returns:
            作成されたイベントの情報
        """
        start_time = None
        end_time = None
        
        if datetime_text:
            parsed = self.parse_datetime(datetime_text)
            if parsed:
                start_time = parsed['start']
                end_time = parsed['end']
        
        # カレンダーIDを確認・取得
        calendar_id = self.calendar_id
        if calendar_id == self.user_email:
            # 実際のカレンダーIDを検索
            found_id = self.find_user_calendar()
            if found_id:
                calendar_id = found_id
        
        event = create_event(
            calendar_id=calendar_id,
            summary=summary,
            start_time=start_time,
            end_time=end_time,
            description=description,
            location=location
        )
        
        return event
    
    def list_upcoming_events(self, days: int = 7, max_results: int = 10) -> List[Dict[str, Any]]:
        """
        今後の予定を取得
        
        Args:
            days: 何日先まで取得するか
            max_results: 最大取得件数
        
        Returns:
            イベント一覧
        """
        # UTC時刻でISO形式（'Z'付き）に変換
        time_min = datetime.utcnow().isoformat() + 'Z'
        time_max = (datetime.utcnow() + timedelta(days=days)).isoformat() + 'Z'
        
        events = list_events(
            calendar_id=self.calendar_id,
            max_results=max_results,
            time_min=time_min,
            time_max=time_max
        )
        
        return events or []
    
    def add_todo(self, title: str, priority: str = 'medium', 
                 due_date: Optional[str] = None, description: str = '') -> Dict[str, Any]:
        """
        TODOを追加
        
        Args:
            title: TODOのタイトル
            priority: 優先度（'high', 'medium', 'low'）
            due_date: 期限（ISO形式文字列）
            description: 説明
        
        Returns:
            作成されたTODOの情報
        """
        todo = {
            'id': len(self.todos) + 1,
            'title': title,
            'priority': priority,
            'due_date': due_date,
            'description': description,
            'status': 'pending',
            'created_at': datetime.now().isoformat(),
            'completed_at': None
        }
        
        self.todos.append(todo)
        self._save_todos()
        
        return todo
    
    def list_todos(self, status: Optional[str] = None, 
                   priority: Optional[str] = None) -> List[Dict[str, Any]]:
        """
        TODO一覧を取得
        
        Args:
            status: フィルタ（'pending', 'completed'）
            priority: 優先度フィルタ
        
        Returns:
            TODO一覧
        """
        todos = self.todos.copy()
        
        if status:
            todos = [t for t in todos if t['status'] == status]
        
        if priority:
            todos = [t for t in todos if t['priority'] == priority]
        
        # 優先度順にソート
        priority_order = {'high': 0, 'medium': 1, 'low': 2}
        todos.sort(key=lambda x: (priority_order.get(x['priority'], 3), x['created_at']))
        
        return todos
    
    def complete_todo(self, todo_id: int) -> bool:
        """
        TODOを完了にする
        
        Args:
            todo_id: TODOのID
        
        Returns:
            成功したかどうか
        """
        for todo in self.todos:
            if todo['id'] == todo_id:
                todo['status'] = 'completed'
                todo['completed_at'] = datetime.now().isoformat()
                self._save_todos()
                return True
        return False
    
    def delete_todo(self, todo_id: int) -> bool:
        """
        TODOを削除
        
        Args:
            todo_id: TODOのID
        
        Returns:
            成功したかどうか
        """
        for i, todo in enumerate(self.todos):
            if todo['id'] == todo_id:
                del self.todos[i]
                self._save_todos()
                return True
        return False
    
    def get_summary(self, days: int = 7) -> str:
        """
        予定とTODOのサマリーを取得
        
        Args:
            days: 何日先まで表示するか
        
        Returns:
            サマリーテキスト
        """
        events = self.list_upcoming_events(days=days)
        todos = self.list_todos(status='pending')
        
        summary = f"📅 今後{days}日間の予定とTODO\n\n"
        
        if events:
            summary += "【予定】\n"
            for event in events:
                start = event.get('start', {}).get('dateTime', event.get('start', {}).get('date', ''))
                summary += f"  • {start} | {event.get('summary', 'タイトルなし')}\n"
        else:
            summary += "【予定】\n  予定はありません\n"
        
        summary += "\n"
        
        if todos:
            summary += "【TODO】\n"
            for todo in todos:
                priority_emoji = {'high': '🔴', 'medium': '🟡', 'low': '🟢'}.get(todo['priority'], '⚪')
                summary += f"  {priority_emoji} [{todo['id']}] {todo['title']}"
                if todo['due_date']:
                    summary += f" (期限: {todo['due_date']})"
                summary += "\n"
        else:
            summary += "【TODO】\n  TODOはありません\n"
        
        return summary


def main():
    """メイン関数（CLIインターフェース）"""
    agent = CalendarAgent()
    
    if len(sys.argv) < 2:
        print("使用方法:")
        print("  python calendar_agent.py add_event <タイトル> [日時] [説明]")
        print("  python calendar_agent.py list_events [日数]")
        print("  python calendar_agent.py add_todo <タイトル> [優先度] [期限]")
        print("  python calendar_agent.py list_todos [status] [priority]")
        print("  python calendar_agent.py complete_todo <ID>")
        print("  python calendar_agent.py delete_todo <ID>")
        print("  python calendar_agent.py summary [日数]")
        print("\n例:")
        print("  python calendar_agent.py add_event '会議' '今月31日の午前中'")
        print("  python calendar_agent.py add_todo 'レポート作成' high '2026-01-15'")
        print("  python calendar_agent.py summary 7")
        sys.exit(1)
    
    command = sys.argv[1]
    
    if command == 'add_event':
        summary = sys.argv[2] if len(sys.argv) > 2 else '新しい予定'
        datetime_text = sys.argv[3] if len(sys.argv) > 3 else None
        description = sys.argv[4] if len(sys.argv) > 4 else ''
        
        event = agent.add_event(summary, datetime_text, description)
        if event:
            print(f"✅ 予定を作成しました: {event.get('summary')}")
            print(f"開始時刻: {event.get('start', {}).get('dateTime')}")
            print(f"終了時刻: {event.get('end', {}).get('dateTime')}")
        else:
            print("❌ 予定の作成に失敗しました")
    
    elif command == 'list_events':
        days = int(sys.argv[2]) if len(sys.argv) > 2 else 7
        events = agent.list_upcoming_events(days=days)
        
        if events:
            print(f"📅 今後{days}日間の予定（{len(events)}件）:")
            for event in events:
                start = event.get('start', {}).get('dateTime', event.get('start', {}).get('date', ''))
                print(f"  • {start} | {event.get('summary', 'タイトルなし')}")
        else:
            print("予定はありません")
    
    elif command == 'add_todo':
        title = sys.argv[2] if len(sys.argv) > 2 else '新しいTODO'
        priority = sys.argv[3] if len(sys.argv) > 3 else 'medium'
        due_date = sys.argv[4] if len(sys.argv) > 4 else None
        
        todo = agent.add_todo(title, priority, due_date)
        print(f"✅ TODOを追加しました: [{todo['id']}] {todo['title']}")
    
    elif command == 'list_todos':
        status = sys.argv[2] if len(sys.argv) > 2 else None
        priority = sys.argv[3] if len(sys.argv) > 3 else None
        
        todos = agent.list_todos(status, priority)
        
        if todos:
            print(f"📝 TODO一覧（{len(todos)}件）:")
            for todo in todos:
                priority_emoji = {'high': '🔴', 'medium': '🟡', 'low': '🟢'}.get(todo['priority'], '⚪')
                status_emoji = '✅' if todo['status'] == 'completed' else '⏳'
                print(f"  {status_emoji} {priority_emoji} [{todo['id']}] {todo['title']}")
                if todo['due_date']:
                    print(f"      期限: {todo['due_date']}")
        else:
            print("TODOはありません")
    
    elif command == 'complete_todo':
        todo_id = int(sys.argv[2]) if len(sys.argv) > 2 else None
        if todo_id and agent.complete_todo(todo_id):
            print(f"✅ TODO [{todo_id}] を完了にしました")
        else:
            print(f"❌ TODO [{todo_id}] が見つかりませんでした")
    
    elif command == 'delete_todo':
        todo_id = int(sys.argv[2]) if len(sys.argv) > 2 else None
        if todo_id and agent.delete_todo(todo_id):
            print(f"✅ TODO [{todo_id}] を削除しました")
        else:
            print(f"❌ TODO [{todo_id}] が見つかりませんでした")
    
    elif command == 'summary':
        days = int(sys.argv[2]) if len(sys.argv) > 2 else 7
        print(agent.get_summary(days=days))
    
    else:
        print(f"不明なコマンド: {command}")
        sys.exit(1)


if __name__ == '__main__':
    main()
