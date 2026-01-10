# ニュース収集・要約ツール選定ガイド

## 📋 要件

- 朝7時にCBD関連や大麻の正しいニュースを収集
- 要約してLINE通知
- 正確な情報源を優先

---

## 🔍 ニュース収集ツール

### 方法A: RSSフィード（推奨・既存実装）

**メリット:**
- ✅ サーバー不要
- ✅ 無料
- ✅ 既存実装を活用
- ✅ 正確な情報源を指定可能

**収集先（CBD・大麻関連）:**
- **Hemp Industry Daily** (https://hempindustrydaily.com/feed/)
- **Leafly** (https://www.leafly.com/news/rss)
- **Cannabis Business Times** (https://www.cannabisbusinesstimes.com/rss/)
- **Marijuana Business Daily** (https://mjbizdaily.com/feed/)
- **日本国内のニュースサイト**（RSSがある場合）

**実装方法:**
```python
# 既存のRSS監視機能を拡張
feed_urls = [
    'https://hempindustrydaily.com/feed/',
    'https://www.leafly.com/news/rss',
    # ...
]
```

---

### 方法B: Google News API

**メリット:**
- ✅ 多様な情報源
- ✅ 最新のニュースを優先
- ✅ 日本語ニュースにも対応

**デメリット:**
- ⚠️ APIキーが必要（有料の可能性）
- ⚠️ 情報源の検証が必要

**実装方法:**
```python
import feedparser

# Google News RSS（無料）
google_news_rss = 'https://news.google.com/rss/search?q=CBD+marijuana+cannabis&hl=ja&gl=JP&ceid=JP:ja'

feed = feedparser.parse(google_news_rss)
```

---

### 方法C: News API（有料サービス）

**メリット:**
- ✅ 高品質なニュース
- ✅ 多様な情報源
- ✅ フィルタリング機能

**デメリット:**
- ⚠️ 有料（月額制）
- ⚠️ APIキーが必要

**参考:** https://newsapi.org/

---

### 方法D: Webスクレイピング（慎重に）

**メリット:**
- ✅ 任意のサイトから収集可能
- ✅ 柔軟な情報取得

**デメリット:**
- ⚠️ 利用規約の確認が必要
- ⚠️ サーバー負荷への配慮
- ⚠️ 法的問題の可能性

**推奨:**
- RSSフィードが利用可能な場合はRSSを優先
- Webスクレイピングは最後の手段

---

## 📝 要約ツール

### 方法A: OpenAI GPT API（推奨）

**メリット:**
- ✅ 高品質な要約
- ✅ 自然な日本語
- ✅ カスタマイズ可能
- ✅ 正確性が高い

**デメリット:**
- ⚠️ 有料（従量課金）
- ⚠️ APIキーが必要

**実装方法:**
```python
from openai import OpenAI

client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))

response = client.chat.completions.create(
    model="gpt-4o-mini",  # または gpt-3.5-turbo（コスト削減）
    messages=[
        {"role": "system", "content": "あなたはCBD・大麻分野の専門ライターです。ニュースを簡潔に要約してください。"},
        {"role": "user", "content": f"以下のニュースを要約してください：\n\n{news_text}"}
    ],
    max_tokens=200,
    temperature=0.3  # 低めに設定して正確性を重視
)

summary = response.choices[0].message.content
```

**料金目安:**
- GPT-4o-mini: $0.15 / 1M input tokens, $0.60 / 1M output tokens
- GPT-3.5-turbo: $0.50 / 1M input tokens, $1.50 / 1M output tokens

---

### 方法B: Claude API（Anthropic）

**メリット:**
- ✅ 高品質な要約
- ✅ 長文に強い
- ✅ 正確性が高い

**デメリット:**
- ⚠️ 有料（従量課金）
- ⚠️ APIキーが必要

**実装方法:**
```python
import anthropic

client = anthropic.Anthropic(api_key=os.getenv('ANTHROPIC_API_KEY'))

message = client.messages.create(
    model="claude-3-haiku-20240307",  # コスト効率重視
    max_tokens=200,
    temperature=0.3,
    system="あなたはCBD・大麻分野の専門ライターです。ニュースを簡潔に要約してください。",
    messages=[
        {"role": "user", "content": f"以下のニュースを要約してください：\n\n{news_text}"}
    ]
)

summary = message.content[0].text
```

**料金目安:**
- Claude 3 Haiku: $0.25 / 1M input tokens, $1.25 / 1M output tokens

---

### 方法C: Google Gemini API

**メリット:**
- ✅ 無料枠あり（月60リクエスト/分）
- ✅ コスト効率が高い
- ✅ 日本語に強い

**デメリット:**
- ⚠️ 無料枠に制限あり
- ⚠️ APIキーが必要

**実装方法:**
```python
import google.generativeai as genai

genai.configure(api_key=os.getenv('GEMINI_API_KEY'))
model = genai.GenerativeModel('gemini-pro')

response = model.generate_content(
    f"以下のニュースを簡潔に要約してください（200文字以内）：\n\n{news_text}"
)

summary = response.text
```

**料金目安:**
- Gemini Pro: 無料枠あり、その後 $0.0005 / 1K characters

---

### 方法D: ローカル要約（無料）

**メリット:**
- ✅ 完全無料
- ✅ APIキー不要
- ✅ プライバシー重視

**デメリット:**
- ⚠️ 要約品質が限定的
- ⚠️ 処理時間がかかる場合がある

**実装方法:**
```python
# 簡易的な要約（最初のN文字 + 要点抽出）
def simple_summary(text, max_length=200):
    # 最初の数段落を取得
    paragraphs = text.split('\n\n')
    summary = '\n\n'.join(paragraphs[:2])
    
    # 長さを調整
    if len(summary) > max_length:
        summary = summary[:max_length-3] + "..."
    
    return summary
```

---

## 💡 推奨アプローチ

### Phase 1: Gemini APIを使用（推奨・既に課金済み）

**ニュース収集:**
- RSSフィード（既存実装を活用）
- Google News RSS（無料）
- CBD・大麻関連ニュースサイト（RSS）

**要約:**
- **Gemini API（推奨）**
  - 既に課金済み（追加コストなし）
  - 日本語に強い
  - 品質が高い

### Phase 2: 必要に応じて他のAIを検討

**ニュース収集:**
- 既存のRSSフィードを継続
- 必要に応じてNews APIを追加

**要約:**
- **OpenAI GPT-4o-mini（オプション）**
  - 追加コストがかかる
  - コスト効率が良い
  - 品質が高い

---

## 🚀 実装方針

### 1. ニュース収集（朝7時実行）

```python
# automation/social_media/news_collector.py
def collect_cbd_news():
    # RSSフィードから最新ニュースを収集
    # 過去24時間のニュースを取得
    # 重要度順にソート
    pass
```

### 2. 要約（AI活用）

```python
# automation/social_media/news_summarizer.py
def summarize_news(news_articles):
    # AI要約APIを使用
    # 簡潔で正確な要約を生成
    # 事実ベースの情報を優先
    pass
```

### 3. LINE通知（朝7時）

```python
# automation/social_media/scheduled_tweet.py（拡張）
def send_daily_news_summary():
    # ニュース収集
    # 要約生成
    # LINE通知
    pass
```

---

## 📊 コスト比較

| ツール | 料金 | 品質 | 推奨度 |
|--------|------|------|--------|
| **RSSフィード** | 無料 | ⭐⭐⭐ | ✅✅✅ |
| **Google News RSS** | 無料 | ⭐⭐⭐ | ✅✅✅ |
| **OpenAI GPT-4o-mini** | $0.15-0.60/1M tokens | ⭐⭐⭐⭐⭐ | ✅✅✅ |
| **Claude API** | $0.25-1.25/1M tokens | ⭐⭐⭐⭐⭐ | ✅✅ |
| **Gemini API** | 無料枠あり | ⭐⭐⭐⭐ | ✅✅ |
| **ローカル要約** | 無料 | ⭐⭐ | ✅ |

---

## 🎯 次のステップ

1. **RSSフィードを拡張**（CBD・大麻関連サイトを追加）
2. **AI要約APIを統合**（OpenAI GPT-4o-mini推奨）
3. **朝7時に実行**（既存の定期実行スクリプトを拡張）
4. **効果を測定**（要約品質・コスト・時間）

---

詳細は `docs/NEWS_COLLECTION_TOOLS.md` を参照してください。
