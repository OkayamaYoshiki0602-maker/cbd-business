# X API認証エラー トラブルシューティング

## 📋 エラー: 401 Unauthorized

### 原因
X APIへの認証が失敗しています。

### 考えられる原因

1. **App permissions が「Read」のまま**
   - ツイート投稿には「Read and write」以上が必要
   - App permissions を変更した場合、Access Token の再生成が必要

2. **Access Token が無効**
   - App permissions を変更した場合、既存のAccess Tokenが無効になる可能性

3. **認証情報の不一致**
   - API Key と API Secret Key が正しくない
   - Access Token と Access Token Secret が正しくない

---

## 🔧 解決方法

### Step 1: App permissions の確認

1. X Developer Portal で「Settings」タブを開く
2. 「User authentication settings」セクションを確認
3. **App permissions が「Read and write」または「Read and write and Direct message」になっているか確認**

### Step 2: App permissions を変更した場合

App permissions を「Read」から「Read and write」に変更した場合：

1. **Access Token と Access Token Secret を再生成**
   - 「Keys and tokens」タブを開く
   - 「Authentication Tokens」セクションの「Access Token and Secret」で「Generate」ボタンをクリック
   - 新しいAccess Token と Access Token Secret をコピー

2. **.envファイルを更新**
   - 新しいAccess Token と Access Token Secret を`.env`ファイルに設定

### Step 3: 認証情報の再確認

`.env`ファイルに以下が正しく設定されているか確認：

```env
X_API_KEY=vvm4zJSdUvYbRmPqsfIHi8bXy
X_API_SECRET_KEY=iqjbHRwUUry83MRAysOtANuYKdB9sp8TMvtWYHSQ7Ti0n8UDDr
X_ACCESS_TOKEN=新しいAccess_Token_をここに設定
X_ACCESS_TOKEN_SECRET=新しいAccess_Token_Secret_をここに設定
X_BEARER_TOKEN=AAAAAAAAAAAAAAAAAAAAADuO6wEAAAAAZEp6MT60uHerFb%2FRpXqrYAvRFe0%3DsX73VgKRUJ3Jk0FTT7u2K03Co7xqmNIBUJygqZwrJLzWw7iGe0
```

**注意:** Client Secret (iqjbHRwUUry83MRAysOtANuYKdB9sp8TMvtWYHSQ7Ti0n8UDDr) は、`X_API_SECRET_KEY` に設定してください。

---

## 📝 確認チェックリスト

- [ ] App permissions: 「Read and write」を選択
- [ ] Type of App: 「Web App, Automated App or Bot」を選択
- [ ] Access Token と Access Token Secret を再生成（App permissions を変更した場合）
- [ ] `.env`ファイルに`X_API_SECRET_KEY=iqjbHRwUUry83MRAysOtANuYKdB9sp8TMvtWYHSQ7Ti0n8UDDr`を設定
- [ ] `.env`ファイルに新しいAccess Token と Access Token Secret を設定
- [ ] `.env`ファイルを保存

---

## 🧪 再テスト

設定を更新したら、再度テスト：

```bash
# ユーザー情報取得テスト
python3 automation/social_media/x_twitter.py user me
```

成功すれば、設定は完了です！
