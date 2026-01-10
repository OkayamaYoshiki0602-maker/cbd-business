#!/usr/bin/env python3
"""
WordPress記事要約スクリプト
記事本文を取得して要約・見所を抽出
"""

import os
import sys
import re
import html
from pathlib import Path
from dotenv import load_dotenv
import requests
from bs4 import BeautifulSoup

# 親ディレクトリをパスに追加
sys.path.insert(0, str(Path(__file__).parent.parent))

from social_media.news_summarizer import summarize_news
from social_media.url_shortener import shorten_url

# .envファイルを読み込む
load_dotenv()

GEMINI_API_KEY = os.getenv('GEMINI_API_KEY', '')


def fetch_article_content(article_url):
    """
    WordPress記事の本文を取得
    
    Args:
        article_url: 記事URL
    
    Returns:
        記事本文テキスト（HTMLタグを除去）
    """
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36'
        }
        
        response = requests.get(article_url, headers=headers, timeout=10)
        response.raise_for_status()
        
        # HTMLをパース
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # WordPress記事本文を取得（一般的なクラス名）
        content_selectors = [
            '.entry-content',
            '.post-content',
            '.article-content',
            'article .content',
            'main article',
            '.wp-block-post-content'
        ]
        
        article_text = ""
        for selector in content_selectors:
            content = soup.select_one(selector)
            if content:
                # テキストのみを取得（HTMLタグを除去）
                article_text = content.get_text(separator='\n', strip=True)
                break
        
        # セレクターで見つからない場合、body全体から本文らしい部分を抽出
        if not article_text:
            # <p>タグのテキストを結合
            paragraphs = soup.find_all('p')
            article_text = '\n'.join([p.get_text(strip=True) for p in paragraphs if p.get_text(strip=True)])
        
        # HTMLエンティティをデコード
        article_text = html.unescape(article_text)
        
        # 余分な空白を除去
        article_text = re.sub(r'\s+', ' ', article_text).strip()
        
        return article_text
    
    except Exception as e:
        print(f"⚠️ 記事本文取得エラー: {e}")
        return None


def summarize_article_with_highlights(article_url, article_title, max_length=200):
    """
    WordPress記事を要約して見所を抽出
    
    Args:
        article_url: 記事URL
        article_title: 記事タイトル
        max_length: 最大文字数
    
    Returns:
        要約テキスト（見所を含む）
    """
    try:
        # 記事本文を取得
        article_content = fetch_article_content(article_url)
        
        if not article_content:
            return None
        
        # Gemini APIで要約（見所を含む）
        if GEMINI_API_KEY:
            import google.generativeai as genai
            
            genai.configure(api_key=GEMINI_API_KEY)
            try:
                model = genai.GenerativeModel('gemini-2.5-flash')  # 最新の安定版
            except:
                try:
                    model = genai.GenerativeModel('gemini-3-flash-preview')  # 最新のプレビュー版
                except:
                    try:
                        model = genai.GenerativeModel('gemini-2.0-flash')  # フォールバック
                    except:
                        models = genai.list_models()
                        if models:
                            model = genai.GenerativeModel(models[0].name)
                        else:
                            raise ValueError("利用可能なGeminiモデルが見つかりません")
            
            prompt = f"""あなたはCBD・大麻分野の専門ライターです。

以下のWordPress記事を読んで、要約と見所を{max_length}文字以内で抽出してください。

要件:
- 記事の要点を簡潔にまとめる
- 見所・重要なポイントを強調する
- 数字や具体的な情報を含める
- 読者の興味を引く表現を使用
- HTMLタグやマークダウン記号は含めない

記事タイトル: {article_title}
記事URL: {article_url}

記事本文:
{article_content[:3000]}  # 最初の3000文字を使用
"""
            
            response = model.generate_content(prompt)
            summary = response.text.strip()
            
            # HTMLタグを除去
            summary = re.sub(r'<[^>]+>', '', summary)
            
            # 文字数制限
            if len(summary) > max_length:
                # 最後の句点まで
                last_period = summary[:max_length].rfind('。')
                if last_period > max_length * 0.7:
                    summary = summary[:last_period+1]
                else:
                    summary = summary[:max_length-3] + "..."
            
            return summary
        
        else:
            # Gemini APIが使えない場合、ローカル要約
            return summarize_news(f"{article_title}\n\n{article_content}", max_length)
    
    except Exception as e:
        print(f"⚠️ 記事要約エラー: {e}")
        import traceback
        traceback.print_exc()
        return None


def main():
    """メイン関数（テスト用）"""
    if len(sys.argv) < 2:
        print("使用方法:")
        print("  python article_summarizer.py summarize <記事URL> [記事タイトル]")
        print("\n例:")
        print("  python article_summarizer.py summarize https://cbd-no-hito.com/article '記事タイトル'")
        sys.exit(1)
    
    command = sys.argv[1]
    
    if command == 'summarize':
        if len(sys.argv) < 3:
            print("エラー: 記事URLが必要です")
            sys.exit(1)
        
        article_url = sys.argv[2]
        article_title = sys.argv[3] if len(sys.argv) > 3 else "記事タイトル"
        
        print(f"📝 記事を要約しています: {article_title}")
        summary = summarize_article_with_highlights(article_url, article_title, max_length=200)
        
        if summary:
            print("\n" + "=" * 60)
            print("要約結果:")
            print("=" * 60)
            print(summary)
            print("=" * 60)
            print(f"\n文字数: {len(summary)}/200")
        else:
            print("❌ 記事の要約に失敗しました")
    
    else:
        print(f"不明なコマンド: {command}")
        sys.exit(1)


if __name__ == '__main__':
    main()
