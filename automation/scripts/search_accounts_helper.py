#!/usr/bin/env python3
"""
バズアカウント検索ヘルパー
手動で見つけたアカウントを記録・分析するためのヘルパースクリプト
"""

import os
import sys
from pathlib import Path
from dotenv import load_dotenv

# 親ディレクトリをパスに追加
sys.path.insert(0, str(Path(__file__).parent.parent))

from social_media.advanced_buzz_analyzer import analyze_advanced_buzz_account

# .envファイルを読み込む
load_dotenv()


def validate_account(username):
    """
    アカウントを検証（フォロワー数などを確認）
    
    Args:
        username: アカウント名（@なし）
    
    Returns:
        検証結果
    """
    try:
        from social_media.x_twitter import get_twitter_client
        
        client = get_twitter_client()
        user = client.get_user(username=username)
        
        if not user.data:
            return {'valid': False, 'error': 'アカウントが見つかりません'}
        
        follower_count = user.data.public_metrics.get('followers_count', 0) if user.data.public_metrics else 0
        
        # フォロワー数のチェック（1万〜10万人）
        if follower_count < 10000:
            return {
                'valid': False,
                'error': f'フォロワー数が少なすぎます（{follower_count:,}人）',
                'follower_count': follower_count
            }
        elif follower_count > 100000:
            return {
                'valid': False,
                'error': f'フォロワー数が多すぎます（{follower_count:,}人）',
                'follower_count': follower_count
            }
        else:
            return {
                'valid': True,
                'follower_count': follower_count,
                'username': username
            }
    
    except Exception as e:
        return {'valid': False, 'error': str(e)}


def interactive_account_selection():
    """
    インタラクティブにアカウントを選択・検証
    """
    print("=" * 60)
    print("バズアカウント検索ヘルパー")
    print("=" * 60)
    print("\n手動でX (Twitter)で検索して見つけたアカウントを入力してください。")
    print("条件: フォロワー1万〜10万人、アフィリエイト・商品紹介をしている専門アカウント\n")
    
    accounts = []
    
    while len(accounts) < 10:
        username = input(f"アカウント名を入力（@{len(accounts)+1}/10、空欄で終了）: ").strip().replace('@', '')
        
        if not username:
            break
        
        print(f"\n🔍 検証中: @{username}")
        validation = validate_account(username)
        
        if validation['valid']:
            print(f"✅ 有効: フォロワー数 {validation['follower_count']:,}人")
            
            # ジャンルを入力
            genre = input("  ジャンル（例: 健康・サプリ、美容・コスメ、投資・金融）: ").strip()
            
            accounts.append({
                'username': username,
                'follower_count': validation['follower_count'],
                'genre': genre
            })
            
            print(f"✅ 追加しました（{len(accounts)}/10）\n")
        else:
            print(f"❌ エラー: {validation.get('error', '不明なエラー')}")
            if validation.get('follower_count'):
                print(f"   フォロワー数: {validation['follower_count']:,}人")
            retry = input("  続行しますか？ (y/n): ").strip().lower()
            if retry != 'y':
                continue
            print()
    
    if not accounts:
        print("\n⚠️ アカウントが追加されませんでした")
        return
    
    print("\n" + "=" * 60)
    print("追加されたアカウント一覧")
    print("=" * 60)
    
    for i, account in enumerate(accounts, 1):
        print(f"{i}. @{account['username']}")
        print(f"   フォロワー: {account['follower_count']:,}人")
        print(f"   ジャンル: {account.get('genre', '未設定')}")
        print()
    
    # weekly_buzz_analyzer.pyへの追加を提案
    print("=" * 60)
    print("次のステップ")
    print("=" * 60)
    print("\n以下のコードを `automation/social_media/weekly_buzz_analyzer.py` の")
    print("`BUZZ_ACCOUNTS` に追加してください:\n")
    
    print("BUZZ_ACCOUNTS = [")
    for account in accounts:
        genre_comment = f"  # {account.get('genre', '')}" if account.get('genre') else ""
        print(f"    '{account['username']}',{genre_comment}")
    print("]")
    
    # 分析を実行するか確認
    analyze = input("\n今すぐ分析を実行しますか？ (y/n): ").strip().lower()
    if analyze == 'y':
        print("\n📊 分析を開始します...\n")
        
        from social_media.weekly_buzz_analyzer import analyze_weekly_buzz_patterns
        # 一時的にアカウントリストを設定
        import automation.social_media.weekly_buzz_analyzer as weekly_module
        weekly_module.BUZZ_ACCOUNTS = [acc['username'] for acc in accounts]
        
        patterns = analyze_weekly_buzz_patterns(use_advanced=True)
        
        if patterns:
            print("\n✅ 分析完了")


def main():
    """メイン関数"""
    if len(sys.argv) > 1:
        # コマンドライン引数でアカウントを指定
        usernames = [u.replace('@', '') for u in sys.argv[1:]]
        
        print(f"🔍 {len(usernames)}件のアカウントを検証中...\n")
        
        valid_accounts = []
        for username in usernames:
            validation = validate_account(username)
            if validation['valid']:
                print(f"✅ @{username}: {validation['follower_count']:,}フォロワー")
                valid_accounts.append(username)
            else:
                print(f"❌ @{username}: {validation.get('error', '不明なエラー')}")
        
        if valid_accounts:
            print(f"\n✅ {len(valid_accounts)}件の有効なアカウントが見つかりました")
            print("\n以下のコードを `automation/social_media/weekly_buzz_analyzer.py` の")
            print("`BUZZ_ACCOUNTS` に追加してください:\n")
            print("BUZZ_ACCOUNTS = [")
            for username in valid_accounts:
                print(f"    '{username}',")
            print("]")
    else:
        # インタラクティブモード
        interactive_account_selection()


if __name__ == '__main__':
    main()
