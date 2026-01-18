#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
CBD記事生成（HTML直接出力版）
過去記事（1085、1097）と同じ構造のHTMLを直接生成
"""

import os
import sys
from pathlib import Path
from datetime import datetime
from dotenv import load_dotenv

sys.path.insert(0, str(Path(__file__).parent.parent))

import google.generativeai as genai
from google_services.google_sheets import read_spreadsheet, write_spreadsheet

load_dotenv()

ARTICLE_SPREADSHEET_ID = os.getenv('ARTICLE_SPREADSHEET_ID', '1-2L6C3NpF8vqnXxHWKP-Js3TMFKYE73tTtxdkZVPTaM')
ARTICLE_SHEET_NAME = 'Article_Theme'  # 旧: 記事生成入力（シート2）
GEMINI_API_KEY = os.getenv('GEMINI_API_KEY')
WORDPRESS_URL = os.getenv('WORDPRESS_URL', 'https://cbd-no-hito.com')
WORDPRESS_USERNAME = os.getenv('WORDPRESS_USERNAME', 'yoshiki')
WORDPRESS_PASSWORD = os.getenv('WORDPRESS_APP_PASSWORD')

genai.configure(api_key=GEMINI_API_KEY)


def generate_article_html(target, concern, article_type, keywords):
    """
    Gemini APIを使用してHTML形式の記事を直接生成
    過去記事（1097のNaturecanレビュー）と同じ構造を再現
    """
    current_year = datetime.now().year
    
    concern_text = f"（{concern}）" if concern else ""
    article_type_text = f"（{article_type}）" if article_type else ""
    keywords_text = "、".join(keywords.split("、")[:5]) if keywords else ""
    
    prompt = f"""あなたはCBD専門ライターです。以下の指定に従い、過去記事と完全に同じHTMLフォーマットの記事を生成してください。

【基本情報】
ターゲット: {target}{concern_text}
記事タイプ: {article_type_text}
キーワード: {keywords_text}
年号: {current_year}年

【必須HTML構造】
過去記事「【決定版】Naturecan(ネイチャーカン)の評判は？世界No.1と言われる3つの理由」と完全に同じ構造で生成してください。

【構造テンプレート】

```html
<h2 class="wp-block-heading is-style-default">【決定版】記事タイトル</h2>

<p>開始文章。<br />改行を含む。<br />最後に結論を入れる。</p>

<p>次の段落。詳細な背景情報。<br />複数行に分割。</p>

<div class="wp-block-group is-style-big_icon_good">
  <div class="wp-block-group__inner-container">
    <p><strong>この記事で分かること</strong></p>
    <ul class="wp-block-list is-style-num_circle">
      <li>項目1</li>
      <li>項目2</li>
      <li>項目3</li>
      <li>項目4</li>
    </ul>
  </div>
</div>

<hr class="wp-block-separator has-css-opacity is-style-wide"/>

<h3 class="wp-block-heading">セクション1タイトル</h3>

<p>本文（短い段落）。</p>

<figure class="wp-block-image size-large">
  <img decoding="async" src="画像URL" alt="画像説明" />
  <figcaption style="font-size:13px;opacity:.8">キャプション</figcaption>
</figure>

<p>説明文。</p>

<div class="wp-block-group is-style-big_icon_good">
  <div class="wp-block-group__inner-container">
    <p><strong>情報タイトル</strong></p>
    <ul class="wp-block-list is-style-good_list">
      <li><span class="swl-marker mark_green">メリット1</span></li>
      <li>メリット2</li>
    </ul>
  </div>
</div>

<figure class="wp-block-table is-style-regular">
  <table>
    <thead>
      <tr>
        <th>項目</th>
        <th>内容</th>
      </tr>
    </thead>
    <tbody>
      <tr>
        <td>項目1</td>
        <td>内容1</td>
      </tr>
      <tr>
        <td>項目2</td>
        <td>内容2</td>
      </tr>
    </tbody>
  </table>
</figure>

<hr class="wp-block-separator has-css-opacity is-style-wide"/>

<h3 class="wp-block-heading">セクション2タイトル</h3>

<p>本文</p>

<h4 class="wp-block-heading">🥇 商品1</h4>

<figure class="wp-block-image size-thumbnail">
  <img decoding="async" src="商品画像URL" alt="商品名" />
</figure>

<figure class="wp-block-table is-style-regular">
  <table>
    <thead><tr><th>項目</th><th>内容</th></tr></thead>
    <tbody>
      <tr><td>商品名</td><td>商品名</td></tr>
      <tr><td>価格</td><td>価格</td></tr>
    </tbody>
  </table>
</figure>

<p><strong>メリット</strong>：</p>
<ul class="wp-block-list is-style-good_list">
  <li><span class="swl-marker mark_green">メリット1</span></li>
  <li>メリット2</li>
</ul>

<p><strong>デメリット</strong>：</p>
<ul class="wp-block-list is-style-bad_list">
  <li>デメリット1</li>
</ul>

<p><strong>こんな人におすすめ</strong>：</p>
<ul class="wp-block-list">
  <li>対象1</li>
  <li>対象2</li>
</ul>

<div class="swell-block-button is-style-btn_normal">
  <a href="アフィリエイトURL" target="_blank" rel="noopener noreferrer" class="swell-block-button__link">
    <span>公式で詳細を見る（ブランド名）</span>
  </a>
</div>

<hr class="wp-block-separator has-css-opacity is-style-wide"/>

<h3 class="wp-block-heading">まとめ</h3>

<div class="wp-block-group is-style-big_icon_good">
  <div class="wp-block-group__inner-container">
    <p><strong>おすすめな人</strong></p>
    <ul class="wp-block-list is-style-check_list">
      <li>特徴1</li>
      <li>特徴2</li>
    </ul>
  </div>
</div>

<p>👉 <strong>最終的な推奨メッセージ</strong></p>
```

【厳守ルール】
1. 全てのコンテンツはHTML形式で出力（Markdownではなく）
2. 段落は`<p>`タグで、必ず`<br />`で改行を含める
3. リストは`<ul class="wp-block-list">`を使用
4. メリット=`is-style-good_list`、デメリット=`is-style-bad_list`、チェック=`is-style-check_list`
5. テーブルは`<figure class="wp-block-table is-style-regular">`で囲む
6. 各セクション前に`<hr class="wp-block-separator has-css-opacity is-style-wide"/>`を入れる
7. 見出しは`<h2>`（タイトル）、`<h3>`（セクション）、`<h4>`（サブセクション）のみ
8. マーカーは`<span class="swl-marker mark_green">`で囲む
9. ボタンは必ず`<div class="swell-block-button is-style-btn_normal">`の形式
10. 画像は`<figure class="wp-block-image size-thumbnail">`（商品）または`size-large"`（その他）

【内容要件】
- 全体：2,500-3,500文字（HTML含む）
- 導入：共感→問題→解決策の流れ
- セクション：3-4個
- 各セクション：150-300文字
- 医療効果の断定表現禁止
- エビデンスベース（推測禁止）
- 初心者向けに平易な表現

それではHTML形式の記事を生成してください：
"""
    
    try:
        model = genai.GenerativeModel('gemini-2.5-flash')
        response = model.generate_content(prompt)
        html_content = response.text.strip()
        
        # HTMLコードブロックの削除
        html_content = html_content.replace('```html', '').replace('```', '')
        html_content = html_content.strip()
        
        return html_content
    except Exception as e:
        print(f"❌ 記事生成エラー: {e}")
        import traceback
        traceback.print_exc()
        return None


def post_to_wordpress(html_content, title, category_name=None, tag_names=None):
    """
    WordPressに記事をポストする
    """
    import requests
    from base64 import b64encode
    
    if not WORDPRESS_PASSWORD:
        print("⚠️ WORDPRESS_APP_PASSWORDが設定されていません")
        return None
    
    auth_string = b64encode(f"{WORDPRESS_USERNAME}:{WORDPRESS_PASSWORD}".encode()).decode()
    
    url = f"{WORDPRESS_URL}/wp-json/wp/v2/posts"
    headers = {
        "Authorization": f"Basic {auth_string}",
        "Content-Type": "application/json"
    }
    
    # カテゴリIDを取得
    category_id = None
    if category_name:
        cat_url = f"{WORDPRESS_URL}/wp-json/wp/v2/categories"
        cat_response = requests.get(cat_url)
        categories = cat_response.json()
        for cat in categories:
            if cat['name'] == category_name:
                category_id = cat['id']
                break
    
    # タグIDを取得
    tag_ids = []
    if tag_names:
        tag_url = f"{WORDPRESS_URL}/wp-json/wp/v2/tags"
        tag_response = requests.get(tag_url)
        tags = tag_response.json()
        for tag_name in tag_names.split("、"):
            tag_name = tag_name.strip()
            for tag in tags:
                if tag['name'] == tag_name:
                    tag_ids.append(tag['id'])
                    break
    
    payload = {
        "title": title,
        "content": html_content,
        "status": "draft",
        "categories": [category_id] if category_id else [],
        "tags": tag_ids if tag_ids else []
    }
    
    try:
        response = requests.post(url, json=payload, headers=headers, timeout=60)
        if response.status_code in [200, 201]:
            post_data = response.json()
            return {
                "id": post_data['id'],
                "link": post_data['link'],
                "status": post_data['status']
            }
        else:
            print(f"❌ WordPressエラー: {response.status_code} - {response.text}")
            return None
    except Exception as e:
        print(f"❌ WordPress連携エラー: {e}")
        return None


def extract_title_and_meta(html_content):
    """
    HTMLから記事タイトルとメタディスクリプションを抽出
    """
    import re
    
    # タイトルを抽出（最初のH2から）
    title_match = re.search(r'<h2[^>]*>([^<]+)</h2>', html_content)
    title = title_match.group(1) if title_match else "記事"
    
    # メタディスクリプション（最初のpタグから）
    desc_match = re.search(r'<p>([^<]+)</p>', html_content)
    description = desc_match.group(1).replace('<br />', ' ') if desc_match else ""
    description = description[:150]
    
    return title, description


def generate_slug(title):
    """
    SEO-friendly slugを生成
    """
    import re
    slug = title.lower()
    slug = re.sub(r'[【】「」『』【決定版】]+', '', slug)
    slug = re.sub(r'[^a-z0-9ぁ-ん]+', '-', slug)
    slug = slug.strip('-')
    return slug


def update_spreadsheet_metadata(row_num, title, description, category, tags, slug, affiliates):
    """
    スプレッドシートにメタデータを反映
    """
    timestamp = datetime.now().isoformat()
    update_data = [[timestamp, "下書き", title, category, "", tags, description, slug, affiliates]]
    
    write_spreadsheet(
        ARTICLE_SPREADSHEET_ID,
        f'{ARTICLE_SHEET_NAME}!A{row_num}:I{row_num}',
        update_data
    )


def main():
    """メイン実行"""
    print("📝 スプレッドシート『記事テーマ』から記事テーマを読み込み中...\n")
    
    # スプレッドシート『記事テーマ』からデータを読み込み
    data = read_spreadsheet(ARTICLE_SPREADSHEET_ID, f'{ARTICLE_SHEET_NAME}!A2:I100')
    
    if not data:
        print("⚠️ スプレッドシートにデータが見つかりません")
        return
    
    print(f"📝 {len(data)}件の記事テーマを読み込みました\n")
    
    generated_count = 0
    
    for row_num, row in enumerate(data, start=2):
        if len(row) < 2:
            continue
        
        # status, title, category, target, tags, description, slug, affiliates
        status = row[1] if len(row) > 1 else ""
        
        if status != "新規":
            print(f"⚠️ 行{row_num}: 既に処理済みです（ステータス: {status}） - スキップ")
            continue
        
        category = row[3] if len(row) > 3 else "商品紹介"
        target = row[4] if len(row) > 4 else "CBD初心者"
        tags_str = row[5] if len(row) > 5 else ""
        
        print(f"📝 HTML形式で記事生成中: {target} / {category}")
        
        # HTML記事を生成
        html_content = generate_article_html(
            target=target,
            concern="",
            article_type=category,
            keywords=tags_str
        )
        
        if not html_content:
            print(f"❌ 記事生成失敗（行{row_num}）")
            continue
        
        # タイトルとメタ情報を抽出
        title, description = extract_title_and_meta(html_content)
        slug = generate_slug(title)
        
        print(f"📝 WordPressに下書きとして投稿中...")
        
        # WordPressにポスト
        result = post_to_wordpress(html_content, title, category_name=category, tag_names=tags_str)
        
        if result:
            print(f"✅ WordPressに投稿しました: {result['link']}")
            print(f"   投稿ID: {result['id']}")
            
            # スプレッドシート『記事一覧』を更新
            update_spreadsheet_metadata(row_num, title, description, category, tags_str, slug, "")
            print(f"✅ スプレッドシート『記事テーマ』のメタデータを反映しました: 行{row_num}")
            
            print(f"✅ 記事を生成しました: {title}")
            print(f"   WordPress下書きURL: {result['link']}\n")
            
            generated_count += 1
        else:
            print(f"❌ WordPress投稿失敗（行{row_num}）\n")
    
    print(f"\n✅ {generated_count}件の記事を生成しました")


if __name__ == '__main__':
    main()
