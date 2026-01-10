# GoogleサービスAPI有効化手順

## 📋 概要

既存のGoogle Cloudプロジェクト（`acoustic-skein-329303`）に、以下のAPIを追加で有効化します：

1. ✅ **Google Drive API**（既に有効化済み）
2. ⏳ **Google Calendar API**（新規有効化）
3. ⏳ **Gmail API**（新規有効化）
4. ⏳ **Google Sheets API**（新規有効化）
5. ⏳ **Google Analytics Data API**（新規有効化、GA4用）

---

## 🚀 手順（あなたがやること）

### STEP 1: Google Cloud Consoleにアクセス

1. **ブラウザで https://console.cloud.google.com にアクセス**
2. **既存のプロジェクトを選択**
   - プロジェクト名: `acoustic-skein-329303`
   - または プロジェクトID: `acoustic-skein-329303`

### STEP 2: APIとサービス → ライブラリに移動

1. **左メニューの「APIとサービス」をクリック**
2. **「ライブラリ」をクリック**

### STEP 3: 各APIを有効化

#### 3-1. Google Calendar API

1. **検索ボックスに「Google Calendar API」と入力**
2. **検索結果から「Google Calendar API」を選択**
3. **「有効にする」をクリック**
4. 有効化完了まで待つ（数秒〜1分）

#### 3-2. Gmail API

1. **検索ボックスに「Gmail API」と入力**
2. **検索結果から「Gmail API」を選択**
3. **「有効にする」をクリック**
4. 有効化完了まで待つ

#### 3-3. Google Sheets API

1. **検索ボックスに「Google Sheets API」と入力**
2. **検索結果から「Google Sheets API」を選択**
3. **「有効にする」をクリック**
4. 有効化完了まで待つ

#### 3-4. Google Analytics Data API（GA4用）

1. **検索ボックスに「Google Analytics Data API」と入力**
2. **検索結果から「Google Analytics Data API」を選択**
3. **「有効にする」をクリック**
4. 有効化完了まで待つ

---

## ✅ 確認方法

### 有効化されたAPIを確認

1. **左メニューの「APIとサービス」→「有効なAPI」をクリック**
2. **以下のAPIが表示されることを確認：**
   - ✅ Google Drive API
   - ✅ Google Calendar API
   - ✅ Gmail API
   - ✅ Google Sheets API
   - ✅ Google Analytics Data API

---

## 🔍 既存のサービスアカウント情報

以下のサービスアカウントが既に作成済みです：

- **サービスアカウント名:** `cursor-mcp`
- **サービスアカウントID:** `cursor-mcp@acoustic-skein-329303.iam.gserviceaccount.com`
- **認証情報ファイル:** `~/.config/cursor/google-drive-credentials.json`

**このサービスアカウントは、全てのGoogle APIで使用可能です。**

---

## 📝 チェックリスト

- [ ] Google Calendar APIを有効化
- [ ] Gmail APIを有効化
- [ ] Google Sheets APIを有効化
- [ ] Google Analytics Data APIを有効化
- [ ] 有効なAPI一覧で全てのAPIが表示されることを確認

---

## 🚀 次のステップ

API有効化後：
1. ✅ 各サービスで権限を付与（次の手順）
2. ✅ Cursorを再起動してMCP連携を確認

詳細は [`GOOGLE_SERVICES_MCP_SETUP.md`](GOOGLE_SERVICES_MCP_SETUP.md) を参照してください。
