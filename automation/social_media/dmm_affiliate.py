#!/usr/bin/env python3
"""
DMMアフィリエイトAPI連携モジュール
商品情報とサンプル画像を取得
"""

import os
import sys
import requests
from pathlib import Path
from dotenv import load_dotenv
from typing import Dict, List, Optional

# 親ディレクトリをパスに追加
sys.path.insert(0, str(Path(__file__).parent.parent))

load_dotenv()

# dmm-search3ライブラリを使用（インストールが必要: pip install dmm-search3）
try:
    from dmm import DMM
    DMM_LIBRARY_AVAILABLE = True
except ImportError:
    DMM_LIBRARY_AVAILABLE = False
    print("⚠️  dmm-search3ライブラリがインストールされていません")
    print("💡 インストール方法: pip install dmm-search3")


class DMMAffiliateAPI:
    """DMMアフィリエイトAPI連携クラス"""
    
    def __init__(self, api_id: Optional[str] = None, affiliate_id: Optional[str] = None):
        """
        初期化
        
        Args:
            api_id: DMM API ID（環境変数 DMM_API_ID からも取得可能）
            affiliate_id: DMMアフィリエイトID（環境変数 DMM_AFFILIATE_ID からも取得可能）
        """
        self.api_id = api_id or os.getenv('DMM_API_ID')
        self.affiliate_id = affiliate_id or os.getenv('DMM_AFFILIATE_ID')
        
        if not self.api_id or not self.affiliate_id:
            raise ValueError(
                "DMM API認証情報が設定されていません。\n"
                ".envファイルに以下を設定してください:\n"
                "- DMM_API_ID\n"
                "- DMM_AFFILIATE_ID\n\n"
                "または、DMMAffiliateAPI(api_id='xxx', affiliate_id='xxx')として直接指定してください。"
            )
        
        if DMM_LIBRARY_AVAILABLE:
            self.dmm = DMM(api_id=self.api_id, affiliate_id=self.affiliate_id)
        else:
            self.dmm = None
    
    def search_products(self, keyword: str = None, hits: int = 20, 
                       service: str = 'digital', floor: str = 'comic') -> List[Dict]:
        """
        商品を検索
        
        Args:
            keyword: 検索キーワード
            hits: 取得件数（デフォルト: 20）
            service: サービス（digital, package等）
            floor: フロア（comic, videoa等）
        
        Returns:
            List[Dict]: 商品情報のリスト
        """
        if not self.dmm:
            raise RuntimeError("dmm-search3ライブラリがインストールされていません")
        
        try:
            # 検索パラメータ
            params = {
                'hits': hits,
                'service': service,
                'floor': floor,
            }
            
            if keyword:
                params['keyword'] = keyword
            
            # 商品検索
            result = self.dmm.search('ItemList', **params)
            
            products = []
            if result and 'items' in result:
                for item in result['items']:
                    product = {
                        'content_id': item.get('content_id', ''),
                        'title': item.get('title', ''),
                        'imageURL': item.get('imageURL', {}).get('list', ''),
                        'sampleImageURL': item.get('sampleImageURL', {}).get('sample_s', {}).get('image', [''])[0] if item.get('sampleImageURL') else '',
                        'affiliateURL': item.get('affiliateURL', ''),
                        'date': item.get('date', ''),
                        'price': item.get('prices', {}).get('price', ''),
                        'author': item.get('author', []),
                        'genre': item.get('genre', []),
                    }
                    products.append(product)
            
            return products
            
        except Exception as e:
            print(f"❌ 商品検索エラー: {e}")
            import traceback
            traceback.print_exc()
            return []
    
    def get_product_by_content_id(self, content_id: str) -> Optional[Dict]:
        """
        コンテンツIDから商品情報を取得
        
        Args:
            content_id: コンテンツID（例: d_715045）
        
        Returns:
            Dict: 商品情報
        """
        # コンテンツIDから検索（keywordにコンテンツIDを含む商品を検索）
        # 注意: 正確なコンテンツIDでの検索が必要な場合は、APIの仕様を確認
        products = self.search_products(keyword=content_id, hits=1)
        
        # コンテンツIDが一致する商品を探す
        for product in products:
            if product['content_id'] == content_id:
                return product
        
        return None
    
    def download_sample_image(self, image_url: str, save_path: str) -> bool:
        """
        サンプル画像をダウンロード
        
        Args:
            image_url: 画像URL
            save_path: 保存先パス
        
        Returns:
            bool: 成功したかどうか
        """
        try:
            headers = {
                'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36'
            }
            response = requests.get(image_url, headers=headers, timeout=15, stream=True)
            response.raise_for_status()
            
            # ディレクトリを作成
            os.makedirs(os.path.dirname(save_path), exist_ok=True)
            
            # 画像を保存
            with open(save_path, 'wb') as f:
                for chunk in response.iter_content(chunk_size=8192):
                    f.write(chunk)
            
            file_size = os.path.getsize(save_path)
            print(f"✅ 画像をダウンロードしました: {save_path} ({file_size} bytes)")
            return True
            
        except Exception as e:
            print(f"❌ 画像のダウンロードに失敗しました ({image_url}): {e}")
            return False


def main():
    """テスト用メイン関数"""
    import sys
    
    if len(sys.argv) < 3:
        print("使用方法:")
        print("  python dmm_affiliate.py search <キーワード>")
        print("  python dmm_affiliate.py get <コンテンツID>")
        print("\n例:")
        print("  python dmm_affiliate.py search 同人誌")
        print("  python dmm_affiliate.py get d_715045")
        sys.exit(1)
    
    command = sys.argv[1]
    
    try:
        api = DMMAffiliateAPI()
    except ValueError as e:
        print(f"❌ {e}")
        sys.exit(1)
    
    if command == 'search':
        keyword = sys.argv[2]
        print(f"🔍 商品を検索中: {keyword}")
        products = api.search_products(keyword=keyword, hits=5)
        
        print(f"\n✅ {len(products)}件の商品が見つかりました\n")
        for i, product in enumerate(products, 1):
            print(f"{i}. {product['title']}")
            print(f"   コンテンツID: {product['content_id']}")
            print(f"   画像URL: {product['sampleImageURL'] or product['imageURL']}")
            print(f"   アフィリエイトURL: {product['affiliateURL']}")
            print()
    
    elif command == 'get':
        content_id = sys.argv[2]
        print(f"📦 商品情報を取得中: {content_id}")
        product = api.get_product_by_content_id(content_id)
        
        if product:
            print(f"\n✅ 商品情報を取得しました\n")
            print(f"タイトル: {product['title']}")
            print(f"コンテンツID: {product['content_id']}")
            print(f"画像URL: {product['sampleImageURL'] or product['imageURL']}")
            print(f"アフィリエイトURL: {product['affiliateURL']}")
            
            # 画像をダウンロード（オプション）
            if len(sys.argv) > 3 and sys.argv[3] == '--download':
                image_url = product['sampleImageURL'] or product['imageURL']
                if image_url:
                    save_path = f"./dmm_images/{content_id}.jpg"
                    api.download_sample_image(image_url, save_path)
        else:
            print(f"❌ 商品が見つかりませんでした: {content_id}")
    
    else:
        print(f"不明なコマンド: {command}")


if __name__ == '__main__':
    main()
