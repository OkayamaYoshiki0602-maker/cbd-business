#!/usr/bin/env python3
"""
ツイートフォーマッター（改善版）
改行、タイトル、濁点を活用して魅力的なツイートに整形
"""

import re


def format_tweet(tweet_text, style='elegant'):
    """
    ツイートを魅力的にフォーマット
    
    Args:
        tweet_text: 元のツイートテキスト
        style: スタイル（'elegant', 'bold', 'minimal'）
    
    Returns:
        フォーマットされたツイートテキスト
    """
    formatted = tweet_text
    
    # URLを保持（後で追加するため）
    url_match = re.search(r'(https?://[^\s]+)', formatted)
    url = url_match.group(1) if url_match else None
    
    # URLを一時的に削除（フォーマット処理のため）
    if url:
        formatted = formatted.replace(url, '').strip()
    
    # ハッシュタグを削除
    formatted = remove_hashtags(formatted)
    
    # 絵文字を削除（信頼感を高めるため）
    formatted = remove_emojis(formatted)
    
    # 【】タイトルの改行を修正（閉じ括弧】が別行になっている場合を修正）
    formatted = fix_title_line_breaks(formatted)
    
    # 改行を整理
    formatted = add_intelligent_breaks(formatted)
    
    # タイトルを追加（適切な場合）
    formatted = add_title_if_needed(formatted, style)
    
    # 濁点を活用した強調（控えめに）
    # formatted = enhance_with_dakuten(formatted)  # 自然さを優先してコメントアウト
    
    # 余分な空白を整理
    formatted = clean_whitespace(formatted)
    
    # URLを再度追加
    if url:
        formatted += f"\n\n{url}"
    
    # 280文字以内に収める
    formatted = ensure_length(formatted, max_length=280)
    
    return formatted.strip()


def remove_hashtags(text):
    """ハッシュタグを削除"""
    # ハッシュタグを削除（#を含む）
    text = re.sub(r'#\w+\s*', '', text)
    text = re.sub(r'\s*#\w+$', '', text)
    text = re.sub(r'\s*#\w+\s*', ' ', text)
    return text.strip()


def remove_emojis(text):
    """絵文字を削除（信頼感を高めるため）"""
    # 絵文字のUnicode範囲を削除
    text = re.sub(r'[\U0001F300-\U0001F9FF]', '', text)  # 一般的な絵文字
    text = re.sub(r'[\U0001FA00-\U0001FAFF]', '', text)  # 拡張絵文字
    text = re.sub(r'[\U00002600-\U000026FF]', '', text)  # 記号・絵文字
    text = re.sub(r'[\U00002700-\U000027BF]', '', text)  # 装飾記号
    text = re.sub(r'[\U0001F600-\U0001F64F]', '', text)  # 顔文字
    text = re.sub(r'[\U0001F680-\U0001F6FF]', '', text)  # 交通・地図記号
    text = re.sub(r'[\U0001F1E0-\U0001F1FF]', '', text)  # 国旗
    text = re.sub(r'[\U0001F900-\U0001F9FF]', '', text)  # 補助絵文字
    # 絵文字の結合文字（ゼロ幅結合子）を削除
    text = re.sub(r'[\u200D\uFE0F]', '', text)  # ゼロ幅結合子、異体字セレクタ
    # 余分な空白を整理
    text = re.sub(r'\s+', ' ', text)
    return text.strip()


def fix_title_line_breaks(text):
    """【】タイトルの改行を修正（閉じ括弧】が別行になっている場合を修正）"""
    lines = text.split('\n')
    formatted_lines = []
    i = 0
    while i < len(lines):
        line = lines[i].strip()
        if line.startswith('【') and not line.endswith('】'):
            # 【で始まっているが】で終わっていない場合、次の行を確認
            if i + 1 < len(lines) and lines[i + 1].strip() == '】':
                # 次の行が】だけの場合、結合
                formatted_lines.append(line + '】')
                i += 2
                continue
            elif i + 1 < len(lines) and '】' in lines[i + 1]:
                # 次の行に】が含まれている場合、結合
                next_line = lines[i + 1].strip()
                formatted_lines.append(line + ' ' + next_line)
                i += 2
                continue
        formatted_lines.append(line)
        i += 1
    return '\n'.join(formatted_lines)


def add_intelligent_breaks(text):
    """知的な改行を追加"""
    # URLの前後で改行
    text = re.sub(r'\s+(https?://[^\s]+)', r'\n\n\1', text)
    
    # 句点の後に改行を追加（ただし短い文の連続は避ける）
    sentences = re.split(r'([。！？])', text)
    formatted = ''
    for i in range(0, len(sentences) - 1, 2):
        sentence = sentences[i] + (sentences[i+1] if i+1 < len(sentences) else '')
        sentence = sentence.strip()
        if sentence:
            # 長い文（40文字以上）の場合は改行
            if len(sentence) > 40:
                formatted += sentence + '\n\n'
            else:
                # 短い文は続ける（ただし3文連続したら改行）
                if formatted and formatted[-2:] == '。\n\n':
                    formatted += sentence
                elif i > 0 and len(sentences[i-2] if i-2 >= 0 else '') < 30:
                    formatted += sentence
                else:
                    formatted += sentence + '\n'
    
    # 連続した改行を2つに制限
    formatted = re.sub(r'\n{3,}', '\n\n', formatted)
    
    # 最後の余分な改行を削除
    formatted = formatted.rstrip('\n')
    
    return formatted


def add_title_if_needed(text, style='elegant'):
    """タイトルを追加（必要に応じて）"""
    # すでにタイトルがある場合は追加しない
    if re.match(r'^【|^「|^【|^■|^▶|^●|^◆|^▼', text):
        return text
    
    # 最初の文を抽出
    first_match = re.match(r'^(.{1,30}[。！？\n]|.{1,30})', text)
    if not first_match:
        return text
    
    first_part = first_match.group(1).strip()
    
    # スタイルに応じてタイトルを追加
    if style == 'elegant':
        # 【】を使用
        title_marker = '【'
        title_marker_end = '】'
    elif style == 'bold':
        # ■を使用
        title_marker = '■'
        title_marker_end = ''
    else:
        # 最小限
        return text
    
    # タイトルが長すぎる場合は短縮
    if len(first_part) > 25:
        first_part = first_part[:22] + '...'
    
    # タイトルを追加
    if title_marker_end:
        title = f"{title_marker}{first_part}{title_marker_end}"
    else:
        title = f"{title_marker} {first_part}"
    
    remaining = text[len(first_match.group(0)):].strip()
    
    if remaining:
        return f"{title}\n\n{remaining}"
    else:
        return title


def enhance_with_dakuten(text):
    """濁点を活用した強調（控えめに）"""
    # 重要そうな単語を特定（数字を含む、固有名詞など）
    # ただし、自然さを優先するため、大幅な変更は避ける
    return text


def clean_whitespace(text):
    """余分な空白を整理"""
    # 連続したスペースを1つに
    text = re.sub(r' {2,}', ' ', text)
    # 行頭・行末のスペースを削除
    lines = [line.strip() for line in text.split('\n')]
    text = '\n'.join([line for line in lines if line])
    # 連続した改行を2つに制限
    text = re.sub(r'\n{3,}', '\n\n', text)
    return text.strip()


def ensure_length(text, max_length=280):
    """280文字以内に収める"""
    if len(text) <= max_length:
        return text
    
    # URLがあれば保持
    url_match = re.search(r'(https?://[^\s]+)', text)
    url = url_match.group(1) if url_match else None
    
    if url:
        # URLを除いた長さ
        text_without_url = text.replace(url, '')
        max_main_length = max_length - len(url) - 2  # URLと改行の余裕
        
        if len(text_without_url) > max_main_length:
            # 最後の句点まで
            last_period = text_without_url[:max_main_length].rfind('。')
            if last_period > max_main_length * 0.7:
                text_without_url = text_without_url[:last_period+1]
            else:
                text_without_url = text_without_url[:max_main_length-3] + '...'
            
            text = f"{text_without_url}\n\n{url}"
    else:
        # URLがない場合は単純に短縮
        last_period = text[:max_length].rfind('。')
        if last_period > max_length * 0.7:
            text = text[:last_period+1]
        else:
            text = text[:max_length-3] + '...'
    
    return text


def main():
    """メイン関数（テスト用）"""
    test_tweets = [
        "CBDの効果が明らかに！2024年のデータで判明した驚きの事実とは？詳しくはこちら https://example.com #CBD",
        "大麻ビジネスが1.65億ドルを記録。これは何を意味するのか？詳しく解説します。",
    ]
    
    for tweet in test_tweets:
        print("=" * 60)
        print("元のツイート:")
        print(tweet)
        print("\nフォーマット後:")
        formatted = format_tweet(tweet)
        print(formatted)
        print(f"\n文字数: {len(formatted)}/280")
        print("=" * 60)
        print()


if __name__ == '__main__':
    main()
