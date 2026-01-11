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
from social_media.advanced_buzz_analyzer import analyze_advanced_buzz_account, compare_advanced_accounts

# .envファイルを読み込む
load_dotenv()

# 分析対象のバズアカウント（他ジャンルの専門アカウント、フォロワー1万〜10万人）
# 選定条件: ニッチな専門アカウント、アフィリエイト・商品紹介をしている
BUZZ_ACCOUNTS = [
    # TODO: ユーザーが指定するバズアカウントのリスト（最大10件）
    # 例: 
    # 'username1',  # 健康・サプリ系
    # 'username2',  # 美容・コスメ系
    # 'username3',  # 投資・金融系
]


def analyze_weekly_buzz_patterns(use_advanced=True):
    """
    週次でバズアカウントを分析してパターンを抽出（高度な分析対応）
    
    Args:
        use_advanced: 高度な分析を使用するか（頻度、マネタイズ、構成を詳細分析）
    
    Returns:
        バズパターンの辞書
    """
    if not BUZZ_ACCOUNTS:
        print("⚠️ 分析対象のアカウントが設定されていません")
        print("   BUZZ_ACCOUNTSに分析したいアカウント名を追加してください")
        print("   詳細: docs/BUZZ_ACCOUNT_SEARCH_GUIDE.md を参照")
        return None
    
    print(f"📊 {len(BUZZ_ACCOUNTS)}件のバズアカウントを分析中...\n")
    
    accounts_data = []
    
    for username in BUZZ_ACCOUNTS:
        print(f"📊 分析中: @{username}")
        
        if use_advanced:
            # 高度な分析（頻度、マネタイズ、構成）
            result = analyze_advanced_buzz_account(username, days=7)
        else:
            # 基本分析
            result = analyze_buzz_tweets(username, days=7)
        
        if result:
            accounts_data.append(result)
    
    if not accounts_data:
        print("⚠️ 分析結果が見つかりませんでした")
        return None
    
    # 共通パターンを抽出
    if use_advanced:
        common_patterns = compare_advanced_accounts(accounts_data)
        
        print("\n" + "=" * 60)
        print("📊 週次バズパターン分析結果（高度分析）")
        print("=" * 60)
        
        print(f"\n📈 頻度パターン:")
        if common_patterns and common_patterns.get('avg_frequency'):
            print(f"  推奨投稿頻度: 1日{common_patterns['avg_frequency']:.1f}回")
        
        print(f"\n💰 マネタイズパターン:")
        if common_patterns and common_patterns.get('avg_affiliate_rate'):
            print(f"  推奨アフィリエイト使用率: {common_patterns['avg_affiliate_rate']:.1f}%")
        
        print(f"\n💡 推奨事項:")
        if common_patterns and common_patterns.get('recommendations'):
            for rec in common_patterns['recommendations']:
                print(f"  - {rec}")
        
        # 各アカウントの詳細も表示
        print(f"\n📊 各アカウントの詳細:")
        for account_data in accounts_data:
            print(f"\n  @{account_data.get('username', 'unknown')}:")
            for rec in account_data.get('recommendations', []):
                print(f"    - {rec}")
    else:
        # 基本分析の結果
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
    # コマンドライン引数で高度分析の有無を制御
    use_advanced = '--advanced' in sys.argv or '-a' in sys.argv
    
    patterns = analyze_weekly_buzz_patterns(use_advanced=use_advanced)
    
    if patterns:
        print("\n✅ 分析完了")
        print("   このパターンは今週のツイート生成に反映されます")
    else:
        print("\n⚠️ 分析をスキップしました")
        print("   使用方法:")
        print("     python weekly_buzz_analyzer.py          # 基本分析")
        print("     python weekly_buzz_analyzer.py --advanced  # 高度分析（頻度、マネタイズ、構成）")


if __name__ == '__main__':
    main()
