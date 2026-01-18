# 記事自動作成フロー v2

## 📋 概要

Google Sheetsから記事テーマを読み込み、Gemini APIでMarkdown記事を生成し、WordPressに下書きとして保存。スプレッドシートには記事内容は含めず、メタデータのみを反映するフロー。

---

## 🔄 ワークフロー

```
1. Google Sheets（シート2）に記事テーマを入力
   ↓
2. article_generator_v2.pyで記事を生成（毎朝8:00自動実行）
   ↓
3. WordPressに「下書き」として記録
   ↓
4. スプレッドシートにメタデータを反映（タイトル、分類、ターゲット、タグ、ディスクリプション、スラッグ、アフィリエイトリンク）
   ↓
5. LINE通知でプレビュー送信
   ↓
6. 私が確認・添削（WordPressの下書きで編集）
   ↓
7. スプレッドシートで「承認済み」に変更
   ↓
8. github_article_publisher.pyでGitHubに保存
   ↓
9. Gitコミット・プッシュ
   ↓
10. GitHub ActionsでWordPressに自動同期（既存のワークフロー）
   ↓
11. ステータスを「投稿済み」に更新
```

---

## 📊 スプレッドシート構成

**スプレッドシートID:** `1-2L6C3NpF8vqnXxHWKP-Js3TMFKYE73tTtxdkZVPTaM`  
**シート名:** `シート2`

**列構成:**

| 列 | 列名 | 説明 | 入力方法 |
|---|------|------|---------|
| A | タイムスタンプ | 記事生成時刻 | 自動入力 |
| B | ステータス | 下書き/承認済み/投稿済み | 自動入力→手動変更 |
| C | 記事タイトル | 生成された記事タイトル | 自動入力 |
| D | 記事の分類 | 商品紹介/悩み解決/経済/ビジネス | **手動入力** |
| E | ターゲット | 記事のターゲット（例: "CBD初心者"） | **手動入力** |
| F | タグ | 関連タグ（カンマ区切り） | **手動入力** |
| G | ディスクリプション | メタディスクリプション | 自動入力 |
| H | スラッグ | URLスラッグ | 自動入力 |
| I | アフィリエイトリンク | アフィリエイトリンク（URLのみ、カンマ区切り） | 自動抽出 |

**記事テーマ入力（手動）:**
- 列D: 記事の分類（例: "商品紹介", "悩み解決", "経済", "ビジネス"）
- 列E: ターゲット（例: "CBD初心者", "睡眠にお困りのあなた"）
- 列F: タグ（カンマ区切り、例: "CBD,睡眠,リラックス"）

**自動生成・反映:**
- 列A, C, G, H, I: 記事生成後に自動入力
- 列B: 初期は「下書き」、承認後に「承認済み」→「投稿済み」

---

## 🛠️ セットアップ

### 1. 環境変数の設定

`.env`ファイルに以下を設定：

```env
# 記事テーマ用スプレッドシートID
ARTICLE_SPREADSHEET_ID=1-2L6C3NpF8vqnXxHWKP-Js3TMFKYE73tTtxdkZVPTaM

# WordPress設定（WordPress REST API用）
WORDPRESS_URL=https://cbd-no-hito.com
WORDPRESS_USERNAME=your_username
WORDPRESS_APP_PASSWORD=your_app_password

# Gemini API（既に設定済み）
GEMINI_API_KEY=your_gemini_api_key_here
```

### 2. WordPressアプリケーションパスワードの取得

1. WordPress管理画面にログイン
2. 「ユーザー」→「プロフィール」を開く
3. 「アプリケーションパスワード」セクションを開く
4. 「新しいアプリケーションパスワード」に名前を入力（例: "Cursor Article Generator"）
5. 「新しいパスワードを追加」をクリック
6. 生成されたパスワードを`.env`の`WORDPRESS_APP_PASSWORD`に設定

### 3. Launch Agentの設定（毎朝8:00自動実行）

**Launch Agentファイル:** `~/Library/LaunchAgents/com.cbd.article-generator.plist`

**既に作成済みの場合:** そのまま使用

**未作成の場合:** 以下のコマンドで確認：

```bash
ls ~/Library/LaunchAgents/com.cbd.article-generator.plist
```

**未作成の場合は作成:**

```bash
nano ~/Library/LaunchAgents/com.cbd.article-generator.plist
```

以下をコピー＆ペースト：

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
        <string>/Users/okayamayoshiki/Library/CloudStorage/GoogleDrive-okayamayoshiki0602o@gmail.com/マイドライブ/cursor/automation/content/article_generator_v2.py</string>
    </array>
    <key>WorkingDirectory</key>
    <string>/Users/okayamayoshiki/Library/CloudStorage/GoogleDrive-okayamayoshiki0602o@gmail.com/マイドライブ/cursor</string>
    <key>StartCalendarInterval</key>
    <dict>
        <key>Hour</key>
        <integer>8</integer>
        <key>Minute</key>
        <integer>0</integer>
    </dict>
    <key>RunAtLoad</key>
    <false/>
    <key>StandardOutPath</key>
    <string>/tmp/cbd-article-generator.log</string>
    <key>StandardErrorPath</key>
    <string>/tmp/cbd-article-generator-error.log</string>
</dict>
</plist>
```

保存（Ctrl+X → Y → Enter）して、Launch Agentを読み込み：

```bash
launchctl bootstrap ~/Library/LaunchAgents ~/Library/LaunchAgents/com.cbd.article-generator.plist
```

---

## 📝 使用方法

### 方法1: 自動実行（毎朝8:00）

Launch Agentが自動的に記事生成を実行します。

### 方法2: 手動実行

```bash
python automation/content/article_generator_v2.py
```

---

## ✅ 承認・投稿フロー

### 1. 記事生成後（毎朝8:00）

- WordPressに「下書き」として投稿される
- スプレッドシートにメタデータが反映される（列A, C, G, H, I）
- LINE通知でプレビューが送信される

### 2. 確認・添削（WordPress管理画面）

- WordPressの「投稿」→「下書き」から記事を確認
- 記事内容を編集・添削
- 問題がなければ、スプレッドシートのステータス（列B）を「承認済み」に変更

### 3. GitHub投稿

承認済み記事をGitHubリポジトリに保存：

```bash
python automation/content/github_article_publisher.py
```

**動作:**
- ステータスが「承認済み」の記事を検出
- Markdownファイルとして`wordpress/posts/`に保存
- Gitにコミット・プッシュ
- ステータスを「投稿済み」に更新
- LINE通知で投稿結果を送信

### 4. WordPress同期

**既存のGitHub Actionsワークフロー**が自動的にWordPressに同期します。

---

## 📊 記事生成の特徴

### 参考記事のスタイル

「【決定版】Naturecan(ネイチャーカン)の評判は？世界No.1と言われる3つの理由」のスタイルを参考に：

1. **導入:** 「〜で、絶対に失敗したくない。」「1ミリの不安も残したくない。」といった共感から入る
2. **「この記事で分かること」セクション:** 箇条書きで読者に期待値を設定
3. **見出しの階層:** H3でサブセクション、H4で詳細を説明
4. **箇条書き:** 「メリット」「デメリット」「こんな人におすすめ」などの構造
5. **比較表:** 商品情報を表形式で整理
6. **アフィリエイトリンク:** 自然に商品紹介の後に配置
7. **トーン:** 「結論は○○一択です」のように断定的だが、根拠を示す

### 記事タイプ別の内容

- **商品紹介**: 実際の使用体験、商品の特徴、価格、購入方法、アフィリエイトリンクを自然に配置
- **悩み解決**: 具体的な解決方法、CBDの効果、エビデンス、実践的なアドバイス
- **経済・ビジネス**: CBD市場の動向、ビジネス事例、投資情報、法規制の変化
- **その他**: ターゲットと悩みに応じた専門的な内容

### 信頼性の高い情報

- 公的な研究結果、論文、エビデンスを引用
- 推測や憶測は避ける
- 医療効果の断定的表現は避ける（薬機法遵守）

---

## 📋 チェックリスト

### 今すぐやること

- [ ] `.env`に`ARTICLE_SPREADSHEET_ID`を設定（既に設定済みの場合は確認のみ）
- [ ] `.env`に`WORDPRESS_USERNAME`と`WORDPRESS_APP_PASSWORD`を設定
- [ ] WordPressアプリケーションパスワードを取得
- [ ] スプレッドシート（シート2）に記事テーマを入力（列D, E, F）
- [ ] Launch Agentファイルを確認・作成

### 今週中にやること

- [ ] 記事生成のテスト実行
- [ ] WordPress下書きの確認・添削フローの確認
- [ ] 承認後のGitHub投稿のテスト

---

## ⚠️ 注意事項

1. **スプレッドシートの列構成**
   - 記事内容はスプレッドシートに保存されない
   - メタデータのみ（タイトル、分類、ターゲット、タグ、ディスクリプション、スラッグ、アフィリエイトリンク）

2. **記事テーマの入力**
   - 列D（記事の分類）、列E（ターゲット）、列F（タグ）を入力
   - 既に処理済みの行（列Bが「下書き」「承認済み」「投稿済み」）はスキップされる

3. **WordPress下書き**
   - 記事はWordPressの「下書き」として保存される
   - WordPress管理画面から編集・添削可能

4. **アフィリエイトリンクの抽出**
   - 記事本文から自動的に抽出される（Amazon、楽天、アフィリエイト関連）
   - スプレッドシートにはURLのみが保存される（カンマ区切り）

---

**最終更新:** 2026-01-11
