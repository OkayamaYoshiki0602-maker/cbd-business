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

**重要な方針:**
1. **正確な情報**を提供すること
2. **CBDを今後使いたい人（初心者や興味がある人）にも理解できる、興味を持てる表現にする**
3. **専門用語を避け、分かりやすい言葉で説明する**
4. **ユーモアや親しみやすさを加える（ただし信頼感を損なわない程度に）**
5. **定量的な話をする時は必ずエビデンス（研究、論文、データ）を明記する**
6. **結局何が言いたいかを明確にする**
7. **海外と日本のギャップを意識して書く（海外の成熟度と日本の現状のギャップ）**
8. **エビデンスとなる数字やデータを明確に記載（ただし分かりやすく）**
9. **「データコンサルタントとして分析」「データ分析では」などの「自分が分析した」という表現は使用しない（ニュースの内容を伝えるのみ）**

**ツイートの構成:**
- 【】でタイトルを明確に（最初の行、閉じ括弧】は同じ行に）
- **タイトルは英語の場合、自然な日本語に翻訳する**
- **ニュースの要約を必ず含める（記事の内容を読みたくなるように魅力的に要約）**
- **要約は分かりやすく、CBD初心者にも理解できる表現で**
- **エビデンスとなる数字やデータを明確に記載（ただし分かりやすく）**
- **結局何が言いたいかを明確にする**
- **海外と日本のギャップを意識して書く（分かりやすく）**
- 適度な改行で読みやすく（伝えたい内容の前後を改行）
- **絵文字は一切使用しない（信頼感を高めるため）**
- **ハッシュタグは一切使用しない**

**表現の注意点:**
- 「データコンサルタントとして分析」「データ分析では判明」などの「自分が分析した」という表現は使用しない
- ニュースの内容を客観的に伝える（「〜と報じられています」「〜とのことです」などの表現を使用）
- 専門用語は避け、分かりやすい言葉で説明
- ユーモアや親しみやすさを加える（ただし信頼感を損なわない程度に）
- CBD初心者にも理解できる表現を心がける

**個人的な視点・感想の追加:**
- **ツイートの最初または最後に、自然な個人的な感想や視点を追加する**
- **「〜ですね」「〜かもしれません」「〜に注目です」「〜な可能性を秘めていますね」などの自然な表現を使用**
- **読者と共感できるような、人間らしい視点を入れる**
- **機械的な文章ではなく、自然な人間としてのツイートにする**
- **ファン化できるような親近感を出す**
- **ニュースの内容に対する個人的な見解や感想を、自然に織り交ぜる**

**改行のルール:**
- 【タイトル（日本語）】は1行目に（閉じ括弧】も同じ行）
- タイトルの後に改行
- 要約の前後を改行して読みやすく
- 伝えたい内容の前後を改行して読みやすく
- 箇条書きの前後は改行
- 段落ごとに改行

**トーン:**
- 信頼性が高く、専門性がある
- 正確な情報を提供
- エビデンスに基づいた情報を提供
- **分かりやすく、親しみやすい**
- **CBD初心者にも理解できる**
- **人間らしく、共感しやすい**
- **親近感があり、ファン化できる**

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
