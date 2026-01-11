#!/usr/bin/env python3
"""
18禁アフィリエイトTwitter投稿自動生成スクリプト
漫画・ビデオのサンプル画像 + アフィリエイトリンクでツイート生成
"""

import os
import sys
import json
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Optional
from dotenv import load_dotenv

# 親ディレクトリをパスに追加
sys.path.insert(0, str(Path(__file__).parent.parent))

from social_media.dmm_affiliate import DMMAffiliateAPI
from social_media.x_twitter import tweet, upload_media
from social_media.tweet_formatter import format_tweet

load_dotenv()


class AdultTwitterGenerator:
    """18禁アフィリエイトTwitter投稿生成クラス"""
    
    def __init__(self, account_type: str = 'comic'):
        """
        初期化
        
        Args:
            account_type: アカウントタイプ ('comic' または 'video')
        """
        self.account_type = account_type
        self.dmm_api = DMMAffiliateAPI()
    
    def generate_comic_tweet(self, product: Dict, image_path: Optional[str] = None) -> Dict:
        """
        漫画ツイートを生成
        
        Args:
            product: 商品情報
            image_path: 画像パス（Noneの場合はダウンロード）
        
        Returns:
            Dict: ツイート情報（text, media_path, product_info）
        """
        title = product.get('title', '')
        author = ', '.join(product.get('author', [])) if product.get('author') else ''
        genre = ', '.join(product.get('genre', [])[:2]) if product.get('genre') else ''
        affiliate_url = product.get('affiliateURL', '')
        sample_image_url = product.get('sampleImageURL') or product.get('imageURL', '')
        
        # ツイート本文を生成
        tweet_text = f"{title}\n\n"
        
        if author:
            tweet_text += f"作者: {author}\n"
        
        if genre:
            tweet_text += f"ジャンル: {genre}\n"
        
        tweet_text += "\n続きを読む⇩\n"
        tweet_text += f"{affiliate_url}\n"
        tweet_text += "#エロ漫画 #同人誌 #R18 🔞"
        
        # 画像をダウンロード（必要に応じて）
        if image_path is None and sample_image_url:
            # 一時ディレクトリにダウンロード
            image_path = f"./temp_images/{product.get('content_id', 'product')}.jpg"
            os.makedirs(os.path.dirname(image_path), exist_ok=True)
            self.dmm_api.download_sample_image(sample_image_url, image_path)
        
        return {
            'text': tweet_text,
            'media_path': image_path,
            'product_info': product,
            'account_type': 'comic'
        }
    
    def generate_video_tweet(self, product: Dict, image_path: Optional[str] = None) -> Dict:
        """
        ビデオツイートを生成
        
        Args:
            product: 商品情報
            image_path: 画像パス（Noneの場合はダウンロード）
        
        Returns:
            Dict: ツイート情報
        """
        title = product.get('title', '')
        # ビデオの場合、女優情報などを取得（APIレスポンスに応じて調整）
        affiliate_url = product.get('affiliateURL', '')
        sample_image_url = product.get('sampleImageURL') or product.get('imageURL', '')
        date = product.get('date', '')
        
        # ツイート本文を生成
        tweet_text = f"{title}\n\n"
        
        if date:
            tweet_text += f"発売日: {date}\n"
        
        # 簡潔な紹介文（30-50文字）
        tweet_text += "\n詳細・購入⇩\n"
        tweet_text += f"{affiliate_url}\n"
        tweet_text += "#AV #エロ動画 #R18 🔞"
        
        # 画像をダウンロード（必要に応じて）
        if image_path is None and sample_image_url:
            image_path = f"./temp_images/{product.get('content_id', 'product')}.jpg"
            os.makedirs(os.path.dirname(image_path), exist_ok=True)
            self.dmm_api.download_sample_image(sample_image_url, image_path)
        
        return {
            'text': tweet_text,
            'media_path': image_path,
            'product_info': product,
            'account_type': 'video'
        }
    
    def post_tweet(self, tweet_data: Dict, dry_run: bool = False) -> bool:
        """
        ツイートを投稿
        
        Args:
            tweet_data: ツイート情報（generate_comic_tweet/generate_video_tweetの戻り値）
            dry_run: テストモード（実際には投稿しない）
        
        Returns:
            bool: 成功したかどうか
        """
        text = tweet_data['text']
        media_path = tweet_data.get('media_path')
        
        # 文字数チェック
        if len(text) > 280:
            print(f"⚠️  ツイートが280文字を超えています ({len(text)}文字)")
            text = text[:277] + "..."
        
        if dry_run:
            print("=" * 60)
            print("📝 ツイートプレビュー（テストモード）")
            print("=" * 60)
            print(text)
            if media_path:
                print(f"\n画像: {media_path}")
            print("=" * 60)
            return True
        
        try:
            media_id = None
            if media_path and os.path.exists(media_path):
                media_id = upload_media(media_path)
                if not media_id:
                    print("⚠️  画像のアップロードに失敗しましたが、テキストのみで投稿します")
            
            result = tweet(text, media_ids=[media_id] if media_id else None)
            
            if result:
                print(f"✅ ツイートを投稿しました")
                return True
            else:
                print("❌ ツイートの投稿に失敗しました")
                return False
                
        except Exception as e:
            print(f"❌ エラーが発生しました: {e}")
            import traceback
            traceback.print_exc()
            return False


def main():
    """メイン関数"""
    import argparse
    
    parser = argparse.ArgumentParser(description='18禁アフィリエイトTwitter投稿生成')
    parser.add_argument('type', choices=['comic', 'video'], help='アカウントタイプ (comic/video)')
    parser.add_argument('--search', type=str, help='検索キーワード')
    parser.add_argument('--content-id', type=str, help='コンテンツID（例: d_715045）')
    parser.add_argument('--dry-run', action='store_true', help='テストモード（投稿しない）')
    parser.add_argument('--count', type=int, default=1, help='生成するツイート数（デフォルト: 1）')
    
    args = parser.parse_args()
    
    generator = AdultTwitterGenerator(account_type=args.type)
    
    # 商品を検索または取得
    if args.content_id:
        product = generator.dmm_api.get_product_by_content_id(args.content_id)
        if not product:
            print(f"❌ 商品が見つかりませんでした: {args.content_id}")
            sys.exit(1)
        products = [product]
    elif args.search:
        products = generator.dmm_api.search_products(keyword=args.search, hits=args.count)
        if not products:
            print(f"❌ 商品が見つかりませんでした: {args.search}")
            sys.exit(1)
    else:
        print("❌ --search または --content-id を指定してください")
        sys.exit(1)
    
    # ツイートを生成して投稿
    for i, product in enumerate(products[:args.count], 1):
        print(f"\n[{i}/{len(products[:args.count])}] 商品: {product.get('title', 'N/A')}")
        
        if args.type == 'comic':
            tweet_data = generator.generate_comic_tweet(product)
        else:
            tweet_data = generator.generate_video_tweet(product)
        
        success = generator.post_tweet(tweet_data, dry_run=args.dry_run)
        
        if not success:
            print(f"⚠️  投稿に失敗しました: {product.get('title', 'N/A')}")
    
    print("\n✅ 処理が完了しました")


if __name__ == '__main__':
    main()
