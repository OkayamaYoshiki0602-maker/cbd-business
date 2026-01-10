# 定期実行ツイート設定ガイド

## 📋 概要

毎日決まったタイミングで自動的にツイート案を生成し、LINE通知で確認するワークフローです。

---

## 🚀 使用方法

### 1. 定期実行スクリプトの実行

#### 方法A: schedule ライブラリで実行（推奨）

```bash
# バックグラウンドで実行
python3 automation/scripts/daily_tweet_scheduler.py &
```

#### 方法B: cron で実行（macOS/Linux）

```bash
# crontabを編集
crontab -e

# 以下を追加（毎日9:00にツイート案生成、9:30に投稿）
0 9 * * * /usr/bin/python3 /path/to/automation/social_media/scheduled_tweet.py
30 9 * * * /usr/bin/python3 /path/to/automation/social_media/approve_tweet.py auto
```

#### 方法C: 手動実行

```bash
# ツイート案生成
python3 automation/social_media/scheduled_tweet.py

# 承認済みツイート投稿
python3 automation/social_media/approve_tweet.py auto
```

---

## ⚙️ 設定

### .envファイルに以下を追加

```env
# 定期実行時刻設定
TWEET_GENERATION_TIME=09:00  # ツイート案生成時刻（HH:MM形式）
TWEET_POSTING_TIME=09:30     # ツイート投稿時刻（HH:MM形式）

# 承認待ちリスト用スプレッドシートID
APPROVAL_SPREADSHEET_ID=スプレッドシートID

# WordPress設定
WORDPRESS_URL=https://cbd-no-hito.com
```

---

## 📝 ワークフロー

### 毎日 9:00（ツイート案生成）

```
1. scheduled_tweet.py が実行
   ↓
2. ツイート文案を自動生成
   ↓
3. 記事動向を要約
   ↓
4. LINE通知で送信：
   「📝 本日のツイート案
   
   [ツイート文案]
   
   📰 記事動向：
   - 新着記事: ...
   
   承認待ちリスト: [スプレッドシートURL]」
   ↓
5. スプレッドシートに「下書き」として記録
```

### 毎日 9:30（承認済みツイート投稿）

```
1. approve_tweet.py auto が実行
   ↓
2. 承認済みツイートを取得
   ↓
3. ツイート投稿
   ↓
4. LINE通知で結果を送信
   ↓
5. ステータスを「投稿済み」に更新
```

---

## 💡 承認フロー

### Step 1: LINEで確認

LINE通知でプレビューを確認

### Step 2: 承認（2つの方法）

**方法A: スプレッドシートで手動承認**

1. スプレッドシートを開く
2. 「ステータス」列を「承認済み」に変更

**方法B: コマンドで承認**

```bash
# 承認待ちリストを表示
python3 automation/social_media/approval_manager.py list

# 行番号を指定して承認
python3 automation/social_media/approval_manager.py approve 2
```

### Step 3: 自動投稿（定期実行）

承認済みツイートは、次の定期実行時刻（9:30）に自動で投稿されます。

---

## 🎯 ベストプラクティス

### 1. ツイート文案生成

- **口数少なく:** 140文字以内を推奨
- **正確な情報:** 記事内容に基づく
- **興味を引く:** 読者の関心を引く表現

### 2. 記事動向要約

- **新着記事のみ:** 過去24時間以内の記事
- **簡潔に:** 各記事を1行で要約
- **URL付き:** 記事URLを含める

### 3. 承認タイミング

- **確認後すぐ承認:** LINE通知を確認後、すぐに承認
- **承認後自動投稿:** 次の定期実行時刻（9:30）に自動投稿

---

## 📝 ステータス管理

### ステータス一覧

- **下書き:** ツイート案生成済み（承認待ち）
- **承認済み:** 承認済み（投稿待ち）
- **投稿済み:** 投稿完了

### ステータス遷移

```
下書き → 承認済み → 投稿済み
```

---

## 🆘 トラブルシューティング

### 定期実行が動かない

**確認事項:**
1. スクリプトが実行されているか確認
2. .envファイルの設定を確認
3. 時刻設定が正しいか確認

### LINE通知が届かない

**確認事項:**
1. LINE_CHANNEL_ACCESS_TOKENが設定されているか確認
2. LINE通知機能が正常に動作しているか確認

### スプレッドシートに記録されない

**確認事項:**
1. APPROVAL_SPREADSHEET_IDが設定されているか確認
2. スプレッドシートの共有設定を確認

---

## 🚀 次のステップ

1. **スプレッドシートを作成**
2. **APPROVAL_SPREADSHEET_IDを.envファイルに設定**
3. **定期実行スクリプトを開始**
4. **テスト実行**

---

この設定で進めますか？
