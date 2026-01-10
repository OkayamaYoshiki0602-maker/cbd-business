#!/bin/bash
# Google Sheets読み込みスクリプト（Phase 2）

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"

if [ $# -lt 1 ]; then
    echo "使用方法: $0 <spreadsheet_id> [range]"
    echo ""
    echo "例:"
    echo "  $0 1BxiMVs0XRA5nFMdKvBdBZjgmUUqptlbs74OgvE2upms"
    echo "  $0 1BxiMVs0XRA5nFMdKvBdBZjgmUUqptlbs74OgvE2upms 'Sheet1!A1:D10'"
    exit 1
fi

SPREADSHEET_ID=$1
RANGE=${2:-"Sheet1!A1:Z1000"}

python3 "$PROJECT_ROOT/automation/google_services/google_sheets.py" read "$SPREADSHEET_ID" "$RANGE"
