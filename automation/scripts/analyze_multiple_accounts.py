#!/usr/bin/env python3
"""
複数アカウントの一括分析スクリプト
戦略、投稿頻度、投稿数、ツイート傾向、文字数などを分析
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


def analyze_accounts_batch(usernames):
    """
    複数のアカウントを一括分析
    
    Args:
        usernames: ユーザー名のリスト
    """
    results = []
    
    print("=" * 60)
    print("複数アカウント一括分析")
    print("=" * 60)
    print(f"分析対象: {len(usernames)}件\n")
    
    for i, username in enumerate(usernames, 1):
        print(f"[{i}/{len(usernames)}] 分析中: @{username}")
        result = analyze_advanced_buzz_account(username, days=7)
        if result:
            results.append(result)
        print()
    
    if not results:
        print("⚠️ 分析結果が見つかりませんでした")
        return
    
    # 分析結果をまとめて表示
    print("\n" + "=" * 60)
    print("分析結果サマリー")
    print("=" * 60)
    
    # カテゴリ別に分類
    categories = {
        'アフィリエイト': [],
        '美容': [],
        '家庭': [],
        '健康': [],
        '投資': [],
    }
    
    # ユーザー名からカテゴリを推測（簡易版）
    category_map = {
        'Oc4Um': 'アフィリエイト',
        'kenshoneki': '美容',
        'urara_money': '家庭',
        'takuyasensei': '健康',
        'show10shitade': '健康',
        'kazama_0425': '健康',
        'hirokazupapi': '健康',
        'tousigatizei': '投資',
        'pygmy_hem': '投資',
    }
    
    for result in results:
        username = result.get('username', '')
        category = category_map.get(username, 'その他')
        if category in categories:
            categories[category].append(result)
    
    # カテゴリ別に表示
    for category, accounts in categories.items():
        if not accounts:
            continue
        
        print(f"\n【{category}系アカウント】")
        print("-" * 60)
        
        for account in accounts:
            print(f"\n@{account.get('username', 'unknown')}")
            print(f"  フォロワー: {account.get('follower_count', 0):,}人")
            
            # 頻度分析
            if account.get('frequency'):
                freq = account['frequency']
                print(f"  投稿頻度: 1日{freq.get('avg_daily_tweets', 0):.1f}回")
                if freq.get('peak_hours'):
                    print(f"  効果的な投稿時間: {', '.join([f'{h}時' for h in freq['peak_hours']])}")
            
            # マネタイズ分析
            if account.get('monetization'):
                mon = account['monetization']
                print(f"  アフィリエイト使用率: {mon.get('affiliate_rate', 0):.1f}%")
                print(f"  商品レビュー数: {mon.get('product_reviews', 0)}件")
            
            # 構成分析
            if account.get('structure'):
                struct = account['structure']
                print(f"  平均改行数: {struct.get('avg_line_breaks', 0):.1f}行")
                print(f"  タイトル使用率: {struct.get('has_title_rate', 0):.1f}%")
                print(f"  絵文字使用率: {struct.get('has_emoji_rate', 0):.1f}%")
                print(f"  平均文字数: {struct.get('avg_length', 0):.0f}文字")
    
    # 共通パターンを抽出
    print("\n" + "=" * 60)
    print("共通パターン分析")
    print("=" * 60)
    
    # 平均投稿頻度
    frequencies = [r['frequency']['avg_daily_tweets'] for r in results if r.get('frequency') and r['frequency'].get('avg_daily_tweets')]
    if frequencies:
        avg_freq = sum(frequencies) / len(frequencies)
        print(f"\n📈 平均投稿頻度: 1日{avg_freq:.1f}回")
    
    # 平均アフィリエイト使用率
    affiliate_rates = [r['monetization']['affiliate_rate'] for r in results if r.get('monetization') and r['monetization'].get('affiliate_rate')]
    if affiliate_rates:
        avg_affiliate = sum(affiliate_rates) / len(affiliate_rates)
        print(f"💰 平均アフィリエイト使用率: {avg_affiliate:.1f}%")
    
    # 平均文字数
    lengths = [r['structure']['avg_length'] for r in results if r.get('structure') and r['structure'].get('avg_length')]
    if lengths:
        avg_length = sum(lengths) / len(lengths)
        print(f"📝 平均文字数: {avg_length:.0f}文字")
    
    # 平均改行数
    line_breaks = [r['structure']['avg_line_breaks'] for r in results if r.get('structure') and r['structure'].get('avg_line_breaks')]
    if line_breaks:
        avg_line_breaks = sum(line_breaks) / len(line_breaks)
        print(f"📊 平均改行数: {avg_line_breaks:.1f}行")
    
    # タイトル使用率
    title_rates = [r['structure']['has_title_rate'] for r in results if r.get('structure') and r['structure'].get('has_title_rate')]
    if title_rates:
        avg_title = sum(title_rates) / len(title_rates)
        print(f"📌 タイトル使用率: {avg_title:.1f}%")
    
    # 推奨事項
    print("\n" + "=" * 60)
    print("取り入れたいポイント（推奨事項）")
    print("=" * 60)
    
    recommendations = []
    
    if frequencies and avg_freq > 0:
        recommendations.append(f"✅ 投稿頻度: 1日{avg_freq:.1f}回程度を目標にする")
    
    if affiliate_rates and avg_affiliate > 0:
        recommendations.append(f"✅ アフィリエイト使用率: {avg_affiliate:.1f}%程度を目安にする")
    
    if lengths and avg_length > 0:
        recommendations.append(f"✅ 文字数: {avg_length:.0f}文字程度を目安にする")
    
    if line_breaks and avg_line_breaks > 0:
        recommendations.append(f"✅ 改行数: {avg_line_breaks:.1f}行程度を目安にする")
    
    if title_rates and avg_title > 50:
        recommendations.append(f"✅ タイトル使用: {avg_title:.1f}%のアカウントが使用しているため、積極的に使用する")
    
    for rec in recommendations:
        print(f"  {rec}")
    
    return results


def main():
    """メイン関数"""
    if len(sys.argv) < 2:
        # デフォルトのアカウントリスト
        usernames = [
            'Oc4Um',  # アフィリエイト
            'kenshoneki',  # 美容
            'urara_money',  # 家庭
            'takuyasensei',  # 健康
            'show10shitade',  # 健康
            'kazama_0425',  # 健康
            'hirokazupapi',  # 健康
            'tousigatizei',  # 投資
            'pygmy_hem',  # 投資
        ]
        print("デフォルトのアカウントリストを使用します")
    else:
        usernames = [u.replace('@', '') for u in sys.argv[1:]]
    
    results = analyze_accounts_batch(usernames)
    
    if results:
        print("\n✅ 分析完了")
        print(f"   分析件数: {len(results)}件")


if __name__ == '__main__':
    main()
