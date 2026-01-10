# MCP連携動作確認手順

## ✅ 現在の状態

### 設定済み
- ✅ **各API有効化済み**（Google Calendar API, Gmail API, Google Sheets API, Google Analytics Data API）
- ✅ **サービスアカウント**: `cursor-mcp@acoustic-skein-329303.iam.gserviceaccount.com`（オーナー権限）
- ✅ **MCP設定ファイル**: 全サービス追加済み
- ✅ **認証情報ファイル**: `~/.config/cursor/google-drive-credentials.json`

---

## 🚀 動作確認手順

### STEP 1: Cursorを再起動

1. **Cursorを完全に終了**
   - `Cmd + Q` で完全に終了
   - または メニューから「Quit Cursor」

2. **Cursorを再起動**

3. **起動時の確認**
   - MCPサーバーの起動メッセージを確認
   - エラーメッセージが出ていないか確認

---

### STEP 2: MCPサーバーの動作確認

#### 確認方法1: CursorのMCP設定から確認

1. **Cursorの設定を開く**
   - `Cmd + ,` または メニューから「Settings」

2. **「Features」→「MCP」セクションを確認**
   - 各MCPサーバーが表示されているか確認
   - エラーがないか確認

#### 確認方法2: Cursor内で直接確認

Cursorで私に以下のように聞いてください：

```
MCPサーバーの動作状況を確認してください
```

または、各サービスをテスト：

```
GitHub MCPが動作しているか確認してください
Google Drive MCPが動作しているか確認してください
Google Calendar MCPが動作しているか確認してください
Gmail MCPが動作しているか確認してください
Google Sheets MCPが動作しているか確認してください
GA4 MCPが動作しているか確認してください
```

---

### STEP 3: 各サービスの機能テスト

#### GitHub MCP
- 「GitHubのリポジトリ一覧を表示してください」
- 「このプロジェクトのGitHubリポジトリ情報を取得してください」

#### Google Drive MCP
- 「Google Driveのファイル一覧を表示してください」
- 「Google Driveから特定のスプレッドシートを読み込んでください」

#### Google Calendar MCP
- 「Googleカレンダーの今週の予定を表示してください」
- 「Googleカレンダーに新しいイベントを作成してください」

#### Gmail MCP
- 「Gmailの未読メール一覧を表示してください」
- 「Gmailでメールを送信してください」

#### Google Sheets MCP
- 「Googleスプレッドシートからデータを読み込んでください」
- 「Googleスプレッドシートにデータを書き込んでください」

#### GA4 MCP
- 「GA4のアクセス解析データを取得してください」
- 「GA4のPV数やセッション数を表示してください」

---

## ⚠️ エラーが発生した場合

### エラー1: MCPサーバーパッケージが見つからない

**症状:**
- `@modelcontextprotocol/server-google-calendar` などのパッケージが見つからない

**原因:**
- 実際に存在しないパッケージ名を使用している可能性

**対応:**
1. 実際に利用可能なMCPサーバーパッケージを確認
2. 正しいパッケージ名に修正
3. または、汎用のGoogle API MCPサーバーを使用

### エラー2: 認証エラー

**症状:**
- `authentication failed` などの認証エラー

**原因:**
- 認証情報ファイルのパスが間違っている
- サービスアカウントに権限がない

**対応:**
1. 認証情報ファイルのパスを確認（`~/.config/cursor/google-drive-credentials.json`）
2. サービスアカウントの権限を確認
3. 各サービスでサービスアカウントが共有されているか確認

### エラー3: APIが有効化されていない

**症状:**
- `API not enabled` などのエラー

**原因:**
- APIが有効化されていない

**対応:**
1. Google Cloud ConsoleでAPIが有効化されているか確認
2. 必要なAPIを有効化

---

## 📋 チェックリスト

### 設定確認
- [ ] 各APIが有効化されているか確認
- [ ] サービスアカウントがオーナー権限になっているか確認
- [ ] MCP設定ファイルが正しく更新されているか確認
- [ ] 認証情報ファイルが正しい場所にあるか確認

### 動作確認
- [ ] Cursorを再起動
- [ ] MCPサーバーが正常に起動しているか確認
- [ ] 各サービスの機能が動作しているか確認

---

## 🔍 トラブルシューティング

### MCPサーバーが起動しない場合

1. **Cursorのログを確認**
   - Cursorの設定からログを確認
   - エラーメッセージを確認

2. **Node.jsがインストールされているか確認**
   ```bash
   node --version
   npm --version
   ```

3. **npxが動作するか確認**
   ```bash
   npx --version
   ```

### 認証情報の確認

認証情報ファイルが正しい場所にあるか確認：

```bash
ls -la ~/.config/cursor/google-drive-credentials.json
```

認証情報ファイルが存在しない、または破損している場合：

1. Google Cloud Consoleから新しい認証情報をダウンロード
2. `~/.config/cursor/google-drive-credentials.json` に配置

---

## 💡 次のステップ

動作確認後：
1. ✅ 各サービスが正常に動作することを確認
2. ✅ 必要に応じてパッケージ名や設定を修正
3. ✅ 診断ツール実装（STEP 1）に進む

---

## 📝 参考

- [`GOOGLE_SERVICES_MCP_SETUP.md`](GOOGLE_SERVICES_MCP_SETUP.md) - セットアップ全体ガイド
- [`GOOGLE_SERVICES_API_ENABLE.md`](GOOGLE_SERVICES_API_ENABLE.md) - API有効化手順
- [`GOOGLE_SERVICES_PERMISSIONS.md`](GOOGLE_SERVICES_PERMISSIONS.md) - 権限設定手順
