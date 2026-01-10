# X API 401エラー解決方法

## 📋 エラー: 401 Unauthorized

### 現在の状況
- ✅ App permissions: 「Read and write」に設定済み
- ✅ Access Token と Access Token Secret: 再生成済み
- ✅ .envファイル: 更新済み
- ❌ 401エラーが継続

---

## 🔍 考えられる原因

### 1. API Key と API Secret Key の不一致

**原因:**
- Consumer Keys（API Key と API Secret Key）を再生成した可能性
- `.env`ファイルのAPI Keyが古い値のまま

**確認方法:**
1. X Developer Portal で「Keys and tokens」タブを開く
2. **Consumer Keys** セクションで API Key を確認
3. `.env`ファイルの`X_API_KEY`と一致しているか確認

**解決方法:**
- API Key と API Secret Key が一致していない場合、X Developer Portal で取得した値を`.env`ファイルに設定

---

### 2. Bearer Token の不一致

**原因:**
- Bearer Token も再生成が必要な可能性

**確認方法:**
1. X Developer Portal で「Keys and tokens」タブを開く
2. **Authentication Tokens** セクションで Bearer Token を確認
3. `.env`ファイルの`X_BEARER_TOKEN`と一致しているか確認

**解決方法:**
- Bearer Token が一致していない場合、X Developer Portal で取得した値を`.env`ファイルに設定

---

### 3. Access Token の権限不足

**原因:**
- App permissions を変更した後、Access Token が正しく再生成されていない

**確認方法:**
1. X Developer Portal で「Settings」タブを開く
2. 「User authentication settings」で App permissions を確認
3. 「Read and write」になっていることを確認

**解決方法:**
- App permissions が「Read and write」になっている場合、Access Token を再生成

---

## 🔧 推奨解決手順

### Step 1: X Developer Portal で全ての認証情報を再取得

1. X Developer Portal で「Keys and tokens」タブを開く

2. **Consumer Keys** セクション:
   - API Key をコピー
   - API Secret Key をコピー（「Reveal」ボタンをクリック）

3. **Authentication Tokens** セクション:
   - Bearer Token をコピー
   - Access Token と Access Token Secret をコピー（既に生成済みの場合は再生成）

### Step 2: .envファイルを完全に更新

以下のすべての値を更新：

```env
# X (Twitter) API認証情報
X_API_KEY=X Developer Portal で取得したAPI Key
X_API_SECRET_KEY=iqjbHRwUUry83MRAysOtANuYKdB9sp8TMvtWYHSQ7Ti0n8UDDr
X_ACCESS_TOKEN=1318210166580412416-OkcCDApUUmH6TnXVB1SUE2IWF6kjDL
X_ACCESS_TOKEN_SECRET=ZaltrsQzGamF0sxTUNF5pIfQSJnUe91n5m1j9Fjup1B5R
X_BEARER_TOKEN=X Developer Portal で取得したBearer Token
```

### Step 3: テスト実行

```bash
python3 automation/social_media/x_twitter.py user me
```

---

## 📝 確認チェックリスト

- [ ] API Key が X Developer Portal と一致しているか
- [ ] API Secret Key が X Developer Portal と一致しているか（iqjbHRwUUry83MRAysOtANuYKdB9sp8TMvtWYHSQ7Ti0n8UDDr）
- [ ] Access Token が X Developer Portal と一致しているか（1318210166580412416-OkcCDApUUmH6TnXVB1SUE2IWF6kjDL）
- [ ] Access Token Secret が X Developer Portal と一致しているか（ZaltrsQzGamF0sxTUNF5pIfQSJnUe91n5m1j9Fjup1B5R）
- [ ] Bearer Token が X Developer Portal と一致しているか
- [ ] App permissions: 「Read and write」を選択
- [ ] .envファイルを保存

---

## 🆘 それでもエラーが出る場合

### デバッグ方法

1. **認証情報の確認:**
   ```bash
   python3 -c "from dotenv import load_dotenv; import os; load_dotenv(); print(f'API Key: {os.getenv(\"X_API_KEY\")[:10]}...'); print(f'API Secret: {os.getenv(\"X_API_SECRET_KEY\")[:10]}...')"
   ```

2. **tweepyのバージョン確認:**
   ```bash
   pip3 show tweepy
   ```

3. **詳細なエラーメッセージの確認:**
   - エラーメッセージの詳細を確認
   - X Developer Portal のエラーログを確認

---

## 💡 ヒント

- すべての認証情報を一度に再取得すると、整合性が保たれます
- Consumer Keys を再生成した場合、Access Token も再生成が必要な場合があります
- Bearer Token は通常、変更されませんが、確認することを推奨します
