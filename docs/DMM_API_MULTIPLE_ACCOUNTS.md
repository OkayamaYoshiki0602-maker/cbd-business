# DMM APIの複数アカウント運用について

## 🤔 同じAPI IDで複数アカウントを使えるか？

### ✅ 結論: 同じAPI IDを使用可能

**理由**:
1. **API IDは開発者単位で発行される**
   - API IDは「デベロッパー」（開発者）に対して発行されるもの
   - 1つのAPI IDで複数のアプリケーション（サイト/アカウント）を運営可能

2. **サイト追加申請は別途必要**
   - 動画アカウント: `https://twitter.com/otonasan_review`
   - 漫画アカウント: `https://twitter.com/[漫画アカウント名]`
   - それぞれ別々にサイト追加申請が必要

3. **アフィリエイトIDも共通**
   - アフィリエイトIDはアカウント単位（開発者単位）
   - 複数のサイト/アカウントで同じアフィリエイトIDを使用

---

## 📋 運用パターン

### パターン1: 同じAPI IDを使用（推奨）✅

```
API ID: [1つ]
アフィリエイトID: [1つ]
↓
動画アカウント (@otonasan_review)
漫画アカウント (@[漫画アカウント名])
```

**メリット**:
- 管理が簡単
- 環境変数が1セットで済む
- コードがシンプル

**注意点**:
- 各サイトをサイト追加申請で登録する必要がある
- ただし、API呼び出し時は同じAPI IDを使用

---

### パターン2: 別々のAPI IDを使用（非推奨）

通常は不要。同じ開発者が複数のサイトを運営する場合は、1つのAPI IDで十分。

---

## 💡 実装方法

### .envファイルの設定

```env
# DMM API認証情報（共通）
DMM_API_ID=your_api_id_here
DMM_AFFILIATE_ID=your_affiliate_id_here

# Twitter認証情報（動画アカウント）
X_API_KEY=...
X_API_SECRET_KEY=...
X_ACCESS_TOKEN=...
X_ACCESS_TOKEN_SECRET=...
X_BEARER_TOKEN=...

# Twitter認証情報（漫画アカウント）- 別途作成する場合
X_API_KEY_COMIC=...
X_API_SECRET_KEY_COMIC=...
X_ACCESS_TOKEN_COMIC=...
X_ACCESS_TOKEN_SECRET_COMIC=...
X_BEARER_TOKEN_COMIC=...
```

### コードでの使い分け

現在の実装では、`adult_twitter_generator.py`の`account_type`パラメータで使い分け:

```python
# 動画アカウント用
generator = AdultTwitterGenerator(account_type='video')
tweet_data = generator.generate_video_tweet(product)

# 漫画アカウント用
generator = AdultTwitterGenerator(account_type='comic')
tweet_data = generator.generate_comic_tweet(product)
```

---

## ⚠️ 注意事項

1. **サイト追加申請は必須**
   - 動画アカウントと漫画アカウント、それぞれをサイト追加申請で登録
   - API ID取得前にサイト追加申請が必要

2. **規約遵守**
   - 各サイトで規約を遵守
   - アフィリエイトリンクは正しく設定

3. **トラッキング**
   - 同じアフィリエイトIDを使用するため、DMM側での区別はサイトURLで行われる
   - 各サイトの成果は個別にトラッキング可能

---

**結論**: 同じAPI IDとアフィリエイトIDを使用して、動画・漫画の両アカウントを運営できます。
