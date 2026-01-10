#!/usr/bin/env python3
"""
Google Analytics 4 (GA4) データ取得スクリプト
GA4からアクセス解析データを取得する
"""

import os
import sys
import json
from datetime import datetime, timedelta
from google.oauth2 import service_account
from google.analytics.data_v1beta import BetaAnalyticsDataClient
from google.analytics.data_v1beta.types import (
    RunReportRequest,
    DateRange,
    Metric,
    Dimension
)


# 認証情報ファイルのパス
CREDENTIALS_FILE = os.path.expanduser("~/.config/cursor/google-drive-credentials.json")

# デフォルトのプロパティID
DEFAULT_PROPERTY_ID = "505457597"  # CBDサイトのGA4プロパティID


def get_credentials():
    """認証情報を取得"""
    if not os.path.exists(CREDENTIALS_FILE):
        raise FileNotFoundError(
            f"認証情報ファイルが見つかりません: {CREDENTIALS_FILE}\n"
            "Google Cloud Consoleから認証情報を取得してください。"
        )
    
    credentials = service_account.Credentials.from_service_account_file(
        CREDENTIALS_FILE,
        scopes=['https://www.googleapis.com/auth/analytics.readonly']
    )
    return credentials


def get_report(property_id, date_range_days=7, metrics=None, dimensions=None):
    """
    GA4からレポートデータを取得
    
    Args:
        property_id: GA4プロパティID
        date_range_days: 日数（デフォルト: 7日間）
        metrics: 取得する指標のリスト（デフォルト: sessions, screenPageViews）
        dimensions: 取得するディメンションのリスト（デフォルト: date）
    
    Returns:
        レポートデータ
    """
    try:
        credentials = get_credentials()
        client = BetaAnalyticsDataClient(credentials=credentials)
        
        # デフォルトの指標
        if metrics is None:
            metrics = [
                Metric(name="sessions"),
                Metric(name="screenPageViews"),
                Metric(name="activeUsers"),
            ]
        else:
            metrics = [Metric(name=m) for m in metrics]
        
        # デフォルトのディメンション
        if dimensions is None:
            dimensions = [Dimension(name="date")]
        else:
            dimensions = [Dimension(name=d) for d in dimensions]
        
        # 日付範囲を計算
        end_date = datetime.now().date()
        start_date = end_date - timedelta(days=date_range_days)
        
        request = RunReportRequest(
            property=f"properties/{property_id}",
            date_ranges=[
                DateRange(
                    start_date=start_date.isoformat(),
                    end_date=end_date.isoformat()
                )
            ],
            metrics=metrics,
            dimensions=dimensions,
        )
        
        response = client.run_report(request)
        return response
    
    except Exception as error:
        print(f"エラーが発生しました: {error}")
        return None


def format_report_data(response):
    """レポートデータをフォーマット"""
    if not response:
        return None
    
    # ヘッダー行
    dimension_headers = [header.name for header in response.dimension_headers]
    metric_headers = [header.name for header in response.metric_headers]
    headers = dimension_headers + metric_headers
    
    # データ行
    rows = []
    for row in response.rows:
        dimension_values = [value.value for value in row.dimension_values]
        metric_values = [value.value for value in row.metric_values]
        rows.append(dimension_values + metric_values)
    
    return {
        'headers': headers,
        'rows': rows,
        'row_count': response.row_count
    }


def get_summary_stats(property_id, date_range_days=7):
    """
    サマリー統計を取得
    
    Args:
        property_id: GA4プロパティID
        date_range_days: 日数
    
    Returns:
        サマリー統計データ
    """
    response = get_report(
        property_id,
        date_range_days=date_range_days,
        metrics=["sessions", "screenPageViews", "activeUsers"]
    )
    
    if not response:
        return None
    
    # 合計値を計算
    total_sessions = sum(
        int(row.metric_values[0].value)
        for row in response.rows
    )
    
    total_pageviews = sum(
        int(row.metric_values[1].value)
        for row in response.rows
    )
    
    total_users = sum(
        int(row.metric_values[2].value)
        for row in response.rows
    )
    
    return {
        'sessions': total_sessions,
        'pageviews': total_pageviews,
        'active_users': total_users,
        'days': date_range_days
    }


def main():
    """メイン関数"""
    if len(sys.argv) < 2:
        print("使用方法:")
        print("  python ga4.py report [property_id] [days]")
        print("  python ga4.py summary [property_id] [days]")
        print("\n例:")
        print(f"  python ga4.py report {DEFAULT_PROPERTY_ID} 7")
        print(f"  python ga4.py summary {DEFAULT_PROPERTY_ID} 30")
        sys.exit(1)
    
    command = sys.argv[1]
    property_id = sys.argv[2] if len(sys.argv) > 2 else DEFAULT_PROPERTY_ID
    days = int(sys.argv[3]) if len(sys.argv) > 3 else 7
    
    if command == 'report':
        response = get_report(property_id, date_range_days=days)
        if response:
            data = format_report_data(response)
            print(json.dumps(data, ensure_ascii=False, indent=2))
    
    elif command == 'summary':
        stats = get_summary_stats(property_id, date_range_days=days)
        if stats:
            print(f"\n📊 GA4統計（過去{stats['days']}日間）")
            print(f"セッション数: {stats['sessions']:,}")
            print(f"ページビュー数: {stats['pageviews']:,}")
            print(f"アクティブユーザー数: {stats['active_users']:,}")
            print(f"1日あたりのPV（平均）: {stats['pageviews'] / stats['days']:.1f}")
    
    else:
        print(f"不明なコマンド: {command}")
        sys.exit(1)


if __name__ == '__main__':
    main()
