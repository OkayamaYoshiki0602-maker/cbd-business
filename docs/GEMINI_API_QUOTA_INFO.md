# Gemini API クォータ情報

## 📊 現在の状況（先ほどのエラーから）

### エラーメッセージ

```
429 You exceeded your current quota, please check your plan and billing details.
Quota exceeded for metric: generativelanguage.googleapis.com/generate_content_free_tier_requests, limit: 20, model: gemini-2.5-flash
```

**意味**:
- Gemini APIの無料プランの1日20リクエスト制限に達している
- モデル: `gemini-2.5-flash`
- メトリック: `generate_content_free_tier_requests`

---

## 🔍 クォータの確認方法

### 1. ブラウザで確認

**URL**: https://ai.dev/rate-limit

このページで以下の情報を確認できます:
- 現在の使用状況
- 残りのクォータ
- リセット時刻

### 2. Google Cloud Consoleで確認

1. [Google Cloud Console](https://console.cloud.google.com/) にアクセス
2. 「APIとサービス」→「ダッシュボード」を選択
3. Gemini APIの使用状況を確認

---

## 💡 クォータ制限について

### 無料プラン（Free Tier）

- **リクエスト数**: 1日20リクエスト
- **リセット**: 24時間ごと（UTC 0時）
- **モデル**: `gemini-2.5-flash`、`gemini-2.0-flash`など

### 有料プラン

詳細は [Gemini API Pricing](https://ai.google.dev/pricing) を確認してください。

---

## 🚀 対処方法

### 1. 24時間待つ（推奨：無料プランの場合）

無料プランでは、24時間後にクォータがリセットされます。

**確認方法**:
- https://ai.dev/rate-limit でリセット時刻を確認

---

### 2. 有料プランにアップグレード

より多くのリクエストが必要な場合:
1. [Google Cloud Console](https://console.cloud.google.com/) にアクセス
2. 請求を有効化
3. Gemini APIの有料プランにアップグレード

---

### 3. リクエスト数を減らす

- ツイート生成の頻度を減らす
- バッチ処理を1日1回にする（現在の設定: 毎朝7:00）

---

## 📝 現在の使用状況

先ほどのツイート生成スクリプト実行時に:
- 10件のツイート案を生成しようとした
- 各ツイートで複数のAPIリクエストが必要（記事要約、ツイート生成など）
- 結果として、20リクエスト制限を超えた

---

## ✅ 次のステップ

1. **クォータを確認**: https://ai.dev/rate-limit
2. **リセット時刻を確認**: 24時間待つか、有料プランにアップグレード
3. **ツイート生成を再実行**: クォータが回復したら実行

---

## 🔗 参考リンク

- [Gemini API レート制限](https://ai.google.dev/gemini-api/docs/rate-limits)
- [Gemini API クォータ確認](https://ai.dev/rate-limit)
- [Gemini API 料金](https://ai.google.dev/pricing)
