#!/usr/bin/env python3
"""
URL短縮スクリプト
長いURLを短縮してツイートに使用
"""

import os
import sys
import re
from pathlib import Path
from dotenv import load_dotenv
import requests

# 親ディレクトリをパスに追加
sys.path.insert(0, str(Path(__file__).parent.parent))

# .envファイルを読み込む
load_dotenv()

# Bitly API設定（オプション）
BITLY_ACCESS_TOKEN = os.getenv('BITLY_ACCESS_TOKEN', '')


def shorten_url_bitly(url):
    """
    Bitly APIでURLを短縮
    
    Args:
        url: 短縮したいURL
    
    Returns:
        短縮されたURL（失敗した場合は元のURL）
    """
    if not BITLY_ACCESS_TOKEN:
        return url
    
    try:
        headers = {
            'Authorization': f'Bearer {BITLY_ACCESS_TOKEN}',
            'Content-Type': 'application/json'
        }
        
        payload = {
            'long_url': url
        }
        
        response = requests.post(
            'https://api-ssl.bitly.com/v4/shorten',
            headers=headers,
            json=payload,
            timeout=10
        )
        
        if response.status_code == 201:
            result = response.json()
            return result.get('link', url)
        else:
            print(f"⚠️ Bitly URL短縮エラー: {response.status_code}, {response.text}")
            return url
    
    except Exception as e:
        print(f"⚠️ Bitly URL短縮エラー: {e}")
        return url


def shorten_url_simple(url):
    """
    簡易的なURL短縮（長いURLを切り詰める）
    
    Args:
        url: 短縮したいURL
    
    Returns:
        短縮されたURL（表示用）
    """
    # 長いURLの場合、表示を短縮
    if len(url) > 50:
        # ドメイン部分を保持して、パスを短縮
        match = re.match(r'(https?://[^/]+)(/.+)', url)
        if match:
            domain = match.group(1)
            path = match.group(2)
            if len(path) > 30:
                path = path[:27] + '...'
            return f"{domain}{path}"
    
    return url


def shorten_url(url, use_service='auto'):
    """
    URLを短縮
    
    Args:
        url: 短縮したいURL
        use_service: 使用するサービス（'bitly', 'simple', 'auto'）
    
    Returns:
        短縮されたURL
    
    注意:
    - Twitter (X) では、実際のURLの長さに関わらず、URLは23文字としてカウントされます
    - ただし、表示上は短縮URLを使用することで、ツイートの見た目をすっきりさせられます
    """
    if not url:
        return url
    
    # Bitlyを使用する場合
    if use_service == 'bitly' or (use_service == 'auto' and BITLY_ACCESS_TOKEN):
        short_url = shorten_url_bitly(url)
        if short_url != url:
            return short_url
    
    # 簡易的な短縮を使用（表示用）
    if use_service == 'simple' or (use_service == 'auto' and not BITLY_ACCESS_TOKEN):
        return shorten_url_simple(url)
    
    # デフォルト: 元のURLを返す
    return url


def main():
    """メイン関数（テスト用）"""
    if len(sys.argv) < 2:
        print("使用方法:")
        print("  python url_shortener.py shorten <URL> [service]")
        print("\n例:")
        print("  python url_shortener.py shorten https://example.com/very/long/url/path bitly")
        print("\nサービス: bitly, simple, auto")
        sys.exit(1)
    
    command = sys.argv[1]
    
    if command == 'shorten':
        if len(sys.argv) < 3:
            print("エラー: URLが必要です")
            sys.exit(1)
        
        url = sys.argv[2]
        service = sys.argv[3] if len(sys.argv) > 3 else 'auto'
        
        short_url = shorten_url(url, service)
        
        print(f"📎 URL短縮結果:")
        print(f"元のURL: {url} ({len(url)}文字)")
        print(f"短縮URL: {short_url} ({len(short_url)}文字)")
    
    else:
        print(f"不明なコマンド: {command}")
        sys.exit(1)


if __name__ == '__main__':
    main()
