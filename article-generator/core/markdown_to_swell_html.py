#!/usr/bin/env python3
"""
Markdown → SWELL HTML変換モジュール
SWELL記事作成ルールに基づいて、MarkdownをWordPress SWELL用のHTMLに変換
"""

import re
from html import unescape


def add_affiliate_disclaimer():
    """
    アフィリエイト免責事項を生成
    
    Returns:
        HTML形式の免責事項
    """
    return '''<div class="wp-block-group cbd-aff-disclaimer">
<div class="wp-block-group__inner-container">
<p style="font-size:13px;opacity:.8">※当サイトはアフィリエイト広告を利用しています。価格・在庫・成分はリンク先の最新情報が正となります。</p>
</div>
</div>

'''


def convert_h2_to_swell(markdown_text):
    """
    MarkdownのH1/H2をSWELL形式のH2に変換
    
    Args:
        markdown_text: Markdown形式のテキスト
    
    Returns:
        変換後のテキスト
    """
    html = markdown_text
    
    # H1をH2に変換（SWELL形式、is-style-default付き）
    html = re.sub(r'^#\s+(.+)$', r'<h2 class="wp-block-heading is-style-default">\1</h2>', html, flags=re.MULTILINE)
    
    # メタディスクリプションのH2は変換しない（後で削除）
    html = re.sub(r'^##\s*メタディスクリプション\s*\n', '## メタディスクリプション\n', html, flags=re.MULTILINE)
    
    # その他のH2は変換（SWELL形式、is-style-default付き）
    html = re.sub(r'^##\s+(.+)$', r'<h2 class="wp-block-heading is-style-default">\1</h2>', html, flags=re.MULTILINE)
    
    return html


def convert_h3_to_swell(markdown_text):
    """
    MarkdownのH3をSWELL形式のH3に変換
    
    Args:
        markdown_text: Markdown形式のテキスト
    
    Returns:
        変換後のテキスト
    """
    html = markdown_text
    
    # H3をSWELL形式に変換
    html = re.sub(r'^###\s+(.+)$', r'<h3 class="wp-block-heading">\1</h3>', html, flags=re.MULTILINE)
    
    return html


def convert_h4_to_swell(markdown_text):
    """
    MarkdownのH4をSWELL形式のH4に変換
    
    Args:
        markdown_text: Markdown形式のテキスト
    
    Returns:
        変換後のテキスト
    """
    html = markdown_text
    
    # H4をSWELL形式に変換
    html = re.sub(r'^####\s+(.+)$', r'<h4 class="wp-block-heading">\1</h4>', html, flags=re.MULTILINE)
    
    return html


def detect_list_style(prev_line, current_line=None):
    """
    リスト行のスタイルを判定
    
    Args:
        prev_line: リストの前の行（コンテキスト）
        current_line: 現在のリスト行（オプション）
    
    Returns:
        スタイル名（'good_list', 'bad_list', 'check_list', 'num_circle', 'default'）
    """
    prev_line_lower = prev_line.lower() if prev_line else ''
    current_line_lower = current_line.lower() if current_line else ''
    
    # **重要**: デメリットリストを先に判定（「メリット」が「デメリット」に含まれるため）
    # デメリットリスト（前の行に「デメリット」などのキーワードがある）
    if any(keyword in prev_line_lower for keyword in ['デメリット', '弱点', '欠点', '注意点']):
        return 'bad_list'
    
    # メリットリスト（前の行に「メリット」などのキーワードがある）
    # 「デメリット」の後で判定することで、「デメリット」が誤って「メリット」と判定されるのを防ぐ
    if any(keyword in prev_line_lower for keyword in ['メリット', 'おすすめポイント', '強み', '利点']):
        return 'good_list'
    
    # チェックリスト（前の行に「おすすめ」などのキーワードがある）
    if any(keyword in prev_line_lower for keyword in ['こんな人におすすめ', 'おすすめな人', '向いている人', 'おすすめ']):
        return 'check_list'
    
    # 番号付きリスト（「この記事で分かること」など）- これはTOC検出で処理されるので通常は到達しない
    if any(keyword in prev_line_lower for keyword in ['この記事で分かること', '目次', '結論']):
        return 'num_circle'
    
    return 'default'


def detect_toc_section(lines, i):
    """
    「この記事で分かること」セクションを検出
    
    Args:
        lines: 行のリスト
        i: 現在のインデックス
    
    Returns:
        (is_toc, end_index): ボックスかどうかと、リストの終了インデックス
    """
    # 「この記事で分かること」を検出
    toc_keywords = ['この記事で分かること', 'この記事でわかること', '目次', '記事の内容']
    
    if i < len(lines):
        line = lines[i].strip()
        # 見出しやリストの前の行を確認
        if any(keyword in line for keyword in toc_keywords):
            # 次の行からリストを探す
            j = i + 1
            while j < len(lines) and j < i + 10:  # 最大10行先まで確認
                if re.match(r'^[-*+]\s+', lines[j]):
                    # リストが見つかったので、TOCセクションと判定
                    # リストの終了位置を探す
                    end_idx = j
                    while end_idx < len(lines) and re.match(r'^[-*+]\s+', lines[end_idx]):
                        end_idx += 1
                    return True, end_idx
                elif lines[j].strip() and not lines[j].strip().startswith('#'):
                    break
                j += 1
    
    return False, i


def convert_lists_to_swell(markdown_text):
    """
    MarkdownのリストをSWELL形式に変換
    
    Args:
        markdown_text: Markdown形式のテキスト
    
    Returns:
        変換後のHTMLテキスト
    """
    lines = markdown_text.split('\n')
    html_lines = []
    in_list = False
    current_list_style = 'default'
    list_tag = '<ul>'
    i = 0
    
    while i < len(lines):
        line = lines[i]
        
        # 「この記事で分かること」セクションを検出
        is_toc, toc_end_idx = detect_toc_section(lines, i)
        
        if is_toc:
            # TOCボックスを生成
            html_lines.append('<div class="wp-block-group is-style-big_icon_good">')
            html_lines.append('<div class="wp-block-group__inner-container">')
            html_lines.append('<p><strong>この記事で分かること</strong></p>')
            html_lines.append('<ul class="wp-block-list is-style-num_circle">')
            
            # リスト項目を追加
            for j in range(i + 1, toc_end_idx):
                if re.match(r'^[-*+]\s+', lines[j]):
                    content = re.sub(r'^[-*+]\s+', '', lines[j]).strip()
                    html_lines.append(f'<li>{content}</li>')
            
            html_lines.append('</ul>')
            html_lines.append('</div>')
            html_lines.append('</div>')
            
            i = toc_end_idx
            continue
        
        # リスト項目を検出
        list_match = re.match(r'^[-*+]\s+(.+)$', line)
        num_match = re.match(r'^\d+\.\s+(.+)$', line)
        
        if list_match or num_match:
            content = list_match.group(1) if list_match else num_match.group(1)
            
            # リストのスタイルを判定（前の行やコンテキストから推測）
            if not in_list:
                # リスト開始前の行を確認（空行をスキップ）
                prev_idx = i - 1
                prev_line = ''
                while prev_idx >= 0:
                    prev_line = lines[prev_idx].strip()
                    if prev_line and not prev_line.startswith('#') and not prev_line.startswith('<'):
                        break
                    prev_idx -= 1
                
                if prev_line:
                    current_list_style = detect_list_style(prev_line, line)
                else:
                    current_list_style = 'default'
                
                # リストの開始
                if num_match:
                    list_tag = '<ul class="wp-block-list is-style-num_circle">'
                elif current_list_style == 'good_list':
                    list_tag = '<ul class="wp-block-list is-style-good_list">'
                elif current_list_style == 'bad_list':
                    list_tag = '<ul class="wp-block-list is-style-bad_list">'
                elif current_list_style == 'check_list':
                    list_tag = '<ul class="wp-block-list is-style-check_list">'
                else:
                    list_tag = '<ul class="wp-block-list">'
                
                html_lines.append(list_tag)
                in_list = True
            
            # リスト項目を変換
            # マーカーを検出（**text**の形式）
            content_html = content
            if re.search(r'\*\*([^*]+)\*\*', content_html):
                # 太字を保持しつつ、重要な部分にマーカーを追加（簡易版）
                # 実際には、プロンプトでマーカーを指定する方が確実
                content_html = re.sub(r'\*\*([^*]+)\*\*', r'<strong>\1</strong>', content_html)
            
            html_lines.append(f'<li>{content_html}</li>')
            
        else:
            # リスト終了
            if in_list:
                html_lines.append('</ul>')
                in_list = False
                current_list_style = 'default'
            
            # 通常の行を処理
            if line.strip():
                # 既にHTMLタグが含まれている行（見出しなど）はそのまま
                if line.strip().startswith('<'):
                    html_lines.append(line)
                # 見出しのマークダウン記号が残っている場合はスキップ（見出し変換で処理されているはず）
                elif re.match(r'^#{1,6}\s+', line.strip()):
                    # 見出し変換が漏れている場合、ここで変換
                    if line.strip().startswith('###'):
                        h3_match = re.match(r'^###\s+(.+)$', line.strip())
                        if h3_match:
                            html_lines.append(f'<h3 class="wp-block-heading">{h3_match.group(1)}</h3>')
                    elif line.strip().startswith('####'):
                        h4_match = re.match(r'^####\s+(.+)$', line.strip())
                        if h4_match:
                            html_lines.append(f'<h4 class="wp-block-heading">{h4_match.group(1)}</h4>')
                    else:
                        html_lines.append(line)
                else:
                    # 通常のテキスト行（後で段落変換で処理される）
                    html_lines.append(line)
            elif not line.strip():
                html_lines.append('')
        
        i += 1
    
    # リストが最後まで続いている場合
    if in_list:
        html_lines.append('</ul>')
    
    return '\n'.join(html_lines)


def convert_images_to_swell(markdown_text):
    """
    Markdownの画像をSWELL形式のHTMLに変換
    
    Args:
        markdown_text: Markdown形式のテキスト
    
    Returns:
        変換後のHTMLテキスト
    """
    html = markdown_text
    
    # Markdown画像形式: ![alt](url) または ![alt](url "title")
    # 商品画像の場合は size-thumbnail、その他は size-large を使用
    def replace_image(match):
        alt_text = match.group(1)
        image_url = match.group(2)
        title = match.group(3) if match.group(3) else ''
        
        # 商品画像かどうかを判定（alt テキストに「商品」「商品名」などが含まれる場合）
        is_product = any(keyword in alt_text for keyword in ['商品', '商品画像', '商品名', 'CBDオイル', 'CBDグミ', 'CBDカプセル', 'CBDベイプ'])
        
        if is_product:
            # 商品画像: size-thumbnail
            figure_class = 'wp-block-image size-thumbnail'
        else:
            # その他の画像: size-large
            figure_class = 'wp-block-image size-large'
        
        figcaption = f'<figcaption style="font-size:13px;opacity:.8">{title}</figcaption>\n' if title else ''
        
        return f'''<figure class="{figure_class}">
<img decoding="async" src="{image_url}" alt="{alt_text}" />
{figcaption}</figure>'''
    
    # Markdown画像パターンを変換
    # パターン1: ![alt](url)
    # パターン2: ![alt](url "title")
    # パターン3: ![alt](url 'title')
    def replace_image_simple(match):
        alt_text = match.group(1) if match.group(1) else ''
        image_url = match.group(2)
        
        # 商品画像かどうかを判定（alt テキストに「商品」「商品名」などが含まれる場合）
        is_product = any(keyword in alt_text for keyword in ['商品', '商品画像', '商品名', 'CBDオイル', 'CBDグミ', 'CBDカプセル', 'CBDベイプ'])
        
        if is_product:
            figure_class = 'wp-block-image size-thumbnail'
        else:
            figure_class = 'wp-block-image size-large'
        
        return f'''<figure class="{figure_class}">
<img decoding="async" src="{image_url}" alt="{alt_text}" />
</figure>'''
    
    # まず、タイトル付き画像を処理（"title" または 'title'）
    html = re.sub(r'!\[([^\]]*)\]\((https?://[^\)]+)\s+"([^"]+)"\)', replace_image, html)
    html = re.sub(r'!\[([^\]]*)\]\((https?://[^\)]+)\s+\'([^\']+)\'\)', replace_image, html)
    # 次に、タイトルなし画像を処理
    html = re.sub(r'!\[([^\]]*)\]\((https?://[^\)]+)\)', replace_image_simple, html)
    
    return html


def convert_links_to_swell(markdown_text):
    """
    MarkdownのリンクをHTMLに変換（アフィリエイトリンクはボタンに変換）
    
    Args:
        markdown_text: Markdown形式のテキスト
    
    Returns:
        変換後のHTMLテキスト
    """
    html = markdown_text
    
    # アフィリエイトリンクパターン（簡易版：URLに特定のキーワードが含まれる場合）
    affiliate_patterns = [
        r'\[([^\]]+)\]\((https?://[^\)]*a8\.net[^\)]+)\)',  # A8.net
        r'\[([^\]]+)\]\((https?://[^\)]*amazon\.co\.jp[^\)]+)\)',  # Amazon
        r'\[([^\]]+)\]\((https?://[^\)]*rakuten\.co\.jp[^\)]+)\)',  # 楽天
        r'\[([^\]]+)\]\((https?://[^\)]*naturecan\.jp[^\)]+)\)', # Naturecan
        r'\[([^\]]+)\]\((https?://[^\)]*rounwellness\.com[^\)]+)\)', # roun
    ]
    
    for pattern in affiliate_patterns:
        html = re.sub(pattern, r'<div class="swell-block-button is-style-btn_normal"><a href="\2" target="_blank" rel="noopener noreferrer" class="swell-block-button__link"><span>\1</span></a></div>', html)
    
    # 通常のリンクを変換（アフィリエイトリンク以外）
    html = re.sub(r'\[([^\]]+)\]\((https?://[^\)]+)\)', r'<a href="\2">\1</a>', html)
    
    return html


def convert_strong_to_marker(markdown_text):
    """
    太字をSWELLマーカーに変換（簡易版：重要なキーワードにmark_greenを適用）
    
    Args:
        markdown_text: Markdown形式のテキスト
    
    Returns:
        変換後のHTMLテキスト
    """
    html = markdown_text
    
    # 太字（**text**）を変換
    # プロンプトで`<span class="swl-marker mark_green">`を指定する方が確実なので、
    # ここでは通常の<strong>タグに変換
    html = re.sub(r'\*\*([^*]+)\*\*', r'<strong>\1</strong>', html)
    
    return html


def add_toc_box(markdown_text):
    """
    「この記事で分かること」ボックスを追加（H3見出しの前に配置）
    
    Args:
        markdown_text: Markdown形式のテキスト
    
    Returns:
        ボックスが追加されたHTMLテキスト
    """
    html = markdown_text
    
    # 最初のH3見出しを見つけて、その前に「この記事で分かること」ボックスを挿入
    h3_pattern = r'(<h3 class="wp-block-heading">[^<]+</h3>)'
    
    # H3見出しからリストを抽出してボックスに含める（簡易版）
    # 実際には、プロンプトで明示的に生成させる方が確実
    
    # 最初のH3の前にボックスを挿入
    first_h3_match = re.search(h3_pattern, html)
    if first_h3_match:
        # 簡易版：固定のボックスを挿入（プロンプトで生成させる方が確実）
        toc_box = '''<div class="wp-block-group is-style-big_icon_good">
<div class="wp-block-group__inner-container">
<p><strong>この記事で分かること</strong></p>
<ul class="wp-block-list is-style-num_circle">
<li>（H3見出しから自動生成）</li>
</ul>
</div>
</div>

'''
        html = html[:first_h3_match.start()] + toc_box + html[first_h3_match.start():]
    
    return html


def add_section_separators(markdown_text):
    """
    セクション間に区切り線を追加
    
    Args:
        markdown_text: Markdown形式のテキスト
    
    Returns:
        区切り線が追加されたHTMLテキスト
    """
    html = markdown_text
    
    # H3見出しの前に区切り線を追加（最初のH3以外）
    h3_pattern = r'(?<!<hr class="wp-block-separator[^"]*/>\s*\n)(<h3 class="wp-block-heading">[^<]+</h3>)'
    
    separator = '<hr class="wp-block-separator has-css-opacity is-style-wide"/>\n\n'
    
    # 最初のH3以外に区切り線を追加
    matches = list(re.finditer(r'<h3 class="wp-block-heading">[^<]+</h3>', html))
    for i, match in enumerate(matches):
        if i > 0:  # 最初のH3以外
            html = html[:match.start()] + separator + html[match.start():]
            # 次のマッチの位置を調整
            matches = list(re.finditer(r'<h3 class="wp-block-heading">[^<]+</h3>', html))
    
    return html


def remove_meta_section(markdown_text):
    """
    メタディスクリプションセクションを削除（本文には不要）
    
    Args:
        markdown_text: Markdown形式のテキスト
    
    Returns:
        メタセクションが削除されたテキスト
    """
    html = markdown_text
    
    # メタディスクリプションセクションを削除
    html = re.sub(r'##\s*メタディスクリプション\s*\n.*?(?=\n##|$)', '', html, flags=re.MULTILINE | re.DOTALL)
    
    return html


def markdown_to_swell_html(markdown_text, add_disclaimer=True, add_toc=True):
    """
    MarkdownをSWELL形式のHTMLに変換
    
    Args:
        markdown_text: Markdown形式のテキスト
        add_disclaimer: アフィリエイト免責事項を追加するか（デフォルト: True）
        add_toc: 「この記事で分かること」ボックスを追加するか（デフォルト: True）
    
    Returns:
        SWELL形式のHTMLテキスト
    """
    html = markdown_text
    
    # メタディスクリプションセクションを削除（本文には不要）
    html = remove_meta_section(html)
    
    # 変換順序が重要：
    # 1. 見出しを先に変換（段落変換の前に）
    html = convert_h2_to_swell(html)
    html = convert_h3_to_swell(html)
    html = convert_h4_to_swell(html)
    
    # 2. 太字を変換
    html = convert_strong_to_marker(html)
    
    # 3. 画像を変換（リンク変換の前に実行）
    html = convert_images_to_swell(html)
    
    # 4. リンクを変換
    html = convert_links_to_swell(html)
    
    # 5. リストを変換（見出し変換後に実行）
    html = convert_lists_to_swell(html)
    
    # 段落を変換（行単位で処理）
    # 既にHTMLタグが含まれている行（見出し、リスト、ボックスなど）はそのまま
    lines = html.split('\n')
    html_lines = []
    current_paragraph = []
    
    for line in lines:
        line_stripped = line.strip()
        
        # 空行
        if not line_stripped:
            # 蓄積された段落を出力
            if current_paragraph:
                para_text = ' '.join(current_paragraph)
                html_lines.append(f'<p>{para_text}</p>')
                current_paragraph = []
            html_lines.append('')
            continue
        
        # 既にHTMLタグが含まれている行（見出し、リスト、ボックスなど）はそのまま
        if line_stripped.startswith('<'):
            # 蓄積された段落を出力
            if current_paragraph:
                para_text = ' '.join(current_paragraph)
                html_lines.append(f'<p>{para_text}</p>')
                current_paragraph = []
            html_lines.append(line_stripped)
            continue
        
        # 見出しのマークダウン記号が残っている場合（変換漏れ）
        if re.match(r'^#{1,6}\s+', line_stripped):
            # 蓄積された段落を出力
            if current_paragraph:
                para_text = ' '.join(current_paragraph)
                html_lines.append(f'<p>{para_text}</p>')
                current_paragraph = []
            # 見出しを変換
            if line_stripped.startswith('###'):
                h3_match = re.match(r'^###\s+(.+)$', line_stripped)
                if h3_match:
                    html_lines.append(f'<h3 class="wp-block-heading">{h3_match.group(1)}</h3>')
            elif line_stripped.startswith('####'):
                h4_match = re.match(r'^####\s+(.+)$', line_stripped)
                if h4_match:
                    html_lines.append(f'<h4 class="wp-block-heading">{h4_match.group(1)}</h4>')
            continue
        
        # リストのマークダウン記号が残っている場合（変換漏れの可能性）
        if re.match(r'^[-*+]\s+', line_stripped):
            # 蓄積された段落を出力
            if current_paragraph:
                para_text = ' '.join(current_paragraph)
                html_lines.append(f'<p>{para_text}</p>')
                current_paragraph = []
            # リストは既に変換されているはずなので、そのまま（変換漏れの場合は後で処理）
            html_lines.append(line_stripped)
            continue
        
        # 通常のテキストを段落に追加
        current_paragraph.append(line_stripped)
    
    # 最後の段落を出力
    if current_paragraph:
        para_text = ' '.join(current_paragraph)
        html_lines.append(f'<p>{para_text}</p>')
    
    html = '\n'.join(html_lines)
    
    # 「この記事で分かること」ボックスを追加（convert_lists_to_swellで処理されなかった場合）
    # ただし、既にボックスが生成されている場合はスキップ
    if add_toc and '<div class="wp-block-group is-style-big_icon_good">' not in html:
        html = add_toc_box(html)
    
    # セクション間に区切り線を追加
    html = add_section_separators(html)
    
    # アフィリエイト免責事項を冒頭に追加
    if add_disclaimer:
        html = add_affiliate_disclaimer() + html
    
    # HTMLエンティティをデコード
    html = unescape(html)
    
    # 余分な空行を削除
    html = re.sub(r'\n{3,}', '\n\n', html)
    
    return html.strip()


if __name__ == '__main__':
    # テスト
    test_markdown = """# 記事タイトル

## メタディスクリプション
これはテスト記事です。

## 導入

これは導入文です。

## セクション1

本文1です。

**重要:** これは重要なポイントです。

- メリット1
- メリット2

## セクション2

本文2です。
"""
    
    result = markdown_to_swell_html(test_markdown)
    print(result)
