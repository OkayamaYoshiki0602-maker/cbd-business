# X Developer Portal 設定ガイド

## 📋 必要な設定

X APIでツイート投稿を行うために、以下の設定が必要です。

---

## 🔐 1. App permissions（アプリ権限）の設定

### 現在の状態
- 「Read」が選択されている

### 必要な設定
**「Read and write」または「Read and write and Direct message」を選択してください**

### 設定手順
1. 「App permissions」セクションで「Read and write」を選択
   - または「Read and write and Direct message」を選択（将来的にDM機能を使う場合）
2. 「Save」ボタンをクリック

### 理由
- ツイート投稿には「Read and write」以上の権限が必要です
- 「Read」のみでは、ツイートの読み取りしかできません

---

## 📱 2. Type of App（アプリタイプ）の設定

### 現在の状態
- どちらも選択されていない（または選択が必要）

### 必要な設定
**「Web App, Automated App or Bot」を選択してください**

### 設定手順
1. 「Type of App」セクションで「Web App, Automated App or Bot」を選択
2. 「Save」ボタンをクリック

### 理由
- サーバーサイドで実行する自動化スクリプトには「Web App」が適しています
- 「Native App」はモバイルアプリ向けの設定です

---

## 📝 3. App info（アプリ情報）の設定

### 必須項目

#### Callback URI / Redirect URL（必須）
```
http://localhost:3000/callback
```
または
```
https://cbd-no-hito.com/callback
```

**推奨:** 開発中は `http://localhost:3000/callback` を使用

#### Website URL（必須）
```
https://cbd-no-hito.com
```

### 任意項目（推奨）

#### Organization name（任意）
```
CBD WORLD
```

#### Organization URL（任意）
```
https://cbd-no-hito.com
```

#### Terms of service（任意）
```
https://cbd-no-hito.com/terms
```
（利用規約ページがある場合）

#### Privacy policy（任意）
```
https://cbd-no-hito.com/privacy
```
（プライバシーポリシーページがある場合）

### 設定手順
1. 「Settings」タブを開く
2. 「App details」セクションで「Edit」ボタンをクリック
3. 上記の情報を入力
4. 「Save」ボタンをクリック

---

## ✅ 設定完了チェックリスト

- [ ] App permissions: 「Read and write」を選択
- [ ] Type of App: 「Web App, Automated App or Bot」を選択
- [ ] Callback URI / Redirect URL: `http://localhost:3000/callback` を設定
- [ ] Website URL: `https://cbd-no-hito.com` を設定
- [ ] Organization name: `CBD WORLD` を設定（任意）
- [ ] Organization URL: `https://cbd-no-hito.com` を設定（任意）
- [ ] すべての設定を保存

---

## 🚀 設定後の確認

設定が完了したら、以下で確認：

1. **認証情報の再確認**
   - Access Token と Access Token Secret が有効であることを確認
   - 必要に応じて再生成

2. **テスト実行**
   ```bash
   python3 automation/social_media/x_twitter.py user me
   ```

---

## ⚠️ 注意事項

### App permissions を変更した場合
- Access Token と Access Token Secret が無効になる可能性があります
- その場合は、再生成が必要です：
  1. 「Keys and tokens」タブを開く
  2. 「Access Token and Secret」セクションで「Generate」ボタンをクリック
  3. 新しいAccess Token と Access Token Secret をコピー
  4. `.env`ファイルを更新

### Type of App を変更した場合
- 通常、Access Token の再生成は不要です
- ただし、エラーが出た場合は再生成を試してください

---

## 📝 設定例（コピー&ペースト用）

### App info 設定例

```
Callback URI / Redirect URL: http://localhost:3000/callback
Website URL: https://cbd-no-hito.com
Organization name: CBD WORLD
Organization URL: https://cbd-no-hito.com
Terms of service: （空欄でもOK）
Privacy policy: （空欄でもOK）
```

---

設定が完了したら、お知らせください。テストを実行します！
