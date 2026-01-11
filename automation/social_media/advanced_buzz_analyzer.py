#!/usr/bin/env python3
"""
高度なバズアカウント分析スクリプト
ツイート内容、構成、頻度、マネタイズを詳細に分析
"""

import os
import sys
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


def analyze_tweet_frequency(tweets_data):
    """
    ツイート頻度を分析
    
    Args:
        tweets_data: ツイートデータのリスト
    
    Returns:
        頻度分析結果
    """
    if not tweets_data:
        return None
    
    # 投稿時間を分析
    hourly_counts = Counter()
    daily_counts = Counter()
    
    for tweet in tweets_data:
        if tweet.get('created_at'):
            try:
                created_at = datetime.fromisoformat(tweet['created_at'].replace('Z', '+00:00'))
                hour = created_at.hour
                day_of_week = created_at.weekday()  # 0=月曜日, 6=日曜日
                
                hourly_counts[hour] += 1
                daily_counts[day_of_week] += 1
            except:
                pass
    
    # 1日の平均ツイート数
    if tweets_data:
        days_span = 7  # 仮に7日間として計算
        avg_daily_tweets = len(tweets_data) / days_span
    
    return {
        'avg_daily_tweets': avg_daily_tweets if tweets_data else 0,
        'hourly_distribution': dict(hourly_counts.most_common(24)),
        'daily_distribution': dict(daily_counts.most_common(7)),
        'peak_hours': [hour for hour, _ in hourly_counts.most_common(3)],
    }


def analyze_monetization(tweets_data):
    """
    マネタイズ方法を分析
    
    Args:
        tweets_data: ツイートデータのリスト
    
    Returns:
        マネタイズ分析結果
    """
    if not tweets_data:
        return None
    
    monetization_patterns = {
        'affiliate_links': 0,  # アフィリエイトリンク
        'product_reviews': 0,  # 商品レビュー
        'promotional_content': 0,  # プロモーションコンテンツ
        'affiliate_rate': 0.0,  # アフィリエイトリンクの割合
    }
    
    # アフィリエイトリンクのパターン（一般的なパターン）
    affiliate_patterns = [
        r'amazon\.co\.jp',  # Amazon
        r'rakuten\.co\.jp',  # Rakuten
        r'a8\.net',  # A8.net
        r'af\.moshimo\.com',  # もしもアフィリエイト
        r'u\.to',  # 短縮URL（アフィリエイトの可能性）
        r'bit\.ly',  # 短縮URL
    ]
    
    product_keywords = [
        r'おすすめ', r'レビュー', r'試してみた', r'使ってみた',
        r'購入', r'買って', r'商品', r'製品', r'サービス',
    ]
    
    for tweet in tweets_data:
        text = tweet.get('text', '')
        
        # アフィリエイトリンクをチェック
        has_affiliate = False
        for pattern in affiliate_patterns:
            if re.search(pattern, text, re.IGNORECASE):
                has_affiliate = True
                monetization_patterns['affiliate_links'] += 1
                break
        
        # 商品レビューをチェック
        if any(re.search(keyword, text) for keyword in product_keywords):
            monetization_patterns['product_reviews'] += 1
        
        # プロモーションコンテンツ（リンク + 商品キーワード）
        if has_affiliate and any(re.search(keyword, text) for keyword in product_keywords):
            monetization_patterns['promotional_content'] += 1
    
    # アフィリエイトリンクの割合
    total_tweets = len(tweets_data)
    if total_tweets > 0:
        monetization_patterns['affiliate_rate'] = monetization_patterns['affiliate_links'] / total_tweets * 100
    
    return monetization_patterns


def analyze_tweet_structure(tweets_data):
    """
    ツイート構成を分析
    
    Args:
        tweets_data: ツイートデータのリスト
    
    Returns:
        構成分析結果
    """
    if not tweets_data:
        return None
    
    structure_patterns = {
        'avg_line_breaks': 0,
        'has_title_rate': 0.0,
        'has_bullet_rate': 0.0,
        'has_emoji_rate': 0.0,
        'has_number_rate': 0.0,
        'has_url_rate': 0.0,
        'avg_length': 0,
        'common_title_markers': [],
    }
    
    title_markers = []
    line_breaks_list = []
    lengths = []
    
    title_patterns = [
        r'^【', r'^「', r'^【', r'^■', r'^▶', r'^●', r'^◆', r'^▼',
    ]
    
    bullet_patterns = [r'[・•→]', r'^\d+[\.、]', r'^[-*]']
    
    for tweet in tweets_data:
        text = tweet.get('text', '')
        
        # 改行数
        line_breaks = text.count('\n')
        line_breaks_list.append(line_breaks)
        
        # タイトルマーカーの有無
        has_title = any(re.search(pattern, text) for pattern in title_patterns)
        if has_title:
            structure_patterns['has_title_rate'] += 1
            # タイトルマーカーを抽出
            for pattern in title_patterns:
                match = re.search(pattern, text)
                if match:
                    marker = text[match.start():match.end()+10]  # マーカー以降10文字
                    title_markers.append(marker[:20])
        
        # 箇条書きの有無
        if any(re.search(pattern, text, re.MULTILINE) for pattern in bullet_patterns):
            structure_patterns['has_bullet_rate'] += 1
        
        # 絵文字の有無
        if re.search(r'[😀-🙏🌀-🗿]', text):
            structure_patterns['has_emoji_rate'] += 1
        
        # 数字の有無
        if re.search(r'\d+', text):
            structure_patterns['has_number_rate'] += 1
        
        # URLの有無
        if re.search(r'https?://', text):
            structure_patterns['has_url_rate'] += 1
        
        # 文字数
        lengths.append(len(text))
    
    # 平均値を計算
    total = len(tweets_data)
    if total > 0:
        structure_patterns['avg_line_breaks'] = sum(line_breaks_list) / total
        structure_patterns['has_title_rate'] = structure_patterns['has_title_rate'] / total * 100
        structure_patterns['has_bullet_rate'] = structure_patterns['has_bullet_rate'] / total * 100
        structure_patterns['has_emoji_rate'] = structure_patterns['has_emoji_rate'] / total * 100
        structure_patterns['has_number_rate'] = structure_patterns['has_number_rate'] / total * 100
        structure_patterns['has_url_rate'] = structure_patterns['has_url_rate'] / total * 100
        structure_patterns['avg_length'] = sum(lengths) / total
    
    # よく使われるタイトルマーカー
    marker_counter = Counter(title_markers)
    structure_patterns['common_title_markers'] = [marker for marker, _ in marker_counter.most_common(5)]
    
    return structure_patterns


def analyze_advanced_buzz_account(username, days=7):
    """
    高度なバズアカウント分析（内容、構成、頻度、マネタイズ）
    
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
        
        print(f"📊 高度な分析: @{username}")
        print(f"   フォロワー数: {follower_count:,}")
        
        # 最近のツイートを取得（最大100件）
        tweets = client.get_users_tweets(
            id=user_id,
            max_results=100,
            tweet_fields=['created_at', 'public_metrics', 'text']
        )
        
        if not tweets.data:
            print(f"⚠️ ツイートが見つかりません")
            return None
        
        # ツイートデータを整形
        tweets_data = []
        high_engagement_tweets = []
        
        for tweet in tweets.data:
            metrics = tweet.public_metrics if hasattr(tweet, 'public_metrics') else {}
            likes = metrics.get('like_count', 0)
            retweets = metrics.get('retweet_count', 0)
            replies = metrics.get('reply_count', 0)
            
            # エンゲージメント率を計算
            engagement_rate = (likes + retweets * 2 + replies * 2) / max(follower_count, 1) * 100
            
            tweet_data = {
                'text': tweet.text,
                'likes': likes,
                'retweets': retweets,
                'replies': replies,
                'engagement_rate': engagement_rate,
                'created_at': tweet.created_at.isoformat() if tweet.created_at else None
            }
            
            tweets_data.append(tweet_data)
            
            # 高いエンゲージメント率のツイートを抽出
            if engagement_rate > 1.0:  # 1%以上
                high_engagement_tweets.append(tweet_data)
        
        # 各種分析を実行
        frequency_analysis = analyze_tweet_frequency(tweets_data)
        monetization_analysis = analyze_monetization(tweets_data)
        structure_analysis = analyze_tweet_structure(tweets_data)
        
        # 高エンゲージメントツイートの分析
        high_engagement_structure = analyze_tweet_structure(high_engagement_tweets) if high_engagement_tweets else None
        
        analysis_result = {
            'username': username,
            'follower_count': follower_count,
            'total_tweets_analyzed': len(tweets_data),
            'high_engagement_count': len(high_engagement_tweets),
            'frequency': frequency_analysis,
            'monetization': monetization_analysis,
            'structure': structure_analysis,
            'high_engagement_structure': high_engagement_structure,
            'recommendations': []
        }
        
        # 推奨事項を生成
        recommendations = []
        
        if frequency_analysis and frequency_analysis.get('avg_daily_tweets', 0) > 0:
            recommendations.append(f"平均投稿頻度: 1日{frequency_analysis['avg_daily_tweets']:.1f}回")
            if frequency_analysis.get('peak_hours'):
                peak_hours_str = '、'.join([f"{h}時" for h in frequency_analysis['peak_hours']])
                recommendations.append(f"効果的な投稿時間: {peak_hours_str}")
        
        if monetization_analysis:
            if monetization_analysis.get('affiliate_rate', 0) > 0:
                recommendations.append(f"アフィリエイトリンク使用率: {monetization_analysis['affiliate_rate']:.1f}%")
            if monetization_analysis.get('product_reviews', 0) > 0:
                recommendations.append(f"商品レビュー頻度: {monetization_analysis['product_reviews']}/{len(tweets_data)}ツイート")
        
        if structure_analysis:
            if structure_analysis.get('has_title_rate', 0) > 50:
                recommendations.append(f"タイトル使用率: {structure_analysis['has_title_rate']:.1f}%")
            if structure_analysis.get('avg_line_breaks', 0) > 2:
                recommendations.append(f"平均改行数: {structure_analysis['avg_line_breaks']:.1f}行")
        
        analysis_result['recommendations'] = recommendations
        
        return analysis_result
    
    except Exception as e:
        print(f"❌ エラーが発生しました: {e}")
        import traceback
        traceback.print_exc()
        return None


def compare_advanced_accounts(accounts_data):
    """
    複数のアカウントを高度に比較
    
    Args:
        accounts_data: アカウント分析結果のリスト
    
    Returns:
        共通点分析結果
    """
    if not accounts_data:
        return None
    
    common_patterns = {
        'avg_frequency': 0,
        'avg_affiliate_rate': 0,
        'common_structure_patterns': {},
        'recommendations': []
    }
    
    frequencies = []
    affiliate_rates = []
    
    for account_data in accounts_data:
        if account_data:
            if account_data.get('frequency') and account_data['frequency'].get('avg_daily_tweets'):
                frequencies.append(account_data['frequency']['avg_daily_tweets'])
            
            if account_data.get('monetization') and account_data['monetization'].get('affiliate_rate'):
                affiliate_rates.append(account_data['monetization']['affiliate_rate'])
    
    if frequencies:
        common_patterns['avg_frequency'] = sum(frequencies) / len(frequencies)
    
    if affiliate_rates:
        common_patterns['avg_affiliate_rate'] = sum(affiliate_rates) / len(affiliate_rates)
    
    # 推奨事項を生成
    recommendations = []
    
    if common_patterns['avg_frequency'] > 0:
        recommendations.append(f"推奨投稿頻度: 1日{common_patterns['avg_frequency']:.1f}回")
    
    if common_patterns['avg_affiliate_rate'] > 0:
        recommendations.append(f"推奨アフィリエイト使用率: {common_patterns['avg_affiliate_rate']:.1f}%")
    
    common_patterns['recommendations'] = recommendations
    
    return common_patterns


def main():
    """メイン関数（テスト用）"""
    if len(sys.argv) < 2:
        print("使用方法:")
        print("  python advanced_buzz_analyzer.py analyze <username> [days]")
        print("\n例:")
        print("  python advanced_buzz_analyzer.py analyze example_user 7")
        sys.exit(1)
    
    command = sys.argv[1]
    
    if command == 'analyze':
        if len(sys.argv) < 3:
            print("エラー: ユーザー名が必要です")
            sys.exit(1)
        
        username = sys.argv[2].replace('@', '')
        days = int(sys.argv[3]) if len(sys.argv) > 3 else 7
        
        result = analyze_advanced_buzz_account(username, days)
        
        if result:
            print("\n" + "=" * 60)
            print("📊 高度な分析結果")
            print("=" * 60)
            
            print(f"\n📈 頻度分析:")
            if result.get('frequency'):
                freq = result['frequency']
                print(f"  平均投稿頻度: 1日{freq.get('avg_daily_tweets', 0):.1f}回")
                if freq.get('peak_hours'):
                    print(f"  効果的な投稿時間: {', '.join([f'{h}時' for h in freq['peak_hours']])}")
            
            print(f"\n💰 マネタイズ分析:")
            if result.get('monetization'):
                mon = result['monetization']
                print(f"  アフィリエイトリンク使用率: {mon.get('affiliate_rate', 0):.1f}%")
                print(f"  商品レビュー数: {mon.get('product_reviews', 0)}件")
            
            print(f"\n📝 構成分析:")
            if result.get('structure'):
                struct = result['structure']
                print(f"  平均改行数: {struct.get('avg_line_breaks', 0):.1f}行")
                print(f"  タイトル使用率: {struct.get('has_title_rate', 0):.1f}%")
                print(f"  絵文字使用率: {struct.get('has_emoji_rate', 0):.1f}%")
                print(f"  平均文字数: {struct.get('avg_length', 0):.0f}文字")
            
            print(f"\n💡 推奨事項:")
            for rec in result.get('recommendations', []):
                print(f"  - {rec}")
    
    else:
        print(f"不明なコマンド: {command}")
        sys.exit(1)


if __name__ == '__main__':
    main()
