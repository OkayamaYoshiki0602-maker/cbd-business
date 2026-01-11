#!/usr/bin/env python3
"""
PDFスクリーンショットからOCRを使ってテキストを抽出する
"""

import sys
from pathlib import Path

# 親ディレクトリをパスに追加
sys.path.insert(0, str(Path(__file__).parent.parent))

try:
    import pytesseract
    from PIL import Image
    from pdf2image import convert_from_path
    OCR_AVAILABLE = True
except ImportError as e:
    OCR_AVAILABLE = False
    print(f"⚠️ OCRライブラリがインストールされていません: {e}")
    print("インストール方法:")
    print("  pip3 install pytesseract Pillow pdf2image")
    print("  brew install tesseract tesseract-lang poppler")


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
            all_text.append(f"--- ページ {i+1} ---\n{text}\n")
        
        return "\n".join(all_text)
    
    except Exception as e:
        print(f"❌ OCRエラー: {e}")
        return None


def extract_text_from_image(image_path, lang='jpn+eng'):
    """
    画像ファイルからテキストを抽出（OCR使用）
    
    Args:
        image_path: 画像ファイルのパス
        lang: 使用する言語（デフォルト: jpn+eng）
    
    Returns:
        抽出されたテキスト
    """
    if not OCR_AVAILABLE:
        return None
    
    try:
        image = Image.open(image_path)
        text = pytesseract.image_to_string(image, lang=lang)
        return text
    
    except Exception as e:
        print(f"❌ OCRエラー: {e}")
        return None


if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("使用方法:")
        print("  python pdf_ocr_extractor.py <PDFファイルパス> [言語コード]")
        print("\n例:")
        print("  python pdf_ocr_extractor.py test.pdf jpn+eng")
        sys.exit(1)
    
    file_path = sys.argv[1]
    lang = sys.argv[2] if len(sys.argv) > 2 else 'jpn+eng'
    
    if not Path(file_path).exists():
        print(f"❌ ファイルが見つかりません: {file_path}")
        sys.exit(1)
    
    print(f"📄 ファイルを処理中: {file_path}")
    print(f"🌐 言語: {lang}")
    print("=" * 60)
    
    if file_path.lower().endswith('.pdf'):
        text = extract_text_from_pdf(file_path, lang)
    else:
        text = extract_text_from_image(file_path, lang)
    
    if text:
        print(text)
        print("=" * 60)
        print(f"\n✅ テキスト抽出完了（文字数: {len(text)}）")
    else:
        print("❌ テキスト抽出に失敗しました")
