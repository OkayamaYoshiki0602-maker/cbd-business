# 承認フロー実装ガイド

## 📋 概要

希望する流れを実現するための承認フローシステム：

```
1. Cursorでニュース作成 or 記事作成
   ↓
2. 作成したタイミングでLINE通知
   ↓
3. ユーザーが確認してOKする（スプレッドシートで承認）
   ↓
4. OKしたらツイート投稿
```

---

## 🚀 実装内容

### 1. 記事作成検知スクリプト

`automation/social_media/article_detector.py`

**機能:**
- WordPress RSSフィードをチェックして新着記事を検知
- 手動でツイート投稿リクエストを作成
- ツイート文案を自動生成
- LINE通知でプレビュー送信
- 承認待ちリストに追加

**使用方法:**
```bash
# WordPress RSSフィードをチェック
python3 automation/social_media/article_detector.py check

# 手動でツイート投稿リクエストを作成
python3 automation/social_media/article_detector.py manual "記事タイトル" "ツイート文案" "記事URL"
```

---

### 2. 承認待ちリスト管理スクリプト

`automation/social_media/approval_manager.py`

**機能:**
- 承認待ちリストを表示
- 承認待ちを承認済みに変更
- 承認済みリストを表示

**使用方法:**
```bash
# 承認待ちリストを表示
python3 automation/social_media/approval_manager.py list

# 承認待ちを承認済みに変更（行番号を指定）
python3 automation/social_media/approval_manager.py approve 2

# 承認済みリストを表示
python3 automation/social_media/approval_manager.py approved
```

---

### 3. 承認済みツイート投稿スクリプト

`automation/social_media/approve_tweet.py`

**機能:**
- 承認済みツイートを取得
- ツイートを投稿
- 投稿結果をLINEで通知
- ステータスを「投稿済み」に更新

**使用方法:**
```bash
# 承認済みツイートを投稿
python3 automation/social_media/approve_tweet.py

# 投稿待ちの承認済みツイートを表示
python3 automation/social_media/approve_tweet.py list
```

---

## 📝 スプレッドシート設定

### 承認待ちリストスプレッドシートの作成

1. Googleスプレッドシートで新しいシートを作成
2. シート名を「承認待ちリスト」に設定
3. 以下のヘッダー行を設定：

| タイムスタンプ | ステータス | 記事タイトル | ツイート文案 | 記事URL | ソース |
|--------------|-----------|------------|------------|---------|--------|
| 2025-01-11T... | 承認待ち | CBDとは？ | CBDについて解説します... | https://... | wordpress |

4. スプレッドシートIDを`.env`ファイルに設定：

```env
APPROVAL_SPREADSHEET_ID=スプレッドシートID
```

---

## 🔄 ワークフロー

### 基本的な流れ

```
1. 記事作成 or 手動実行
   ↓
2. article_detector.py を実行
   ↓
3. ツイート文案を生成
   ↓
4. LINE通知でプレビュー送信
   ↓
5. スプレッドシートに承認待ちとして記録
   ↓
6. ユーザーがスプレッドシートで確認
   ↓
7. 承認待ちを承認済みに変更（手動またはapproval_manager.py）
   ↓
8. approve_tweet.py を実行
   ↓
9. ツイート投稿
   ↓
10. LINE通知で結果を送信
```

---

## 📋 使用方法

### Step 1: 記事作成検知・LINE通知

```bash
# WordPress RSSフィードをチェック
python3 automation/social_media/article_detector.py check
```

**動作:**
1. WordPress RSSフィードをチェック
2. 新着記事を検知
3. ツイート文案を自動生成
4. LINE通知でプレビュー送信
5. スプレッドシートに承認待ちとして記録

### Step 2: 手動でツイート投稿リクエストを作成

```bash
# 手動でツイート投稿リクエストを作成
python3 automation/social_media/article_detector.py manual "CBDとは？" "CBDについて解説します #CBD" "https://cbd-no-hito.com/article"
```

**動作:**
1. ツイート文案を生成（または指定）
2. LINE通知でプレビュー送信
3. スプレッドシートに承認待ちとして記録

### Step 3: 承認待ちリストを確認

```bash
# 承認待ちリストを表示
python3 automation/social_media/approval_manager.py list
```

**出力例:**
```
📋 承認待ちリスト（1件）:
============================================================

行2: CBDとは？
  ツイート文案: CBDについて解説します...
  URL: https://cbd-no-hito.com/article
  ソース: wordpress
  タイムスタンプ: 2025-01-11T12:00:00
```

### Step 4: 承認

**方法A: スプレッドシートで手動承認**

1. スプレッドシートを開く
2. 「ステータス」列を「承認済み」に変更

**方法B: コマンドで承認**

```bash
# 行番号を指定して承認
python3 automation/social_media/approval_manager.py approve 2
```

### Step 5: 承認済みツイートを投稿

```bash
# 承認済みツイートを投稿
python3 automation/social_media/approve_tweet.py
```

**動作:**
1. 承認済みツイートを取得
2. ツイートを投稿
3. LINE通知で結果を送信
4. ステータスを「投稿済み」に更新

---

## 🎯 完全なワークフロー例

### 例1: WordPress記事更新検知

```bash
# 1. 記事作成検知・LINE通知
python3 automation/social_media/article_detector.py check

# LINEでプレビューを確認
# → OKならスプレッドシートで承認

# 2. 承認（スプレッドシートで手動、またはコマンドで）
python3 automation/social_media/approval_manager.py approve 2

# 3. 承認済みツイートを投稿
python3 automation/social_media/approve_tweet.py
```

### 例2: 手動でツイート投稿リクエスト

```bash
# 1. 手動でツイート投稿リクエストを作成
python3 automation/social_media/article_detector.py manual "CBDニュース" "最新のCBD情報をお届けします #CBD" "https://cbd-no-hito.com/news"

# LINEでプレビューを確認
# → OKならスプレッドシートで承認

# 2. 承認
python3 automation/social_media/approval_manager.py approve 2

# 3. 承認済みツイートを投稿
python3 automation/social_media/approve_tweet.py
```

---

## 📝 .envファイル設定

`.env`ファイルに以下を追加：

```env
# 承認待ちリスト用スプレッドシートID
APPROVAL_SPREADSHEET_ID=スプレッドシートID

# WordPress設定
WORDPRESS_URL=https://cbd-no-hito.com
```

---

## 🚀 次のステップ

1. **承認待ちリスト用スプレッドシートを作成**
2. **APPROVAL_SPREADSHEET_IDを.envファイルに設定**
3. **テスト実行**

---

## 💡 将来的な拡張

### Phase 2: スプレッドシート承認フロー自動化

- 定期実行スクリプトで承認待ちリストをチェック
- 承認済みになったら自動でツイート投稿

### Phase 3: LINE Webhook承認フロー（完全自動化）

- LINEからOK返信を受け取る
- WebhookでOK返信を検知
- 自動でツイート投稿

---

このワークフローで進めますか？まずは承認待ちリスト用のスプレッドシートを作成しましょう！
