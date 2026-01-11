#!/usr/bin/env python3
"""
サイトの現状分析スクリプト
- GA4データの取得
- サイト構造の分析
- コンバージョン分析
"""

import os
import sys
from pathlib import Path
from dotenv import load_dotenv
from datetime import datetime, timedelta
import json

# 親ディレクトリをパスに追加
sys.path.insert(0, str(Path(__file__).parent.parent))

from google_services.ga4 import get_report, format_report_data

load_dotenv()

# GA4設定（プロパティIDはURLから取得: a368683003p505457597 → 505457597）
GA4_PROPERTY_ID = os.getenv('GA4_PROPERTY_ID', '505457597')

def analyze_site_traffic():
    """サイトのトラフィック分析"""
    print("=" * 60)
    print("📊 サイトトラフィック分析")
    print("=" * 60)
    
    try:
        # 過去30日間のデータを取得
        response = get_report(
            property_id=GA4_PROPERTY_ID,
            date_range_days=30,
            metrics=['sessions', 'screenPageViews', 'activeUsers'],
            dimensions=['date']
        )
        
        if response and response.rows:
            formatted_data = format_report_data(response)
            if formatted_data:
                total_sessions = sum(int(row[1]) for row in formatted_data['rows'])
                total_pageviews = sum(int(row[2]) for row in formatted_data['rows'])
                total_users = sum(int(row[3]) for row in formatted_data['rows'])
                
                print(f"\n📈 過去30日間の統計:")
                print(f"  - セッション数: {total_sessions:,}")
                print(f"  - ユーザー数: {total_users:,}")
                print(f"  - ページビュー: {total_pageviews:,}")
                print(f"  - 1日あたりの平均セッション: {total_sessions/30:.1f}")
                print(f"  - 1日あたりの平均PV: {total_pageviews/30:.1f}")
            else:
                print("⚠️ データが取得できませんでした")
        else:
            print("⚠️ データが取得できませんでした")
            
    except Exception as e:
        print(f"❌ エラー: {e}")
        import traceback
        traceback.print_exc()

def analyze_top_pages():
    """人気ページの分析"""
    print("\n" + "=" * 60)
    print("📄 人気ページ分析（過去30日間）")
    print("=" * 60)
    
    try:
        response = get_report(
            property_id=GA4_PROPERTY_ID,
            date_range_days=30,
            metrics=['screenPageViews', 'sessions'],
            dimensions=['pagePath']
        )
        
        if response and response.rows:
            formatted_data = format_report_data(response)
            if formatted_data:
                # ページビューでソート（降順）
                rows = formatted_data['rows']
                rows_sorted = sorted(rows, key=lambda x: int(x[1]), reverse=True)[:10]
                
                print("\nトップ10ページ:")
                for i, row in enumerate(rows_sorted, 1):
                    page_path = row[0]
                    pageviews = row[1]
                    sessions = row[2]
                    
                    print(f"\n{i}. {page_path}")
                    print(f"   ページビュー: {pageviews}")
                    print(f"   セッション: {sessions}")
            else:
                print("⚠️ データが取得できませんでした")
        else:
            print("⚠️ データが取得できませんでした")
            
    except Exception as e:
        print(f"❌ エラー: {e}")
        import traceback
        traceback.print_exc()

def analyze_traffic_sources():
    """トラフィックソース分析"""
    print("\n" + "=" * 60)
    print("🔍 トラフィックソース分析（過去30日間）")
    print("=" * 60)
    
    try:
        response = get_report(
            property_id=GA4_PROPERTY_ID,
            date_range_days=30,
            metrics=['sessions', 'activeUsers'],
            dimensions=['sessionSource', 'sessionMedium']
        )
        
        if response and response.rows:
            formatted_data = format_report_data(response)
            if formatted_data:
                # セッション数でソート（降順）
                rows = formatted_data['rows']
                rows_sorted = sorted(rows, key=lambda x: int(x[2]), reverse=True)[:10]
                
                print("\nトップ10トラフィックソース:")
                for i, row in enumerate(rows_sorted, 1):
                    source = row[0]
                    medium = row[1]
                    sessions = row[2]
                    users = row[3]
                    
                    print(f"\n{i}. {source} / {medium}")
                    print(f"   セッション: {sessions}")
                    print(f"   ユーザー: {users}")
            else:
                print("⚠️ データが取得できませんでした")
        else:
            print("⚠️ データが取得できませんでした")
            
    except Exception as e:
        print(f"❌ エラー: {e}")
        import traceback
        traceback.print_exc()

def analyze_site_structure():
    """サイト構造の分析（ウェブサイトから取得した情報を基に）"""
    print("\n" + "=" * 60)
    print("🏗️  サイト構造分析")
    print("=" * 60)
    
    # ウェブサイトから取得した情報を基に分析
    structure = {
        'メニュー構成': [
            'そもそもCBDとは？',
            '睡眠にお困りのあなた',
            'ストレスでお困りのあなた',
            '仕事/勉強に集中したいあなた',
            'CBDオイル',
            'CBDカプセル',
            'CBDグミ',
            'CBDベイプ',
            'お問い合わせ'
        ],
        'カテゴリー': [
            'Uncategorized',
            'オイル',
            'グミ',
            'ストレス',
            'タバコ',
            'ベイプ',
            '基礎知識（Basics）',
            '摂取方法（Methods）',
            '睡眠',
            '課題別（Issues）',
            '集中'
        ],
        '主要コンテンツ': {
            '記事タイプ': [
                '課題別（睡眠、ストレス、集中）',
                '商品タイプ別（オイル、カプセル、グミ、ベイプ）',
                '基礎知識',
                '摂取方法'
            ],
            'コンバージョンポイント': [
                '商品リンク（アフィリエイト）',
                'お問い合わせフォーム'
            ]
        }
    }
    
    print("\n📋 メニュー構成:")
    for item in structure['メニュー構成']:
        print(f"  - {item}")
    
    print("\n📂 カテゴリー:")
    for category in structure['カテゴリー']:
        print(f"  - {category}")
    
    print("\n📝 主要コンテンツ:")
    print("  記事タイプ:")
    for content_type in structure['主要コンテンツ']['記事タイプ']:
        print(f"    - {content_type}")
    
    print("  コンバージョンポイント:")
    for conversion_point in structure['主要コンテンツ']['コンバージョンポイント']:
        print(f"    - {conversion_point}")

def generate_summary_report():
    """サマリーレポートの生成"""
    print("\n" + "=" * 60)
    print("📊 サマリーレポート")
    print("=" * 60)
    
    print("\n✅ 確認事項:")
    print("  1. GA4は設定済み")
    print("  2. サイト構造は明確（課題別×商品タイプ別）")
    print("  3. コンテンツ戦略が明確（実体験×データ分析型60%、ライフスタイル型30%、その他10%）")
    
    print("\n⚠️  改善が必要な点:")
    print("  1. コンバージョン目標の設定（GA4）")
    print("  2. 記事のコンバージョン率の分析")
    print("  3. コンバージョン導線の最適化")
    print("  4. CTA（Call to Action）の配置最適化")
    
    print("\n🎯 次のアクション:")
    print("  1. GA4コンバージョン目標の設定")
    print("  2. 記事ごとのコンバージョン率の分析")
    print("  3. コンバージョン導線の設計")
    print("  4. 記事テンプレートの作成")

def main():
    """メイン処理"""
    print("=" * 60)
    print("🚀 サイト現状分析を開始します")
    print("=" * 60)
    
    # サイト構造分析
    analyze_site_structure()
    
    # GA4データ分析
    analyze_site_traffic()
    analyze_top_pages()
    analyze_traffic_sources()
    
    # サマリーレポート
    generate_summary_report()
    
    print("\n" + "=" * 60)
    print("✅ 分析完了")
    print("=" * 60)

if __name__ == '__main__':
    main()
