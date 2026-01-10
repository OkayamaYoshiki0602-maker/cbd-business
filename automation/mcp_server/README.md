# Google Services MCP Server

## 📋 概要

Googleサービスと連携するカスタムMCPサーバー（Phase 3）

## ⚠️ 注意事項

**現在、Python版のMCP SDKは標準では提供されていない可能性があります。**

MCPサーバーは主にNode.jsで実装されています。Python版のMCP SDKが存在しない場合、以下の代替案があります：

### 代替案1: Node.js版のMCPサーバーを作成

Node.jsでMCPサーバーを実装し、Pythonスクリプトを呼び出す方法：

```javascript
// automation/mcp_server/google_services_mcp.js
const { exec } = require('child_process');
const { Server } = require('@modelcontextprotocol/sdk/server/index.js');

const server = new Server({
  name: 'google-services-mcp',
  version: '1.0.0',
}, {
  capabilities: {
    tools: {},
  },
});

// Pythonスクリプトを呼び出す
server.setRequestHandler(ListToolsRequestSchema, async () => {
  return {
    tools: [
      {
        name: 'read_google_sheets',
        description: 'Googleスプレッドシートからデータを読み込む',
        // ...
      },
    ],
  };
});

server.setRequestHandler(CallToolRequestSchema, async (request) => {
  // Pythonスクリプトを実行
  const result = await exec(`python3 automation/google_services/google_sheets.py read ${spreadsheet_id}`);
  return result;
});
```

### 代替案2: Phase 1-2を使用（推奨）

Phase 1-2の実装で十分な機能を提供しています：

**Phase 1: Pythonスクリプト**
```bash
python3 automation/google_services/google_sheets.py read <spreadsheet_id>
python3 automation/google_services/ga4.py summary 505457597 7
```

**Phase 2: シェルスクリプト**
```bash
./scripts/google-sheets-read.sh <spreadsheet_id>
./scripts/ga4-report.sh summary 505457597 7
```

これらのスクリプトは、Cursorから実行可能です。

### 代替案3: stdio経由でMCPプロトコルを実装

PythonでMCPプロトコルを直接実装する方法（複雑ですが可能）：

- MCPプロトコルの仕様に従ってstdio経由で通信
- JSON-RPC形式でメッセージを送受信

## 🚀 推奨アプローチ

**現時点では、Phase 1-2の実装を使用することを推奨します。**

Phase 3（カスタムMCPサーバー）は、将来的に以下のいずれかで実装可能です：

1. Node.js版のMCPサーバーを作成（Pythonスクリプトを呼び出す）
2. Python版のMCP SDKが公開されたら移行
3. stdio経由でMCPプロトコルを直接実装

## 📝 参考

- [MCP公式ドキュメント](https://modelcontextprotocol.io/)
- [MCP SDK (Node.js)](https://github.com/modelcontextprotocol/sdk)
- [MCPサーバー実装例](https://github.com/modelcontextprotocol/servers)
