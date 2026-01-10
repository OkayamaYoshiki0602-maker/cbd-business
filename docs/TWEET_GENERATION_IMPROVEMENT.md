# ツイート生成機能の改善

## 📋 改善内容

### 1. WordPress記事の要約・見所抽出機能

**実装:**
- `automation/social_media/article_summarizer.py`
- WordPress記事の本文を取得して要約・見所を抽出

**機能:**
- 記事URLから本文を取得（BeautifulSoupを使用）
- Gemini APIで要約・見所を抽出
- 280文字以内で見所を含む要約を生成

**使用方法:**
```python
from social_media.article_summarizer import summarize_article_with_highlights

summary = summarize_article_with_highlights(
    article_url,
    article_title,
    max_length=200
)
```

---

### 2. ニュース収集期間の拡張（直近1か月）

**実装:**
- `automation/social_media/news_collector.py`
- `collect_cbd_news`関数に`days`パラメータを追加

**変更内容:**
- 以前: 過去24時間のニュースのみ
- 現在: 直近30日間のニュースを取得可能

**使用方法:**
```python
from social_media.news_collector import collect_cbd_news

# 直近30日間のニュースを取得
cbd_news = collect_cbd_news(days=30, max_articles=10)
```

---

### 3. ニュース要約ロジックの改善（AI活用版）

**実装:**
- `automation/social_media/news_tweet_generator.py`
- AIを使用してニュース型ツイートを生成

**要件:**
- **正確な情報**を提供
- **意外性**や**知られざる情報**を強調
- **CBDや大麻成分の効果、研究結果**を含める
- **大麻による社会への影響（政治、経済など）**を含める
- 数字や具体的な情報を含める
- 日本の人々が興味を持ちそうな内容

**使用方法:**
```python
from social_media.news_tweet_generator import generate_news_tweet_with_ai

tweet = generate_news_tweet_with_ai(
    news_title,
    news_content,
    news_url,
    max_length=280
)
```

---

### 4. URL短縮機能

**実装:**
- `automation/social_media/url_shortener.py`
- URLを短縮してツイートに使用

**機能:**
- Bitly API対応（オプション）
- 簡易的なURL短縮（表示用）

**注意:**
- Twitter (X)では、実際のURLの長さに関わらず、URLは23文字としてカウントされます
- ただし、表示上は短縮URLを使用することで、ツイートの見た目をすっきりさせられます

**使用方法:**
```python
from social_media.url_shortener import shorten_url

short_url = shorten_url(url, use_service='auto')
```

---

### 5. ツイート生成ロジックの改善

**実装:**
- `automation/social_media/article_detector.py`
- `generate_tweet_text`関数を改善

**改善内容:**
- WordPress記事の本文を取得して要約・見所を抽出
- URL短縮対応
- 280文字以内で要約・見所を含むツイート文案を生成

---

## 📊 ワークフロー（改善後）

### パターン1: WordPress新着記事の場合

1. **WordPress RSSフィードから新着記事を取得**
2. **記事URLから本文を取得**（BeautifulSoup）
3. **Gemini APIで要約・見所を抽出**
4. **URLを短縮**
5. **280文字以内でツイート文案を生成**
   - タイトル
   - 要約・見所
   - 短縮URL
   - ハッシュタグ

---

### パターン2: CBD・大麻関連ニュースの場合

1. **RSSフィードから直近1か月のニュースを収集**
2. **最新のニュースを選択**
3. **Gemini APIでツイート文案を生成**
   - 正確な情報
   - 意外性・知られざる情報
   - CBDや大麻成分の効果、研究結果
   - 大麻による社会への影響（政治、経済など）
4. **URLを短縮**
5. **280文字以内でツイート文案を生成**
   - ツイート本文
   - 短縮URL
   - ハッシュタグ

---

## ✅ 改善された機能

### 1. WordPress記事の要約・見所抽出

- ✅ 記事本文を取得（BeautifulSoup）
- ✅ Gemini APIで要約・見所を抽出
- ✅ 280文字以内で生成

### 2. ニュース収集期間の拡張

- ✅ 直近30日間のニュースを取得
- ✅ より多くのニュースから選択可能

### 3. ニュース要約ロジックの改善

- ✅ AIを使用してツイート文案を生成
- ✅ 意外性・効果・研究・社会への影響を考慮
- ✅ 日本の人々が興味を持ちそうな内容

### 4. URL短縮機能

- ✅ Bitly API対応（オプション）
- ✅ 簡易的なURL短縮（表示用）

---

## 🚀 使用方法

### WordPress新着記事の場合

```python
from social_media.article_detector import generate_tweet_text

tweet_text = generate_tweet_text(
    article_title,
    None,  # 要約は自動取得
    article_url
)
```

### CBD・大麻関連ニュースの場合

```python
from social_media.news_tweet_generator import generate_news_tweet_with_ai

tweet_text = generate_news_tweet_with_ai(
    news_title,
    news_content,
    news_url
)
```

---

## 📝 設定

### Bitly API（オプション）

`.env`ファイルに追加:

```env
BITLY_ACCESS_TOKEN=your_bitly_access_token
```

**取得方法:**
1. Bitlyにアクセス: https://bitly.com/
2. アカウント作成
3. APIトークンを取得
4. `.env`ファイルに設定

**注意:** Bitly APIは無料プランで利用可能です。

---

## 🧪 テスト実行

### WordPress記事の要約テスト

```bash
python3 automation/social_media/article_summarizer.py summarize "https://cbd-no-hito.com/article" "記事タイトル"
```

### ニュースツイート生成テスト

```bash
python3 automation/social_media/news_tweet_generator.py generate "ニュースタイトル" "ニュース本文..." "https://example.com"
```

### URL短縮テスト

```bash
python3 automation/social_media/url_shortener.py shorten "https://example.com/very/long/url/path"
```

---

詳細は各スクリプトのドキュメントを参照してください。
