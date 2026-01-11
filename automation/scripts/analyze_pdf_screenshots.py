#!/usr/bin/env python3
"""
PDFスクリーンショットからアカウント分析データを抽出してスプレッドシートに書き込む
OCRを使用してPDFからテキストを抽出し、情報を自動で分析
"""

import os
import sys
from pathlib import Path
from datetime import datetime
import re

# 親ディレクトリをパスに追加
sys.path.insert(0, str(Path(__file__).parent.parent))

from dotenv import load_dotenv
from google_services.google_sheets import write_spreadsheet

# OCRライブラリのインポート
try:
    import pytesseract
    from PIL import Image
    from pdf2image import convert_from_path
    OCR_AVAILABLE = True
except ImportError:
    OCR_AVAILABLE = False
    print("⚠️ OCRライブラリがインストールされていません。基本的な情報のみ抽出します。")

# .envファイルを読み込む
load_dotenv()


def extract_text_from_pdf(pdf_path, lang='jpn+eng'):
    """
    PDFファイルからテキストを抽出（OCR使用）
    
    Args:
        pdf_path: PDFファイルのパス
        lang: 使用する言語（デフォルト: jpn+eng）
    
    Returns:
        抽出されたテキスト
    """
    if not OCR_AVAILABLE:
        return None
    
    try:
        # PDFを画像に変換
        images = convert_from_path(str(pdf_path), dpi=300)
        
        all_text = []
        for i, image in enumerate(images):
            # OCRでテキスト抽出
            text = pytesseract.image_to_string(image, lang=lang)
            all_text.append(text)
        
        return "\n".join(all_text)
    
    except Exception as e:
        print(f"⚠️ OCRエラー: {e}")
        return None


def extract_account_info_from_pdf(pdf_path):
    """
    PDFファイルからアカウント情報を抽出（ファイル名とOCRから）
    
    Args:
        pdf_path: PDFファイルのパス
    
    Returns:
        アカウント情報の辞書
    """
    filename = Path(pdf_path).stem
    
    # ファイル名からアカウント名を抽出
    # 新しい形式: YYYY-MM-DD_accountname.pdf
    if re.match(r'\d{4}-\d{2}-\d{2}_', filename):
        # 日付部分を除いた部分がアカウント名
        account_name = re.sub(r'^\d{4}-\d{2}-\d{2}_', '', filename)
        display_name = ""
    else:
        # 古い形式: "FireShot Capture 001 - さくら🌸- AI×ショート動画 (@Oc4Um) _ X - [x.com]"
        match = re.search(r'@(\w+)', filename)
        account_name = match.group(1) if match else None
        display_name_match = re.search(r' - ([^-]+) \(@', filename)
        display_name = display_name_match.group(1).strip() if display_name_match else ""
    
    account_info = {
        'account_name': account_name,
        'display_name': display_name,
        'filename': filename,
        'pdf_path': pdf_path
    }
    
    # OCRでテキストを抽出
    if OCR_AVAILABLE:
        ocr_text = extract_text_from_pdf(pdf_path)
        if ocr_text:
            account_info['ocr_text'] = ocr_text
            # OCRテキストから追加情報を抽出
            extracted_data = extract_data_from_ocr_text(ocr_text)
            account_info.update(extracted_data)
    
    return account_info


def extract_data_from_ocr_text(text):
    """
    OCRで抽出したテキストから分析データを抽出
    
    Args:
        text: OCRで抽出したテキスト
    
    Returns:
        抽出されたデータの辞書
    """
    data = {}
    
    if not text:
        return data
    
    # フォロワー数を抽出
    # パターン: "フォロワー 12,345" または "12,345 Followers" または "21.9万人" など
    follower_patterns = [
        r'フォロワー[\s:：]*([\d,]+)',
        r'([\d.]+)[万人千]*(?:フォロワー|Followers)',
        r'(\d+)\s*Followers',
        r'(\d+)\s*Following',
    ]
    for pattern in follower_patterns:
        match = re.search(pattern, text, re.IGNORECASE)
        if match:
            try:
                follower_str = match.group(1).replace(',', '').replace('，', '')
                # "21.9万"のような形式を処理
                if '万' in text[match.start():match.end()+5]:
                    data['followers'] = str(int(float(follower_str) * 10000))
                else:
                    data['followers'] = follower_str
                break
            except:
                pass
    
    # ツイート数を抽出
    # パターン: "ツイート 1,234" または "1,234 Posts" など
    tweet_patterns = [
        r'ツイート[\s:：]*([\d,]+)',
        r'Posts[\s:：]*([\d,]+)',
        r'(\d+)\s*Posts',
    ]
    for pattern in tweet_patterns:
        match = re.search(pattern, text, re.IGNORECASE)
        if match:
            try:
                data['tweets'] = match.group(1).replace(',', '').replace('，', '')
                break
            except:
                pass
    
    # ジャンルを推測（表示名や説明から）
    genre_keywords = {
        'アフィリエイト': ['アフィリエイト', 'アフィリ', 'affiliate'],
        '美容': ['美容', 'コスメ', 'スキンケア', 'エステ'],
        '家庭': ['家庭', '家計', '節約', 'マネー'],
        '健康': ['健康', 'サプリ', '漢方', 'メンタル', '薬剤師'],
        '投資': ['投資', '株', 'FX', '資産運用'],
        'AI': ['AI', '人工知能', 'ChatGPT', '生成AI'],
    }
    text_lower = text.lower()
    for genre, keywords in genre_keywords.items():
        if any(kw.lower() in text_lower for kw in keywords):
            data['genre'] = genre
            break
    
    # 説明文から職業や特徴を抽出
    description_patterns = [
        r'職業[:：]?([^\n]+)',
        r'職種[:：]?([^\n]+)',
        r'([^\n]{10,50})',  # 長めの説明文
    ]
    for pattern in description_patterns:
        matches = re.findall(pattern, text)
        if matches:
            # 最も長い説明文を取得
            description = max(matches, key=len)
            if len(description) > 10:
                data['description'] = description[:100]  # 最初の100文字
                break
    
    return data


def get_sheet_structure():
    """
    スプレッドシートの構造を定義
    """
    headers = [
        'アカウント名',
        '表示名',
        'ジャンル',
        'フォロワー数',
        'ツイート数',
        '1日の平均投稿数',
        '投稿時間帯',
        '投稿パターン',
        '平均文字数',
        '改行数',
        'タイトル記号使用率',
        '絵文字使用率',
        '箇条書き使用率',
        'アフィリエイト使用率',
        '商品紹介頻度',
        'アフィリエイトリンクの配置',
        'コンテンツタイプ',
        'よく使うキーワード',
        'バズツイートの特徴',
        '平均いいね数',
        '平均リツイート数',
        '取り入れたいポイント1',
        '取り入れたいポイント2',
        '取り入れたいポイント3',
        '取り入れたいポイント4',
        '取り入れたいポイント5',
        '分析日',
        'PDFファイル名'
    ]
    
    return headers


def create_analysis_template(account_info):
    """
    分析用のテンプレートデータを作成
    
    Args:
        account_info: アカウント情報の辞書（OCR抽出データを含む）
    
    Returns:
        テンプレートデータ（リスト）
    """
    today = datetime.now().strftime('%Y-%m-%d')
    
    return [
        account_info.get('account_name', ''),
        account_info.get('display_name', ''),
        account_info.get('genre', ''),  # OCRから抽出したジャンル
        account_info.get('followers', ''),  # OCRから抽出したフォロワー数
        account_info.get('tweets', ''),  # OCRから抽出したツイート数
        account_info.get('daily_post_count', ''),  # OCRから推測した1日の平均投稿数
        '',  # 投稿時間帯（OCRでは抽出困難、手動入力）
        '',  # 投稿パターン（手動入力）
        account_info.get('avg_length', ''),  # OCRから分析した平均文字数
        account_info.get('avg_line_breaks', ''),  # OCRから分析した改行数
        account_info.get('title_marker_rate', ''),  # OCRから分析したタイトル記号使用率
        account_info.get('emoji_rate', ''),  # OCRから分析した絵文字使用率
        account_info.get('bullet_rate', ''),  # OCRから分析した箇条書き使用率
        account_info.get('affiliate_detected', ''),  # OCRから検出したアフィリエイト使用率
        '',  # 商品紹介頻度（手動入力）
        '',  # アフィリエイトリンクの配置（手動入力）
        '',  # コンテンツタイプ（手動入力）
        '',  # よく使うキーワード（手動入力）
        '',  # バズツイートの特徴（手動入力）
        '',  # 平均いいね数（手動入力）
        '',  # 平均リツイート数（手動入力）
        '',  # 取り入れたいポイント1（手動入力）
        '',  # 取り入れたいポイント2（手動入力）
        '',  # 取り入れたいポイント3（手動入力）
        '',  # 取り入れたいポイント4（手動入力）
        '',  # 取り入れたいポイント5（手動入力）
        today,  # 分析日
        account_info.get('filename', '')  # PDFファイル名
    ]


def rename_pdf_file(pdf_path, account_name, date_str=None):
    """
    PDFファイル名を日付とアカウント名に合わせて修正
    
    Args:
        pdf_path: PDFファイルのパス
        account_name: アカウント名（@は除く）
        date_str: 日付文字列（YYYY-MM-DD形式、省略時は現在の日付）
    
    Returns:
        新しいファイルパス
    """
    if date_str is None:
        date_str = datetime.now().strftime('%Y-%m-%d')
    
    old_path = Path(pdf_path)
    new_filename = f"{date_str}_{account_name}.pdf"
    new_path = old_path.parent / new_filename
    
    if old_path.exists() and old_path != new_path:
        try:
            if new_path.exists():
                print(f"⚠️ 既に存在するためスキップ: {new_filename}")
            else:
                old_path.rename(new_path)
                print(f"✅ ファイル名を変更: {old_path.name} → {new_filename}")
            return str(new_path)
        except Exception as e:
            print(f"⚠️ ファイル名変更エラー: {e}")
            return str(old_path)
    
    return str(old_path)


def main():
    """メイン関数"""
    # PDFファイルのパス
    base_dir = Path(__file__).parent.parent.parent / "CBD関連" / "他アカウントデータ"
    
    # 新しいファイル名形式で検索（YYYY-MM-DD_accountname.pdf）
    pdf_files = []
    if base_dir.exists():
        pdf_files = list(base_dir.glob("2026-01-11_*.pdf"))
        pdf_files.sort()
    
    if not pdf_files:
        print("⚠️ PDFファイルが見つかりませんでした")
        print(f"検索ディレクトリ: {base_dir}")
        return
    
    # スプレッドシートID
    spreadsheet_id = "1Lc1cXwWbp20QpimPDGfaKSBk2hY6FhG_3_0-JCknU3Q"
    sheet_name = "シート1"
    
    print("=" * 60)
    print("PDFスクリーンショット分析とスプレッドシート書き込み")
    print("=" * 60)
    print(f"📁 検出されたPDFファイル: {len(pdf_files)}件")
    if OCR_AVAILABLE:
        print("✅ OCR機能: 利用可能")
    else:
        print("⚠️ OCR機能: 利用不可（基本的な情報のみ抽出）")
    print("=" * 60)
    
    # アカウント情報を抽出
    account_data_list = []
    for pdf_path in pdf_files:
        print(f"\n📄 処理中: {pdf_path.name}")
        account_info = extract_account_info_from_pdf(str(pdf_path))
        
        # 抽出結果を表示
        if 'followers' in account_info:
            print(f"  ✅ フォロワー数: {account_info['followers']}")
        if 'tweets' in account_info:
            print(f"  ✅ ツイート数: {account_info['tweets']}")
        if 'genre' in account_info:
            print(f"  ✅ ジャンル: {account_info['genre']}")
        if 'daily_post_count' in account_info:
            print(f"  ✅ 1日の平均投稿数: {account_info['daily_post_count']}")
        if 'avg_length' in account_info and account_info['avg_length']:
            print(f"  ✅ 平均文字数: {account_info['avg_length']}")
        if 'avg_line_breaks' in account_info and account_info['avg_line_breaks']:
            print(f"  ✅ 平均改行数: {account_info['avg_line_breaks']}")
        if 'title_marker_rate' in account_info and account_info['title_marker_rate']:
            print(f"  ✅ タイトル記号使用率: {account_info['title_marker_rate']}%")
        if 'emoji_rate' in account_info and account_info['emoji_rate']:
            print(f"  ✅ 絵文字使用率: {account_info['emoji_rate']}%")
        if 'affiliate_detected' in account_info:
            print(f"  ✅ アフィリエイト検出: {account_info['affiliate_detected']}")
        
        account_data_list.append(account_info)
    
    if not account_data_list:
        print("❌ 分析対象のPDFファイルが見つかりませんでした")
        return
    
    print(f"\n📊 {len(account_data_list)}件のアカウント情報を抽出しました")
    
    # スプレッドシートの構造を取得
    headers = get_sheet_structure()
    
    # ヘッダーを書き込み（既にある場合はスキップ）
    try:
        range_name = f"{sheet_name}!A1"
        # 既存のデータを確認
        from google_services.google_sheets import read_spreadsheet
        existing_data = read_spreadsheet(spreadsheet_id, f"{sheet_name}!A1:Z1")
        if not existing_data or existing_data[0] != headers:
            write_spreadsheet(spreadsheet_id, range_name, [headers])
            print(f"\n✅ ヘッダーを書き込みました")
        else:
            print(f"\n✅ ヘッダーは既に存在します")
    except Exception as e:
        print(f"⚠️ ヘッダー書き込みエラー: {e}")
    
    # 各アカウントのテンプレートデータを書き込み
    print(f"\n📝 データをスプレッドシートに書き込み中...")
    
    for i, account_info in enumerate(account_data_list, start=2):
        template_data = create_analysis_template(account_info)
        
        try:
            range_name = f"{sheet_name}!A{i}"
            write_spreadsheet(spreadsheet_id, range_name, [template_data])
            print(f"✅ [{i-1}/{len(account_data_list)}] @{account_info.get('account_name', 'unknown')} のデータを書き込みました")
        except Exception as e:
            print(f"❌ [{i-1}/{len(account_data_list)}] @{account_info.get('account_name', 'unknown')} の書き込みエラー: {e}")
    
    print("\n" + "=" * 60)
    print("✅ 処理完了")
    print("=" * 60)
    print(f"\n📋 スプレッドシート:")
    print(f"https://docs.google.com/spreadsheets/d/{spreadsheet_id}/edit")
    print(f"\n💡 次のステップ:")
    print(f"1. スプレッドシートを開いて、自動抽出されたデータを確認")
    print(f"2. PDFスクリーンショットを確認しながら、残りの項目を手動で入力")
    print(f"3. OCRで抽出できなかった情報は手動で補完してください")


if __name__ == '__main__':
    main()
