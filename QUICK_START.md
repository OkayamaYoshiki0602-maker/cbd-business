# MCP連携クイックスタートガイド

## 🎯 あなたがやること vs 私がやること

### ✅ 私が自動でやること（準備済み）
- ✅ MCP設定ファイルのテンプレート作成
- ✅ 設定ファイルを自動生成するスクリプト準備
- ✅ 詳細な手順書作成

### 🔴 あなたがやること（必須）
1. **GitHub PAT取得**（5分）- 自分でログインして取得
2. **Google Drive API認証情報取得**（10-15分）- 自分でログインして取得

---

## 🚀 最短手順（私が自動設定）

### 方法A: スクリプトを使う（自動化・推奨）

1. **GitHub PATを取得**（手順は後述）
2. **Google Drive JSONファイルを取得**（手順は後述）
3. **以下のコマンドを実行:**

```bash
cd "/Users/okayamayoshiki/Library/CloudStorage/GoogleDrive-okayamayoshiki0602o@gmail.com/マイドライブ/cursor"
./setup_mcp.sh
```

4. **PATとJSONファイルのパスを入力**
5. **Cursorを再起動**

---

### 方法B: 私に直接教えてもらう

1. **GitHub PATを取得して私に教える**
2. **Google Drive JSONファイルを取得して配置場所を教える**
3. **私が自動的に設定ファイルに追加します**

---

## 📋 あなたがやる具体的な手順

### PART 1: GitHub PAT取得（5分）

**超シンプル版:**

1. https://github.com/settings/tokens にアクセス
2. 「Generate new token (classic)」をクリック
3. **Note:** `Cursor MCP Integration` と入力
4. **Expiration:** 1年（お好みで）
5. **Select scopes:** ✅ `repo`（すべて）、✅ `read:org` にチェック
6. 「Generate token」をクリック
7. **`ghp_` で始まる文字列をコピー**（一度しか表示されない！）

**詳細手順:** `SETUP_STEP_BY_STEP.md` の「PART 1」を参照

---

### PART 2: Google Drive API認証情報取得（10-15分）

**超シンプル版:**

1. https://console.cloud.google.com にアクセス
2. 新しいプロジェクトを作成（名前: `cbd-side-business`）
3. 「APIとサービス」→「ライブラリ」→「Google Drive API」を検索→「有効にする」
4. 「APIとサービス」→「認証情報」→「認証情報を作成」→「サービスアカウント」
5. サービスアカウントを作成（名前: `cursor-mcp`）
6. 「キー」タブ→「キーを追加」→「新しいキーを作成」→「JSON」を選択
7. **JSONファイルがダウンロードされる**
8. **以下のコマンドで移動:**

```bash
# ダウンロードしたJSONファイルを確認（ファイル名は実際のものに置き換える）
ls ~/Downloads/*.json

# ファイルを移動してリネーム（ファイル名は実際のものに置き換える）
mv ~/Downloads/cbd-side-business-xxxxx-xxxxxxxxxxxx.json ~/.config/cursor/google-drive-credentials.json
```

**詳細手順:** `SETUP_STEP_BY_STEP.md` の「PART 2」を参照

---

## 💡 次にやること

### ステップ1: GitHub PAT取得
- 上記の「PART 1」を実行
- PAT（`ghp_` で始まる文字列）をコピー

### ステップ2: 私にPATを教える、またはスクリプトを実行
- **方法A:** 私にPATを教えてもらえれば、自動的に設定ファイルに追加します
- **方法B:** `./setup_mcp.sh` を実行して、PATを入力

### ステップ3: Google Drive JSON取得（STEP 2実装前に必須）
- 上記の「PART 2」を実行
- JSONファイルを `~/.config/cursor/google-drive-credentials.json` に配置

### ステップ4: 私に確認してもらう、またはスクリプトを実行
- **方法A:** 配置が完了したら私に教えてください
- **方法B:** `./setup_mcp.sh` を実行して、JSONファイルのパスを入力

### ステップ5: Cursor再起動
- Cursorを完全に終了（`Cmd + Q`）
- Cursorを再起動

---

## ❓ よくある質問

### Q: GitHub PATは必須ですか？
A: 必須ではありませんが、コード管理が便利になります。後からでも設定可能です。

### Q: Google Drive JSONは必須ですか？
A: STEP 2（自動記事生成）の実装前に必須です。今すぐでなくてもOKです。

### Q: 手順が分からない
A: `SETUP_STEP_BY_STEP.md` に詳細な手順を記載しています。スクリーンショットがあれば、より具体的に案内できます。

---

## 🎯 今すぐ始めるなら

**まずはGitHub PAT取得から始めましょう！**

1. https://github.com/settings/tokens にアクセス
2. 「Generate new token (classic)」をクリック
3. スコープで `repo` と `read:org` にチェック
4. 生成されたトークン（`ghp_` で始まる文字列）をコピー
5. **私に教えてください！** 自動的に設定ファイルに追加します
