# 18禁アフィリエイトTwitter実装ガイド

## 📋 概要

このガイドでは、DMMアフィリエイトを活用した18禁コンテンツ（漫画・ビデオ）のTwitterアカウント自動運営システムの実装方法を説明します。

---

## 🎯 実装済み機能

### 1. DMMアフィリエイトAPI連携 (`dmm_affiliate.py`)

**機能**:
- DMMアフィリエイトAPIを使用した商品検索
- 商品情報の取得（タイトル、作者、画像URL、アフィリエイトリンク等）
- サンプル画像のダウンロード

**使用方法**:
```bash
# 商品検索
python automation/social_media/dmm_affiliate.py search 同人誌

# 特定商品の取得
python automation/social_media/dmm_affiliate.py get d_715045 --download
```

### 2. Twitter投稿自動生成 (`adult_twitter_generator.py`)

**機能**:
- 漫画・ビデオ用のツイート本文自動生成
- サンプル画像 + アフィリエイトリンクの組み合わせ
- テストモード（dry-run）対応

**使用方法**:
```bash
# 漫画ツイート生成（テストモード）
python automation/social_media/adult_twitter_generator.py comic --search 同人誌 --dry-run

# ビデオツイート生成（テストモード）
python automation/social_media/adult_twitter_generator.py video --search AV --dry-run

# 実際に投稿
python automation/social_media/adult_twitter_generator.py comic --content-id d_715045
```

---

## ⚙️ セットアップ手順

### Step 1: DMMアフィリエイト登録

1. **DMMアフィリエイトに登録**
   - URL: https://affiliate.dmm.com/
   - アカウント作成・審査通過

2. **API IDとアフィリエイトIDを取得**
   - DMMアフィリエイトの「webサービス 利用登録」からAPI IDを申請
   - アフィリエイトIDを確認

3. **環境変数を設定**
   - `.env`ファイルに以下を追加:
   ```env
   DMM_API_ID=your_api_id_here
   DMM_AFFILIATE_ID=your_affiliate_id_here
   ```

### Step 2: 依存ライブラリのインストール

```bash
cd automation
pip install -r requirements.txt
```

**新規追加されたライブラリ**:
- `dmm-search3>=2.0.0`: DMMアフィリエイトAPI連携

### Step 3: Twitter API認証情報の確認

`.env`ファイルにTwitter API認証情報が設定されているか確認:

```env
X_API_KEY=your_api_key
X_API_SECRET_KEY=your_api_secret
X_ACCESS_TOKEN=your_access_token
X_ACCESS_TOKEN_SECRET=your_access_token_secret
X_BEARER_TOKEN=your_bearer_token
```

### Step 4: 動作確認

```bash
# DMM API接続テスト
python automation/social_media/dmm_affiliate.py search テスト

# Twitter投稿テスト（dry-run）
python automation/social_media/adult_twitter_generator.py comic --search テスト --dry-run
```

---

## 📊 実装ステータス

| 機能 | 実装状況 | 備考 |
|------|---------|------|
| DMM API連携 | ✅ 完了 | `dmm_affiliate.py` |
| 商品検索 | ✅ 完了 | キーワード検索、コンテンツID検索 |
| 画像ダウンロード | ✅ 完了 | サンプル画像取得 |
| ツイート生成（漫画） | ✅ 完了 | `adult_twitter_generator.py` |
| ツイート生成（ビデオ） | ✅ 完了 | `adult_twitter_generator.py` |
| Twitter投稿 | ✅ 完了 | 既存の`x_twitter.py`を活用 |
| スケジュール投稿 | ⚠️ 未実装 | 今後の実装予定 |
| スプレッドシート連携 | ⚠️ 未実装 | 今後の実装予定 |

---

## 🔄 今後の実装予定

### 優先度: 高

1. **スケジュール投稿機能**
   - 指定時間に自動投稿
   - 既存の`scheduled_tweet.py`を拡張

2. **スプレッドシート管理**
   - 商品リストの管理
   - 投稿履歴の記録
   - 承認フロー（既存システムを活用）

3. **画像リサイズ・最適化**
   - Twitter推奨サイズ（1200x675px）へのリサイズ
   - 画像品質の最適化

### 優先度: 中

4. **ジャンル特化機能**
   - 特定ジャンル/作者の自動検索
   - フィルタリング機能

5. **分析機能**
   - クリック率の追跡
   - 人気コンテンツの分析
   - 投稿時間の最適化

6. **複数アカウント対応**
   - 漫画アカウントとビデオアカウントの同時運営
   - アカウント別設定管理

---

## 💡 使用例

### 例1: 漫画ツイートの生成と投稿

```bash
# 1. 商品を検索して確認
python automation/social_media/dmm_affiliate.py search 同人誌

# 2. テストモードでツイート内容を確認
python automation/social_media/adult_twitter_generator.py comic \
  --content-id d_715045 \
  --dry-run

# 3. 実際に投稿
python automation/social_media/adult_twitter_generator.py comic \
  --content-id d_715045
```

### 例2: ビデオツイートの一括生成

```bash
# 複数の商品を検索して、それぞれツイート生成
python automation/social_media/adult_twitter_generator.py video \
  --search AV \
  --count 5 \
  --dry-run
```

---

## ⚠️ 注意事項

### コンプライアンス

1. **R18表記**
   - すべてのツイートに「🔞」絵文字を付与
   - プロフィールに「18歳未満閲覧禁止」表記

2. **著作権**
   - DMM公式サンプル画像のみ使用
   - 無断転載は禁止

3. **Twitter規約**
   - 過度に露骨な画像は避ける
   - モザイク処理済み画像のみ使用

4. **アフィリエイト規約**
   - DMMアフィリエイト規約を遵守
   - 広告リンクである旨を明記

### 技術的な注意点

1. **APIレート制限**
   - DMM APIのレート制限を確認
   - 適切な間隔でリクエスト

2. **画像ダウンロード**
   - 一時ファイルの管理
   - ディスク容量の確保

3. **エラーハンドリング**
   - APIエラー時のリトライ機能
   - 画像取得失敗時のフォールバック

---

## 📝 次のステップ

### 即座に実行可能

1. **DMMアフィリエイト登録・API取得**
   - DMMアフィリエイトに登録
   - API IDとアフィリエイトIDを取得
   - `.env`ファイルに設定

2. **テスト実行**
   - 上記の「動作確認」を実行
   - 実際の商品でツイート生成をテスト

3. **Twitterアカウント準備**
   - 漫画用・ビデオ用アカウントを作成
   - プロフィール設定（R18表記等）

### 1週間以内

4. **スケジュール投稿機能の実装**
   - 既存の`scheduled_tweet.py`を拡張
   - 定時投稿の設定

5. **スプレッドシート管理の実装**
   - 商品リストの管理
   - 投稿履歴の記録

### 1ヶ月以内

6. **本格運用開始**
   - 毎日3-5回の投稿
   - データ分析と最適化

---

## 🆘 トラブルシューティング

### DMM API接続エラー

**エラー**: `ValueError: DMM API認証情報が設定されていません`

**解決方法**:
- `.env`ファイルに`DMM_API_ID`と`DMM_AFFILIATE_ID`が設定されているか確認

### 画像ダウンロードエラー

**エラー**: 画像のダウンロードに失敗

**原因**:
- 画像URLが無効
- ネットワークエラー
- ディスク容量不足

**解決方法**:
- 画像URLを確認
- インターネット接続を確認
- ディスク容量を確認

### Twitter投稿エラー

**エラー**: ツイートの投稿に失敗

**原因**:
- API認証情報の誤り
- レート制限
- 画像サイズが大きすぎる

**解決方法**:
- Twitter API認証情報を確認
- レート制限を確認（しばらく待つ）
- 画像をリサイズ

---

**作成日**: 2025-01-30  
**最終更新**: 2025-01-30
