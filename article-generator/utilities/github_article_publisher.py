#!/usr/bin/env python3
"""
GitHub経由の記事投稿スクリプト
スプレッドシートから承認済み記事を読み込み、MarkdownファイルとしてGitHubリポジトリにコミット
"""

import os
import sys
import re
from pathlib import Path
from datetime import datetime
from dotenv import load_dotenv
import subprocess
import json

# 親ディレクトリをパスに追加
sys.path.insert(0, str(Path(__file__).parent.parent))

from google_services.google_sheets import read_spreadsheet, write_spreadsheet
from social_media.line_notify import send_line_message

# .envファイルを読み込む
load_dotenv()

# 環境変数
APPROVAL_SPREADSHEET_ID = os.getenv('APPROVAL_SPREADSHEET_ID', '')

# リポジトリのルートディレクトリ
REPO_ROOT = Path(__file__).parent.parent.parent

# 記事保存ディレクトリ
ARTICLES_DIR = REPO_ROOT / 'wordpress' / 'posts'
DRAFTS_DIR = REPO_ROOT / 'wordpress' / 'drafts'  # 下書き用

# ディレクトリが存在しない場合は作成
ARTICLES_DIR.mkdir(parents=True, exist_ok=True)
DRAFTS_DIR.mkdir(parents=True, exist_ok=True)


def sanitize_filename(title):
    """
    タイトルをファイル名に変換（安全な文字のみ使用）
    
    Args:
        title: 記事タイトル
    
    Returns:
        ファイル名（.md拡張子付き）
    """
    # ファイル名として使えない文字を置換
    filename = re.sub(r'[<>:"/\\|?*]', '-', title)
    # 連続するハイフンを1つに
    filename = re.sub(r'-+', '-', filename)
    # 前後のハイフンを削除
    filename = filename.strip('-')
    # 長すぎる場合は切り詰め
    if len(filename) > 100:
        filename = filename[:100]
    
    # 小文字に変換（オプション）
    filename = filename.lower()
    
    return f"{filename}.md"


def save_article_to_github(title, markdown_content, status='draft'):
    """
    記事をMarkdownファイルとしてGitHubリポジトリに保存
    
    Args:
        title: 記事タイトル
        markdown_content: Markdown形式の記事本文
        status: ステータス（'draft' または 'published'）
    
    Returns:
        ファイルパス（成功時）、None（失敗時）
    """
    # ファイル名を生成
    filename = sanitize_filename(title)
    
    # 保存先ディレクトリを決定
    if status == 'draft':
        save_dir = DRAFTS_DIR
    else:
        save_dir = ARTICLES_DIR
    
    # ファイルパス
    file_path = save_dir / filename
    
    # ファイルを保存
    try:
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(markdown_content)
        
        print(f"✅ ファイルを保存しました: {file_path}")
        return file_path
    except Exception as e:
        print(f"❌ ファイル保存エラー: {e}")
        import traceback
        traceback.print_exc()
        return None


def git_add_and_commit(file_path, title, status='draft'):
    """
    Gitにファイルを追加してコミット
    
    Args:
        file_path: ファイルパス
        title: 記事タイトル
        status: ステータス（'draft' または 'published'）
    
    Returns:
        成功した場合True
    """
    try:
        # Gitリポジトリか確認
        git_dir = REPO_ROOT / '.git'
        if not git_dir.exists():
            print("⚠️ Gitリポジトリが見つかりません")
            return False
        
        # ファイルをステージング
        subprocess.run(
            ['git', 'add', str(file_path)],
            cwd=REPO_ROOT,
            check=True,
            capture_output=True
        )
        
        # コミットメッセージ
        status_text = '下書き' if status == 'draft' else '公開'
        commit_message = f"記事追加: {title} ({status_text})"
        
        # コミット
        subprocess.run(
            ['git', 'commit', '-m', commit_message],
            cwd=REPO_ROOT,
            check=True,
            capture_output=True
        )
        
        print(f"✅ Gitコミット完了: {commit_message}")
        return True
    except subprocess.CalledProcessError as e:
        print(f"⚠️ Git操作エラー: {e}")
        print(f"   標準出力: {e.stdout.decode() if e.stdout else ''}")
        print(f"   標準エラー: {e.stderr.decode() if e.stderr else ''}")
        return False
    except Exception as e:
        print(f"❌ Git操作エラー: {e}")
        import traceback
        traceback.print_exc()
        return False


def git_push():
    """
    Gitにプッシュ（オプション）
    
    Returns:
        成功した場合True
    """
    try:
        # 現在のブランチを取得
        result = subprocess.run(
            ['git', 'rev-parse', '--abbrev-ref', 'HEAD'],
            cwd=REPO_ROOT,
            check=True,
            capture_output=True,
            text=True
        )
        branch = result.stdout.strip()
        
        # プッシュ
        subprocess.run(
            ['git', 'push', 'origin', branch],
            cwd=REPO_ROOT,
            check=True,
            capture_output=True
        )
        
        print(f"✅ Gitプッシュ完了: {branch}")
        return True
    except subprocess.CalledProcessError as e:
        print(f"⚠️ Gitプッシュエラー: {e}")
        print(f"   標準エラー: {e.stderr.decode() if e.stderr else ''}")
        # プッシュエラーは致命的ではない（リモートリポジトリが設定されていない場合など）
        return False
    except Exception as e:
        print(f"❌ Gitプッシュエラー: {e}")
        import traceback
        traceback.print_exc()
        return False


def publish_approved_articles():
    """
    スプレッドシートから承認済み記事を読み込んでGitHubに保存
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
        print(f"📝 保存中: {article['title']}")
        
        # 記事をMarkdownファイルとして保存
        file_path = save_article_to_github(
            article['title'],
            article['content'],
            status='published'
        )
        
        if file_path:
            # Gitにコミット
            if git_add_and_commit(file_path, article['title'], status='published'):
                # ステータスを「投稿済み」に更新
                row_number = article['row_number']
                range_name = f'シート1!B{row_number}'
                write_spreadsheet(APPROVAL_SPREADSHEET_ID, range_name, [['投稿済み']])
                
                published_count += 1
                print(f"✅ 保存完了: {file_path}\n")
            else:
                print(f"⚠️ Gitコミットに失敗しました（ファイルは保存済み）\n")
        else:
            print(f"❌ ファイル保存に失敗しました\n")
    
    # Gitプッシュ（オプション）
    if published_count > 0:
        git_push()
        
        # LINE通知
        message = f"📝 GitHub記事保存完了\n\n{published_count}件の記事をGitHubリポジトリに保存しました。\nGitHub ActionsでWordPressに自動同期されます。"
        send_line_message(message)
        print(f"\n✅ {published_count}件の記事を保存しました")
    else:
        print("\n⚠️ 保存された記事はありませんでした")


def main():
    """メイン関数"""
    publish_approved_articles()


if __name__ == '__main__':
    main()
