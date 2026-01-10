#!/usr/bin/env python3
"""
バズアカウント分析スクリプト
専門分野でバズっているアカウントを分析して共通点・パターンを抽出
"""

import os
import sys
import json
from datetime import datetime, timedelta
from pathlib import Path
from dotenv import load_dotenv
from collections import Counter
import re

# 親ディレクトリをパスに追加
sys.path.insert(0, str(Path(__file__).parent.parent))

from social_media.x_twitter import get_twitter_client

# .envファイルを読み込む
load_dotenv()


def analyze_buzz_tweets(username, days=7):
    """
    バズアカウントのツイートを分析
    
    Args:
        username: アカウント名（@なし）
        days: 分析期間（日数）
    
    Returns:
        分析結果
    """
    try:
        client = get_twitter_client()
        
        # ユーザー情報を取得
        user = client.get_user(username=username)
        if not user.data:
            print(f"❌ ユーザーが見つかりません: @{username}")
            return None
        
        user_id = user.data.id
        follower_count = user.data.public_metrics.get('followers_count', 0) if user.data.public_metrics else 0
        
        print(f"📊 アカウント分析: @{username}")
        print(f"   フォロワー数: {follower_count:,}")
        
        # 最近のツイートを取得
        tweets = client.get_users_tweets(
            id=user_id,
            max_results=100,
            tweet_fields=['created_at', 'public_metrics', 'text']
        )
        
        if not tweets.data:
            print(f"⚠️ ツイートが見つかりません")
            return None
        
        # 分析データを収集
        analysis = {
            'username': username,
            'follower_count': follower_count,
            'total_tweets': len(tweets.data),
            'high_engagement_tweets': [],
            'patterns': {
                'common_keywords': [],
                'common_structures': [],
                'engagement_indicators': []
            }
        }
        
        # エンゲージメント率の高いツイートを抽出
        for tweet in tweets.data:
            metrics = tweet.public_metrics if hasattr(tweet, 'public_metrics') else {}
            likes = metrics.get('like_count', 0)
            retweets = metrics.get('retweet_count', 0)
            replies = metrics.get('reply_count', 0)
            
            # エンゲージメント率を計算（簡易版）
            engagement_rate = (likes + retweets * 2 + replies * 2) / max(follower_count, 1) * 100
            
            # 高いエンゲージメント率のツイートを抽出（上位20%）
            if engagement_rate > 1.0:  # 1%以上のエンゲージメント率
                analysis['high_engagement_tweets'].append({
                    'text': tweet.text,
                    'likes': likes,
                    'retweets': retweets,
                    'replies': replies,
                    'engagement_rate': engagement_rate,
                    'created_at': tweet.created_at.isoformat() if tweet.created_at else None
                })
        
        # パターン分析
        analyze_patterns(analysis)
        
        return analysis
    
    except Exception as e:
        print(f"❌ エラーが発生しました: {e}")
        import traceback
        traceback.print_exc()
        return None


def analyze_patterns(analysis):
    """
    ツイートのパターンを分析
    
    Args:
        analysis: 分析結果データ
    """
    high_engagement_tweets = analysis['high_engagement_tweets']
    
    if not high_engagement_tweets:
        return
    
    # キーワード分析
    keywords = []
    for tweet in high_engagement_tweets:
        text = tweet['text']
        
        # 数字を抽出
        numbers = re.findall(r'\d+[%億万人件]', text)
        keywords.extend(numbers)
        
        # 日付を抽出
        dates = re.findall(r'\d{1,2}[-/]\d{1,2}', text)
        keywords.extend(dates)
        
        # 疑問符・感嘆符の使用
        if '?' in text:
            keywords.append('疑問文')
        if '！' in text or '!' in text:
            keywords.append('感嘆符')
        
        # 改行の使用
        if '\n' in text:
            keywords.append('改行あり')
    
    # 頻出キーワード
    keyword_counter = Counter(keywords)
    analysis['patterns']['common_keywords'] = keyword_counter.most_common(10)
    
    # 構造パターン分析
    structures = []
    for tweet in high_engagement_tweets:
        text = tweet['text']
        
        # 段落数
        paragraphs = len([p for p in text.split('\n') if p.strip()])
        structures.append(f'{paragraphs}段落')
        
        # 文字数範囲
        length = len(text)
        if length < 100:
            structures.append('短い（100文字未満）')
        elif length < 200:
            structures.append('中程度（100-200文字）')
        else:
            structures.append('長い（200文字以上）')
    
    structure_counter = Counter(structures)
    analysis['patterns']['common_structures'] = structure_counter.most_common(10)
    
    # エンゲージメント指標
    avg_likes = sum(t['likes'] for t in high_engagement_tweets) / len(high_engagement_tweets)
    avg_retweets = sum(t['retweets'] for t in high_engagement_tweets) / len(high_engagement_tweets)
    
    analysis['patterns']['engagement_indicators'] = {
        'average_likes': avg_likes,
        'average_retweets': avg_retweets,
        'average_engagement_rate': sum(t['engagement_rate'] for t in high_engagement_tweets) / len(high_engagement_tweets)
    }


def compare_accounts(accounts_data):
    """
    複数のアカウントを比較して共通点を抽出
    
    Args:
        accounts_data: アカウント分析結果のリスト
    
    Returns:
        共通点分析結果
    """
    common_patterns = {
        'common_keywords': Counter(),
        'common_structures': Counter(),
        'avg_engagement_rate': 0,
        'recommendations': []
    }
    
    # 共通キーワードを集計
    for account_data in accounts_data:
        if account_data and 'patterns' in account_data:
            patterns = account_data['patterns']
            
            # キーワードを集計
            for keyword, count in patterns.get('common_keywords', []):
                common_patterns['common_keywords'][keyword] += count
            
            # 構造を集計
            for structure, count in patterns.get('common_structures', []):
                common_patterns['common_structures'][structure] += count
    
    # 推奨事項を生成
    top_keywords = common_patterns['common_keywords'].most_common(5)
    top_structures = common_patterns['common_structures'].most_common(5)
    
    recommendations = []
    
    if top_keywords:
        recommendations.append(f"頻出キーワード: {', '.join([k for k, _ in top_keywords])}")
    
    if top_structures:
        recommendations.append(f"推奨構造: {', '.join([s for s, _ in top_structures])}")
    
    common_patterns['recommendations'] = recommendations
    
    return common_patterns


def main():
    """メイン関数"""
    if len(sys.argv) < 2:
        print("使用方法:")
        print("  python buzz_analyzer.py analyze <username> [days]")
        print("  python buzz_analyzer.py compare <username1> <username2> ...")
        print("\n例:")
        print("  python buzz_analyzer.py analyze example_user 7")
        print("  python buzz_analyzer.py compare user1 user2 user3")
        sys.exit(1)
    
    command = sys.argv[1]
    
    if command == 'analyze':
        if len(sys.argv) < 3:
            print("エラー: ユーザー名が必要です")
            sys.exit(1)
        
        username = sys.argv[2].replace('@', '')
        days = int(sys.argv[3]) if len(sys.argv) > 3 else 7
        
        result = analyze_buzz_tweets(username, days)
        
        if result:
            print("\n📊 分析結果:")
            print("=" * 60)
            print(f"高エンゲージメントツイート: {len(result['high_engagement_tweets'])}件")
            print(f"\n頻出キーワード:")
            for keyword, count in result['patterns']['common_keywords'][:5]:
                print(f"  - {keyword}: {count}回")
            print(f"\n推奨構造:")
            for structure, count in result['patterns']['common_structures'][:5]:
                print(f"  - {structure}: {count}回")
            print(f"\n平均エンゲージメント率: {result['patterns']['engagement_indicators']['average_engagement_rate']:.2f}%")
    
    elif command == 'compare':
        if len(sys.argv) < 3:
            print("エラー: ユーザー名が必要です")
            sys.exit(1)
        
        usernames = [u.replace('@', '') for u in sys.argv[2:]]
        accounts_data = []
        
        for username in usernames:
            print(f"\n📊 分析中: @{username}")
            result = analyze_buzz_tweets(username)
            if result:
                accounts_data.append(result)
        
        if accounts_data:
            common_patterns = compare_accounts(accounts_data)
            
            print("\n📊 共通点分析結果:")
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
    
    else:
        print(f"不明なコマンド: {command}")
        sys.exit(1)


if __name__ == '__main__':
    main()
