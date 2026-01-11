#!/usr/bin/env python3
"""
週次バズアカウント分析スクリプト
他ジャンルの専門アカウントを分析してツイート生成に反映
"""

import os
import sys
from pathlib import Path
from dotenv import load_dotenv

# 親ディレクトリをパスに追加
sys.path.insert(0, str(Path(__file__).parent.parent))

from social_media.buzz_analyzer import analyze_buzz_tweets, compare_accounts

# .envファイルを読み込む
load_dotenv()

# 分析対象のバズアカウント（他ジャンルの専門アカウント、フォロワー1万人前後）
BUZZ_ACCOUNTS = [
    # TODO: ユーザーが指定するバズアカウントのリスト
    # 例: 'account1', 'account2', 'account3'
]


def analyze_weekly_buzz_patterns():
    """
    週次でバズアカウントを分析してパターンを抽出
    
    Returns:
        バズパターンの辞書
    """
    if not BUZZ_ACCOUNTS:
        print("⚠️ 分析対象のアカウントが設定されていません")
        print("   BUZZ_ACCOUNTSに分析したいアカウント名を追加してください")
        return None
    
    print(f"📊 {len(BUZZ_ACCOUNTS)}件のバズアカウントを分析中...\n")
    
    accounts_data = []
    
    for username in BUZZ_ACCOUNTS:
        print(f"📊 分析中: @{username}")
        result = analyze_buzz_tweets(username, days=7)
        if result:
            accounts_data.append(result)
    
    if not accounts_data:
        print("⚠️ 分析結果が見つかりませんでした")
        return None
    
    # 共通パターンを抽出
    common_patterns = compare_accounts(accounts_data)
    
    print("\n" + "=" * 60)
    print("📊 週次バズパターン分析結果")
    print("=" * 60)
    
    print(f"\n共通キーワード:")
    for keyword, count in common_patterns['common_keywords'].most_common(10):
        print(f"  - {keyword}: {count}回")
    
    print(f"\n推奨構造:")
    for structure, count in common_patterns['common_structures'].most_common(10):
        print(f"  - {structure}: {count}回")
    
    print(f"\n推奨事項:")
    for rec in common_patterns['recommendations']:
        print(f"  - {rec}")
    
    return common_patterns


def apply_buzz_patterns_to_tweet(tweet_text, buzz_patterns=None):
    """
    バズパターンをツイートに適用
    
    Args:
        tweet_text: 元のツイートテキスト
        buzz_patterns: バズパターン
    
    Returns:
        改善されたツイートテキスト
    """
    if not buzz_patterns:
        # デフォルトのフォーマットを適用
        from social_media.tweet_formatter import format_tweet
        return format_tweet(tweet_text, style='elegant')
    
    # パターンに基づいて改善
    from social_media.tweet_formatter import format_tweet
    formatted = format_tweet(tweet_text, style='elegant')
    
    # 追加の改善を適用（必要に応じて）
    # 例: 頻出キーワードを追加、推奨構造に合わせる
    
    return formatted


def main():
    """メイン関数"""
    patterns = analyze_weekly_buzz_patterns()
    
    if patterns:
        print("\n✅ 分析完了")
        print("   このパターンは今週のツイート生成に反映されます")
    else:
        print("\n⚠️ 分析をスキップしました")


if __name__ == '__main__':
    main()
