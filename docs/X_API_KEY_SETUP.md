# X API Key と API Secret Key の取得方法

## 📋 手順

X Developer Portalで、API Key と API Secret Key を取得します。

### Step 1: Consumer Keys セクションを開く

1. X Developer Portal にログイン: https://developer.twitter.com/
2. 「Projects & Apps」→ プロジェクトを選択
3. 「Keys and tokens」タブを開く

### Step 2: API Key を取得

**Consumer Keys** セクションで：

1. **API Key** をコピー
   - 現在は "****rgJtr8" のように一部のみ表示されている可能性があります
   - **「Regenerate」ボタンの左側に表示されているキーをコピー**

### Step 3: API Secret Key を取得

1. **「API Secret Key」の下にある「シークレットを表示」または「Reveal」ボタンをクリック**
2. 表示されたAPI Secret Keyをコピー
3. **重要:** このキーは一度しか表示されない可能性があるため、必ずコピーして保存してください

### Step 4: .envファイルに設定

取得したAPI Key と API Secret Key を `.env` ファイルに設定：

```env
X_API_KEY=取得したAPI_Key_をここに貼り付け
X_API_SECRET_KEY=取得したAPI_Secret_Key_をここに貼り付け
```

---

## ⚠️ 注意事項

- API Secret Key は一度しか表示されない場合があります
- 失った場合は、「Regenerate」ボタンで再生成する必要があります
- 再生成すると、既存のAccess Tokenが無効になる可能性があります

---

## ✅ 設定確認

設定が完了したら、以下で確認：

```bash
# ユーザー情報取得テスト
python3 automation/social_media/x_twitter.py user me
```

成功すれば、設定は完了です！
