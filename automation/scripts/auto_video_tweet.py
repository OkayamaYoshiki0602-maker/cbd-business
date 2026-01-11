#!/usr/bin/env python3
"""
動画アフィリエイトツイート完全自動化スクリプト
ステップ1-5を一括実行
"""

import os
import sys
from pathlib import Path
from dotenv import load_dotenv

# 親ディレクトリをパスに追加
sys.path.insert(0, str(Path(__file__).parent.parent))

from social_media.dmm_affiliate import DMMAffiliateAPI
from social_media.adult_twitter_generator import AdultTwitterGenerator

load_dotenv()


def auto_video_tweet(keyword: str = None, content_id: str = None, count: int = 1, dry_run: bool = False):
    """
    動画アフィリエイトツイートの完全自動化
    
    ステップ1: 商品検索
    ステップ2: 商品情報取得
    ステップ3: 画像ダウンロード
    ステップ4: ツイート文案生成
    ステップ5: Twitter投稿
    
    Args:
        keyword: 検索キーワード（例: "新作AV"）
        content_id: コンテンツID（例: "d_715045"）- keywordと同時指定不可
        count: 投稿件数（デフォルト: 1）
        dry_run: テストモード（実際には投稿しない）
    """
    print("=" * 60)
    print("動画アフィリエイトツイート自動化スクリプト")
    print("=" * 60)
    
    if dry_run:
        print("⚠️  テストモード: 実際には投稿しません\n")
    
    try:
        # DMM API初期化
        print("📡 DMM APIに接続中...")
        dmm_api = DMMAffiliateAPI()
        print("✅ DMM API接続成功\n")
        
        # Twitter投稿生成器初期化
        generator = AdultTwitterGenerator(account_type='video')
        
        # 商品情報を取得
        if content_id:
            # ステップ1-2: 特定商品の情報取得
            print(f"📦 商品情報を取得中: {content_id}")
            product = dmm_api.get_product_by_content_id(content_id)
            
            if not product:
                print(f"❌ 商品が見つかりませんでした: {content_id}")
                return False
            
            products = [product]
            print(f"✅ 商品情報を取得しました: {product.get('title', 'N/A')}\n")
        elif keyword:
            # ステップ1-2: キーワード検索
            print(f"🔍 商品を検索中: {keyword}")
            products = dmm_api.search_products(keyword=keyword, hits=count, service='digital', floor='videoa')
            
            if not products:
                print(f"❌ 商品が見つかりませんでした: {keyword}")
                return False
            
            print(f"✅ {len(products)}件の商品が見つかりました\n")
        else:
            print("❌ keyword または content_id を指定してください")
            return False
        
        # 各商品についてツイート生成・投稿
        success_count = 0
        for i, product in enumerate(products[:count], 1):
            print(f"[{i}/{len(products[:count])}] 処理中: {product.get('title', 'N/A')}")
            print("-" * 60)
            
            # ステップ3-4: 画像ダウンロード + ツイート文案生成
            print("📥 画像をダウンロード中...")
            tweet_data = generator.generate_video_tweet(product)
            
            if tweet_data.get('media_path') and os.path.exists(tweet_data['media_path']):
                print(f"✅ 画像: {tweet_data['media_path']}")
            else:
                print("⚠️  画像のダウンロードに失敗しました（テキストのみで投稿）")
            
            print(f"📝 ツイート文案生成完了 ({len(tweet_data['text'])}文字)")
            if not dry_run:
                print("\nツイート内容:")
                print(tweet_data['text'])
                print("-" * 60)
            
            # ステップ5: Twitter投稿
            if not dry_run:
                print("📤 Twitterに投稿中...")
                success = generator.post_tweet(tweet_data, dry_run=False)
                
                if success:
                    success_count += 1
                    print("✅ 投稿成功\n")
                else:
                    print("❌ 投稿失敗\n")
            else:
                # テストモード: プレビューのみ表示
                print("\n📝 ツイートプレビュー:")
                print(tweet_data['text'])
                if tweet_data.get('media_path'):
                    print(f"画像: {tweet_data['media_path']}")
                print("-" * 60)
                success_count += 1
                print("✅ テスト完了（実際には投稿していません）\n")
        
        # 結果サマリー
        print("=" * 60)
        if dry_run:
            print(f"✅ テスト完了: {success_count}/{len(products[:count])}件")
        else:
            print(f"✅ 処理完了: {success_count}/{len(products[:count])}件の投稿に成功")
        print("=" * 60)
        
        return success_count > 0
        
    except ValueError as e:
        print(f"❌ 設定エラー: {e}")
        print("\n💡 .envファイルに以下を設定してください:")
        print("   - DMM_API_ID")
        print("   - DMM_AFFILIATE_ID")
        return False
    except Exception as e:
        print(f"❌ エラーが発生しました: {e}")
        import traceback
        traceback.print_exc()
        return False


def main():
    """メイン関数"""
    import argparse
    
    parser = argparse.ArgumentParser(description='動画アフィリエイトツイート完全自動化')
    parser.add_argument('--search', type=str, help='検索キーワード（例: 新作AV）')
    parser.add_argument('--content-id', type=str, help='コンテンツID（例: d_715045）')
    parser.add_argument('--count', type=int, default=1, help='投稿件数（デフォルト: 1）')
    parser.add_argument('--dry-run', action='store_true', help='テストモード（投稿しない）')
    
    args = parser.parse_args()
    
    if not args.search and not args.content_id:
        print("使用方法:")
        print("  python auto_video_tweet.py --search '新作AV' --count 3")
        print("  python auto_video_tweet.py --content-id d_715045")
        print("  python auto_video_tweet.py --search '新作AV' --dry-run  # テストモード")
        sys.exit(1)
    
    success = auto_video_tweet(
        keyword=args.search,
        content_id=args.content_id,
        count=args.count,
        dry_run=args.dry_run
    )
    
    sys.exit(0 if success else 1)


if __name__ == '__main__':
    main()
