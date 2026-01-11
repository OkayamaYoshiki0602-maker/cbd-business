#!/usr/bin/env python3
"""
GitHub Actions用: WordPress REST APIで記事を同期するスクリプト

使用方法:
1. GitHub Secretsに以下を設定:
   - WORDPRESS_URL: https://cbd-no-hito.com
   - WORDPRESS_USERNAME: WordPressのユーザー名
   - WORDPRESS_APP_PASSWORD: アプリケーションパスワード

2. wordpress/posts/ または wordpress/pages/ のファイルが変更されると自動実行
"""

import os
import sys
import requests
import base64
import re
from pathlib import Path
from typing import Optional, Dict, Any

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
    'User-Agent': 'WordPress-GitHub-Sync/1.0'  # User-Agentを設定
}

API_BASE = f"{WORDPRESS_URL}/wp-json/wp/v2"


def get_post_by_slug(slug: str) -> Optional[Dict[str, Any]]:
    """スラッグで投稿を検索"""
    try:
        response = requests.get(
            f"{API_BASE}/posts",
            params={'slug': slug, 'per_page': 1},
            headers=headers,
            timeout=10
        )
        response.raise_for_status()
        posts = response.json()
        return posts[0] if posts else None
    except Exception as e:
        print(f"⚠️  投稿検索エラー: {e}")
        return None


def extract_title_from_html(html_content: str) -> Optional[str]:
    """HTMLコンテンツから最初のh2見出しを抽出してタイトルとして使用"""
    # h2タグを検索（wp-block-headingクラスを含む）
    match = re.search(r'<h2[^>]*class="[^"]*wp-block-heading[^"]*"[^>]*>(.*?)</h2>', html_content, re.IGNORECASE | re.DOTALL)
    if match:
        title = match.group(1).strip()
        # HTMLタグを除去
        title = re.sub(r'<[^>]+>', '', title)
        return title
    return None


def create_or_update_post(file_path: Path, slug: str, title: str, content: str) -> bool:
    """投稿を作成または更新"""
    try:
        # 既存の投稿を検索
        existing_post = get_post_by_slug(slug)
        
        if existing_post:
            # 更新
            post_id = existing_post['id']
            response = requests.post(
                f"{API_BASE}/posts/{post_id}",
                json={
                    'title': title,
                    'content': content,
                    'status': 'publish'
                },
                headers=headers,
                timeout=10
            )
            response.raise_for_status()
            print(f"✅ 投稿を更新しました: {title} (ID: {post_id})")
            return True
        else:
            # 新規作成
            response = requests.post(
                f"{API_BASE}/posts",
                json={
                    'title': title,
                    'content': content,
                    'status': 'publish',
                    'slug': slug
                },
                headers=headers,
                timeout=10
            )
            response.raise_for_status()
            post_data = response.json()
            print(f"✅ 投稿を作成しました: {title} (ID: {post_data['id']})")
            return True
            
    except Exception as e:
        print(f"❌ 投稿の作成/更新エラー: {e}")
        if hasattr(e, 'response') and e.response is not None:
            print(f"   レスポンス: {e.response.text}")
        return False


def main():
    """メイン処理"""
    # 変更されたファイルを取得（GitHub Actionsの環境変数から）
    # 実際の実装では、git diffやchanged files APIを使用
    
    # wordpress/posts/ ディレクトリをチェック
    posts_dir = Path('wordpress/posts')
    if not posts_dir.exists():
        print("⚠️  wordpress/posts/ ディレクトリが見つかりません")
        return
    
    # 全てのHTMLファイルを処理
    html_files = list(posts_dir.glob('*.html'))
    
    if not html_files:
        print("ℹ️  同期するファイルがありません")
        return
    
    print(f"📝 {len(html_files)}件のファイルを同期します...")
    
    for file_path in html_files:
        try:
            # ファイル名からスラッグを生成
            slug = file_path.stem  # 拡張子を除いたファイル名
            
            # ファイル内容を読み込み
            content = file_path.read_text(encoding='utf-8')
            
            # HTMLからタイトルを抽出（最初のh2見出しを優先）
            title = extract_title_from_html(content)
            if not title:
                # h2が見つからない場合はファイル名から生成
                title = slug.replace('-', ' ').replace('_', ' ').title()
            
            # WordPressに同期
            success = create_or_update_post(file_path, slug, title, content)
            
            if not success:
                print(f"⚠️  {file_path.name} の同期に失敗しました")
                
        except Exception as e:
            print(f"❌ エラー ({file_path.name}): {e}")
            continue
    
    print("✅ 同期処理が完了しました")


if __name__ == '__main__':
    main()
