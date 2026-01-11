#!/usr/bin/env python3
"""
ニュース型ツイート生成スクリプト（AI活用版）
直近1か月のCBD・大麻関連ニュースから、意外性・効果・研究・社会への影響を考慮したツイートを生成
"""

import os
import sys
import re
from pathlib import Path
from dotenv import load_dotenv

# 親ディレクトリをパスに追加
sys.path.insert(0, str(Path(__file__).parent.parent))

from social_media.news_summarizer import summarize_news
from social_media.url_shortener import shorten_url

# .envファイルを読み込む
load_dotenv()

GEMINI_API_KEY = os.getenv('GEMINI_API_KEY', '')


def generate_news_tweet_with_ai(news_title, news_content, news_url=None, max_length=280):
    """
    AIを使用してニュース型ツイートを生成（意外性・効果・研究・社会への影響を考慮）
    
    Args:
        news_title: ニュースタイトル
        news_content: ニュース本文
        news_url: ニュースURL（オプション）
        max_length: 最大文字数（デフォルト: 280）
    
    Returns:
        ツイート文案（280文字以内、リンク短縮対応）
    """
    try:
        # Gemini APIで要約・ツイート文案を生成
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
            
            # URLの長さを考慮（TwitterではURLは23文字としてカウント）
            url_length = 23 if news_url else 0
            hashtag = "#CBD"
            hashtag_length = len(hashtag) + 1  # +1は改行
            available_length = max_length - url_length - hashtag_length - 10  # 余裕を持たせる
            
            prompt = f"""あなたはCBD・大麻分野の専門ライターです。

以下のニュースを読んで、日本の人々が興味を持ちそうなツイート文案を{available_length}文字以内で生成してください。

要件:
1. **正確な情報**を提供すること
2. **意外性**や**知られざる情報**を強調すること
3. **CBDや大麻成分の効果、研究結果**を含めること
4. **大麻による社会への影響（政治、経済など）**を含めること
5. 数字や具体的な情報を含めること
6. 読者の興味を引く表現を使用すること
7. HTMLタグやマークダウン記号は含めないこと
8. 改行は\nを使用すること

ニュースタイトル: {news_title}
ニュースURL: {news_url or 'なし'}

ニュース本文:
{news_content[:2000]}  # 最初の2000文字を使用

ツイート文案を生成してください（{available_length}文字以内）:
"""
            
            response = model.generate_content(prompt)
            tweet_body = response.text.strip()
            
            # HTMLタグを除去
            tweet_body = re.sub(r'<[^>]+>', '', tweet_body)
            
            # 文字数制限
            if len(tweet_body) > available_length:
                # 最後の句点まで
                last_period = tweet_body[:available_length].rfind('。')
                if last_period > available_length * 0.7:
                    tweet_body = tweet_body[:last_period+1]
                else:
                    tweet_body = tweet_body[:available_length-3] + "..."
            
            # ツイート文案を組み立て
            tweet_text = tweet_body
            if news_url:
                short_url = shorten_url(news_url)
                tweet_text += f"\n\n{short_url}"
            
            # ツイートフォーマッターを適用（ハッシュタグは削除、改行・タイトルを追加）
            try:
                from social_media.tweet_formatter import format_tweet
                tweet_text = format_tweet(tweet_text, style='elegant')
            except Exception as e:
                print(f"⚠️ ツイートフォーマットエラー: {e}")
                # フォールバック: ハッシュタグのみ削除
                tweet_text = re.sub(r'#\w+\s*', '', tweet_text)
                tweet_text = tweet_text.strip()
            
            # 最終チェック
            if len(tweet_text) > max_length:
                # URLがあれば保持
                url_match = re.search(r'(https?://[^\s]+)', tweet_text)
                url = url_match.group(1) if url_match else None
                
                if url:
                    text_without_url = tweet_text.replace(url, '')
                    max_main_length = max_length - len(url) - 2
                    if len(text_without_url) > max_main_length:
                        last_period = text_without_url[:max_main_length].rfind('。')
                        if last_period > max_main_length * 0.7:
                            text_without_url = text_without_url[:last_period+1]
                        else:
                            text_without_url = text_without_url[:max_main_length-3] + '...'
                        tweet_text = f"{text_without_url}\n\n{url}"
                else:
                    last_period = tweet_text[:max_length].rfind('。')
                    if last_period > max_length * 0.7:
                        tweet_text = tweet_text[:last_period+1]
                    else:
                        tweet_text = tweet_text[:max_length-3] + '...'
            
            return tweet_text
        
        else:
            # Gemini APIが使えない場合、既存のロジックを使用
            from social_media.tweet_generator_v2 import generate_news_tweet
            return generate_news_tweet(news_title, news_content, news_url)
    
    except Exception as e:
        print(f"⚠️ ニュースツイート生成エラー: {e}")
        import traceback
        traceback.print_exc()
        
        # フォールバック: 既存のロジックを使用
        from social_media.tweet_generator_v2 import generate_news_tweet
        return generate_news_tweet(news_title, news_content, news_url)


def main():
    """メイン関数（テスト用）"""
    if len(sys.argv) < 2:
        print("使用方法:")
        print("  python news_tweet_generator.py generate <ニュースタイトル> <ニュース本文> [URL]")
        print("\n例:")
        print("  python news_tweet_generator.py generate 'ニュースタイトル' 'ニュース本文...' 'https://example.com'")
        sys.exit(1)
    
    command = sys.argv[1]
    
    if command == 'generate':
        if len(sys.argv) < 4:
            print("エラー: ニュースタイトルと本文が必要です")
            sys.exit(1)
        
        news_title = sys.argv[2]
        news_content = sys.argv[3]
        news_url = sys.argv[4] if len(sys.argv) > 4 else None
        
        tweet = generate_news_tweet_with_ai(news_title, news_content, news_url)
        
        print("📝 生成されたツイート文案:")
        print("=" * 60)
        print(tweet)
        print("=" * 60)
        print(f"文字数: {len(tweet)}/280")
    
    else:
        print(f"不明なコマンド: {command}")
        sys.exit(1)


if __name__ == '__main__':
    main()
