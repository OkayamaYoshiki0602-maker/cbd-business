#!/usr/bin/env python3
"""
WordPress記事投稿スクリプト
スプレッドシートから承認済み記事を読み込み、WordPress REST APIで投稿
"""

import os
import sys
import re
import base64
from pathlib import Path
from dotenv import load_dotenv
import requests
from html import unescape

# 親ディレクトリをパスに追加
sys.path.insert(0, str(Path(__file__).parent.parent))

from google_services.google_sheets import read_spreadsheet, write_spreadsheet
from social_media.line_notify import send_line_message
from content.markdown_to_swell_html import markdown_to_swell_html

# .envファイルを読み込む
load_dotenv()

# 環境変数
WORDPRESS_URL = os.getenv('WORDPRESS_URL', 'https://cbd-no-hito.com')
WORDPRESS_USERNAME = os.getenv('WORDPRESS_USERNAME', '')
WORDPRESS_APP_PASSWORD = os.getenv('WORDPRESS_APP_PASSWORD', '')  # アプリケーションパスワード
APPROVAL_SPREADSHEET_ID = os.getenv('APPROVAL_SPREADSHEET_ID', '')

# WordPress REST APIエンドポイント
WORDPRESS_API_URL = f"{WORDPRESS_URL}/wp-json/wp/v2"


def markdown_to_html(markdown_text):
    """
    MarkdownをHTMLに変換（簡易版）
    
    Args:
        markdown_text: Markdown形式のテキスト
    
    Returns:
        HTML形式のテキスト
    """
    html = markdown_text
    
    # H1をH2に変換（WordPressではH1は記事タイトルとして扱われるため）
    html = re.sub(r'^#\s+(.+)$', r'<h2>\1</h2>', html, flags=re.MULTILINE)
    
    # H2
    html = re.sub(r'^##\s+(.+)$', r'<h2>\1</h2>', html, flags=re.MULTILINE)
    
    # H3
    html = re.sub(r'^###\s+(.+)$', r'<h3>\1</h3>', html, flags=re.MULTILINE)
    
    # H4
    html = re.sub(r'^####\s+(.+)$', r'<h4>\1</h4>', html, flags=re.MULTILINE)
    
    # 太字 **text**
    html = re.sub(r'\*\*(.+?)\*\*', r'<strong>\1</strong>', html)
    
    # リンク [text](url)
    html = re.sub(r'\[([^\]]+)\]\(([^\)]+)\)', r'<a href="\2">\1</a>', html)
    
    # リスト（簡易版）
    lines = html.split('\n')
    html_lines = []
    in_list = False
    
    for line in lines:
        # リスト項目
        if re.match(r'^[-*+]\s+', line):
            if not in_list:
                html_lines.append('<ul>')
                in_list = True
            content = re.sub(r'^[-*+]\s+', '', line)
            html_lines.append(f'<li>{content}</li>')
        elif re.match(r'^\d+\.\s+', line):
            if not in_list:
                html_lines.append('<ol>')
                in_list = True
            content = re.sub(r'^\d+\.\s+', '', line)
            html_lines.append(f'<li>{content}</li>')
        else:
            if in_list:
                html_lines.append('</ul>' if '<ul>' in html_lines else '</ol>')
                in_list = False
            
            # 空行でない場合、段落として扱う
            if line.strip() and not line.strip().startswith('<'):
                html_lines.append(f'<p>{line}</p>')
            elif not line.strip():
                html_lines.append('')
    
    if in_list:
        html_lines.append('</ul>')
    
    html = '\n'.join(html_lines)
    
    # HTMLエンティティをデコード
    html = unescape(html)
    
    return html


def extract_meta_description(markdown_text):
    """
    Markdownからメタディスクリプションを抽出
    
    Args:
        markdown_text: Markdown形式のテキスト
    
    Returns:
        メタディスクリプション（150文字以内）
    """
    # 「## メタディスクリプション」セクションを探す
    meta_match = re.search(r'^##\s*メタディスクリプション\s*\n(.+?)(?=\n##|$)', markdown_text, re.MULTILINE | re.DOTALL)
    if meta_match:
        meta = meta_match.group(1).strip()
        # 150文字以内に制限
        if len(meta) > 150:
            meta = meta[:147] + '...'
        return meta
    
    # メタディスクリプションが見つからない場合、最初の段落を使用
    first_paragraph = re.search(r'^[^#\n]+', markdown_text, re.MULTILINE)
    if first_paragraph:
        meta = first_paragraph.group(0).strip()
        if len(meta) > 150:
            meta = meta[:147] + '...'
        return meta
    
    return None


def get_wordpress_category_id(category_name):
    """
    WordPressのカテゴリー名からIDを取得
    
    Args:
        category_name: カテゴリー名
    
    Returns:
        カテゴリーID（見つからない場合はNone）
    """
    if not WORDPRESS_USERNAME or not WORDPRESS_APP_PASSWORD:
        return None
    
    auth = base64.b64encode(f"{WORDPRESS_USERNAME}:{WORDPRESS_APP_PASSWORD}".encode()).decode()
    headers = {
        'Authorization': f'Basic {auth}',
        'Content-Type': 'application/json'
    }
    
    try:
        # カテゴリー一覧を取得
        response = requests.get(
            f"{WORDPRESS_API_URL}/categories?search={category_name}",
            headers=headers,
            timeout=30
        )
        
        if response.status_code == 200:
            categories = response.json()
            # 完全一致するカテゴリーを探す
            for cat in categories:
                if cat.get('name', '').lower() == category_name.lower():
                    return cat.get('id')
            # 部分一致でも見つからない場合は最初の結果を返す
            if categories:
                return categories[0].get('id')
        
        return None
    except Exception as e:
        print(f"⚠️ カテゴリーID取得エラー: {e}")
        return None


def get_wordpress_tag_ids(tag_names):
    """
    WordPressのタグ名のリストからIDのリストを取得（存在しない場合は作成）
    
    Args:
        tag_names: タグ名のリスト
    
    Returns:
        タグIDのリスト
    """
    if not WORDPRESS_USERNAME or not WORDPRESS_APP_PASSWORD:
        return []
    
    if not tag_names:
        return []
    
    auth = base64.b64encode(f"{WORDPRESS_USERNAME}:{WORDPRESS_APP_PASSWORD}".encode()).decode()
    headers = {
        'Authorization': f'Basic {auth}',
        'Content-Type': 'application/json'
    }
    
    tag_ids = []
    
    for tag_name in tag_names:
        if not tag_name.strip():
            continue
        
        try:
            # 既存のタグを検索
            response = requests.get(
                f"{WORDPRESS_API_URL}/tags?search={tag_name}",
                headers=headers,
                timeout=30
            )
            
            found = False
            if response.status_code == 200:
                tags = response.json()
                # 完全一致するタグを探す
                for tag in tags:
                    if tag.get('name', '').lower() == tag_name.lower():
                        tag_ids.append(tag.get('id'))
                        found = True
                        break
            
            # 見つからない場合は新規作成
            if not found:
                create_response = requests.post(
                    f"{WORDPRESS_API_URL}/tags",
                    headers=headers,
                    json={'name': tag_name},
                    timeout=30
                )
                
                if create_response.status_code == 201:
                    tag_data = create_response.json()
                    tag_ids.append(tag_data.get('id'))
                elif create_response.status_code == 200:
                    # 既に存在する場合（200が返される場合がある）
                    tag_data = create_response.json()
                    tag_ids.append(tag_data.get('id'))
        
        except Exception as e:
            print(f"⚠️ タグ「{tag_name}」のID取得エラー: {e}")
            continue
    
    return tag_ids


def post_to_wordpress(title, content_markdown, status='draft', category_ids=None, tags=None, category_name=None, tag_names=None):
    """
    WordPress REST APIで記事を投稿
    
    Args:
        title: 記事タイトル
        content_markdown: Markdown形式の記事本文
        status: 投稿ステータス（'draft', 'publish'）
        category_ids: カテゴリIDのリスト
        tags: タグのリスト
    
    Returns:
        投稿された記事のURL（成功時）、None（失敗時）
    """
    if not WORDPRESS_USERNAME or not WORDPRESS_APP_PASSWORD:
        print("⚠️ WORDPRESS_USERNAMEまたはWORDPRESS_APP_PASSWORDが設定されていません")
        return None
    
    # MarkdownをSWELL形式のHTMLに変換
    try:
        content_html = markdown_to_swell_html(content_markdown, add_disclaimer=True, add_toc=True)
        print(f"✅ SWELL変換完了（HTML文字数: {len(content_html)}）")
    except Exception as e:
        print(f"⚠️ SWELL変換エラー: {e}（簡易変換にフォールバック）")
        import traceback
        traceback.print_exc()
        # エラー時は簡易変換にフォールバック
        content_html = markdown_to_html(content_markdown)
    
    # メタディスクリプションを抽出
    meta_description = extract_meta_description(content_markdown)
    
    # WordPress REST APIで投稿
    auth = base64.b64encode(f"{WORDPRESS_USERNAME}:{WORDPRESS_APP_PASSWORD}".encode()).decode()
    
    headers = {
        'Authorization': f'Basic {auth}',
        'Content-Type': 'application/json'
    }
    
    data = {
        'title': title,
        'content': content_html,
        'status': status,
        'format': 'standard'  # 標準フォーマット（HTMLブロック）
    }
    
    # メタディスクリプションを追加（Yoast SEOプラグインを使用している場合）
    if meta_description:
        data['meta'] = {
            'description': meta_description
        }
    
    # カテゴリーIDを取得・設定
    if category_ids:
        data['categories'] = category_ids
    elif category_name:
        # カテゴリー名からIDを取得
        cat_id = get_wordpress_category_id(category_name)
        if cat_id:
            data['categories'] = [cat_id]
    
    # タグIDを取得・設定
    if tags:
        # tagsがIDのリストの場合
        data['tags'] = tags
    elif tag_names:
        # tag_namesがタグ名のリストの場合、IDを取得
        tag_ids = get_wordpress_tag_ids(tag_names)
        if tag_ids:
            data['tags'] = tag_ids
    
    try:
        response = requests.post(
            f"{WORDPRESS_API_URL}/posts",
            headers=headers,
            json=data,
            timeout=60  # タイムアウトを60秒に延長
        )
        
        if response.status_code == 201:
            post_data = response.json()
            post_url = post_data.get('link', '')
            post_id = post_data.get('id', '')
            
            # 投稿されたコンテンツを確認
            content_raw = post_data.get('content', {}).get('raw', '')
            content_rendered = post_data.get('content', {}).get('rendered', '')
            print(f"✅ WordPressに投稿しました: {post_url}")
            print(f"   投稿ID: {post_id}")
            print(f"   コンテンツ（raw）文字数: {len(content_raw)}")
            print(f"   コンテンツ（rendered）文字数: {len(content_rendered)}")
            
            if not content_raw and content_rendered:
                print(f"   ⚠️ rawコンテンツは空ですが、renderedコンテンツは存在します")
                print(f"   エディタで表示されるはずです。確認してください: {post_url}")
            
            return post_url
        else:
            print(f"❌ WordPress投稿エラー: {response.status_code}")
            print(f"   レスポンス: {response.text[:500]}")  # レスポンスを拡大表示
            return None
    except requests.exceptions.ReadTimeout:
        print(f"⚠️ WordPress REST APIへの接続がタイムアウトしました（60秒）")
        print(f"   WordPressサイト（{WORDPRESS_URL}）がアクセス可能か確認してください")
        return None
    except requests.exceptions.ConnectionError as e:
        print(f"⚠️ WordPress REST APIへの接続エラー: {e}")
        print(f"   WordPressサイト（{WORDPRESS_URL}）がアクセス可能か確認してください")
        return None
    except Exception as e:
        print(f"❌ WordPress投稿エラー: {e}")
        import traceback
        traceback.print_exc()
        return None


def publish_approved_articles():
    """
    スプレッドシートから承認済み記事を読み込んでWordPressに投稿
    """
    if not APPROVAL_SPREADSHEET_ID:
        print("⚠️ APPROVAL_SPREADSHEET_IDが設定されていません")
        return
    
    # スプレッドシートからデータを読み込み
    # 列A: タイムスタンプ、列B: ステータス、列C: 記事タイトル、列D: 記事本文（Markdown）
    sheet_data = read_spreadsheet(APPROVAL_SPREADSHEET_ID, 'シート1!A:F')
    
    if not sheet_data or len(sheet_data) < 2:
        print("⚠️ スプレッドシートにデータが見つかりません")
        return
    
    # ヘッダー行をスキップ
    rows = sheet_data[1:]
    
    # ステータスが「承認済み」の記事を探す
    approved_articles = []
    for i, row in enumerate(rows, start=2):
        if len(row) >= 3 and row[1] == '承認済み':
            approved_articles.append({
                'row_number': i,
                'title': row[2] if len(row) > 2 else '',
                'content': row[3] if len(row) > 3 else '',
                'target': row[4] if len(row) > 4 else '',
                'concern': row[5] if len(row) > 5 else ''
            })
    
    if not approved_articles:
        print("✅ 承認済みの記事はありません")
        return
    
    print(f"📝 {len(approved_articles)}件の承認済み記事を検出しました\n")
    
    published_count = 0
    
    for article in approved_articles:
        print(f"📝 投稿中: {article['title']}")
        
        # WordPressに投稿
        post_url = post_to_wordpress(
            article['title'],
            article['content'],
            status='publish'  # 公開状態で投稿
        )
        
        if post_url:
            # ステータスを「投稿済み」に更新
            row_number = article['row_number']
            range_name = f'シート1!B{row_number}'
            write_spreadsheet(APPROVAL_SPREADSHEET_ID, range_name, [['投稿済み']])
            
            published_count += 1
            print(f"✅ 投稿完了: {post_url}\n")
        else:
            print(f"❌ 投稿失敗\n")
    
    # LINE通知
    if published_count > 0:
        message = f"📝 WordPress投稿完了\n\n{published_count}件の記事を投稿しました。"
        send_line_message(message)
        print(f"\n✅ {published_count}件の記事を投稿しました")
    else:
        print("\n⚠️ 投稿された記事はありませんでした")


def main():
    """メイン関数"""
    publish_approved_articles()


if __name__ == '__main__':
    main()
