# GitHubプッシュ完了後の確認事項

## ✅ プッシュ完了後

GitHubへのプッシュが完了したら、以下を確認してください。

---

## 📋 確認事項

### 1. GitHubリポジトリの確認

1. **GitHubリポジトリを開く**
   - https://github.com/OkayamaYoshiki0602-maker/cbd-business

2. **ファイルが反映されているか確認**
   - [x] `wordpress/posts/cbd-oil-howto.html` が存在する
   - [x] `.github/workflows/sync-wordpress.yml` が存在する
   - [x] `.github/scripts/sync_to_wordpress.py` が存在する

---

### 2. GitHub Actionsの実行を確認

1. **GitHubリポジトリ → Actionsタブ**
   - https://github.com/OkayamaYoshiki0602-maker/cbd-business/actions

2. **「Sync to WordPress」ワークフローを確認**
   - ✅ 緑色のチェックマーク = 成功
   - ⚠️ 黄色/赤色 = エラー（ログを確認）

3. **初回実行の場合、約1-2分かかります**

---

### 3. GitHub Actionsのログを確認（エラーの場合）

1. **Actionsタブ → 「Sync to WordPress」ワークフローをクリック**
2. **実行ジョブをクリック**
3. **「Sync to WordPress via REST API」ステップを展開**
4. **エラーメッセージを確認**

**よくあるエラー:**
- `401 Unauthorized` → GitHub Secretsの設定を確認
- `404 Not Found` → WordPress URLを確認
- `記事が作成されない` → スクリプトのログを確認

---

### 4. WordPressサイトの確認

1. **WordPress管理画面にログイン**
   - https://cbd-no-hito.com/wp-admin/

2. **投稿 → 投稿一覧**
   - 記事が自動反映されているか確認

3. **記事が表示されない場合**
   - GitHub Actionsのログを確認
   - WordPress REST APIが有効か確認
   - アプリケーションパスワードを確認

---

## 🎯 次のステップ

### 自動連携のテスト

1. **記事コードを編集**（ローカル）
   ```bash
   # wordpress/posts/cbd-oil-howto.html を編集
   ```

2. **GitHubにプッシュ**
   ```bash
   git add wordpress/posts/cbd-oil-howto.html
   git commit -m "Update: CBDオイル記事を更新"
   git push origin main
   ```

3. **自動同期の確認**
   - GitHub Actionsが自動実行
   - WordPressに記事が自動反映
   - **コードエディタは触る必要なし！**

---

## 📝 参考情報

### セットアップ完了チェックリスト

- [x] WordPress側の設定（アプリケーションパスワード作成）
- [x] GitHub Secretsの設定
- [x] GitHub CLIのインストールと認証
- [x] GitHubへのプッシュ
- [ ] GitHub Actionsの実行確認
- [ ] WordPressサイトでの記事確認

---

## 🔧 トラブルシューティング

### GitHub Actionsが実行されない

**原因:** ワークフローファイルのパスが間違っている

**解決方法:**
1. `.github/workflows/sync-wordpress.yml` が存在するか確認
2. ファイルのパスが正しいか確認

---

### 記事がWordPressに反映されない

**原因:** WordPress REST APIの認証エラー

**解決方法:**
1. GitHub Secretsの設定を確認
2. WordPressのアプリケーションパスワードを確認
3. GitHub Actionsのログを確認

---

## ✅ 完了

すべての設定が完了すれば、今後は**GitHubにプッシュするだけでWordPressに自動反映**されます！
