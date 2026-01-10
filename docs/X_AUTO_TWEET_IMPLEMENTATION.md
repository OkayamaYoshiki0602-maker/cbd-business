# X自動ツイート機能 実装計画

## 📋 実装概要

X（旧Twitter）API v2を使用して、以下の機能を実装：
1. ツイート投稿機能
2. LINE通知連携（投稿前確認）
3. WordPress記事更新検知・自動投稿
4. スケジュール投稿機能
5. CBDニュース取得・自動投稿

---

## 🎯 Phase 1: 基本機能実装（4-5時間）

### 実装内容
1. X API v2の設定・認証
2. 基本的なツイート投稿スクリプト
3. LINE通知連携（投稿前に確認）

### 必要な準備

#### 1. X Developer Portal での設定

**手順:**
1. X Developer Portal にアクセス: https://developer.twitter.com/
2. 開発者アカウント申請（まだの場合）
3. プロジェクト・アプリを作成
4. APIキー・アクセストークンを取得
   - API Key
   - API Secret Key
   - Bearer Token
   - Access Token
   - Access Token Secret

**必要な権限:**
- Read & Write（ツイート投稿のため）

**設定手順:**
```
1. X Developer Portal にログイン
2. 「Projects & Apps」→「+ Create Project」
3. プロジェクト名を入力（例: "CBD Auto Tweet"）
4. アプリを作成
5. 「Keys and tokens」タブで以下を取得:
   - API Key
   - API Secret Key
   - Bearer Token
   - Access Token
   - Access Token Secret
6. 「User authentication settings」で以下を設定:
   - App permissions: Read and write
   - Type of App: Web App
   - Callback URL: http://localhost:3000/callback（開発用）
```

#### 2. LINE Messaging API の設定

**手順:**
1. LINE Developers にアクセス: https://developers.line.biz/
2. プロバイダー作成（まだの場合）
3. チャネル作成（Messaging API）
4. Channel Access Token を取得
5. Webhook URL を設定（開発時は不要）

**設定手順:**
```
1. LINE Developers にログイン
2. 「プロバイダー」→「新規作成」
3. 「Messaging API」チャネルを作成
4. 「Messaging API」タブで以下を取得:
   - Channel Access Token（発行ボタンをクリック）
5. 「Webhook設定」でWebhook URLを設定（開発時は不要）
```

### 実装ファイル構成

```
automation/
├── social_media/
│   ├── __init__.py
│   ├── x_twitter.py          # X API操作
│   ├── line_notify.py        # LINE通知
│   └── article_detector.py   # WordPress記事更新検知
└── requirements.txt          # 依存関係追加
```

### 技術スタック

- **X API:** `tweepy` (Python library)
- **LINE API:** `line-bot-sdk` または `requests` (直接API呼び出し)
- **RSS取得:** `feedparser`
- **スケジューラー:** `schedule` / `APScheduler`

---

## 🚀 Phase 2: 自動化機能（1-2時間）

### 実装内容
1. WordPress記事更新検知（RSS / Webhook）
2. スケジュール投稿機能
3. CBDニュース取得・自動投稿

### WordPress記事更新検知

**方法A: RSSを使用（推奨）**
- WordPressのRSSフィードを定期的にチェック
- 新しい記事を検知してツイート

**方法B: Webhookを使用**
- WordPressプラグイン「WP Webhooks」を使用
- 記事公開時にWebhookを送信

### スケジュール投稿機能

**実装方法:**
- Googleカレンダーと連携（既存実装を活用）
- スケジュールされた予定を検知してツイート

---

## 🎨 Phase 3: 最適化（1-2時間）

### 実装内容
1. 投稿タイミング最適化（GA4データ活用）
2. エンゲージメント分析
3. A/Bテスト機能

---

## 📝 実装ステップ

### Step 1: 依存関係の追加

`automation/requirements.txt` に以下を追加:
```
tweepy>=4.14.0
feedparser>=6.0.10
schedule>=1.2.0
requests>=2.31.0
```

### Step 2: X API操作スクリプトの作成

`automation/social_media/x_twitter.py` を作成:
- ツイート投稿機能
- メディアアップロード機能
- スレッド投稿機能

### Step 3: LINE通知スクリプトの作成

`automation/social_media/line_notify.py` を作成:
- LINE通知送信機能
- 投稿前確認機能

### Step 4: WordPress記事更新検知スクリプトの作成

`automation/social_media/article_detector.py` を作成:
- RSS取得・解析
- 新着記事検知
- ツイート文案生成

---

## 🔐 セキュリティ

### 認証情報の管理

**方法A: 環境変数を使用（推奨）**
```bash
# .env ファイルに保存（.gitignoreに追加）
X_API_KEY=your_api_key
X_API_SECRET_KEY=your_api_secret_key
X_ACCESS_TOKEN=your_access_token
X_ACCESS_TOKEN_SECRET=your_access_token_secret
LINE_CHANNEL_ACCESS_TOKEN=your_line_token
```

**方法B: 設定ファイルを使用**
- `config/credentials/x_twitter.json` に保存
- `.gitignore` に追加してGit管理から除外

---

## 📊 使用方法

### 基本的なツイート投稿

```bash
python3 automation/social_media/x_twitter.py tweet "ツイート内容"
```

### WordPress記事更新検知・自動投稿

```bash
python3 automation/social_media/article_detector.py check-and-tweet
```

### スケジュール投稿

```bash
python3 automation/social_media/x_twitter.py schedule "ツイート内容" "2025-01-11 16:00:00"
```

---

## ⚠️ 注意事項

### X APIの制限
- **Free Tier:** 1,500ツイート/月
- **Basic Tier:** 3,000ツイート/月
- **Pro Tier:** 300,000ツイート/月

### レート制限
- **投稿:** 300ツイート/3時間（ユーザーアカウント単位）
- **メディアアップロード:** 350アップロード/15分

### ベストプラクティス
1. 過度な自動投稿を避ける
2. 投稿前にLINE通知で確認
3. スパムとみなされないよう間隔を空ける
4. エンゲージメントを優先した投稿内容

---

## 🚀 次のステップ

1. **X Developer Portal での設定完了を確認**
2. **LINE Messaging API の設定完了を確認**
3. **実装開始**

---

## 📝 実装チェックリスト

- [ ] X Developer Portal での設定完了
- [ ] LINE Messaging API の設定完了
- [ ] 依存関係のインストール
- [ ] X API操作スクリプトの作成
- [ ] LINE通知スクリプトの作成
- [ ] WordPress記事更新検知スクリプトの作成
- [ ] テスト実行
- [ ] エラーハンドリング実装
- [ ] ドキュメント更新
