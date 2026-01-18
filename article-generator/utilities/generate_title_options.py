#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
タイトル候補をGoogle Sheets に自動入力するスクリプト
Article_Theme の「新規」ステータスの行にタイトル候補を生成して入力
"""

import os
import sys
import re
from pathlib import Path
from datetime import datetime
from dotenv import load_dotenv
import json

sys.path.insert(0, str(Path(__file__).parent.parent))

import google.generativeai as genai
from google_services.google_sheets import read_spreadsheet, write_spreadsheet

load_dotenv()

ARTICLE_SPREADSHEET_ID = os.getenv('ARTICLE_SPREADSHEET_ID', '1-2L6C3NpF8vqnXxHWKP-Js3TMFKYE73tTtxdkZVPTaM')
ARTICLE_SHEET_NAME = 'Article_Theme'
GEMINI_API_KEY = os.getenv('GEMINI_API_KEY')

genai.configure(api_key=GEMINI_API_KEY)

# テンプレート定義（全15個に拡張）
TEMPLATES = {
    1: {"name": "単一商品レビュー型", "require_product": True},
    2: {"name": "複数商品比較型", "require_product": True},
    3: {"name": "ブランド比較型", "require_product": True},
    4: {"name": "初心者向け商品ガイド型", "require_product": True},
    5: {"name": "上級者向け商品ガイド型", "require_product": True},
    6: {"name": "購入ガイド・コスパ型", "require_product": True},
    7: {"name": "基礎知識解説型", "require_product": False},
    8: {"name": "科学的根拠解説型", "require_product": False},
    9: {"name": "歴史・背景解説型", "require_product": False},
    10: {"name": "法律・規制解説型", "require_product": False},
    11: {"name": "業界トレンド解説型", "require_product": False},
    12: {"name": "医学的課題解決型", "require_product": True},
    13: {"name": "日常的課題解決型", "require_product": True},
    14: {"name": "ビジネス・パフォーマンス型", "require_product": False},
    15: {"name": "体験談型", "require_product": True},
}


def generate_title_variations(theme, template_id):
    """
    複数のタイトル候補を生成
    """
    model = genai.GenerativeModel("gemini-2.5-flash")
    current_year = datetime.now().year
    template_name = TEMPLATES.get(template_id, {}).get("name", "")
    
    prompt = f"""あなたはSEO最適化と読者の興味を引き出すプロのライターです。

【指定内容】
テーマ: {theme}
テンプレート: {template_name}
年号: {current_year}

【要件】
以下の5つのタイトル候補を生成してください。各タイトルは異なるアプローチで、読みたくなるようにしてください。

1. 数字を活用したタイトル（例：「3つの」「5つの理由」など）
2. 疑問形のタイトル（例：「○○って本当に効く？」）
3. 解決策を示すタイトル（例：「××を解決する方法は？」）
4. 権威性を持つタイトル（例：「【プロが選ぶ】」「【データで証明】」）
5. 希少性・最新性を活用したタイトル（例：「2026年最新」「知られざる」）

【禁止事項】
- 「【決定版】」を全てに付けない
- 同じ枕詞を複数使わない
- 説教的な表現は避ける
- 誇大広告のような表現は避ける

【出力形式】
JSON形式で、以下の構造で返してください：
{{
  "titles": [
    {{"number": 1, "title": "タイトル1"}},
    {{"number": 2, "title": "タイトル2"}},
    {{"number": 3, "title": "タイトル3"}},
    {{"number": 4, "title": "タイトル4"}},
    {{"number": 5, "title": "タイトル5"}}
  ]
}}

タイトルのみ返してください。前置きや説明は不要です。
"""
    
    try:
        response = model.generate_content(prompt)
        json_str = response.text.strip()
        
        # JSON を抽出
        match = re.search(r'\{[\s\S]*\}', json_str)
        if match:
            data = json.loads(match.group())
            titles = [item["title"] for item in data.get("titles", [])]
            return titles[:5]
        else:
            return []
    
    except Exception as e:
        print(f"⚠️ タイトル生成エラー: {e}")
        return []


def populate_title_options_in_sheet():
    """
    Article_Theme の「新規」ステータスの行にタイトル候補を入力
    """
    
    print("📝 Article_Theme からデータを読み込み中...\n")
    print("=" * 120)
    
    try:
        # Article_Theme から全データを取得
        sheet_data = read_spreadsheet(ARTICLE_SPREADSHEET_ID, f"{ARTICLE_SHEET_NAME}!A:P")
        
        if not sheet_data or len(sheet_data) < 2:
            print("⚠️ スプレッドシートにデータが見つかりません")
            return
        
        headers = sheet_data[0]
        
        print(f"✅ ヘッダーを取得しました（{len(headers)}列）\n")
        
        # 「新規」ステータスの行を処理
        rows_updated = 0
        
        for row_idx, row in enumerate(sheet_data[1:], start=2):
            # 必要な列を取得（列番号で直接指定）
            # A: タイムスタンプ(0), B: ステータス(1), C: テーマ(2), D: テンプレート(3)
            status = row[1] if len(row) > 1 else ""
            theme = row[2] if len(row) > 2 else ""
            template_str = row[3] if len(row) > 3 else ""
            
            # K列（タイトル候補1）はインデックス10
            title_option_1 = row[10] if len(row) > 10 else ""
            
            # 「新規」ステータスで、タイトル候補がまだ入力されていない行
            if status == "新規" and not title_option_1:
                print(f"【行{row_idx}】テーマ: {theme[:50]}...")
                print(f"  テンプレート: {template_str}")
                
                # テンプレートIDを取得
                template_id = None
                for tid, tinfo in TEMPLATES.items():
                    if tinfo["name"] == template_str:
                        template_id = tid
                        break
                
                if not template_id:
                    print(f"  ❌ テンプレート '{template_str}' が見つかりません\n")
                    continue
                
                # タイトル候補を生成
                print(f"  📋 タイトル候補を生成中...")
                titles = generate_title_variations(theme, template_id)
                
                if not titles or len(titles) < 5:
                    print(f"  ❌ タイトル候補の生成に失敗しました\n")
                    continue
                
                # Google Sheets に書き込み
                print(f"  ✓ 5つのタイトル候補を生成しました")
                print(f"    1. {titles[0][:60]}...")
                print(f"    2. {titles[1][:60]}...")
                print(f"    3. {titles[2][:60]}...")
                print(f"    4. {titles[3][:60]}...")
                print(f"    5. {titles[4][:60]}...")
                
                # K～O 列（タイトル候補1～5）に書き込み
                for col_idx, title in enumerate(titles, start=10):  # K列は10
                    col_letter = chr(64 + col_idx + 1)
                    cell_range = f"{ARTICLE_SHEET_NAME}!{col_letter}{row_idx}"
                    write_spreadsheet(ARTICLE_SPREADSHEET_ID, cell_range, [[title]])
                
                # ステータスを「タイトル選択待ち」に変更
                status_range = f"{ARTICLE_SHEET_NAME}!B{row_idx}"
                write_spreadsheet(ARTICLE_SPREADSHEET_ID, status_range, [["タイトル選択待ち"]])
                
                print(f"  ✅ タイトル候補をシートに書き込みました")
                print(f"  ステータスを「タイトル選択待ち」に変更しました\n")
                
                rows_updated += 1
        
        print("=" * 120)
        
        if rows_updated > 0:
            print(f"\n✅ {rows_updated}行のタイトル候補を生成・書き込みしました")
            print("\n【次のステップ】")
            print("1. Google Sheets で P列「選択されたタイトル」に選択したタイトルを入力")
            print("2. ステータスを「生成待ち」に変更")
            print("3. article_generator_html_v2.py を実行")
        else:
            print("\n✓ 処理対象の行がありません（既に全て処理済み）")
    
    except Exception as e:
        print(f"❌ エラー: {e}")
        import traceback
        traceback.print_exc()


def show_title_candidates(row_number=None):
    """
    Sheets のタイトル候補を表示
    """
    
    print("📋 【タイトル候補の確認】\n")
    print("=" * 120)
    
    try:
        sheet_data = read_spreadsheet(ARTICLE_SPREADSHEET_ID, f"{ARTICLE_SHEET_NAME}!A:P")
        
        if not sheet_data or len(sheet_data) < 2:
            print("⚠️ データが見つかりません")
            return
        
        headers = sheet_data[0]
        
        # 行を選定
        if row_number and row_number < len(sheet_data):
            rows_to_show = [sheet_data[row_number]]
            start_row = row_number + 1
        else:
            # 「タイトル選択待ち」ステータスの行のみ
            rows_to_show = []
            start_row_list = []
            for idx, row in enumerate(sheet_data[1:], start=2):
                if len(row) > 1 and row[1] == "タイトル選択待ち":
                    rows_to_show.append(row)
                    start_row_list.append(idx)
        
        for row_idx, row in zip(start_row_list, rows_to_show):
            print(f"\n【行{row_idx}】")
            print(f"テーマ: {row[2] if len(row) > 2 else 'N/A'}")
            print(f"\nタイトル候補:")
            
            for i in range(5):
                col_idx = 10 + i  # K列から始まる
                if col_idx < len(row) and row[col_idx]:
                    print(f"  {i+1}. {row[col_idx]}")
            
            print(f"\nP列「選択されたタイトル」に上記の1つを入力してください")
        
        if not rows_to_show:
            print("✓ 「タイトル選択待ち」ステータスの行がありません")
    
    except Exception as e:
        print(f"❌ エラー: {e}")
    
    print("\n" + "=" * 120)


if __name__ == '__main__':
    import argparse
    
    parser = argparse.ArgumentParser(description='Article_Theme のタイトル候補を生成・表示')
    parser.add_argument('--generate', action='store_true', help='タイトル候補を生成して Sheets に入力')
    parser.add_argument('--show', action='store_true', help='タイトル候補を表示')
    parser.add_argument('--row', type=int, help='特定の行のタイトル候補を表示（デフォルトは「タイトル選択待ち」の全行）')
    
    args = parser.parse_args()
    
    if args.generate:
        populate_title_options_in_sheet()
    elif args.show:
        show_title_candidates(args.row)
    else:
        print("使用方法:")
        print("  python3 generate_title_options.py --generate    # タイトル候補を生成")
        print("  python3 generate_title_options.py --show        # タイトル候補を表示")
        print("  python3 generate_title_options.py --show --row 2 # 2行目のタイトル候補を表示")
