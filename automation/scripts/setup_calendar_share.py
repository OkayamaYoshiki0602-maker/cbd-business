#!/usr/bin/env python3
"""
Googleカレンダー共有設定支援スクリプト
ユーザーにカレンダー共有設定の手順を表示します。
"""

import sys

def print_setup_instructions():
    """カレンダー共有設定の手順を表示"""
    print("=" * 60)
    print("Googleカレンダー共有設定手順")
    print("=" * 60)
    print()
    print("サービスアカウントがあなたのカレンダーにアクセスできるように、")
    print("カレンダーを共有する必要があります。")
    print()
    print("【手順】")
    print()
    print("1. Googleカレンダーにアクセス")
    print("   https://calendar.google.com")
    print("   ログイン: okayamayoshiki0602o@gmail.com")
    print()
    print("2. 「マイカレンダー」から「岡山純樹」カレンダーを選択")
    print("   - 左側の「マイカレンダー」セクションから「岡山純樹」をクリック")
    print()
    print("3. カレンダー名の右側にある「⋮」（三点リーダー）をクリック")
    print()
    print("4. 「設定と共有」をクリック")
    print()
    print("5. 「特定のユーザーと共有」セクションにスクロール")
    print()
    print("6. 「ユーザーを追加」をクリック")
    print()
    print("7. 以下のメールアドレスを入力:")
    print("   cursor-mcp@acoustic-skein-329303.iam.gserviceaccount.com")
    print()
    print("8. 権限を選択:")
    print("   「変更可能なイベントを表示」を選択（推奨）")
    print()
    print("9. 「送信」をクリック")
    print()
    print("=" * 60)
    print("設定完了後、このエージェントがあなたのカレンダーに予定を追加できます。")
    print("=" * 60)
    print()
    print("設定が完了したら、以下を実行して確認してください:")
    print("  python3 automation/calendar_agent.py add_event 'テスト' '明日10時'")


if __name__ == '__main__':
    print_setup_instructions()
