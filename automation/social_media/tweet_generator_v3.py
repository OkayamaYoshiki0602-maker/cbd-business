#!/usr/bin/env python3
"""
ツイート生成スクリプト（v3: 新しい方向性に合わせた改善版）
実体験×データ分析型: 60%、ライフスタイル型: 30%、その他: 10%

目標: 「安心してCBDを買ってくれる人を増やす（CBDの不安感を払拭）」
「幅広く正確なCBDや大麻情報を発信する」
"""

import os
import sys
import re
import random
from pathlib import Path
from dotenv import load_dotenv

# 親ディレクトリをパスに追加
sys.path.insert(0, str(Path(__file__).parent.parent))

from social_media.url_shortener import shorten_url
from social_media.tweet_formatter import format_tweet

# .envファイルを読み込む
load_dotenv()

GEMINI_API_KEY = os.getenv('GEMINI_API_KEY', '')


def generate_tweet_by_type(content_type, article_title=None, article_content=None, article_url=None, news_title=None, news_content=None, news_url=None, max_length=280):
    """
    方向性に応じたツイートを生成
    
    Args:
        content_type: 'data_analysis' (60%), 'lifestyle' (30%), 'other' (10%)
        article_title: 記事タイトル（記事の場合）
        article_content: 記事本文（記事の場合）
        article_url: 記事URL（記事の場合）
        news_title: ニュースタイトル（ニュースの場合）
        news_content: ニュース本文（ニュースの場合）
        news_url: ニュースURL（ニュースの場合）
        max_length: 最大文字数
    
    Returns:
        ツイート文案
    """
    if content_type == 'data_analysis':
        return generate_data_analysis_tweet(article_title, article_content, article_url, news_title, news_content, news_url, max_length)
    elif content_type == 'lifestyle':
        return generate_lifestyle_tweet(article_title, article_content, article_url, max_length)
    elif content_type == 'other':
        return generate_other_tweet(news_title, news_content, news_url, max_length)
    else:
        # デフォルト: データ分析型
        return generate_data_analysis_tweet(article_title, article_content, article_url, news_title, news_content, news_url, max_length)


def generate_data_analysis_tweet(article_title=None, article_content=None, article_url=None, news_title=None, news_content=None, news_url=None, max_length=280):
    """
    実体験×データ分析型のツイートを生成（60%）
    
    コンセプト:
    - CBDの実体験とデータ分析を組み合わせて、信頼性と専門性を両立
    - 幅広く正確なCBDや大麻情報を発信
    - 趣味（ポーカー、マラソン、お酒）は無理に組み合わせない
    """
    try:
        if GEMINI_API_KEY:
            import google.generativeai as genai
            
            genai.configure(api_key=GEMINI_API_KEY)
            try:
                model = genai.GenerativeModel('gemini-2.5-flash')
            except:
                try:
                    model = genai.GenerativeModel('gemini-3-flash-preview')
                except:
                    try:
                        model = genai.GenerativeModel('gemini-2.0-flash')
                    except:
                        models = genai.list_models()
                        model = genai.GenerativeModel(models[0].name) if models else None
            
            if not model:
                return generate_fallback_tweet(article_title, article_url, news_title, news_url, max_length)
            
            # URLの長さを考慮
            url = article_url or news_url
            url_length = 23 if url else 0
            available_length = max_length - url_length - 10  # 余裕を持たせる
            
            # コンテンツを取得
            is_news = False
            if article_title and article_content:
                source_text = f"タイトル: {article_title}\n\n{article_content[:2000]}"
                source_type = "記事"
            elif news_title and news_content:
                source_text = f"タイトル: {news_title}\n\n{news_content[:2000]}"
                source_type = "ニュース"
                is_news = True
            else:
                return generate_fallback_tweet(article_title, article_url, news_title, news_url, max_length)
            
            # ニュースの場合は特別な注意事項を追加
            news_warning = ""
            if is_news:
                news_warning = """
**ニュースに関する重要な注意事項:**
- **「データコンサルタントとして分析」「データ分析では」などの「自分が分析した」という表現は使用しない**
- **ニュースの内容を客観的に伝える（「〜と報じられています」「〜とのことです」などの表現を使用）**
- **CBD初心者にも理解できる、分かりやすい表現を心がける**
- **専門用語を避け、分かりやすい言葉で説明する**
- **ユーモアや親しみやすさを加える（ただし信頼感を損なわない程度に）**
"""
            
            prompt = f"""あなたはCBD・大麻分野の専門ライターで、データコンサルタントの視点を持っています。

以下の{source_type}を読んで、実体験×データ分析型のツイート文案を{available_length}文字以内で生成してください。

**重要な方針:**
1. **幅広く正確なCBDや大麻情報を発信する**
2. **実体験とデータ分析を組み合わせる（ただし、ニュースの場合は「自分が分析した」という表現は使用しない）**
3. **信頼性・専門性を最優先**
4. **趣味（ポーカー、マラソン、お酒）を無理に組み合わせない**
5. **実際の論文や研究で関係性がある場合のみ、実体験を絡める**
{news_warning}

**ツイートの構成:**
- 【】でタイトルを明確に（最初の行、閉じ括弧】は同じ行に）
- **記事の要約を必ず含める（記事の内容を読みたくなるように魅力的に要約）**
- **要約は見やすい形で、記事の要点を簡潔に伝える**
- データ分析の視点を入れる（「〇〇件分析」「〇〇%」など）
- 実体験がある場合は、簡潔に含める
- 具体的な数字や根拠を含める
- **定量的な話をする時は必ずエビデンス（研究、論文、データ）を明記する**
- 適度な改行で読みやすく（伝えたい内容の前後を改行）
- 箇条書き（・）を活用
- **絵文字は一切使用しない（信頼感を高めるため）**
- **ハッシュタグは一切使用しない**

**要約の要件:**
- 記事の要点を簡潔に伝える（2-3文程度）
- 読者が「この記事を読みたい」と思うような魅力的な要約
- 具体的な情報や数字を含める
- 記事の価値を明確に伝える

**個人的な視点・感想の追加:**
- **ツイートの最初または最後に、自然な個人的な感想や視点を追加する**
- **「〜ですね」「〜かもしれません」「〜に注目です」などの自然な表現を使用**
- **読者と共感できるような、人間らしい視点を入れる**
- **機械的な文章ではなく、自然な人間としてのツイートにする**
- **ファン化できるような親近感を出す**

**トーン:**
- 信頼性が高く、専門性がある
- 安心感を与える
- 正確な情報を提供
- エビデンスに基づいた情報を提供
- **人間らしく、共感しやすい**
- **親近感があり、ファン化できる**

**改行のルール:**
- 【タイトル】は1行目に（閉じ括弧】も同じ行）
- タイトルの後に改行
- 要約の前後を改行して読みやすく
- 伝えたい内容の前後を改行して読みやすく
- 箇条書きの前後は改行
- 段落ごとに改行

{source_type}:
{source_text}

ツイート文案を生成してください（{available_length}文字以内）:
"""
            
            response = model.generate_content(prompt)
            tweet_body = response.text.strip()
            tweet_body = re.sub(r'<[^>]+>', '', tweet_body)
            
            # 文字数制限
            if len(tweet_body) > available_length:
                last_period = tweet_body[:available_length].rfind('。')
                if last_period > available_length * 0.7:
                    tweet_body = tweet_body[:last_period+1]
                else:
                    tweet_body = tweet_body[:available_length-3] + "..."
            
            # フォーマット
            tweet_text = format_tweet(tweet_body, style='elegant')
            
            # URLを追加
            if url:
                short_url = shorten_url(url)
                if short_url not in tweet_text:
                    tweet_text += f"\n\n{short_url}"
            
            return tweet_text
        
        else:
            return generate_fallback_tweet(article_title, article_url, news_title, news_url, max_length)
    
    except Exception as e:
        print(f"⚠️ データ分析型ツイート生成エラー: {e}")
        import traceback
        traceback.print_exc()
        return generate_fallback_tweet(article_title, article_url, news_title, news_url, max_length)


def generate_lifestyle_tweet(article_title=None, article_content=None, article_url=None, max_length=280):
    """
    ライフスタイル型のツイートを生成（30%）
    
    コンセプト:
    - CBD情報を親しみやすく、分かりやすく伝える
    - 趣味（ポーカー、マラソン、お酒）は無理に組み合わせない
    - 実用的な情報を提供
    """
    try:
        if GEMINI_API_KEY and article_title:
            import google.generativeai as genai
            
            genai.configure(api_key=GEMINI_API_KEY)
            try:
                model = genai.GenerativeModel('gemini-2.5-flash')
            except:
                try:
                    model = genai.GenerativeModel('gemini-3-flash-preview')
                except:
                    try:
                        model = genai.GenerativeModel('gemini-2.0-flash')
                    except:
                        models = genai.list_models()
                        model = genai.GenerativeModel(models[0].name) if models else None
            
            if not model:
                return generate_fallback_tweet(article_title, article_url, None, None, max_length)
            
            url_length = 23 if article_url else 0
            available_length = max_length - url_length - 10
            
            # 記事の場合、記事要約を取得
            if article_url:
                try:
                    from social_media.article_summarizer import summarize_article_with_highlights
                    article_summary = summarize_article_with_highlights(article_url, article_title, max_length=300)
                    if article_summary:
                        source_text = f"タイトル: {article_title}\n\n記事要約:\n{article_summary}\n\n元の要約: {article_content[:500] if article_content else 'なし'}"
                    else:
                        source_text = f"タイトル: {article_title}\n\n{article_content[:1500] if article_content else '要約なし'}"
                except Exception as e:
                    print(f"    ⚠️ 記事要約取得エラー: {e}")
                    source_text = f"タイトル: {article_title}\n\n{article_content[:1500] if article_content else '要約なし'}"
            else:
                source_text = f"タイトル: {article_title}"
                if article_content:
                    source_text += f"\n\n{article_content[:1500]}"
            
            prompt = f"""あなたはCBD・大麻分野の専門ライターです。

以下の記事を読んで、ライフスタイル型のツイート文案を{available_length}文字以内で生成してください。

**重要な方針:**
1. **CBD情報を親しみやすく、分かりやすく伝える**
2. **趣味（ポーカー、マラソン、お酒）を無理に組み合わせない**
3. **実用的な情報を提供**
4. **入門者にも分かりやすい**
5. **信頼感を高めるため、絵文字は一切使用しない**

**ツイートの構成:**
- 【】でタイトルを明確に（最初の行、閉じ括弧】は同じ行に）
- **記事の要約を必ず含める（記事の内容を読みたくなるように魅力的に要約）**
- **要約は見やすい形で、記事の要点を簡潔に伝える**
- 親しみやすいトーン
- 実用的な情報（使い方、選び方など）
- 適度な改行で読みやすく（伝えたい内容の前後を改行）
- **絵文字は一切使用しない（信頼感を高めるため）**
- **ハッシュタグは一切使用しない**

**要約の要件:**
- 記事の要点を簡潔に伝える（2-3文程度）
- 読者が「この記事を読みたい」と思うような魅力的な要約
- 具体的な情報やポイントを含める
- 記事の価値を明確に伝える

**個人的な視点・感想の追加:**
- **ツイートの最初または最後に、自然な個人的な感想や視点を追加する**
- **「〜ですね」「〜かもしれません」「〜に注目です」などの自然な表現を使用**
- **読者と共感できるような、人間らしい視点を入れる**
- **機械的な文章ではなく、自然な人間としてのツイートにする**
- **ファン化できるような親近感を出す**

**改行のルール:**
- 【タイトル】は1行目に（閉じ括弧】も同じ行）
- タイトルの後に改行
- 要約の前後を改行して読みやすく
- 伝えたい内容の前後を改行して読みやすく
- 箇条書きの前後は改行
- 段落ごとに改行

**トーン:**
- 親しみやすく、敷居が低い
- 実用的
- 分かりやすい
- 信頼感がある
- **人間らしく、共感しやすい**
- **親近感があり、ファン化できる**

記事:
{source_text}

ツイート文案を生成してください（{available_length}文字以内）:
"""
            
            response = model.generate_content(prompt)
            tweet_body = response.text.strip()
            tweet_body = re.sub(r'<[^>]+>', '', tweet_body)
            
            if len(tweet_body) > available_length:
                last_period = tweet_body[:available_length].rfind('。')
                if last_period > available_length * 0.7:
                    tweet_body = tweet_body[:last_period+1]
                else:
                    tweet_body = tweet_body[:available_length-3] + "..."
            
            tweet_text = format_tweet(tweet_body, style='elegant')
            
            if article_url:
                short_url = shorten_url(article_url)
                if short_url not in tweet_text:
                    tweet_text += f"\n\n{short_url}"
            
            return tweet_text
        
        else:
            return generate_fallback_tweet(article_title, article_url, None, None, max_length)
    
    except Exception as e:
        print(f"⚠️ ライフスタイル型ツイート生成エラー: {e}")
        return generate_fallback_tweet(article_title, article_url, None, None, max_length)


def generate_other_tweet(news_title=None, news_content=None, news_url=None, max_length=280):
    """
    その他型のツイートを生成（10%）
    
    コンセプト:
    - ニュース、情報提供など
    - 幅広く正確なCBDや大麻情報を発信
    """
    try:
        if GEMINI_API_KEY and news_title:
            import google.generativeai as genai
            
            genai.configure(api_key=GEMINI_API_KEY)
            try:
                model = genai.GenerativeModel('gemini-2.5-flash')
            except:
                try:
                    model = genai.GenerativeModel('gemini-3-flash-preview')
                except:
                    try:
                        model = genai.GenerativeModel('gemini-2.0-flash')
                    except:
                        models = genai.list_models()
                        model = genai.GenerativeModel(models[0].name) if models else None
            
            if not model:
                return generate_fallback_tweet(None, None, news_title, news_url, max_length)
            
            url_length = 23 if news_url else 0
            available_length = max_length - url_length - 10
            
            source_text = f"タイトル: {news_title}"
            if news_content:
                source_text += f"\n\n{news_content[:1500]}"
            
            prompt = f"""あなたはCBD・大麻分野の専門ライターです。

以下のニュースを読んで、ツイート文案を{available_length}文字以内で生成してください。

**重要な方針:**
1. **幅広く正確なCBDや大麻情報を発信する**
2. **正確な情報を提供**
3. **簡潔にまとめる**
4. **CBDを今後使いたい人（初心者や興味がある人）にも理解できる、興味を持てる表現にする**
5. **専門用語を避け、分かりやすい言葉で説明する**
6. **ユーモアや親しみやすさを加える（ただし信頼感を損なわない程度に）**
7. **定量的な話をする時は必ずエビデンス（研究、論文、データ）を明記する**
8. **結局何が言いたいかを明確にする**
9. **海外と日本のギャップを意識して書く（海外の成熟度と日本の現状のギャップ）**
10. **「データコンサルタントとして分析」「データ分析では」などの「自分が分析した」という表現は使用しない（ニュースの内容を伝えるのみ）**

**ツイートの構成:**
- 【】でタイトルを明確に（最初の行、閉じ括弧】は同じ行に）
- **タイトルは英語の場合、自然な日本語に翻訳する**
- **ニュースの要約を必ず含める（記事の内容を読みたくなるように魅力的に要約）**
- **要約は見やすい形で、以下の要素を含める:**
  * 日本と海外のギャップ（海外の成熟度と日本の現状のギャップ）を分かりやすく説明
  * 常識が変わるような意外性を、誰でも理解できる表現で
  * 実は〇〇の効果があったような研究や論文を、分かりやすく説明
  * 定量的なCBDの体への効果を、具体的で分かりやすい数字で
  * 政治（法律の改正など）への影響を、一般の人にも理解できる表現で
  * 経済への影響を、具体的で分かりやすい表現で
- **エビデンスとなる数字やデータを明確に記載（ただし分かりやすく）**
- **結局何が言いたいかを明確にする**
- 適度な改行で読みやすく（伝えたい内容の前後を改行）
- **絵文字は一切使用しない（信頼感を高めるため）**
- **ハッシュタグは一切使用しない**

**要約の要件:**
- ニュースの要点を簡潔に伝える（2-4文程度）
- **CBD初心者や興味がある人でも理解できる、分かりやすい表現**
- **専門用語は避け、誰でも理解できる言葉で説明**
- 読者が「このニュースを読みたい」と思うような魅力的な要約
- 上記の要素（ギャップ、意外性、研究、定量的効果、政治・経済影響）を含める
- 具体的な数字やデータを含める（ただし分かりやすく）
- ニュースの価値を明確に伝える

**個人的な視点・感想の追加:**
- **ツイートの最初または最後に、自然な個人的な感想や視点を追加する**
- **「〜ですね」「〜かもしれません」「〜に注目です」「〜な可能性を秘めていますね」などの自然な表現を使用**
- **読者と共感できるような、人間らしい視点を入れる**
- **機械的な文章ではなく、自然な人間としてのツイートにする**
- **ファン化できるような親近感を出す**
- **ニュースの内容に対する個人的な見解や感想を、自然に織り交ぜる**

**表現の注意点:**
- 「データコンサルタントとして分析」「データ分析では判明」などの「自分が分析した」という表現は使用しない
- ニュースの内容を客観的に伝える（「〜と報じられています」「〜とのことです」などの表現を使用）
- 専門用語は避け、分かりやすい言葉で説明
- ユーモアや親しみやすさを加える（ただし信頼感を損なわない程度に）
- CBD初心者にも理解できる表現を心がける

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

ニュース:
{source_text}

ツイート文案を生成してください（{available_length}文字以内）:
"""
            
            response = model.generate_content(prompt)
            tweet_body = response.text.strip()
            tweet_body = re.sub(r'<[^>]+>', '', tweet_body)
            
            if len(tweet_body) > available_length:
                last_period = tweet_body[:available_length].rfind('。')
                if last_period > available_length * 0.7:
                    tweet_body = tweet_body[:last_period+1]
                else:
                    tweet_body = tweet_body[:available_length-3] + "..."
            
            tweet_text = format_tweet(tweet_body, style='elegant')
            
            if news_url:
                short_url = shorten_url(news_url)
                if short_url not in tweet_text:
                    tweet_text += f"\n\n{short_url}"
            
            return tweet_text
        
        else:
            return generate_fallback_tweet(None, None, news_title, news_url, max_length)
    
    except Exception as e:
        print(f"⚠️ その他型ツイート生成エラー: {e}")
        return generate_fallback_tweet(None, None, news_title, news_url, max_length)


def generate_fallback_tweet(article_title=None, article_url=None, news_title=None, news_url=None, max_length=280):
    """
    フォールバック: シンプルなツイート文案を生成
    """
    title = article_title or news_title
    url = article_url or news_url
    
    if title:
        tweet_text = f"【{title}】\n\n"
        if url:
            short_url = shorten_url(url)
            tweet_text += f"{short_url}"
        else:
            tweet_text = tweet_text.strip()
    else:
        tweet_text = "CBDに関する最新情報をお届けします"
    
    if len(tweet_text) > max_length:
        tweet_text = tweet_text[:max_length-3] + "..."
    
    return tweet_text


def select_content_type():
    """
    投稿比率に基づいてコンテンツタイプを選択
    
    Returns:
        'data_analysis' (60%), 'lifestyle' (30%), 'other' (10%)
    """
    rand = random.random()
    if rand < 0.6:
        return 'data_analysis'
    elif rand < 0.9:
        return 'lifestyle'
    else:
        return 'other'


def get_persona_and_engagement(content_type):
    """
    コンテンツタイプに応じたペルソナと引き付け期待を返す
    
    Args:
        content_type: 'data_analysis', 'lifestyle', 'other'
    
    Returns:
        (ペルソナ, 引き付け期待) のタプル
    """
    if content_type == 'data_analysis':
        return (
            "データやエビデンスを重視する層、信頼性を求める層",
            "データ分析の専門性と信頼性で安心感を与え、サイトで詳細情報を確認したいと感じてもらう"
        )
    elif content_type == 'lifestyle':
        return (
            "CBD初心者、親しみやすい情報を求める層",
            "親しみやすさと実用性で興味を持ち、サイトで使い方や選び方を確認したいと感じてもらう"
        )
    else:
        return (
            "幅広い層、最新情報を求める層",
            "最新情報の価値で興味を持ち、サイトで詳しい情報を確認したいと感じてもらう"
        )
