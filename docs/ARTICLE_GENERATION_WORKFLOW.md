# 記事自動作成フロー

## 📋 概要

Google Sheetsから記事テーマ・キーワードを読み込み、Gemini APIでMarkdown記事を自動生成し、承認後にWordPressに投稿するフロー。

---

## 🔄 ワークフロー

```
1. Google Sheetsに記事テーマを入力
   ↓
2. Cursor/AIでMarkdown記事を自動生成
   ↓
3. スプレッドシートに「下書き」として記録
   ↓
4. LINE通知でプレビュー送信
   ↓
5. 私が確認・添削（スプレッドシート上で編集）
   ↓
6. 「承認済み」に変更
   ↓
7. WordPress REST APIで自動投稿
   ↓
8. ステータスを「投稿済み」に更新
```

---

## 🛠️ セットアップ

### 1. 環境変数の設定

`.env`ファイルに以下を追加：

```env
# WordPress設定
WORDPRESS_URL=https://cbd-no-hito.com
WORDPRESS_USERNAME=your_username
WORDPRESS_APP_PASSWORD=your_app_password

# 記事テーマ用スプレッドシートID
ARTICLE_SPREADSHEET_ID=your_spreadsheet_id_here

# 承認待ちリスト用スプレッドシートID（既存のものを使用）
APPROVAL_SPREADSHEET_ID=your_spreadsheet_id_here

# Gemini API（既に設定済み）
GEMINI_API_KEY=your_gemini_api_key_here
```

### 2. WordPressアプリケーションパスワードの取得

1. WordPress管理画面にログイン
2. 「ユーザー」→「プロフィール」を開く
3. 「アプリケーションパスワード」セクションを開く
4. 「新しいアプリケーションパスワード」に名前を入力（例: "Cursor Article Publisher"）
5. 「新しいパスワードを追加」をクリック
6. 生成されたパスワードを`.env`の`WORDPRESS_APP_PASSWORD`に設定

### 3. Google Sheetsの準備

#### A. 記事テーマ用スプレッドシート（新規作成）

**シート名:** 「シート1」

**列構成:**
- 列A: ターゲット（例: "睡眠にお困りのあなた"）
- 列B: 悩み（例: "寝つきが悪い"）
- 列C: 関連キーワード（カンマ区切り、例: "CBD,睡眠,リラックス"）
- 列D: SEOキーワード（例: "CBD 睡眠"）

**例:**
```
A列: 睡眠にお困りのあなた
B列: 寝つきが悪い
C列: CBD,睡眠,リラックス,ストレス
D列: CBD 睡眠
```

**スプレッドシートIDを`.env`の`ARTICLE_SPREADSHEET_ID`に設定**

#### B. 承認待ちリスト用スプレッドシート（既存を使用）

**列構成:**
- 列A: タイムスタンプ
- 列B: ステータス（下書き/承認済み/投稿済み）
- 列C: 記事タイトル
- 列D: 記事本文（Markdown）
- 列E: ターゲット
- 列F: 悩み

---

## 📝 使用方法

### 方法1: スプレッドシートから一括生成

1. Google Sheetsに記事テーマを入力（上記の列構成に従う）
2. 以下を実行：
```bash
python automation/content/article_generator.py
```

### 方法2: コマンドラインから個別生成

```bash
python automation/content/article_generator.py "睡眠にお困りのあなた" "寝つきが悪い" "CBD,睡眠,リラックス" "CBD 睡眠"
```

**引数:**
1. ターゲット（必須）
2. 悩み（必須）
3. 関連キーワード（オプション、カンマ区切り）
4. SEOキーワード（オプション）

---

## ✅ 承認・投稿フロー

### 1. 記事生成後

- スプレッドシートに「下書き」として追加される
- LINE通知でプレビューが送信される

### 2. 確認・添削

- スプレッドシートの記事本文（列D）を編集可能
- タイトルも編集可能（列C）
- 問題がなければ、ステータス（列B）を「承認済み」に変更

### 3. WordPress投稿

承認済み記事をWordPressに投稿：
```bash
python automation/content/wordpress_publisher.py
```

**動作:**
- ステータスが「承認済み」の記事を検出
- WordPress REST APIで投稿
- ステータスを「投稿済み」に更新
- LINE通知で投稿結果を送信

---

## 🔧 定期実行設定（オプション）

Launch Agentで記事生成を定期実行する場合：

### 週次記事生成（月曜日の朝7:00）

`~/Library/LaunchAgents/com.cbd.article-generator.plist`を作成：

```xml
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
    <key>Label</key>
    <string>com.cbd.article-generator</string>
    <key>ProgramArguments</key>
    <array>
        <string>/usr/bin/python3</string>
        <string>/Users/okayamayoshiki/Library/CloudStorage/GoogleDrive-okayamayoshiki0602o@gmail.com/マイドライブ/cursor/automation/content/article_generator.py</string>
    </array>
    <key>StartCalendarInterval</key>
    <dict>
        <key>Weekday</key>
        <integer>1</integer>
        <key>Hour</key>
        <integer>7</integer>
        <key>Minute</key>
        <integer>0</integer>
    </dict>
    <key>StandardOutPath</key>
    <string>/tmp/cbd-article-generator.log</string>
    <key>StandardErrorPath</key>
    <string>/tmp/cbd-article-generator-error.log</string>
</dict>
</plist>
```

---

## 📊 記事生成の品質

### 生成される記事の特徴

1. **SEO最適化**
   - タイトルにSEOキーワードを含む
   - 本文にキーワードを3-5回自然に配置
   - メタディスクリプションを生成（150文字以内）

2. **見出し構造**
   - H1: 記事タイトル
   - H2: 主要セクション（3-5セクション）
   - H3: サブセクション（必要に応じて）

3. **アフィリエイトリンク配置ポイント**
   - 「おすすめ商品」セクションを自動追加
   - 商品紹介の後に自然にアフィリエイトリンクを配置

4. **トーン**
   - 専門的でありながら親しみやすい
   - データコンサルタントの視点（数字・エビデンス重視）
   - 適度なユーモア（ポーカー・マラソン・お酒のエピソード）

5. **文字数**
   - 本文: 2,000-3,000文字
   - 見出し・リストを含めて全体で3,000-4,000文字

---

## ⚠️ 注意事項

1. **Markdownの制限**
   - スプレッドシートのセルサイズ制限（約5万文字）を考慮
   - 記事本文は最初の5,000文字のみ保存（長い場合は編集が必要）

2. **WordPress投稿時の制限**
   - アプリケーションパスワードの有効期限を確認
   - カテゴリ・タグは手動で設定（将来的に自動化可能）

3. **エラーハンドリング**
   - 記事生成に失敗した場合は、スプレッドシートに追加されない
   - WordPress投稿に失敗した場合は、ステータスは「承認済み」のまま

---

## 🔄 今後の改善

1. **カテゴリ・タグの自動設定**
   - ターゲット・悩みから自動的にカテゴリを決定
   - SEOキーワードから自動的にタグを生成

2. **画像の自動生成**
   - 記事タイトルに基づいてアイキャッチ画像を生成
   - アフィリエイト商品の画像を自動取得

3. **記事品質の向上**
   - バズアカウント分析の結果を記事生成プロンプトに組み込む
   - エンゲージメント率の高い記事パターンを学習

---

**最終更新:** 2026-01-11
