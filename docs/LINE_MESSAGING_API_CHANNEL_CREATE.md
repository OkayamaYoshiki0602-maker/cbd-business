# LINE Messaging API チャネル作成ガイド

## 📋 現在の状況

現在表示されているのは「LINE MINI App」チャネルの設定画面です。
**Channel Access Token は Messaging API チャネルで取得します。**

---

## 🔍 Messaging API チャネルを確認する方法

### 方法1: LINE Developers コンソールで確認

1. LINE Developers にアクセス: https://developers.line.biz/
2. 「Providers」→「CBD WORLD」を選択
3. 「Channels」タブを開く
4. チャネル一覧を確認：
   - **Messaging API** チャネルがあるか確認
   - **LINE MINI App** チャネルとは別です

### 方法2: LINE Official Account Manager で確認

1. LINE Official Account Manager にアクセス: https://manager.line.biz/
2. 「CBD WORLD」を選択
3. 「設定」タブを開く
4. 「Messaging API」セクションを確認
   - ここにChannel Access Tokenがあるはずです

---

## 🚀 Messaging API チャネルを作成する方法

### チャネルが存在しない場合

#### Step 1: LINE Developers コンソールで作成

1. LINE Developers にアクセス: https://developers.line.biz/
2. 「Providers」→「CBD WORLD」を選択
3. 「Channels」タブを開く
4. **「チャネルを追加」または「Add channel」ボタンをクリック**
5. **「Messaging API」を選択**（LINE MINI App ではない）
6. チャネル情報を入力：
   - チャネル名: "CBD Auto Tweet Messaging API"
   - チャネル説明: "CBDサイト運営の自動化システム"
   - 大業種: 「個人」
   - 小業種: 「個人（その他）」
7. 「作成」をクリック

#### Step 2: LINE Official Account Manager で Messaging API を有効化

1. LINE Official Account Manager にアクセス: https://manager.line.biz/
2. 「CBD WORLD」を選択
3. 「設定」タブを開く
4. 「Messaging API」セクションを確認
5. 「Messaging API を有効化」をクリック（まだ有効化していない場合）

---

## 🔐 Channel Access Token の取得場所

### 推奨方法: LINE Official Account Manager経由

LINE Official Account Manager の画面（添付画像）に表示されている場合：

1. **「Messaging API」セクション**を確認
2. **「Channel Access Token」セクション**を探す
3. **「発行」または「Issue」ボタン**をクリック
4. Channel Access Token が表示される
5. **コピーして保存**

### 別の方法: LINE Developers コンソール経由

1. LINE Developers にアクセス: https://developers.line.biz/
2. 「Providers」→「CBD WORLD」を選択
3. **Messaging API チャネル**を選択（LINE MINI App ではない）
4. 「Messaging API」タブを開く
5. 「Channel access token」セクションで「Issue」をクリック

---

## 🔍 チャネルの違い

### LINE MINI App チャネル

- **用途:** ウェブアプリの配信
- **機能:** ウェブアプリの設定
- **Channel Access Token:** なし

### Messaging API チャネル

- **用途:** メッセージ送受信
- **機能:** Messaging API の設定
- **Channel Access Token:** あり（必要）

---

## 📝 確認事項

### 現在のチャネル確認

1. LINE Developers コンソールで「Channels」タブを開く
2. チャネル一覧を確認：
   - 「CBD Auto Tweet」が「LINE MINI App」になっている
   - **Messaging API チャネル**が存在するか確認

### Messaging API チャネルがない場合

- LINE Official Account Manager で Messaging API を有効化
- または、新しい Messaging API チャネルを作成

---

## 💡 推奨手順

### Step 1: LINE Official Account Manager で確認

1. https://manager.line.biz/ にアクセス
2. 「CBD WORLD」を選択
3. 「設定」→「Messaging API」を開く
4. **「Channel Access Token」セクション**を確認
5. 「発行」ボタンをクリック

### Step 2: Channel Access Token を取得

- 「発行」ボタンをクリック
- Channel Access Token が表示される
- コピーして保存

### Step 3: .envファイルに設定

```env
LINE_CHANNEL_ACCESS_TOKEN=取得したChannel_Access_Token_をここに貼り付け
```

---

## 🆘 それでも見つからない場合

### 確認事項

1. **Messaging API が有効化されているか**
   - LINE Official Account Manager で「Messaging API」セクションを確認
   - 「利用中」と表示されているか確認

2. **チャネルのタイプを確認**
   - LINE MINI App チャネルではなく、Messaging API チャネルが必要

3. **権限を確認**
   - 管理者権限があるか確認

---

## 📋 現在の設定状況

✅ **Channel ID:** 2008863419
✅ **Channel Secret:** 615da785c3f141e9e02f312c9458aa49
⏳ **Channel Access Token:** 取得待ち（LINE Official Account Manager の Messaging API セクションで取得可能）

---

詳細は `docs/LINE_CHANNEL_ACCESS_TOKEN_GUIDE.md` を参照してください。

LINE Official Account Manager の「Messaging API」セクションで「Channel Access Token」を確認してください。見つからない場合は、お知らせください。別の方法を案内します。
