#!/usr/bin/env python3
"""
記事自動作成スクリプト v2
Google Sheetsから記事テーマを読み込み、Gemini APIでMarkdown記事を生成
WordPressに下書きとして保存し、スプレッドシートにメタデータを反映
"""

import os
import sys
import re
from pathlib import Path
from datetime import datetime
from dotenv import load_dotenv
import google.generativeai as genai

# 親ディレクトリをパスに追加
sys.path.insert(0, str(Path(__file__).parent.parent))

from google_services.google_sheets import read_spreadsheet, write_spreadsheet
from social_media.line_notify import send_line_message
from content.wordpress_publisher import post_to_wordpress
from content.markdown_to_swell_html import markdown_to_swell_html

# .envファイルを読み込む
load_dotenv()

# 環境変数
GEMINI_API_KEY = os.getenv('GEMINI_API_KEY', '')
ARTICLE_SPREADSHEET_ID = os.getenv('ARTICLE_SPREADSHEET_ID', '1-2L6C3NpF8vqnXxHWKP-Js3TMFKYE73tTtxdkZVPTaM')
ARTICLE_SHEET_NAME = 'Article_Theme'  # 旧: 記事生成入力（シート2）

# Gemini APIの設定
if GEMINI_API_KEY:
    genai.configure(api_key=GEMINI_API_KEY)


def get_gemini_model():
    """利用可能なGeminiモデルを取得"""
    try:
        model = genai.GenerativeModel('gemini-2.5-flash')
        return model
    except:
        try:
            model = genai.GenerativeModel('gemini-3-flash-preview')
            return model
        except:
            try:
                model = genai.GenerativeModel('gemini-2.0-flash')
                return model
            except:
                models = genai.list_models()
                if models:
                    return genai.GenerativeModel(models[0].name)
                else:
                    raise ValueError("利用可能なGeminiモデルが見つかりません")


def generate_slug(title):
    """
    タイトルからスラッグを生成
    
    Args:
        title: 記事タイトル
    
    Returns:
        スラッグ（小文字、ハイフン区切り）
    """
    # 日本語の文字を削除し、英数字のみを使用
    slug = re.sub(r'[^\w\s-]', '', title)
    slug = re.sub(r'[^\x00-\x7F]+', '', slug)  # 非ASCII文字を削除
    
    # スペースをハイフンに変換
    slug = re.sub(r'[-\s]+', '-', slug)
    
    # 連続するハイフンを1つに
    slug = re.sub(r'-+', '-', slug)
    
    # 前後のハイフンを削除
    slug = slug.strip('-').lower()
    
    # 長すぎる場合は切り詰め
    if len(slug) > 100:
        slug = slug[:100]
    
    # 空の場合はデフォルト値を返す
    if not slug:
        slug = f"article-{datetime.now().strftime('%Y%m%d')}"
    
    return slug


def extract_affiliate_links(markdown_content):
    """
    Markdownからアフィリエイトリンクを抽出
    
    Args:
        markdown_content: Markdown形式の記事本文
    
    Returns:
        アフィリエイトリンクのリスト
    """
    # リンクパターンを検索
    link_pattern = r'\[([^\]]+)\]\((https?://[^\)]+)\)'
    matches = re.findall(link_pattern, markdown_content)
    
    # Amazon、楽天、アフィリエイト関連のリンクを抽出
    affiliate_links = []
    for text, url in matches:
        # アフィリエイトリンクかどうかを判定（簡易版）
        if any(keyword in url.lower() for keyword in ['amazon', 'rakuten', 'affiliate', 'a8.net', 'af.moshimo']):
            affiliate_links.append({
                'text': text,
                'url': url
            })
    
    return affiliate_links


def generate_article_markdown(target, concern=None, keywords=None, article_type=None, category=None):
    """
    記事のMarkdownを生成
    
    Args:
        target: ターゲット（例: "CBD初心者"）
        concern: 悩み（例: "寝つきが悪い"）
        keywords: 関連キーワード（リスト）
        article_type: 記事タイプ（例: "商品紹介", "悩み解決", "経済", "ビジネス"）
        category: カテゴリ（例: "CBDオイル", "CBDベイプ"）
    
    Returns:
        Markdown形式の記事本文
    """
    if not GEMINI_API_KEY:
        raise ValueError("GEMINI_API_KEYが設定されていません。")
    
    model = get_gemini_model()
    
    # プロンプト作成
    keywords_text = ', '.join(keywords) if keywords else ''
    concern_text = f"\n**悩み:** {concern}" if concern else ''
    article_type_text = f"\n**記事タイプ:** {article_type}" if article_type else ''
    category_text = f"\n**カテゴリ:** {category}" if category else ''
    
    # 現在の年を取得（2026年）
    current_year = datetime.now().year
    
    prompt = f"""あなたはCBD専門ライターです。過去記事（1085、1097）と全く同じ構造・デザインでWordPress記事をMarkdown形式で生成してください。

【基本情報】
ターゲット: {target}{concern_text}
記事タイプ: {article_type or '商品紹介'}
キーワード: {keywords_text}
年号: {current_year}年を必ず使用

【厳密な構造（過去記事1097と同じ）】

## メタディスクリプション
（120文字以内、キーワード含む）

CBD選びで、絶対に失敗したくない。<br>
自分の体に入れるものだから、1ミリの不安も残したくない。<br>
そう思うなら、結論は**○○一択**です。

「なぜこれほど高いのか？」「なぜ世界中で売れているのか？」<br>
その理由は、○○による「品質革命」と、異常なまでの「安全への執着」にありました。

この記事で分かること:
- 項目1（具体的な内容）
- 項目2（具体的な内容）  
- 項目3（具体的な内容）
- 項目4（具体的な内容）

### セクション1タイトル

短い説明文（1-2文）。<br>
次の文も短く。

| 項目 | 内容 |
|------|------|
| 商品名 | ○○ |
| 価格 | ○○円 |
| 容量 | ○○mL |

短い説明文。

### セクション2タイトル

短い説明文。

メリット:
- 項目1
- 項目2

デメリット:
- 項目1
- 項目2

### おすすめ商品

商品説明（短く）。

#### 商品名

![商品名](商品画像URL)

| 項目 | 内容 |
|------|------|
| 商品名 | ○○ |
| 価格 | ○○円 |

メリット:
- 項目1
- 項目2

こんな人におすすめ:
- 対象1
- 対象2

[公式で詳細・成分表を見る（ブランド名）](URL)

### まとめ

短い結論（1-2文）。<br>
行動喚起。

### 参考文献（エビデンスURL）

- [研究タイトル](URL) - 研究機関
- [厚生労働省資料](URL) - 日本政府
- [WHO報告](URL) - 世界保健機関

### 関連記事

- [記事タイトル1](URL) - 記事説明
- [記事タイトル2](URL) - 記事説明
- [記事タイトル3](URL) - 記事説明

【厳守ルール】
1. **導入は必ず<br>タグで改行**（「失敗したくない」「1ミリの不安も残したくない」「結論は○○一択」の流れ）
2. **段落は1-2文のみ**（3文以上禁止）
3. **テーブルを多用**（商品情報は必ずテーブル）
4. **メリット/デメリットは必ずリスト形式**
5. **全体2,500-3,000文字**（Markdown文字数ベース）
6. **年号は{current_year}年のみ**
7. **H2見出し禁止**（H3のみ使用）
8. **専門用語は括弧説明**（例：CBD（カンナビジオール））

Markdown形式で記事を生成してください：
"""
    
    try:
        response = model.generate_content(prompt)
        article_text = response.text.strip()
        
        # Markdownブロック記号を除去（もし含まれていれば）
        article_text = re.sub(r'^```markdown\s*\n', '', article_text, flags=re.MULTILINE)
        article_text = re.sub(r'\n```\s*$', '', article_text, flags=re.MULTILINE)
        
        return article_text
    except Exception as e:
        print(f"❌ 記事生成エラー: {e}")
        import traceback
        traceback.print_exc()
        return None


def extract_meta_from_markdown(markdown_content):
    """
    Markdownからメタデータを抽出
    
    Args:
        markdown_content: Markdown形式の記事本文
    
    Returns:
        メタデータの辞書（title, description, category, tags, affiliate_links）
    """
    meta = {
        'title': '',
        'description': '',
        'category': '',
        'tags': [],
        'affiliate_links': []
    }
    
    # タイトルを抽出（最初のH1から）
    title_match = re.search(r'^#\s+(.+)$', markdown_content, re.MULTILINE)
    if title_match:
        meta['title'] = title_match.group(1).strip()
    
    # メタディスクリプションを抽出
    desc_match = re.search(r'^##\s*メタディスクリプション\s*\n(.+?)(?=\n##|$)', markdown_content, re.MULTILINE | re.DOTALL)
    if desc_match:
        meta['description'] = desc_match.group(1).strip()
    else:
        # メタディスクリプションが見つからない場合、最初の段落を使用
        first_paragraph = re.search(r'^[^#\n]+', markdown_content, re.MULTILINE)
        if first_paragraph:
            desc = first_paragraph.group(0).strip()
            if len(desc) > 150:
                desc = desc[:147] + '...'
            meta['description'] = desc
    
    # アフィリエイトリンクを抽出
    meta['affiliate_links'] = extract_affiliate_links(markdown_content)
    
    return meta


def save_article_to_wordpress_draft(title, markdown_content, meta=None, category_name=None, tag_names=None):
    """
    WordPressに下書きとして投稿
    
    Args:
        title: 記事タイトル
        markdown_content: Markdown形式の記事本文
        meta: メタデータ（オプション）
        category_name: カテゴリー名（オプション）
        tag_names: タグ名のリスト（オプション）
    
    Returns:
        投稿された記事のURL（成功時）、None（失敗時）
    """
    # WordPress REST APIで投稿（下書きとして）
    post_url = post_to_wordpress(
        title,
        markdown_content,
        status='draft',  # 下書きとして投稿
        category_name=category_name,
        tag_names=tag_names
    )
    
    return post_url


def update_spreadsheet_with_metadata(row_number, meta, article_type=None, category=None, target=None, concern=None, slug=None):
    """
    スプレッドシートにメタデータを反映
    既存の行を更新（記事内容は含めない、メタデータのみ）
    
    Args:
        row_number: 行番号
        meta: メタデータの辞書
        article_type: 記事タイプ
        category: カテゴリ
        target: ターゲット
        concern: 悩み
        slug: スラッグ
    
    Returns:
        成功した場合True
    """
    if not ARTICLE_SPREADSHEET_ID:
        print("⚠️ ARTICLE_SPREADSHEET_IDが設定されていません")
        return False
    
    # スラッグが指定されていない場合は生成
    if not slug and meta.get('title'):
        slug = generate_slug(meta['title'])
    
    # アフィリエイトリンクを文字列化（URLのみ、カンマ区切り）
    affiliate_urls = ','.join([link['url'] for link in meta.get('affiliate_links', [])])
    
    # スプレッドシートの列構成
    # 列A: タイムスタンプ、列B: ステータス、列C: 記事タイトル、列D: 記事の分類、列E: ターゲット、
    # 列F: タグ、列G: ディスクリプション、列H: スラッグ、列I: アフィリエイトリンク
    # 既存の行を更新するため、列Aは既存のタイムスタンプを保持、列B〜Iを更新
    row_data = [
        datetime.now().isoformat(),  # 列A: タイムスタンプ（更新時刻）
        '下書き',  # 列B: ステータス
        meta.get('title', ''),  # 列C: 記事タイトル
        article_type or '',  # 列D: 記事の分類
        target or '',  # 列E: ターゲット
        ','.join(meta.get('tags', [])),  # 列F: タグ（カンマ区切り）
        meta.get('description', ''),  # 列G: ディスクリプション
        slug or '',  # 列H: スラッグ
        affiliate_urls  # 列I: アフィリエイトリンク（URLのみ、カンマ区切り）
    ]
    
    # スプレッドシートに書き込み（既存の行を更新）
    range_name = f'{ARTICLE_SHEET_NAME}!A{row_number}:I{row_number}'
    result = write_spreadsheet(ARTICLE_SPREADSHEET_ID, range_name, [row_data])
    
    if result:
        print(f"✅ スプレッドシートにメタデータを反映しました: 行{row_number}")
        return True
    else:
        print(f"❌ スプレッドシートへの反映に失敗しました: 行{row_number}")
        return False


def generate_articles_from_sheet():
    """
    Google Sheetsから記事テーマを読み込んで記事を生成
    """
    if not ARTICLE_SPREADSHEET_ID:
        print("⚠️ ARTICLE_SPREADSHEET_IDが設定されていません")
        return
    
    # スプレッドシートからデータを読み込み
    # 列A: タイムスタンプ、列B: ステータス、列C: 記事タイトル、列D: 記事の分類、列E: ターゲット、
    # 列F: タグ、列G: ディスクリプション、列H: スラッグ、列I: アフィリエイトリンク
    sheet_data = read_spreadsheet(ARTICLE_SPREADSHEET_ID, f'{ARTICLE_SHEET_NAME}!A:I')
    
    if not sheet_data or len(sheet_data) < 2:
        print("⚠️ スプレッドシートにデータが見つかりません")
        print(f"   {ARTICLE_SHEET_NAME}の列A〜Iに記事テーマを入力してください")
        return
    
    # ヘッダー行をスキップ
    rows = sheet_data[1:]
    
    print(f"📝 {len(rows)}件の記事テーマを読み込みました\n")
    
    generated_count = 0
    
    for i, row in enumerate(rows, start=2):
        # 既に記事が生成されている場合はスキップ（ステータス列を確認）
        # 列Bに「下書き」「承認済み」「投稿済み」が入っている場合はスキップ
        if len(row) >= 2 and row[1] and row[1] in ['下書き', '承認済み', '投稿済み']:
            print(f"⚠️ 行{i}: 既に処理済みです（ステータス: {row[1]}） - スキップ")
            continue
        
        # 記事タイプ、ターゲット、タグを取得（列D, E, F）
        # 列D: 記事の分類、列E: ターゲット、列F: タグ
        article_type = row[3].strip() if len(row) > 3 and row[3] else None
        target = row[4].strip() if len(row) > 4 and row[4] else ''
        tags_str = row[5].strip() if len(row) > 5 and row[5] else ''
        tags = [tag.strip() for tag in tags_str.split(',') if tag.strip()] if tags_str else []
        
        # ターゲットが入力されていない場合はスキップ
        if not target:
            print(f"⚠️ 行{i}: ターゲット（列E）が入力されていません（スキップ）")
            continue
        
        # 悩みを取得（オプション、別の列から取得する場合）
        concern = None  # 現在はターゲットのみで生成
        
        # カテゴリを取得（タグから推測、または別の列から）
        category = tags[0] if tags else None
        
        print(f"📝 記事生成中: {target} / {article_type}")
        
        # 記事を生成
        article_markdown = generate_article_markdown(
            target,
            concern=concern,
            keywords=tags,
            article_type=article_type,
            category=category
        )
        
        if not article_markdown:
            print(f"❌ 記事生成に失敗しました")
            continue
        
        # メタデータを抽出
        meta = extract_meta_from_markdown(article_markdown)
        
        # タイトルを取得（メタデータから、または生成）
        title = meta.get('title') or f"{target}: CBDに関する記事"
        
        # スラッグを生成
        slug = generate_slug(title)
        
        # WordPressに下書きとして投稿
        print(f"📝 WordPressに下書きとして投稿中...")
        post_url = save_article_to_wordpress_draft(title, article_markdown, meta, category_name=category, tag_names=tags)
        
        if post_url:
            # スプレッドシートにメタデータを反映
            update_spreadsheet_with_metadata(
                i,
                meta,
                article_type=article_type,
                category=category,
                target=target,
                concern=concern,
                slug=slug
            )
            
            generated_count += 1
            print(f"✅ 記事を生成しました: {title}")
            print(f"   WordPress下書きURL: {post_url}\n")
        else:
            print(f"❌ WordPress投稿に失敗しました\n")
    
    # LINE通知
    if generated_count > 0:
        message = f"📝 記事生成完了\n\n{generated_count}件の記事を生成しました。\nWordPressの下書きを確認・添削してください。"
        send_line_message(message)
        print(f"\n✅ {generated_count}件の記事を生成しました")
    else:
        print("\n⚠️ 記事が生成されませんでした")


def main():
    """メイン関数"""
    generate_articles_from_sheet()


if __name__ == '__main__':
    main()
