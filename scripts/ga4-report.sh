#!/bin/bash
# GA4レポート取得スクリプト（Phase 2）

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"

PROPERTY_ID=${1:-"505457597"}
DAYS=${2:-"7"}

if [ "$1" = "summary" ]; then
    python3 "$PROJECT_ROOT/automation/google_services/ga4.py" summary "$PROPERTY_ID" "$DAYS"
else
    python3 "$PROJECT_ROOT/automation/google_services/ga4.py" report "$PROPERTY_ID" "$DAYS"
fi
