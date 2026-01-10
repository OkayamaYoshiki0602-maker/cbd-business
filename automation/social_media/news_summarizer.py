#!/usr/bin/env python3
"""
ニュース要約スクリプト（AI要約対応）
OpenAI GPT API、Claude API、Gemini APIに対応
"""

import os
import sys
from pathlib import Path
from dotenv import load_dotenv

# 親ディレクトリをパスに追加
sys.path.insert(0, str(Path(__file__).parent.parent))

# .envファイルを読み込む
load_dotenv()

# API設定
OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')
ANTHROPIC_API_KEY = os.getenv('ANTHROPIC_API_KEY')
GEMINI_API_KEY = os.getenv('GEMINI_API_KEY')

# 使用するAI要約サービス（優先順位）
AI_SUMMARIZER = os.getenv('AI_SUMMARIZER', 'gemini')  # openai, claude, gemini, local（デフォルト: gemini）


def summarize_with_openai(text, max_length=200):
    """
    OpenAI GPT APIで要約
    
    Args:
        text: 要約対象のテキスト
        max_length: 最大文字数
    
    Returns:
        要約テキスト
    """
    try:
        from openai import OpenAI
        
        if not OPENAI_API_KEY:
            raise ValueError("OPENAI_API_KEYが設定されていません")
        
        client = OpenAI(api_key=OPENAI_API_KEY)
        
        response = client.chat.completions.create(
            model="gpt-4o-mini",  # コスト効率重視
            messages=[
                {
                    "role": "system",
                    "content": "あなたはCBD・大麻分野の専門ライターです。ニュースを簡潔で正確に要約してください。事実ベースの情報を優先し、専門用語は簡潔に説明してください。"
                },
                {
                    "role": "user",
                    "content": f"以下のニュースを{max_length}文字以内で要約してください：\n\n{text}"
                }
            ],
            max_tokens=int(max_length * 2),  # 日本語は文字数×2程度のトークン数
            temperature=0.3  # 低めに設定して正確性を重視
        )
        
        summary = response.choices[0].message.content.strip()
        return summary
    
    except ImportError:
        print("⚠️ openaiライブラリがインストールされていません: pip install openai")
        return None
    except Exception as e:
        print(f"⚠️ OpenAI要約エラー: {e}")
        return None


def summarize_with_claude(text, max_length=200):
    """
    Claude APIで要約
    
    Args:
        text: 要約対象のテキスト
        max_length: 最大文字数
    
    Returns:
        要約テキスト
    """
    try:
        import anthropic
        
        if not ANTHROPIC_API_KEY:
            raise ValueError("ANTHROPIC_API_KEYが設定されていません")
        
        client = anthropic.Anthropic(api_key=ANTHROPIC_API_KEY)
        
        message = client.messages.create(
            model="claude-3-haiku-20240307",  # コスト効率重視
            max_tokens=int(max_length * 2),
            temperature=0.3,
            system="あなたはCBD・大麻分野の専門ライターです。ニュースを簡潔で正確に要約してください。事実ベースの情報を優先し、専門用語は簡潔に説明してください。",
            messages=[
                {
                    "role": "user",
                    "content": f"以下のニュースを{max_length}文字以内で要約してください：\n\n{text}"
                }
            ]
        )
        
        summary = message.content[0].text.strip()
        return summary
    
    except ImportError:
        print("⚠️ anthropicライブラリがインストールされていません: pip install anthropic")
        return None
    except Exception as e:
        print(f"⚠️ Claude要約エラー: {e}")
        return None


def summarize_with_gemini(text, max_length=200):
    """
    Google Gemini APIで要約
    
    Args:
        text: 要約対象のテキスト
        max_length: 最大文字数
    
    Returns:
        要約テキスト
    """
    try:
        import google.generativeai as genai
        
        if not GEMINI_API_KEY:
            raise ValueError("GEMINI_API_KEYが設定されていません")
        
        genai.configure(api_key=GEMINI_API_KEY)
        model = genai.GenerativeModel('gemini-pro')
        
        prompt = f"""あなたはCBD・大麻分野の専門ライターです。以下のニュースを{max_length}文字以内で簡潔で正確に要約してください。

事実ベースの情報を優先し、専門用語は簡潔に説明してください。

ニュース:
{text}
"""
        
        response = model.generate_content(prompt)
        summary = response.text.strip()
        
        # 文字数制限
        if len(summary) > max_length:
            summary = summary[:max_length-3] + "..."
        
        return summary
    
    except ImportError:
        print("⚠️ google-generativeaiライブラリがインストールされていません: pip install google-generativeai")
        return None
    except Exception as e:
        print(f"⚠️ Gemini要約エラー: {e}")
        return None


def summarize_local(text, max_length=200):
    """
    ローカル要約（簡易版・無料）
    
    Args:
        text: 要約対象のテキスト
        max_length: 最大文字数
    
    Returns:
        要約テキスト
    """
    # 段落に分割
    paragraphs = [p.strip() for p in text.split('\n\n') if p.strip()]
    
    if not paragraphs:
        return text[:max_length-3] + "..." if len(text) > max_length else text
    
    # 最初の段落を要約として使用
    summary = paragraphs[0]
    
    # 長さを調整
    if len(summary) > max_length:
        # 文章の途中で切らないように、最後の句点まで
        last_period = summary[:max_length].rfind('。')
        if last_period > max_length * 0.7:  # 70%以上が有効な場合
            summary = summary[:last_period+1]
        else:
            summary = summary[:max_length-3] + "..."
    
    return summary


def summarize_news(text, max_length=200, use_ai=None):
    """
    ニュースを要約
    
    Args:
        text: 要約対象のテキスト
        max_length: 最大文字数
        use_ai: 使用するAI要約サービス（Noneの場合は環境変数から取得）
    
    Returns:
        要約テキスト
    """
    if use_ai is None:
        use_ai = AI_SUMMARIZER
    
    # AI要約を試行（優先順位順：gemini優先）
    if use_ai == 'gemini' or use_ai == 'auto':
        summary = summarize_with_gemini(text, max_length)
        if summary:
            return summary
    
    if use_ai == 'openai' or (use_ai == 'auto' and not summary):
        summary = summarize_with_openai(text, max_length)
        if summary:
            return summary
    
    if use_ai == 'claude' or (use_ai == 'auto' and not summary):
        summary = summarize_with_claude(text, max_length)
        if summary:
            return summary
    
    # AI要約が失敗した場合、ローカル要約を使用
    print("⚠️ AI要約が利用できないため、ローカル要約を使用します")
    return summarize_local(text, max_length)


def main():
    """メイン関数（テスト用）"""
    if len(sys.argv) < 2:
        print("使用方法:")
        print("  python news_summarizer.py summarize <text> [max_length] [ai_service]")
        print("\n例:")
        print("  python news_summarizer.py summarize 'ニュース本文...' 200 openai")
        print("\nAI要約サービス: openai, claude, gemini, local")
        sys.exit(1)
    
    command = sys.argv[1]
    
    if command == 'summarize':
        if len(sys.argv) < 3:
            print("エラー: 要約対象のテキストが必要です")
            sys.exit(1)
        
        text = sys.argv[2]
        max_length = int(sys.argv[3]) if len(sys.argv) > 3 else 200
        ai_service = sys.argv[4] if len(sys.argv) > 4 else 'auto'
        
        print(f"📝 ニュースを要約しています... (最大{max_length}文字, AI: {ai_service})")
        summary = summarize_news(text, max_length, ai_service)
        
        print("\n" + "=" * 60)
        print("要約結果:")
        print("=" * 60)
        print(summary)
        print("=" * 60)
        print(f"\n文字数: {len(summary)}/{max_length}")
    
    else:
        print(f"不明なコマンド: {command}")
        sys.exit(1)


if __name__ == '__main__':
    main()
