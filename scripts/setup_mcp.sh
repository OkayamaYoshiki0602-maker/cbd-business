#!/bin/bash
# MCP設定ファイルを自動生成・更新するスクリプト

MCP_SETTINGS_DIR="$HOME/Library/Application Support/Cursor/User/globalStorage/saoudrizwan.claude-dev/settings"
MCP_SETTINGS_FILE="$MCP_SETTINGS_DIR/cline_mcp_settings.json"
GOOGLE_CREDENTIALS_DIR="$HOME/.config/cursor"
GOOGLE_CREDENTIALS_FILE="$GOOGLE_CREDENTIALS_DIR/google-drive-credentials.json"

# ディレクトリが存在しない場合は作成
mkdir -p "$MCP_SETTINGS_DIR"
mkdir -p "$GOOGLE_CREDENTIALS_DIR"

echo "MCP設定ファイルの場所: $MCP_SETTINGS_FILE"
echo "Google Drive認証情報の場所: $GOOGLE_CREDENTIALS_FILE"
echo ""

# 既存の設定ファイルがあるか確認
if [ -f "$MCP_SETTINGS_FILE" ]; then
    echo "既存のMCP設定ファイルが見つかりました。"
    echo "現在の設定内容:"
    cat "$MCP_SETTINGS_FILE" | python3 -m json.tool 2>/dev/null || cat "$MCP_SETTINGS_FILE"
    echo ""
    echo "このファイルをバックアップしますか？ (y/n)"
    read -r response
    if [[ "$response" =~ ^[Yy]$ ]]; then
        cp "$MCP_SETTINGS_FILE" "$MCP_SETTINGS_FILE.backup.$(date +%Y%m%d_%H%M%S)"
        echo "バックアップを作成しました。"
    fi
else
    echo "MCP設定ファイルが見つかりませんでした。新規作成します。"
fi

echo ""
echo "GitHub Personal Access Token (PAT) を入力してください:"
echo "(入力したくない場合は Enter を押してスキップ)"
read -r GITHUB_TOKEN

echo ""
echo "Google Drive認証情報ファイルのパスを入力してください:"
echo "(デフォルト: $GOOGLE_CREDENTIALS_FILE)"
echo "(Enter を押すとデフォルトを使用、スキップする場合は 'skip' と入力)"
read -r GOOGLE_CREDENTIALS_PATH

if [ -z "$GOOGLE_CREDENTIALS_PATH" ]; then
    GOOGLE_CREDENTIALS_PATH="$GOOGLE_CREDENTIALS_FILE"
elif [ "$GOOGLE_CREDENTIALS_PATH" = "skip" ]; then
    GOOGLE_CREDENTIALS_PATH=""
fi

# JSON設定を生成
cat > "$MCP_SETTINGS_FILE" << EOF
{
  "mcpServers": {
EOF

if [ -n "$GITHUB_TOKEN" ]; then
    cat >> "$MCP_SETTINGS_FILE" << EOF
    "github": {
      "command": "npx",
      "args": [
        "-y",
        "@modelcontextprotocol/server-github"
      ],
      "env": {
        "GITHUB_TOKEN": "$GITHUB_TOKEN"
      }
    }$(if [ -n "$GOOGLE_CREDENTIALS_PATH" ]; then echo ","; fi)
EOF
fi

if [ -n "$GOOGLE_CREDENTIALS_PATH" ]; then
    cat >> "$MCP_SETTINGS_FILE" << EOF
    "google-drive": {
      "command": "npx",
      "args": [
        "-y",
        "@modelcontextprotocol/server-google-drive"
      ],
      "env": {
        "GOOGLE_DRIVE_CREDENTIALS": "$GOOGLE_CREDENTIALS_PATH"
      }
    }
EOF
fi

cat >> "$MCP_SETTINGS_FILE" << EOF
  }
}
EOF

echo ""
echo "✅ MCP設定ファイルを更新しました: $MCP_SETTINGS_FILE"
echo ""
echo "設定内容:"
cat "$MCP_SETTINGS_FILE" | python3 -m json.tool 2>/dev/null || cat "$MCP_SETTINGS_FILE"
echo ""
echo "⚠️  重要: Cursorを再起動してください。"
echo "設定が反映されない場合は、Cursorを完全に終了（Cmd+Q）してから再起動してください。"
