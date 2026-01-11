#!/usr/bin/env python3
"""
DMM商品ページから画像を取得するスクリプト
同人誌・アダルトビデオのサンプル画像をダウンロード
"""

import os
import sys
import re
import requests
from pathlib import Path
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse
from dotenv import load_dotenv

# 親ディレクトリをパスに追加
sys.path.insert(0, str(Path(__file__).parent.parent))

load_dotenv()


class DMMImageExtractor:
    """DMMから画像を抽出するクラス"""
    
    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Language': 'ja,en-US;q=0.7,en;q=0.3',
            'Accept-Encoding': 'gzip, deflate, br',
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1',
        })
    
    def extract_images_from_product_page(self, url):
        """
        商品ページから画像URLを抽出
        
        Args:
            url: DMM商品ページのURL（例: https://dmm.co.jp/dc/doujin/-/detail/=/cid=d_715045/）
        
        Returns:
            list: 画像URLのリスト
        """
        try:
            print(f"📥 商品ページを取得中: {url}")
            response = self.session.get(url, timeout=15, allow_redirects=True)
            response.raise_for_status()
            
            # 年齢確認ページの可能性がある場合は警告
            if 'age_check' in response.url or 'age-verification' in response.text.lower():
                print("⚠️  年齢確認ページが検出されました")
                print("💡 手動でブラウザでアクセスし、Cookieを設定する必要がある可能性があります")
            
            soup = BeautifulSoup(response.text, 'html.parser')
            
            # 様々な方法で画像を検索
            image_urls = []
            
            # 1. サンプル画像（sample画像）
            sample_images = soup.find_all('img', {'src': re.compile(r'sample|preview|thumbnail', re.I)})
            for img in sample_images:
                src = img.get('src') or img.get('data-src') or img.get('data-original')
                if src and self._is_valid_image_url(src):
                    image_urls.append(urljoin(url, src))
            
            # 2. 商品画像（product画像）
            product_images = soup.find_all('img', {'src': re.compile(r'product|goods|doujin', re.I)})
            for img in product_images:
                src = img.get('src') or img.get('data-src') or img.get('data-original')
                if src and self._is_valid_image_url(src) and src not in image_urls:
                    image_urls.append(urljoin(url, src))
            
            # 3. 一般的な画像（.jpg, .png等）
            all_images = soup.find_all('img')
            for img in all_images:
                src = img.get('src') or img.get('data-src') or img.get('data-original')
                if src and self._is_valid_image_url(src):
                    full_url = urljoin(url, src)
                    # サンプル/商品画像のみ（ロゴや広告を除外）
                    if any(keyword in full_url.lower() for keyword in ['sample', 'preview', 'product', 'doujin', 'cid=']):
                        if full_url not in image_urls:
                            image_urls.append(full_url)
            
            # 4. JavaScript内の画像URL（data-src属性など）
            scripts = soup.find_all('script')
            for script in scripts:
                if script.string:
                    # JSON形式のデータから画像URLを抽出
                    matches = re.findall(r'https?://[^\s"\'<>]+\.(?:jpg|jpeg|png|gif|webp)', script.string, re.I)
                    for match in matches:
                        if any(keyword in match.lower() for keyword in ['sample', 'preview', 'product']):
                            if match not in image_urls:
                                image_urls.append(match)
            
            # 重複を削除
            image_urls = list(dict.fromkeys(image_urls))  # 順序を保ったまま重複削除
            
            print(f"✅ {len(image_urls)}個の画像URLを検出しました")
            return image_urls
            
        except requests.exceptions.RequestException as e:
            print(f"❌ リクエストエラー: {e}")
            return []
        except Exception as e:
            print(f"❌ エラーが発生しました: {e}")
            import traceback
            traceback.print_exc()
            return []
    
    def _is_valid_image_url(self, url):
        """有効な画像URLかチェック"""
        if not url:
            return False
        if url.startswith('data:'):
            return False
        if any(excluded in url.lower() for excluded in ['logo', 'icon', 'button', 'banner', 'ad']):
            return False
        return any(ext in url.lower() for ext in ['.jpg', '.jpeg', '.png', '.gif', '.webp'])
    
    def download_image(self, image_url, save_path):
        """
        画像をダウンロード
        
        Args:
            image_url: 画像のURL
            save_path: 保存先パス
        
        Returns:
            bool: 成功したかどうか
        """
        try:
            response = self.session.get(image_url, timeout=15, stream=True)
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
    
    def extract_product_info(self, url):
        """
        商品情報を抽出
        
        Args:
            url: DMM商品ページのURL
        
        Returns:
            dict: 商品情報（タイトル、作者、ジャンル等）
        """
        try:
            response = self.session.get(url, timeout=15)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.text, 'html.parser')
            
            info = {
                'title': '',
                'author': '',
                'genre': '',
                'price': '',
                'url': url
            }
            
            # タイトルを抽出（複数のパターンを試行）
            title_selectors = [
                'h1.title',
                '.product-title',
                'h1',
                'title'
            ]
            
            for selector in title_selectors:
                title_elem = soup.select_one(selector)
                if title_elem:
                    info['title'] = title_elem.get_text(strip=True)
                    break
            
            # 作者を抽出
            author_elem = soup.find('span', string=re.compile(r'作者|著者|サークル', re.I))
            if not author_elem:
                author_elem = soup.find('a', href=re.compile(r'circle|author'))
            if author_elem:
                info['author'] = author_elem.get_text(strip=True)
            
            # ジャンルを抽出
            genre_elems = soup.find_all('a', href=re.compile(r'genre|category'))
            if genre_elems:
                info['genre'] = ', '.join([elem.get_text(strip=True) for elem in genre_elems[:3]])
            
            return info
            
        except Exception as e:
            print(f"❌ 商品情報の抽出に失敗しました: {e}")
            return {'url': url}


def main():
    """メイン関数"""
    if len(sys.argv) < 2:
        print("使用方法:")
        print("  python dmm_image_extractor.py <DMM商品URL> [出力ディレクトリ]")
        print("\n例:")
        print("  python dmm_image_extractor.py https://dmm.co.jp/dc/doujin/-/detail/=/cid=d_715045/")
        print("  python dmm_image_extractor.py https://dmm.co.jp/dc/doujin/-/detail/=/cid=d_715045/ ./images")
        sys.exit(1)
    
    url = sys.argv[1]
    output_dir = sys.argv[2] if len(sys.argv) > 2 else './dmm_images'
    
    extractor = DMMImageExtractor()
    
    # 商品情報を取得
    print("\n" + "="*60)
    print("📦 商品情報を取得中...")
    print("="*60)
    product_info = extractor.extract_product_info(url)
    
    print(f"\n📝 商品情報:")
    for key, value in product_info.items():
        print(f"  {key}: {value}")
    
    # 画像を抽出
    print("\n" + "="*60)
    print("🖼️  画像を抽出中...")
    print("="*60)
    image_urls = extractor.extract_images_from_product_page(url)
    
    if not image_urls:
        print("\n❌ 画像が見つかりませんでした")
        print("💡 以下の可能性があります:")
        print("  1. 年齢確認が必要なページの可能性")
        print("  2. JavaScriptで動的に読み込まれる画像の可能性")
        print("  3. ログインが必要な可能性")
        sys.exit(1)
    
    print(f"\n📸 検出された画像 ({len(image_urls)}件):")
    for i, img_url in enumerate(image_urls[:10], 1):  # 最初の10件のみ表示
        print(f"  {i}. {img_url}")
    
    if len(image_urls) > 10:
        print(f"  ... 他 {len(image_urls) - 10}件")
    
    # 画像をダウンロード（最初の5枚まで）
    print("\n" + "="*60)
    print("💾 画像をダウンロード中...")
    print("="*60)
    
    # 出力ディレクトリを作成
    os.makedirs(output_dir, exist_ok=True)
    
    # 商品IDをURLから抽出（ファイル名に使用）
    cid_match = re.search(r'cid=([^/]+)', url)
    product_id = cid_match.group(1) if cid_match else 'product'
    
    downloaded_count = 0
    for i, img_url in enumerate(image_urls[:5], 1):  # 最初の5枚のみダウンロード
        # 拡張子を取得
        parsed = urlparse(img_url)
        ext = os.path.splitext(parsed.path)[1] or '.jpg'
        filename = f"{product_id}_{i:02d}{ext}"
        save_path = os.path.join(output_dir, filename)
        
        if extractor.download_image(img_url, save_path):
            downloaded_count += 1
    
    print(f"\n✅ {downloaded_count}枚の画像をダウンロードしました")
    print(f"📁 保存先: {os.path.abspath(output_dir)}")


if __name__ == '__main__':
    main()
