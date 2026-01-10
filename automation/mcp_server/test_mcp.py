#!/usr/bin/env python3
"""
MCPサーバーのテストスクリプト
"""

import sys
import json
import subprocess
from pathlib import Path

SCRIPT_DIR = Path(__file__).parent
MCP_SERVER = SCRIPT_DIR / "google_services_mcp.py"

def test_mcp_server():
    """MCPサーバーをテスト"""
    print("🧪 MCPサーバーのテストを開始...")
    
    # テスト1: 初期化メッセージ
    print("\n1. 初期化メッセージのテスト")
    request = {
        "jsonrpc": "2.0",
        "method": "initialize",
        "params": {},
        "id": 1
    }
    
    try:
        result = subprocess.run(
            ["python3", str(MCP_SERVER)],
            input=json.dumps(request) + "\n",
            capture_output=True,
            text=True,
            timeout=5
        )
        
        if result.returncode == 0:
            print("✅ 初期化成功")
            if result.stdout:
                print(f"出力: {result.stdout[:200]}")
        else:
            print(f"❌ エラー: {result.stderr[:500]}")
    except Exception as e:
        print(f"❌ エラー: {e}")
    
    # テスト2: ツール一覧取得
    print("\n2. ツール一覧取得のテスト")
    request = {
        "jsonrpc": "2.0",
        "method": "tools/list",
        "params": {},
        "id": 2
    }
    
    try:
        result = subprocess.run(
            ["python3", str(MCP_SERVER)],
            input=json.dumps(request) + "\n",
            capture_output=True,
            text=True,
            timeout=5
        )
        
        if result.returncode == 0:
            print("✅ ツール一覧取得成功")
            if result.stdout:
                print(f"出力: {result.stdout[:200]}")
        else:
            print(f"❌ エラー: {result.stderr[:500]}")
    except Exception as e:
        print(f"❌ エラー: {e}")
    
    print("\n✅ テスト完了")

if __name__ == '__main__':
    test_mcp_server()
