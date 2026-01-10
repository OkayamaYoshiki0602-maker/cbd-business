# Google Apps Script トリガー実装ガイド

## 📋 概要

スプレッドシートで承認した瞬間にツイートされるようにするため、Google Apps Script (GAS) のトリガーを使用します。

---

## 🚀 実装方法

### Step 1: Google Apps Script エディタを開く

1. 承認待ちリスト用スプレッドシートを開く
2. 「拡張機能」→「Apps Script」を選択
3. Apps Script エディタが開きます

### Step 2: スクリプトを作成

以下のスクリプトをコピー＆ペースト：

```javascript
/**
 * スプレッドシートの編集を検知して承認済みツイートを投稿
 */

// 設定
const CONFIG = {
  // APIエンドポイント（Heroku、AWS Lambda、Google Cloud Functionsなど）
  API_ENDPOINT: 'https://your-api-endpoint.com/api/approve-tweet',
  
  // または、直接Webhookを呼び出す場合
  WEBHOOK_URL: 'https://hooks.slack.com/services/YOUR/WEBHOOK/URL', // 例：Slack Webhook
  
  // 承認済みステータス
  APPROVED_STATUS: '承認済み',
  
  // ステータス列（B列 = 2）
  STATUS_COLUMN: 2,
  
  // ツイート文案列（D列 = 4）
  TWEET_TEXT_COLUMN: 4,
};

/**
 * スプレッドシートの編集を検知
 */
function onEdit(e) {
  const sheet = e.source.getActiveSheet();
  const range = e.range;
  const row = range.getRow();
  const col = range.getColumn();
  
  // ヘッダー行は無視
  if (row === 1) {
    return;
  }
  
  // ステータス列が編集された場合のみ処理
  if (col === CONFIG.STATUS_COLUMN) {
    const status = sheet.getRange(row, col).getValue();
    
    // 承認済みの場合
    if (status === CONFIG.APPROVED_STATUS) {
      const tweetText = sheet.getRange(row, CONFIG.TWEET_TEXT_COLUMN).getValue();
      
      // ツイート投稿APIを呼び出す
      postTweetApproved(row, tweetText);
    }
  }
}

/**
 * 承認済みツイートを投稿
 */
function postTweetApproved(row, tweetText) {
  try {
    // APIエンドポイントを呼び出す
    const response = UrlFetchApp.fetch(CONFIG.API_ENDPOINT, {
      method: 'post',
      contentType: 'application/json',
      payload: JSON.stringify({
        row: row,
        tweet_text: tweetText,
        action: 'approve'
      }),
      muteHttpExceptions: true
    });
    
    const result = JSON.parse(response.getContentText());
    
    if (result.success) {
      // ステータスを「投稿済み」に更新
      const sheet = SpreadsheetApp.getActiveSheet();
      sheet.getRange(row, CONFIG.STATUS_COLUMN).setValue('投稿済み');
      
      Logger.log(`✅ ツイート投稿完了: Row ${row}`);
    } else {
      Logger.log(`❌ ツイート投稿失敗: ${result.error}`);
    }
  } catch (error) {
    Logger.log(`❌ エラー: ${error.message}`);
  }
}
```

### Step 3: APIエンドポイントを作成（オプション）

GASから直接X APIを呼び出す場合は、以下のように実装：

```javascript
/**
 * X APIを使用してツイート投稿（OAuth 1.0a認証が必要）
 */
function postTweetToX(tweetText) {
  // 注意: X APIはOAuth 1.0a認証が必要
  // セキュアな方法として、サーバーサイドAPIを経由することを推奨
  
  const payload = {
    text: tweetText
  };
  
  const options = {
    method: 'post',
    contentType: 'application/json',
    headers: {
      'Authorization': 'Bearer YOUR_ACCESS_TOKEN' // セキュリティ上、Properties Serviceを使用
    },
    payload: JSON.stringify(payload)
  };
  
  // X API v2を使用
  const response = UrlFetchApp.fetch('https://api.x.com/2/tweets', options);
  return JSON.parse(response.getContentText());
}
```

### Step 4: より簡単な方法：Webhookを使用

サーバー不要で実現する方法：

```javascript
/**
 * Webhookを使用して承認済みツイートを通知
 */
function postTweetApproved(row, tweetText) {
  // Zapier、IFTTT、Make (Integromat) などのWebhookサービスを使用
  
  const webhookUrl = 'https://hooks.zapier.com/hooks/catch/YOUR/WEBHOOK/ID';
  
  const payload = {
    row: row,
    tweet_text: tweetText,
    action: 'approve',
    timestamp: new Date().toISOString()
  };
  
  UrlFetchApp.fetch(webhookUrl, {
    method: 'post',
    contentType: 'application/json',
    payload: JSON.stringify(payload)
  });
}
```

---

## 💡 推奨アプローチ

### 方法A: Google Cloud Functions + GAS（推奨）

1. **Google Cloud Functions** でAPIエンドポイントを作成
2. **GASトリガー** でスプレッドシートの編集を検知
3. **Cloud Functions** でX APIを呼び出してツイート投稿

**メリット:**
- ✅ サーバーレス
- ✅ セキュア
- ✅ スケーラブル

### 方法B: Zapier / Make を使用（最も簡単）

1. **Zapier** または **Make (Integromat)** でWebhookを作成
2. **GASトリガー** でWebhookを呼び出し
3. **Zapier/Make** でX APIを呼び出してツイート投稿

**メリット:**
- ✅ サーバー不要
- ✅ コード不要（GUIで設定）
- ✅ すぐに実装可能

### 方法C: 定期実行スクリプト（現在の方法）

1. **定期実行スクリプト** で承認済みツイートを検知
2. 自動でツイート投稿

**メリット:**
- ✅ サーバー不要
- ✅ 既存実装を活用

**デメリット:**
- ⚠️ リアルタイムではない（定期実行の間隔による）

---

## 🎯 最も簡単な実装：定期実行間隔を短くする

現在の方法を改善して、承認から投稿までの待ち時間を短くする：

```python
# 定期実行間隔を短くする（例：1分ごと）
schedule.every(1).minutes.do(daily_tweet_posting_job)
```

---

## 📝 実装ステップ（方法B: Zapier推奨）

### Step 1: ZapierでWebhookを作成

1. Zapier にアクセス: https://zapier.com/
2. 「Create Zap」をクリック
3. **Trigger:** Webhooks by Zapier → Catch Hook
4. Webhook URLをコピー

### Step 2: GASスクリプトを更新

Webhook URLをGASスクリプトに設定：

```javascript
const WEBHOOK_URL = 'https://hooks.zapier.com/hooks/catch/YOUR/WEBHOOK/ID';
```

### Step 3: ZapierでX APIアクションを設定

1. **Action:** X (Twitter) → Create Tweet
2. X API認証情報を設定
3. ツイート文案をWebhookから取得して設定

---

## 🚀 次のステップ

1. **GASスクリプトを作成**
2. **Webhookサービスを設定**（Zapier推奨）
3. **テスト実行**

---

詳細は `docs/GOOGLE_APPS_SCRIPT_TRIGGER.md` を参照してください。
