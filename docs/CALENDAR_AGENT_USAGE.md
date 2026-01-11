# 予定・TODO管理エージェント 使い方ガイド

## 📋 概要

`calendar_agent.py`は、Googleカレンダーと連携して予定やTODOを管理し、あなたをマネージメントするエージェントです。

## 🚀 主な機能

### 1. 予定管理
- ✅ 自然言語から予定を作成（例: "今月31日の午前中"）
- ✅ 今後の予定一覧を表示
- ✅ Googleカレンダーと自動同期

### 2. TODO管理
- ✅ TODOの追加・完了・削除
- ✅ 優先度管理（high/medium/low）
- ✅ 期限設定
- ✅ ステータス管理（pending/completed）

### 3. サマリー表示
- ✅ 予定とTODOを一覧で表示
- ✅ 優先度順にソート

---

## 📖 使用方法

### 予定を追加する

```bash
# 基本的な使い方
python3 automation/calendar_agent.py add_event "会議" "今月31日の午前中"

# 説明も追加
python3 automation/calendar_agent.py add_event "会議" "今月31日の午前中" "プロジェクトの進捗確認"
```

**日時の指定方法:**
- `今月31日の午前中` → 今月31日の9:00-12:00
- `今月31日の午後` → 今月31日の13:00-17:00
- `来週の月曜日` → 来週の月曜日10:00-11:00
- `明日10時` → 明日の10:00-11:00
- `15時30分` → 今日または明日の15:30-16:30

### 予定一覧を表示する

```bash
# 今後7日間の予定（デフォルト）
python3 automation/calendar_agent.py list_events

# 今後30日間の予定
python3 automation/calendar_agent.py list_events 30
```

### TODOを追加する

```bash
# 基本的な使い方
python3 automation/calendar_agent.py add_todo "レポート作成"

# 優先度を指定（high/medium/low）
python3 automation/calendar_agent.py add_todo "レポート作成" high

# 期限も指定
python3 automation/calendar_agent.py add_todo "レポート作成" high "2026-01-15"
```

### TODO一覧を表示する

```bash
# すべてのTODO
python3 automation/calendar_agent.py list_todos

# 未完了のTODOのみ
python3 automation/calendar_agent.py list_todos pending

# 高優先度のTODOのみ
python3 automation/calendar_agent.py list_todos pending high
```

### TODOを完了にする

```bash
python3 automation/calendar_agent.py complete_todo 1
```

### TODOを削除する

```bash
python3 automation/calendar_agent.py delete_todo 1
```

### サマリーを表示する

```bash
# 今後7日間の予定とTODO（デフォルト）
python3 automation/calendar_agent.py summary

# 今後30日間の予定とTODO
python3 automation/calendar_agent.py summary 30
```

---

## 💡 使用例

### 例1: 今月31日の予定を追加

```bash
python3 automation/calendar_agent.py add_event "Geminiとカーソルの課金額を確かめる" "今月31日の午前中"
```

### 例2: 高優先度のTODOを追加

```bash
python3 automation/calendar_agent.py add_todo "月次レポート作成" high "2026-01-15"
```

### 例3: 今週の予定とTODOを確認

```bash
python3 automation/calendar_agent.py summary 7
```

---

## 🔧 技術的な詳細

### データ保存場所

- **TODOデータ**: `~/.config/cursor/todos.json`
- **予定データ**: Googleカレンダー（`primary`カレンダー）

### 自然言語解析の対応パターン

1. **日付指定**
   - `今月X日` / `X月X日`
   - `明日` / `明後日`
   - `来週のX曜日`

2. **時刻指定**
   - `X時` / `X時X分`
   - `午前` / `午後` / `夜` / `夕方`

3. **時間帯指定**
   - `午前中` → 9:00-12:00
   - `午後` → 13:00-17:00
   - `夜` / `夕方` → 18:00-21:00

---

## 🎯 今後の拡張予定

- [ ] リマインダー機能
- [ ] 定期的な予定の作成
- [ ] 予定の更新・削除機能
- [ ] より高度な自然言語解析（Gemini API連携）
- [ ] 予定の重複チェック
- [ ] カレンダー間の同期

---

## 📝 注意事項

- GoogleカレンダーAPIの認証情報が必要です（`~/.config/cursor/google-drive-credentials.json`）
- サービスアカウントにカレンダーへのアクセス権限が必要です
- TODOはローカルファイルに保存されます（Googleカレンダーとは別管理）
