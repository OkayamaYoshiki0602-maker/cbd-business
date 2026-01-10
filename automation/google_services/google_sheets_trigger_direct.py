"""
Google Apps Script用: 直接X APIを呼び出すバージョン（代替案）

注意: この方法は、Zapierが利用できない場合の代替案です。
OAuth 1.0a署名の完全な実装が必要です。
"""

# このファイルは、Apps Scriptから直接X APIを呼び出す方法の参考例です。
# 完全な実装には、OAuth 1.0a署名ライブラリが必要です。

# Apps Scriptにコピー＆ペーストする場合のテンプレート:
"""
/**
 * Google Apps Script: スプレッドシート編集検知トリガー（直接X API呼び出し版）
 * 
 * 注意: この方法は、OAuth 1.0a署名の完全な実装が必要です。
 * 推奨: 定期実行スクリプトを使用（docs/FREE_AUTO_TWEET_SETUP.md参照）
 */

// 設定
const CONFIG = {
  // ステータス設定
  APPROVED_STATUS: '承認済み',
  POSTED_STATUS: '投稿済み',
  
  // 列番号（A列=1, B列=2, ...）
  TIMESTAMP_COLUMN: 1,
  STATUS_COLUMN: 2,
  TITLE_COLUMN: 3,
  TWEET_TEXT_COLUMN: 4,
  URL_COLUMN: 5,
  SOURCE_COLUMN: 6,
};

/**
 * スプレッドシートの編集を検知
 */
function onEdit(e) {
  try {
    const sheet = e.source.getActiveSheet();
    const range = e.range;
    const row = range.getRow();
    const col = range.getColumn();
    
    if (row === 1) {
      return;
    }
    
    if (col === CONFIG.STATUS_COLUMN) {
      const status = sheet.getRange(row, col).getValue();
      
      if (status === CONFIG.APPROVED_STATUS) {
        handleApprovedTweet(sheet, row);
      }
    }
  } catch (error) {
    Logger.log(`❌ エラー: ${error.message}`);
  }
}

/**
 * 承認済みツイートを処理
 */
function handleApprovedTweet(sheet, row) {
  try {
    const tweetText = sheet.getRange(row, CONFIG.TWEET_TEXT_COLUMN).getValue();
    const title = sheet.getRange(row, CONFIG.TITLE_COLUMN).getValue();
    
    if (!tweetText) {
      Logger.log(`⚠️ 行${row}: ツイート文案が空です`);
      return;
    }
    
    Logger.log(`📝 承認済みツイートを検知: 行${row}, ${title}`);
    
    // 注意: OAuth 1.0a署名の完全な実装が必要です
    // 推奨: 定期実行スクリプトを使用（docs/FREE_AUTO_TWEET_SETUP.md参照）
    const success = postTweetDirectly(tweetText);
    
    if (success) {
      sheet.getRange(row, CONFIG.STATUS_COLUMN).setValue(CONFIG.POSTED_STATUS);
      Logger.log(`✅ ツイート投稿完了: 行${row}`);
    } else {
      Logger.log(`❌ ツイート投稿失敗: 行${row}`);
    }
  } catch (error) {
    Logger.log(`❌ エラー: ${error.message}`);
  }
}

/**
 * X APIに直接投稿
 * 
 * 注意: OAuth 1.0a署名の完全な実装が必要です。
 * 簡易版は動作しない可能性があります。
 * 推奨: 定期実行スクリプトを使用（docs/FREE_AUTO_TWEET_SETUP.md参照）
 */
function postTweetDirectly(tweetText) {
  try {
    // X API認証情報（スクリプトプロパティに保存推奨）
    const apiKey = PropertiesService.getScriptProperties().getProperty('X_API_KEY');
    const apiSecret = PropertiesService.getScriptProperties().getProperty('X_API_SECRET_KEY');
    const accessToken = PropertiesService.getScriptProperties().getProperty('X_ACCESS_TOKEN');
    const accessTokenSecret = PropertiesService.getScriptProperties().getProperty('X_ACCESS_TOKEN_SECRET');
    
    if (!apiKey || !apiSecret || !accessToken || !accessTokenSecret) {
      Logger.log('⚠️ X API認証情報が設定されていません');
      return false;
    }
    
    // OAuth 1.0a署名を生成（完全な実装が必要）
    // 注意: この簡易版は動作しない可能性があります
    const url = 'https://api.twitter.com/2/tweets';
    
    const payload = {
      text: tweetText
    };
    
    // 注意: OAuth 1.0a署名ライブラリを使用する必要があります
    // この簡易版は動作しない可能性があります
    const options = {
      method: 'post',
      contentType: 'application/json',
      headers: {
        'Authorization': 'Bearer ' + accessToken  // 簡易版（実際にはOAuth 1.0aが必要）
      },
      payload: JSON.stringify(payload)
    };
    
    const response = UrlFetchApp.fetch(url, options);
    const responseCode = response.getResponseCode();
    
    Logger.log(`X APIレスポンス: ${responseCode}, ${response.getContentText()}`);
    
    return responseCode === 201;
  } catch (error) {
    Logger.log(`❌ X API呼び出しエラー: ${error.message}`);
    return false;
  }
}
"""
