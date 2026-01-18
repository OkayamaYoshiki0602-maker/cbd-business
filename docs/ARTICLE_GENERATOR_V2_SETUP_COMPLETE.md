# 記事自動作成フローv2 セットアップ完了

## ✅ 設定完了

### 現在の設定状態

**WordPress認証情報:**
- ✅ `WORDPRESS_USERNAME=yoshiki`（設定済み）
- ✅ `WORDPRESS_APP_PASSWORD=u7X7oO2oyaGv80RJPbw84SUm`（既存の「GitHub Sync」パスワードを使用）

**スプレッドシート:**
- ✅ `ARTICLE_SPREADSHEET_ID`が設定されているか確認が必要

**Gemini API:**
- ✅ `GEMINI_API_KEY`が設定されているか確認が必要

---

## 📋 次のステップ

### 1. スプレッドシートの設定確認

スプレッドシート（シート2）に記事テーマを入力：

- **列D:** 記事の分類（例: "商品紹介", "悩み解決", "経済", "ビジネス"）
- **列E:** ターゲット（例: "CBD初心者", "睡眠にお困りのあなた"）
- **列F:** タグ（カンマ区切り、例: "CBD,睡眠,リラックス"）

**スプレッドシートURL:**
```
https://docs.google.com/spreadsheets/d/1-2L6C3NpF8vqnXxHWKP-Js3TMFKYE73tTtxdkZVPTaM/edit?gid=534297966#gid=534297966
```

### 2. テスト実行

記事生成スクリプトをテスト実行：

```bash
python automation/content/article_generator_v2.py
```

**期待される動作:**
1. スプレッドシート（シート2）から記事テーマを読み込み
2. Gemini APIで記事を生成
3. WordPressに「下書き」として投稿
4. スプレッドシートにメタデータを反映
5. LINE通知で結果を送信

### 3. Launch Agentの設定（毎朝8:00自動実行）

`docs/LAUNCH_AGENT_ARTICLE_GENERATOR.md`を参照して、Launch Agentファイルを作成：

```bash
nano ~/Library/LaunchAgents/com.cbd.article-generator.plist
```

設定内容は`docs/LAUNCH_AGENT_ARTICLE_GENERATOR.md`を参照してください。

---

## 🔍 動作確認チェックリスト

### 環境変数の確認

```bash
grep -E "WORDPRESS_URL|WORDPRESS_USERNAME|WORDPRESS_APP_PASSWORD|ARTICLE_SPREADSHEET_ID|GEMINI_API_KEY" .env
```

**期待される結果:**
```
WORDPRESS_URL=https://cbd-no-hito.com
WORDPRESS_USERNAME=yoshiki
WORDPRESS_APP_PASSWORD=u7X7oO2oyaGv80RJPbw84SUm
ARTICLE_SPREADSHEET_ID=1-2L6C3NpF8vqnXxHWKP-Js3TMFKYE73tTtxdkZVPTaM
GEMINI_API_KEY=AIzaSyCBzyNE0XfRPyUqzm1aTjbv5u2THPzpAmQ
```

### テスト実行

```bash
python automation/content/article_generator_v2.py
```

**成功時の出力例:**
```
📝 1件の記事テーマを読み込みました

📝 記事生成中: CBD初心者 / 商品紹介
📝 WordPressに下書きとして投稿中...
✅ 記事を生成しました: 【決定版】CBD初心者向けおすすめ商品5選
   WordPress下書きURL: https://cbd-no-hito.com/wp-admin/post.php?post=1234&action=edit

✅ スプレッドシートにメタデータを反映しました: 行2

✅ 1件の記事を生成しました
```

---

## 📝 ワークフロー（再確認）

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

## 🔧 トラブルシューティング

### エラー1: `WORDPRESS_APP_PASSWORDが設定されていません`

**解決方法:**
`.env`ファイルに`WORDPRESS_APP_PASSWORD`を設定してください（既に設定済み）

### エラー2: `ARTICLE_SPREADSHEET_IDが設定されていません`

**解決方法:**
`.env`ファイルに以下を設定：

```env
ARTICLE_SPREADSHEET_ID=1-2L6C3NpF8vqnXxHWKP-Js3TMFKYE73tTtxdkZVPTaM
```

### エラー3: `401 Unauthorized`（WordPress）

**解決方法:**
1. `.env`ファイルの`WORDPRESS_USERNAME`と`WORDPRESS_APP_PASSWORD`を確認
2. WordPress管理画面でアプリケーションパスワードが有効か確認

### エラー4: `GEMINI_API_KEYが設定されていません`

**解決方法:**
`.env`ファイルに以下を設定：

```env
GEMINI_API_KEY=AIzaSyCBzyNE0XfRPyUqzm1aTjbv5u2THPzpAmQ
```

---

## 📚 関連ドキュメント

- `docs/ARTICLE_GENERATION_V2_WORKFLOW.md`: 記事自動作成フローv2の詳細ガイド
- `docs/LAUNCH_AGENT_ARTICLE_GENERATOR.md`: Launch Agent設定ガイド
- `docs/WORDPRESS_APP_PASSWORD_UPDATE.md`: アプリケーションパスワード設定ガイド

---

**最終更新:** 2026-01-11
