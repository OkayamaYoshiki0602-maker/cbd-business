#!/usr/bin/env python3
"""
Google Services MCP Server
Googleサービスと連携するカスタムMCPサーバー
"""

import sys
import os
import json
import asyncio
from pathlib import Path

# MCP SDKをインポート（利用可能な場合）
try:
    from mcp.server import Server
    from mcp.types import Tool, TextContent
    MCP_AVAILABLE = True
except ImportError:
    MCP_AVAILABLE = False
    print("Warning: MCP SDK not available. Install with: pip install mcp", file=sys.stderr)

# Googleサービスモジュールをインポート
sys.path.insert(0, str(Path(__file__).parent.parent))
from google_services.google_sheets import read_spreadsheet, write_spreadsheet, list_spreadsheets
from google_services.ga4 import get_report, format_report_data, get_summary_stats


# MCPサーバーのインスタンス
if MCP_AVAILABLE:
    server = Server("google-services-mcp")
else:
    server = None


# ツール定義
def get_tools():
    """MCPツールの定義"""
    if not MCP_AVAILABLE:
        return []
    
    return [
        Tool(
            name="read_google_sheets",
            description="Googleスプレッドシートからデータを読み込む",
            inputSchema={
                "type": "object",
                "properties": {
                    "spreadsheet_id": {
                        "type": "string",
                        "description": "スプレッドシートID"
                    },
                    "range": {
                        "type": "string",
                        "description": "読み込む範囲（例: 'Sheet1!A1:D10'）",
                        "default": "Sheet1!A1:Z1000"
                    }
                },
                "required": ["spreadsheet_id"]
            }
        ),
        Tool(
            name="write_google_sheets",
            description="Googleスプレッドシートにデータを書き込む",
            inputSchema={
                "type": "object",
                "properties": {
                    "spreadsheet_id": {
                        "type": "string",
                        "description": "スプレッドシートID"
                    },
                    "range": {
                        "type": "string",
                        "description": "書き込む範囲（例: 'Sheet1!A1'）"
                    },
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
        ),
        Tool(
            name="list_google_sheets",
            description="Google Driveからスプレッドシート一覧を取得",
            inputSchema={
                "type": "object",
                "properties": {
                    "query": {
                        "type": "string",
                        "description": "検索クエリ（例: \"name contains 'CBD'\"）",
                        "default": ""
                    },
                    "max_results": {
                        "type": "integer",
                        "description": "最大取得件数",
                        "default": 10
                    }
                }
            }
        ),
        Tool(
            name="get_ga4_report",
            description="GA4からレポートデータを取得",
            inputSchema={
                "type": "object",
                "properties": {
                    "property_id": {
                        "type": "string",
                        "description": "GA4プロパティID",
                        "default": "505457597"
                    },
                    "days": {
                        "type": "integer",
                        "description": "日数（デフォルト: 7日間）",
                        "default": 7
                    }
                }
            }
        ),
        Tool(
            name="get_ga4_summary",
            description="GA4のサマリー統計を取得",
            inputSchema={
                "type": "object",
                "properties": {
                    "property_id": {
                        "type": "string",
                        "description": "GA4プロパティID",
                        "default": "505457597"
                    },
                    "days": {
                        "type": "integer",
                        "description": "日数（デフォルト: 7日間）",
                        "default": 7
                    }
                }
            }
        ),
    ]


# ツールハンドラー
async def handle_call_tool(name: str, arguments: dict):
    """ツール呼び出しハンドラー"""
    try:
        if name == "read_google_sheets":
            spreadsheet_id = arguments.get("spreadsheet_id")
            range_name = arguments.get("range", "Sheet1!A1:Z1000")
            data = read_spreadsheet(spreadsheet_id, range_name)
            
            if data:
                return TextContent(
                    type="text",
                    text=json.dumps(data, ensure_ascii=False, indent=2)
                )
            else:
                return TextContent(
                    type="text",
                    text="エラー: データの読み込みに失敗しました"
                )
        
        elif name == "write_google_sheets":
            spreadsheet_id = arguments.get("spreadsheet_id")
            range_name = arguments.get("range")
            values = arguments.get("values")
            
            success = write_spreadsheet(spreadsheet_id, range_name, values)
            if success:
                return TextContent(
                    type="text",
                    text="✅ データの書き込みが完了しました"
                )
            else:
                return TextContent(
                    type="text",
                    text="❌ データの書き込みに失敗しました"
                )
        
        elif name == "list_google_sheets":
            query = arguments.get("query", "")
            max_results = arguments.get("max_results", 10)
            files = list_spreadsheets(query, max_results)
            
            if files:
                result = []
                for file in files:
                    result.append(f"- {file['name']} ({file['id']})")
                return TextContent(
                    type="text",
                    text="\n".join(result)
                )
            else:
                return TextContent(
                    type="text",
                    text="スプレッドシートが見つかりませんでした"
                )
        
        elif name == "get_ga4_report":
            property_id = arguments.get("property_id", "505457597")
            days = arguments.get("days", 7)
            response = get_report(property_id, date_range_days=days)
            
            if response:
                data = format_report_data(response)
                return TextContent(
                    type="text",
                    text=json.dumps(data, ensure_ascii=False, indent=2)
                )
            else:
                return TextContent(
                    type="text",
                    text="エラー: レポートデータの取得に失敗しました"
                )
        
        elif name == "get_ga4_summary":
            property_id = arguments.get("property_id", "505457597")
            days = arguments.get("days", 7)
            stats = get_summary_stats(property_id, date_range_days=days)
            
            if stats:
                result = f"""📊 GA4統計（過去{stats['days']}日間）
セッション数: {stats['sessions']:,}
ページビュー数: {stats['pageviews']:,}
アクティブユーザー数: {stats['active_users']:,}
1日あたりのPV（平均）: {stats['pageviews'] / stats['days']:.1f}"""
                return TextContent(
                    type="text",
                    text=result
                )
            else:
                return TextContent(
                    type="text",
                    text="エラー: サマリー統計の取得に失敗しました"
                )
        
        else:
            return TextContent(
                type="text",
                text=f"不明なツール: {name}"
            )
    
    except Exception as e:
        return TextContent(
            type="text",
            text=f"エラー: {str(e)}"
        )


async def main():
    """メイン関数"""
    if not MCP_AVAILABLE:
        print("エラー: MCP SDKがインストールされていません", file=sys.stderr)
        print("インストール方法: pip install mcp", file=sys.stderr)
        sys.exit(1)
    
    # ツールを登録
    tools = get_tools()
    
    @server.list_tools()
    async def list_tools():
        return tools
    
    @server.call_tool()
    async def call_tool(name: str, arguments: dict):
        result = await handle_call_tool(name, arguments)
        return [result]
    
    # MCPサーバーを起動
    from mcp.server.stdio import stdio_server
    
    async with stdio_server() as (read_stream, write_stream):
        await server.run(
            read_stream,
            write_stream,
            server.create_initialization_options()
        )


if __name__ == '__main__':
    asyncio.run(main())
