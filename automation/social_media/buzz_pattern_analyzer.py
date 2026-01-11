#!/usr/bin/env python3
"""
バズツイートパターン分析スクリプト（改善版）
他ジャンルの専門アカウントからバズツイートの本質を抽出
"""

import os
import sys
import re
from pathlib import Path
from dotenv import load_dotenv

# 親ディレクトリをパスに追加
sys.path.insert(0, str(Path(__file__).parent.parent))

# .envファイルを読み込む
load_dotenv()

GEMINI_API_KEY = os.getenv('GEMINI_API_KEY', '')


def analyze_buzz_pattern(tweet_text, engagement_metrics=None):
    """
    ツイートテキストからバズパターンを分析
    
    Args:
        tweet_text: ツイートテキスト
        engagement_metrics: エンゲージメント指標（いいね数、リツイート数など）
    
    Returns:
        バズパターンの辞書
    """
    patterns = {
        'has_emoji': bool(re.search(r'[😀-🙏🌀-🗿]', tweet_text)),
        'has_number': bool(re.search(r'\d+', tweet_text)),
        'has_date': bool(re.search(r'\d{1,2}月|\d{1,2}日|202\d', tweet_text)),
        'has_question': '？' in tweet_text or '?' in tweet_text,
        'has_exclamation': '！' in tweet_text or '!' in tweet_text,
        'line_breaks': tweet_text.count('\n'),
        'has_title': bool(re.search(r'^【|^「|^【|^■|^▶|^●', tweet_text)),
        'has_bullet': '・' in tweet_text or '•' in tweet_text or '→' in tweet_text,
        'has_ellipsis': '…' in tweet_text or '...' in tweet_text,
        'has_dakuten': bool(re.search(r'[が-ぽ]|[ガ-ポ]', tweet_text)),
        'length': len(tweet_text),
        'sentence_count': len(re.split(r'[。！？]', tweet_text)),
    }
    
    # ハッシュタグの有無
    patterns['has_hashtag'] = bool(re.search(r'#\w+', tweet_text))
    
    # 改行パターン（段落の有無）
    lines = tweet_text.split('\n')
    patterns['paragraph_count'] = len([l for l in lines if l.strip()])
    patterns['has_paragraph_break'] = patterns['paragraph_count'] > 2
    
    # 濁点・半濁点の活用度（強調の指標）
    dakuten_chars = len(re.findall(r'[が-ぽ]|[ガ-ポ]', tweet_text))
    patterns['dakuten_density'] = dakuten_chars / max(len(tweet_text), 1)
    
    return patterns


def extract_buzz_essence(tweets_data, use_ai=True):
    """
    複数のバズツイートから本質を抽出（AI活用）
    
    Args:
        tweets_data: ツイートデータのリスト（テキスト、エンゲージメント指標など）
        use_ai: AIを使用するか
    
    Returns:
        バズツイートの本質（構成パターン、要素など）
    """
    if not tweets_data:
        return None
    
    # パターン分析
    all_patterns = []
    for tweet_data in tweets_data[:10]:  # 最大10件
        tweet_text = tweet_data.get('text', '')
        if not tweet_text:
            continue
        
        patterns = analyze_buzz_pattern(tweet_text, tweet_data.get('metrics'))
        patterns['text'] = tweet_text[:100]  # サンプルとして保存
        all_patterns.append(patterns)
    
    if not all_patterns:
        return None
    
    # AIで本質を抽出
    if use_ai and GEMINI_API_KEY:
        try:
            import google.generativeai as genai
            
            genai.configure(api_key=GEMINI_API_KEY)
            try:
                model = genai.GenerativeModel('gemini-2.5-flash')
            except:
                try:
                    model = genai.GenerativeModel('gemini-3-flash-preview')
                except:
                    model = genai.GenerativeModel('gemini-2.0-flash')
            
            # ツイートサンプルをまとめる
            tweet_samples = '\n\n'.join([p['text'] for p in all_patterns[:5]])
            
            prompt = f"""あなたはSNSマーケティングの専門家です。

以下のバズツイートを分析して、バズる本質（構成パターン、要素、表現方法）を抽出してください。

分析項目:
1. **構成パターン**: ツイートの構造（導入→本題→結論など）
2. **視覚的魅力**: 改行、記号、絵文字の使い方
3. **情報の提示方法**: 数字、日付、具体的な情報の使い方
4. **読者の感情に訴える要素**: 疑問、驚き、共感を呼ぶ表現
5. **濁点・強調の活用**: 重要な部分の強調方法

ツイートサンプル:
{tweet_samples}

バズる本質を簡潔にまとめてください（300文字以内）:
"""
            
            response = model.generate_content(prompt)
            essence = response.text.strip()
            
            return {
                'essence': essence,
                'patterns': all_patterns[0],  # 代表的なパターン
                'common_patterns': _extract_common_patterns(all_patterns)
            }
        
        except Exception as e:
            print(f"⚠️ AI分析エラー: {e}")
            return _extract_manual_essence(all_patterns)
    
    else:
        return _extract_manual_essence(all_patterns)


def _extract_common_patterns(patterns_list):
    """共通パターンを抽出"""
    if not patterns_list:
        return {}
    
    common = {
        'avg_line_breaks': sum(p['line_breaks'] for p in patterns_list) / len(patterns_list),
        'has_title_rate': sum(1 for p in patterns_list if p['has_title']) / len(patterns_list),
        'has_emoji_rate': sum(1 for p in patterns_list if p['has_emoji']) / len(patterns_list),
        'has_number_rate': sum(1 for p in patterns_list if p['has_number']) / len(patterns_list),
        'avg_length': sum(p['length'] for p in patterns_list) / len(patterns_list),
        'has_hashtag_rate': sum(1 for p in patterns_list if p['has_hashtag']) / len(patterns_list),
    }
    
    return common


def _extract_manual_essence(patterns_list):
    """手動で本質を抽出（AIが使えない場合）"""
    common = _extract_common_patterns(patterns_list)
    
    essence_parts = []
    
    if common['has_title_rate'] > 0.5:
        essence_parts.append("タイトル（【】「」■など）を使用")
    
    if common['avg_line_breaks'] > 2:
        essence_parts.append("改行を活用した段落構成")
    
    if common['has_number_rate'] > 0.7:
        essence_parts.append("具体的な数字を含む")
    
    if common['has_emoji_rate'] > 0.5:
        essence_parts.append("絵文字を効果的に使用")
    
    if common['has_hashtag_rate'] < 0.3:
        essence_parts.append("ハッシュタグは控えめまたは不使用")
    
    essence = "。".join(essence_parts) if essence_parts else "パターンが見つかりませんでした"
    
    return {
        'essence': essence,
        'patterns': patterns_list[0] if patterns_list else {},
        'common_patterns': common
    }


def apply_buzz_pattern(tweet_text, buzz_essence=None):
    """
    バズパターンを適用してツイートを改善
    
    Args:
        tweet_text: 元のツイートテキスト
        buzz_essence: バズツイートの本質
    
    Returns:
        改善されたツイートテキスト
    """
    if not buzz_essence:
        # デフォルトの改善を適用
        return _improve_tweet_default(tweet_text)
    
    # パターンに基づいて改善
    improved = tweet_text
    
    # ハッシュタグを削除
    improved = re.sub(r'#\w+\s*', '', improved)
    improved = re.sub(r'\s*#\w+$', '', improved)
    
    # 改行を適切に追加
    if buzz_essence.get('common_patterns', {}).get('avg_line_breaks', 0) > 2:
        # 段落を意識した改行
        improved = _add_paragraph_breaks(improved)
    
    # タイトルを追加（必要に応じて）
    if buzz_essence.get('common_patterns', {}).get('has_title_rate', 0) > 0.5:
        improved = _add_title(improved)
    
    # 濁点を活用した強調
    improved = _enhance_with_dakuten(improved)
    
    return improved.strip()


def _improve_tweet_default(tweet_text):
    """デフォルトの改善を適用"""
    improved = tweet_text
    
    # ハッシュタグを削除
    improved = re.sub(r'#\w+\s*', '', improved)
    improved = re.sub(r'\s*#\w+$', '', improved)
    
    # 改行を適切に追加（句点の後）
    improved = re.sub(r'([。！？])\s*([^。！？\n])', r'\1\n\n\2', improved)
    
    # 不要な空白を整理
    improved = re.sub(r'\n{3,}', '\n\n', improved)
    improved = improved.strip()
    
    return improved


def _add_paragraph_breaks(text):
    """段落の改行を追加"""
    # 句点の後に改行を追加（ただし連続しないように）
    text = re.sub(r'([。！？])([^\n])', r'\1\n\n\2', text)
    # 連続した改行を2つに制限
    text = re.sub(r'\n{3,}', '\n\n', text)
    return text.strip()


def _add_title(text):
    """タイトルを追加（先頭に）"""
    # すでにタイトルがある場合は追加しない
    if re.match(r'^【|^「|^【|^■|^▶', text):
        return text
    
    # 最初の文をタイトルとして抽出
    first_sentence = re.split(r'[。！？\n]', text)[0]
    if len(first_sentence) > 30:
        # タイトルが長すぎる場合は短縮
        first_sentence = first_sentence[:27] + '...'
    
    # タイトルを追加
    title = f"【{first_sentence}】"
    remaining = text[len(first_sentence):].strip()
    
    if remaining:
        return f"{title}\n\n{remaining}"
    else:
        return title


def _enhance_with_dakuten(text):
    """濁点を活用した強調（重要な部分を濁点で強調）"""
    # 重要そうな単語を濁点で強調（例：「とても」→「どても」などは自然ではないので、控えめに）
    # 実際には、AI生成時に自然な強調を行う
    return text


def main():
    """メイン関数（テスト用）"""
    # テストデータ
    test_tweets = [
        {'text': '【最新研究】CBDの効果が明らかに！2024年のデータで判明した驚きの事実とは？', 'metrics': {'likes': 1000}},
        {'text': '大麻ビジネスが1.65億ドルを記録。これは何を意味するのか？', 'metrics': {'likes': 800}},
    ]
    
    essence = extract_buzz_essence(test_tweets)
    
    if essence:
        print("📊 バズツイートの本質:")
        print("=" * 60)
        print(essence.get('essence', '分析できませんでした'))
        print("=" * 60)
        
        print("\n📈 共通パターン:")
        common = essence.get('common_patterns', {})
        for key, value in common.items():
            print(f"  {key}: {value}")


if __name__ == '__main__':
    main()
