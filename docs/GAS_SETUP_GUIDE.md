# Google Apps Script 設定ガイド（コピー＆ペースト用）

## 📋 概要

Google Apps Scriptに貼り付ける**正確なコード**をまとめました。

---

## 🚀 Step 1: Google Apps Script エディタを開く

1. **スプレッドシートを開く:**
   https://docs.google.com/spreadsheets/d/1-2L6C3NpF8vqnXxHWKP-Js3TMFKYE73tTtxdkZVPTaM/edit

2. **「拡張機能」→「Apps Script」を選択**

3. Apps Script エディタが開きます

---

## 📋 Step 2: コードをコピー＆ペースト

### 以下のコードをすべてコピーして、Apps Script エディタに貼り付け

**注意:** `SETUP_CHECKLIST.md` ではなく、**以下のコード**を貼り付けてください。

---

## ✅ コピー＆ペースト用コード（完全版）

```javascript
/**
 * Google Apps Script: スプレッドシート編集検知トリガー
 * 
 * 使用方法:
 * 1. 承認待ちリスト用スプレッドシートを開く
 * 2. 「拡張機能」→「Apps Script」を選択
 * 3. このスクリプトをコピー＆ペースト
 * 4. Webhook URLを設定（Zapier、Make、または独自API）
 * 5. 「保存」して「実行」→「承認を確認」
 */

// 設定
const CONFIG = {
  // Webhook URL（Zapier推奨）
  // Zapierで「Webhooks by Zapier」→「Catch Hook」を作成し、URLをコピー
  WEBHOOK_URL: 'https://hooks.zapier.com/hooks/catch/25995545/ug3pexl/',
  
  // または、独自APIエンドポイント（Google Cloud Functions、AWS Lambdaなど）
  // API_ENDPOINT: 'https://your-api-endpoint.com/api/approve-tweet',
  
  // ステータス設定
  APPROVED_STATUS: '承認済み',
  POSTED_STATUS: '投稿済み',
  
  // 列番号（A列=1, B列=2, ...）
  TIMESTAMP_COLUMN: 1,      // A列: タイムスタンプ
  STATUS_COLUMN: 2,         // B列: ステータス
  TITLE_COLUMN: 3,          // C列: 記事タイトル
  TWEET_TEXT_COLUMN: 4,     // D列: ツイート文案
  URL_COLUMN: 5,            // E列: 記事URL
  SOURCE_COLUMN: 6,         // F列: ソース
};

/**
 * スプレッドシートの編集を検知
 * 
 * トリガー: onEdit
 */
function onEdit(e) {
  try {
    const sheet = e.source.getActiveSheet();
    const range = e.range;
    const row = range.getRow();
    const col = range.getColumn();
    
    // ヘッダー行は無視
    if (row === 1) {
      return;
    }
    
    // ステータス列（B列）が編集された場合のみ処理
    if (col === CONFIG.STATUS_COLUMN) {
      const status = sheet.getRange(row, col).getValue();
      
      // 承認済みの場合
      if (status === CONFIG.APPROVED_STATUS) {
        handleApprovedTweet(sheet, row);
      }
    }
  } catch (error) {
    Logger.log(`❌ エラー: ${error.message}`);
    // エラーを通知（LINEなど）
    sendErrorNotification(error.message);
  }
}

/**
 * 承認済みツイートを処理
 */
function handleApprovedTweet(sheet, row) {
  try {
    // ツイート情報を取得
    const tweetText = sheet.getRange(row, CONFIG.TWEET_TEXT_COLUMN).getValue();
    const title = sheet.getRange(row, CONFIG.TITLE_COLUMN).getValue();
    const url = sheet.getRange(row, CONFIG.URL_COLUMN).getValue();
    const source = sheet.getRange(row, CONFIG.SOURCE_COLUMN).getValue();
    
    if (!tweetText) {
      Logger.log(`⚠️ 行${row}: ツイート文案が空です`);
      return;
    }
    
    Logger.log(`📝 承認済みツイートを検知: 行${row}, ${title}`);
    
    // Webhookを呼び出してツイート投稿を実行
    const success = callWebhookForTweetPosting(row, tweetText, title, url, source);
    
    if (success) {
      // ステータスを「投稿済み」に更新
      sheet.getRange(row, CONFIG.STATUS_COLUMN).setValue(CONFIG.POSTED_STATUS);
      Logger.log(`✅ ツイート投稿完了: 行${row}`);
    } else {
      Logger.log(`❌ ツイート投稿失敗: 行${row}`);
    }
  } catch (error) {
    Logger.log(`❌ エラー: ${error.message}`);
    sendErrorNotification(`行${row}の処理中にエラー: ${error.message}`);
  }
}

/**
 * Webhookを呼び出してツイート投稿を実行
 */
function callWebhookForTweetPosting(row, tweetText, title, url, source) {
  try {
    const payload = {
      row: row,
      tweet_text: tweetText,
      title: title,
      url: url,
      source: source,
      action: 'approve',
      timestamp: new Date().toISOString(),
      spreadsheet_id: SpreadsheetApp.getActiveSpreadsheet().getId()
    };
    
    const options = {
      method: 'post',
      contentType: 'application/json',
      payload: JSON.stringify(payload),
      muteHttpExceptions: true
    };
    
    const response = UrlFetchApp.fetch(CONFIG.WEBHOOK_URL, options);
    const responseCode = response.getResponseCode();
    const responseText = response.getContentText();
    
    Logger.log(`Webhookレスポンス: ${responseCode}, ${responseText}`);
    
    if (responseCode === 200) {
      return true;
    } else {
      Logger.log(`⚠️ Webhook呼び出し失敗: ${responseCode}, ${responseText}`);
      return false;
    }
  } catch (error) {
    Logger.log(`❌ Webhook呼び出しエラー: ${error.message}`);
    return false;
  }
}

/**
 * エラー通知（オプション）
 */
function sendErrorNotification(errorMessage) {
  // LINE通知など、エラーを通知する処理を追加
  // 現時点ではログに記録のみ
  Logger.log(`⚠️ エラー通知: ${errorMessage}`);
}

/**
 * 手動テスト用関数
 */
function testApprovedTweet() {
  const sheet = SpreadsheetApp.getActiveSheet();
  const testRow = 2; // テスト用の行番号
  
  // ステータスを「承認済み」に設定
  sheet.getRange(testRow, CONFIG.STATUS_COLUMN).setValue(CONFIG.APPROVED_STATUS);
  
  Logger.log('テスト実行: 行2のステータスを「承認済み」に設定しました');
}
```

---

## ✅ Step 3: ファイルを保存

1. **ファイルを保存**（Ctrl+S / Cmd+S）
2. **プロジェクト名を設定**（オプション）: 「承認待ちツイート自動投稿」

---

## 🧪 Step 4: テスト実行

### 方法A: 手動テスト

1. **スプレッドシートを開く**
2. **2行目（B2）に「承認済み」と入力**
3. **Enterを押す**
4. **X (Twitter)でツイートを確認**

### 方法B: テスト関数を実行

1. **Apps Script エディタで「実行」→「testApprovedTweet」を選択**
2. **「実行」をクリック**
3. **実行ログを確認**（「表示」→「ログ」）

---

## ⚠️ 注意点

### 1. 正しいファイルをコピー

- ❌ **`SETUP_CHECKLIST.md`** - これは設定手順のチェックリスト（GASコードではない）
- ✅ **`automation/google_services/google_sheets_trigger.gs`** - これがGAS用のコード

### 2. Webhook URLの確認

- 16行目の `WEBHOOK_URL` が正しく設定されているか確認
- 現在の設定: `https://hooks.zapier.com/hooks/catch/25995545/ug3pexl/`

### 3. トリガーの設定

- `onEdit` 関数は自動的にトリガーされます
- 手動でトリガーを設定する必要はありません

---

## 🆘 トラブルシューティング

### エラー: "Webhook URLが正しくありません"

**解決方法:**
1. Webhook URLが正しく設定されているか確認
2. ZapierでWebhookが正しく作成されているか確認

### エラー: "ツイートが投稿されない"

**解決方法:**
1. Zapierダッシュボードで実行履歴を確認
2. X (Twitter)アカウントの接続を確認
3. Apps Scriptの実行ログを確認

---

## 📚 参考ドキュメント

- `automation/google_services/google_sheets_trigger.gs`: 元のGASコードファイル
- `docs/ZAPIER_WEBHOOK_CONFIGURED.md`: Zapier Webhook設定完了ガイド
- `docs/GOOGLE_APPS_SCRIPT_TRIGGER.md`: GASトリガー実装ガイド

---

**結論: SETUP_CHECKLIST.mdは設定手順のチェックリストです。GASに貼り付けるのは、上記のJavaScriptコードです！**
