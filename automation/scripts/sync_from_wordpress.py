#!/usr/bin/env python3
"""
WordPressからGitHubリポジトリに投稿・固定ページを同期するスクリプト

使用方法:
1. 環境変数または.envファイルに以下を設定:
   - WORDPRESS_URL: https://cbd-no-hito.com
   - WORDPRESS_USERNAME: WordPressのユーザー名
   - WORDPRESS_APP_PASSWORD: アプリケーションパスワード

2. スクリプトを実行:
   python3 automation/scripts/sync_from_wordpress.py
"""

import os
import sys
import requests
import base64
from pathlib import Path
from typing import List, Dict, Any
from datetime import datetime

# プロジェクトルートを取得
project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root))

# WordPress REST API設定
WORDPRESS_URL = os.getenv('WORDPRESS_URL', '').rstrip('/')
WORDPRESS_USERNAME = os.getenv('WORDPRESS_USERNAME', '')
WORDPRESS_APP_PASSWORD = os.getenv('WORDPRESS_APP_PASSWORD', '')

if not all([WORDPRESS_URL, WORDPRESS_USERNAME, WORDPRESS_APP_PASSWORD]):
    print("❌ エラー: 環境変数が設定されていません")
    print("   WORDPRESS_URL, WORDPRESS_USERNAME, WORDPRESS_APP_PASSWORD を設定してください")
    sys.exit(1)

# ベーシック認証用のヘッダー
credentials = f"{WORDPRESS_USERNAME}:{WORDPRESS_APP_PASSWORD}"
token = base64.b64encode(credentials.encode()).decode()
headers = {
    'Authorization': f'Basic {token}',
    'Content-Type': 'application/json',
    'User-Agent': 'WordPress-GitHub-Sync/1.0'
}

API_BASE = f"{WORDPRESS_URL}/wp-json/wp/v2"

# 出力ディレクトリ
POSTS_DIR = project_root / 'wordpress' / 'posts'
PAGES_DIR = project_root / 'wordpress' / 'pages'

# ディレクトリを作成
POSTS_DIR.mkdir(parents=True, exist_ok=True)
PAGES_DIR.mkdir(parents=True, exist_ok=True)


def get_all_posts(post_type: str = 'posts') -> List[Dict[str, Any]]:
    """WordPressからすべての投稿または固定ページを取得"""
    all_items = []
    page = 1
    per_page = 100
    
    while True:
        try:
            response = requests.get(
                f"{API_BASE}/{post_type}",
                params={
                    'per_page': per_page,
                    'page': page,
                    'status': 'publish',  # 公開済みのみ
                    '_embed': True
                },
                headers=headers,
                timeout=30
            )
            response.raise_for_status()
            items = response.json()
            
            if not items:
                break
            
            all_items.extend(items)
            
            # 次のページがあるか確認
            total_pages = int(response.headers.get('X-WP-TotalPages', '1'))
            if page >= total_pages:
                break
            
            page += 1
            
        except Exception as e:
            print(f"❌ エラー ({post_type}, ページ {page}): {e}")
            break
    
    return all_items


def sanitize_filename(slug: str) -> str:
    """ファイル名として使用可能な形式に変換"""
    # スラッグをそのまま使用（通常は既に安全な形式）
    return slug


def save_post_to_file(post: Dict[str, Any], output_dir: Path) -> bool:
    """投稿または固定ページをHTMLファイルとして保存"""
    try:
        slug = post['slug']
        content = post['content']['rendered']
        title = post['title']['rendered']
        
        # ファイル名を生成
        filename = sanitize_filename(slug) + '.html'
        file_path = output_dir / filename
        
        # コンテンツをそのまま保存（既にHTML形式）
        file_path.write_text(content, encoding='utf-8')
        
        print(f"✅ 保存しました: {title} ({filename})")
        return True
        
    except Exception as e:
        print(f"❌ エラー ({post.get('slug', 'unknown')}): {e}")
        return False


def main():
    """メイン処理"""
    print("📥 WordPressから投稿・固定ページを取得します...")
    print(f"   URL: {WORDPRESS_URL}")
    print()
    
    # 投稿を取得
    print("📝 投稿記事を取得中...")
    posts = get_all_posts('posts')
    print(f"   {len(posts)}件の投稿を取得しました")
    
    # 固定ページを取得
    print("📄 固定ページを取得中...")
    pages = get_all_posts('pages')
    print(f"   {len(pages)}件の固定ページを取得しました")
    print()
    
    # 投稿を保存
    if posts:
        print(f"💾 {len(posts)}件の投稿を保存中...")
        success_count = 0
        for post in posts:
            if save_post_to_file(post, POSTS_DIR):
                success_count += 1
        print(f"   ✅ {success_count}/{len(posts)}件の投稿を保存しました")
        print()
    
    # 固定ページを保存
    if pages:
        print(f"💾 {len(pages)}件の固定ページを保存中...")
        success_count = 0
        for page in pages:
            if save_post_to_file(page, PAGES_DIR):
                success_count += 1
        print(f"   ✅ {success_count}/{len(pages)}件の固定ページを保存しました")
        print()
    
    print("✅ 同期処理が完了しました")
    print()
    print("📝 次のステップ:")
    print("   1. 保存されたファイルを確認してください")
    print("   2. git add wordpress/posts/ wordpress/pages/")
    print("   3. git commit -m 'Sync posts and pages from WordPress'")
    print("   4. git push origin main")


if __name__ == '__main__':
    main()
