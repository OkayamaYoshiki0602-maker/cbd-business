#!/usr/bin/env python3
"""
Google Services MCP Server
Googleサービスと連携するカスタムMCPサーバー（stdio版 - 簡易実装）
"""

import sys
import os
import json
from pathlib import Path

# パスの設定
SCRIPT_DIR = Path(__file__).parent.parent
sys.path.insert(0, str(SCRIPT_DIR))

# Googleサービスモジュールをインポート
try:
    from google_services.google_sheets import read_spreadsheet, write_spreadsheet, list_spreadsheets, create_sheet, list_sheets
    from google_services.ga4 import get_report, format_report_data, get_summary_stats, get_today_stats
    from google_services.google_calendar import create_event, list_events, list_calendars
    from google_services.gmail import list_messages, get_message, decode_message_body
except ImportError as e:
    print(f"Error importing Google services modules: {e}", file=sys.stderr)
    print(f"Python path: {sys.path}", file=sys.stderr)
    sys.exit(1)

# MCPプロトコル（簡易版 - stdio経由）
def send_response(response):
    """MCPプロトコルに従ってレスポンスを送信"""
    try:
        json.dump(response, sys.stdout, ensure_ascii=False)
        sys.stdout.write("\n")
        sys.stdout.flush()
    except Exception as e:
        print(f"Error sending response: {e}", file=sys.stderr)

def handle_request(request):
    """MCPリクエストを処理"""
    try:
        method = request.get("method")
        params = request.get("params", {})
        request_id = request.get("id")
        
        if method == "initialize":
            # 初期化メッセージ
            send_response({
                "jsonrpc": "2.0",
                "id": request_id,
                "result": {
                    "protocolVersion": "2024-11-05",
                    "capabilities": {
                        "tools": {}
                    },
                    "serverInfo": {
                        "name": "google-services-mcp",
                        "version": "1.0.0"
                    }
                }
            })
        
        elif method == "tools/list":
            # ツール一覧を返す
            tools = [
                {
                    "name": "read_google_sheets",
                    "description": "Googleスプレッドシートからデータを読み込む",
                    "inputSchema": {
                        "type": "object",
                        "properties": {
                            "spreadsheet_id": {"type": "string", "description": "スプレッドシートID"},
                            "range": {"type": "string", "description": "読み込む範囲（例: 'Sheet1!A1:D10'）", "default": "Sheet1!A1:Z1000"}
                        },
                        "required": ["spreadsheet_id"]
                    }
                },
                {
                    "name": "write_google_sheets",
                    "description": "Googleスプレッドシートにデータを書き込む",
                    "inputSchema": {
                        "type": "object",
                        "properties": {
                            "spreadsheet_id": {"type": "string", "description": "スプレッドシートID"},
                            "range": {"type": "string", "description": "書き込む範囲（例: 'Sheet1!A1'）"},
                            "values": {
                                "type": "array",
                                "items": {
                                    "type": "array",
                                    "items": {"type": "string"}
                                },
                                "description": "書き込むデータ（2次元配列）"
                            }
                        },
                        "required": ["spreadsheet_id", "range", "values"]
                    }
                },
                {
                    "name": "list_google_sheets",
                    "description": "Google Driveからスプレッドシート一覧を取得",
                    "inputSchema": {
                        "type": "object",
                        "properties": {
                            "query": {"type": "string", "description": "検索クエリ", "default": ""},
                            "max_results": {"type": "integer", "description": "最大取得件数", "default": 10}
                        }
                    }
                },
                {
                    "name": "get_ga4_summary",
                    "description": "GA4のサマリー統計を取得",
                    "inputSchema": {
                        "type": "object",
                        "properties": {
                            "property_id": {"type": "string", "description": "GA4プロパティID", "default": "505457597"},
                            "days": {"type": "integer", "description": "日数", "default": 7}
                        }
                    }
                },
                {
                    "name": "get_ga4_today",
                    "description": "GA4の本日のアクセス数を取得",
                    "inputSchema": {
                        "type": "object",
                        "properties": {
                            "property_id": {"type": "string", "description": "GA4プロパティID", "default": "505457597"}
                        }
                    }
                },
                {
                    "name": "create_calendar_event",
                    "description": "Googleカレンダーに予定を作成",
                    "inputSchema": {
                        "type": "object",
                        "properties": {
                            "summary": {"type": "string", "description": "イベントのタイトル"},
                            "start_time": {"type": "string", "description": "開始時刻（ISO形式: 2025-01-11T14:00:00）"},
                            "end_time": {"type": "string", "description": "終了時刻（ISO形式: 2025-01-11T15:00:00）"},
                            "description": {"type": "string", "description": "説明", "default": ""},
                            "location": {"type": "string", "description": "場所", "default": ""},
                            "calendar_id": {"type": "string", "description": "カレンダーID", "default": "primary"}
                        },
                        "required": ["summary", "start_time"]
                    }
                },
                {
                    "name": "create_sheet_tab",
                    "description": "スプレッドシートに新しいシート（タブ）を作成",
                    "inputSchema": {
                        "type": "object",
                        "properties": {
                            "spreadsheet_id": {"type": "string", "description": "スプレッドシートID"},
                            "sheet_title": {"type": "string", "description": "新しいシートのタイトル"}
                        },
                        "required": ["spreadsheet_id", "sheet_title"]
                    }
                },
                {
                    "name": "list_gmail_messages",
                    "description": "Gmailのメール一覧を取得（okayamayoshiki0602o@gmail.com）",
                    "inputSchema": {
                        "type": "object",
                        "properties": {
                            "max_results": {"type": "integer", "description": "最大取得件数", "default": 10},
                            "query": {"type": "string", "description": "検索クエリ（例: 'is:unread'）", "default": ""}
                        }
                    }
                }
            ]
            
            send_response({
                "jsonrpc": "2.0",
                "id": request_id,
                "result": {
                    "tools": tools
                }
            })
        
        elif method == "tools/call":
            # ツールを実行
            tool_name = params.get("name")
            arguments = params.get("arguments", {})
            
            try:
                if tool_name == "read_google_sheets":
                    spreadsheet_id = arguments.get("spreadsheet_id")
                    range_name = arguments.get("range", "Sheet1!A1:Z1000")
                    data = read_spreadsheet(spreadsheet_id, range_name)
                    
                    if data:
                        result_text = json.dumps(data, ensure_ascii=False, indent=2)
                    else:
                        result_text = "エラー: データの読み込みに失敗しました"
                
                elif tool_name == "write_google_sheets":
                    spreadsheet_id = arguments.get("spreadsheet_id")
                    range_name = arguments.get("range")
                    values = arguments.get("values")
                    success = write_spreadsheet(spreadsheet_id, range_name, values)
                    result_text = "✅ データの書き込みが完了しました" if success else "❌ データの書き込みに失敗しました"
                
                elif tool_name == "list_google_sheets":
                    query = arguments.get("query", "")
                    max_results = arguments.get("max_results", 10)
                    files = list_spreadsheets(query, max_results)
                    
                    if files:
                        result = [f"- {f['name']} ({f['id']})" for f in files]
                        result_text = "\n".join(result)
                    else:
                        result_text = "スプレッドシートが見つかりませんでした"
                
                elif tool_name == "get_ga4_summary":
                    property_id = arguments.get("property_id", "505457597")
                    days = arguments.get("days", 7)
                    stats = get_summary_stats(property_id, date_range_days=days)
                    
                    if stats:
                        result_text = f"""📊 GA4統計（過去{stats['days']}日間）
セッション数: {stats['sessions']:,}
ページビュー数: {stats['pageviews']:,}
アクティブユーザー数: {stats['active_users']:,}
1日あたりのPV（平均）: {stats['pageviews'] / stats['days']:.1f}"""
                    else:
                        result_text = "エラー: サマリー統計の取得に失敗しました"
                
                else:
                    result_text = f"不明なツール: {tool_name}"
                
                send_response({
                    "jsonrpc": "2.0",
                    "id": request_id,
                    "result": {
                        "content": [
                            {
                                "type": "text",
                                "text": result_text
                            }
                        ]
                    }
                })
            
            except Exception as e:
                send_response({
                    "jsonrpc": "2.0",
                    "id": request_id,
                    "error": {
                        "code": -32000,
                        "message": f"ツール実行エラー: {str(e)}"
                    }
                })
        
        else:
            send_response({
                "jsonrpc": "2.0",
                "id": request_id,
                "error": {
                    "code": -32601,
                    "message": f"Method not found: {method}"
                }
            })
    
    except Exception as e:
        send_response({
            "jsonrpc": "2.0",
            "id": request.get("id"),
            "error": {
                "code": -32700,
                "message": f"Parse error: {str(e)}"
            }
        })

def main():
    """メイン関数 - stdio経由でMCPプロトコルを処理"""
    try:
        # リクエストを読み込んで処理
        for line in sys.stdin:
            if not line.strip():
                continue
            
            try:
                request = json.loads(line.strip())
                handle_request(request)
            except json.JSONDecodeError as e:
                print(f"JSON decode error: {e}", file=sys.stderr)
                continue
    
    except KeyboardInterrupt:
        pass
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        import traceback
        traceback.print_exc(file=sys.stderr)
        sys.exit(1)

if __name__ == '__main__':
    main()
