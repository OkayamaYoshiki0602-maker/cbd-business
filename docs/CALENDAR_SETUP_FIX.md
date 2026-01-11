# Googleカレンダー予定が表示されない問題の解決方法

## 🔍 問題の原因

サービスアカウント（`cursor-mcp@acoustic-skein-329303.iam.gserviceaccount.com`）で作成したイベントが、サービスアカウント自身のカレンダーに作成されており、ユーザーの個人カレンダー（`okayamayoshiki0602o@gmail.com`）には表示されていません。

---

## ✅ 解決方法

### ステップ1: Googleカレンダーでカレンダーを共有する

1. **Googleカレンダーにアクセス**
   - https://calendar.google.com にアクセス
   - `okayamayoshiki0602o@gmail.com` でログイン

2. **左側の「マイカレンダー」からカレンダーを選択**
   - 「岡山純樹」カレンダー（または使用したいカレンダー）をクリック
   - カレンダー名の右側にある「⋮」（三点リーダー）をクリック

3. **「設定と共有」をクリック**

4. **「特定のユーザーと共有」セクションに移動**
   - 画面を下にスクロール

5. **「ユーザーを追加」をクリック**

6. **サービスアカウントのメールアドレスを入力**
   ```
   cursor-mcp@acoustic-skein-329303.iam.gserviceaccount.com
   ```

7. **権限を選択**
   - **「変更可能なイベントを表示」** を選択（推奨）
   - または「変更と共有の権限を管理」を選択

8. **「送信」をクリック**

### ステップ2: カレンダーIDを確認する

共有設定後、カレンダーIDを確認します：

1. **カレンダーの設定画面で「カレンダーの統合」セクションを確認**
   - 「カレンダーID」が表示されます
   - 通常は `okayamayoshiki0602o@gmail.com` または別のID

2. **または、スクリプトで確認**
   ```bash
   python3 automation/google_services/google_calendar.py calendars
   ```

### ステップ3: 正しいカレンダーIDで予定を作成

カレンダーを共有した後、エージェントが自動的に正しいカレンダーIDを使用します：

```bash
# 予定を追加（自動的にユーザーのカレンダーに作成されます）
python3 automation/calendar_agent.py add_event "Geminiとカーソルの課金額を確かめる" "今月31日の午前中"
```

---

## 🔧 手動でカレンダーIDを指定する場合

もし自動検出がうまくいかない場合は、カレンダーIDを明示的に指定できます：

```python
from automation.calendar_agent import CalendarAgent

# カレンダーIDを指定
agent = CalendarAgent(calendar_id='okayamayoshiki0602o@gmail.com')
agent.add_event("会議", "今月31日の午前中")
```

---

## 📝 確認方法

### 1. Googleカレンダーで確認
- https://calendar.google.com にアクセス
- 1月31日の午前中に予定が表示されているか確認

### 2. スクリプトで確認
```bash
# 今後30日間の予定を表示
python3 automation/calendar_agent.py list_events 30
```

---

## ⚠️ 注意事項

1. **共有設定が必要**
   - サービスアカウントがユーザーのカレンダーにアクセスするには、必ずカレンダーの共有設定が必要です
   - 共有設定をしないと、サービスアカウント自身のカレンダーに予定が作成されます

2. **権限の選択**
   - 「変更可能なイベントを表示」: 予定の作成・編集・削除が可能
   - 「変更と共有の権限を管理」: 上記に加えて、カレンダーの共有設定も変更可能

3. **複数のカレンダーがある場合**
   - 使用したいカレンダーごとに共有設定を行う必要があります
   - 「岡山純樹」「ToDoリスト」など、それぞれのカレンダーに共有設定を追加してください

---

## 🎯 次のステップ

1. ✅ カレンダーの共有設定を完了
2. ✅ 予定を作成して確認
3. ✅ タイムツリーで同期を確認（タイムツリーとGoogleカレンダーを連携している場合）

---

## 📚 関連ドキュメント

- [Googleサービス権限設定手順](GOOGLE_SERVICES_PERMISSIONS.md)
- [タイムツリーとGoogleカレンダーの連携方法](TIMETREE_GOOGLE_CALENDAR_SYNC.md)
- [予定・TODO管理エージェント使い方](CALENDAR_AGENT_USAGE.md)
