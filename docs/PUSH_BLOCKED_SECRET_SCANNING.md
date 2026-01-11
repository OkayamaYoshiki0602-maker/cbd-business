# GitHub Push Protection エラー対応

## ⚠️ エラー内容

GitHubのPush Protection機能がPersonal Access Tokenを検出して、プッシュをブロックしています。

```
remote: error: GH013: Repository rule violations found for refs/heads/main.
remote: - GITHUB PUSH PROTECTION
remote: - Push cannot contain secrets
remote: - GitHub Personal Access Token
remote:   locations:
remote:     - .cursor/mcp.json:10
```

---

## 🔧 解決方法

### 方法1: GitHubで一時的に許可（簡単・推奨）

1. **GitHubのURLを開く**
   - エラーメッセージに表示されたURLをクリック
   - 例: https://github.com/OkayamaYoshiki0602-maker/cbd-business/security/secret-scanning/unblock-secret/...

2. **「Allow secret」をクリック**
   - 一時的にプッシュを許可します
   - 今後はトークンを削除することを推奨

---

### 方法2: トークンを削除（推奨・セキュア）

1. **`.cursor/mcp.json`を`.gitignore`に追加**
   ```bash
   echo ".cursor/" >> .gitignore
   git add .gitignore
   git commit -m "Add: .cursor/を.gitignoreに追加"
   ```

2. **`.cursor/`フォルダをGit管理から削除**
   ```bash
   git rm -r --cached .cursor/
   git commit -m "Remove: .cursor/をGit管理から除外"
   ```

3. **再度プッシュ**
   ```bash
   git push origin main
   ```

---

## ✅ 推奨事項

**`.cursor/`フォルダは個人設定ファイルなので、GitHubにプッシュしないことを推奨します。**

### `.gitignore`に追加済み

既に`.cursor/`を`.gitignore`に追加済みです。次回以降のプッシュでは問題ありません。

ただし、過去のコミットにトークンが含まれているため、今回のプッシュはブロックされています。

---

## 🎯 次のステップ

### 方法A: GitHubで一時的に許可（すぐにプッシュしたい場合）

1. エラーメッセージのURLをクリック
2. 「Allow secret」をクリック
3. 再度プッシュを実行

### 方法B: トークンを削除（セキュア）

1. `.cursor/mcp.json`からトークンを削除
2. 新しいコミットを作成
3. プッシュを実行

---

## 📝 参考

- [GitHub Secret Scanning](https://docs.github.com/code-security/secret-scanning)
- [Working with Push Protection](https://docs.github.com/code-security/secret-scanning/working-with-secret-scanning-and-push-protection/working-with-push-protection-from-the-command-line)
