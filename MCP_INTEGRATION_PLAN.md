# MCP連携プラン - 推奨設定一覧

## 📊 優先度別MCP連携候補

### 🔴 最優先（プロジェクトに必須）

#### 1. Google Drive MCP
**目的:** 記事自動生成（STEP 2）の基盤、診断ロジック管理  
**メリット:**
- スプレッドシートをDBとして活用可能
- 診断ロジックの質問・分岐を管理
- 記事ネタの管理（ターゲット、悩み、キーワード）
- Cursor内で直接スプレッドシート読み込み可能

**設定難易度:** ⭐⭐⭐（API認証必要）  
**影響度:** 高（STEP 2実装に必須）

#### 2. GitHub MCP（オプション）
**目的:** コード管理の自動化、Issue・PR管理  
**メリット:**
- Cursor内でGitHub操作（Issue作成、PR管理等）
- コードレビュー支援
- リポジトリ情報の参照

**設定難易度:** ⭐⭐（PAT取得のみ）  
**影響度:** 中（便利だが必須ではない）

---

### 🟡 次優先（効率化に有効）

#### 3. Notion MCP（オプション）
**目的:** プロジェクト管理、ドキュメント管理  
**メリット:**
- プロジェクト計画の一元管理
- 記事ネタの管理（Google Driveの代替にも）
- タスク管理との連携

**設定難易度:** ⭐⭐⭐（API認証必要）  
**影響度:** 中（便利だがGoogle Driveで代替可能）

---

### 🟢 将来的に（運用効率化）

#### 4. Slack MCP（オプション）
**目的:** 通知・連携の自動化  
**メリット:**
- 新着記事公開通知
- 診断ツールの利用通知
- エラー通知

**設定難易度:** ⭐⭐⭐（Bot設定必要）  
**影響度:** 低（現時点では不要）

#### 5. Twitter/X MCP（オプション）
**目的:** 自動投稿システム（STEP 3）と連携  
**メリット:**
- Cursor内でツイート管理
- 投稿スケジュール管理

**設定難易度:** ⭐⭐⭐⭐（API認証複雑）  
**影響度:** 中（STEP 3実装時に検討）

---

## 🎯 推奨設定順序

### Phase 1: 基盤整備（今すぐ）
1. ✅ **Git初期化・GitHub連携** ← 今ここ
2. ⏳ **Google Drive MCP** ← STEP 2実装前に必須

### Phase 2: 効率化（STEP 1実装後）
3. **GitHub MCP**（オプション）- コード管理の自動化

### Phase 3: 運用最適化（STEP 2-3実装時）
4. **Twitter/X MCP**（オプション）- 自動投稿システム連携
5. **Slack MCP**（オプション）- 通知自動化

---

## 📝 MCP設定ファイルの場所

### macOS (Cursor)
```
~/Library/Application Support/Cursor/User/globalStorage/saoudrizwan.claude-dev/settings/cline_mcp_settings.json
```

または Cursor設定内の `MCP Settings` から直接編集可能

### 設定例（JSON形式）
```json
{
  "mcpServers": {
    "google-drive": {
      "command": "npx",
      "args": [
        "-y",
        "@modelcontextprotocol/server-google-drive"
      ],
      "env": {
        "GOOGLE_DRIVE_CREDENTIALS": "/path/to/credentials.json"
      }
    },
    "github": {
      "command": "npx",
      "args": [
        "-y",
        "@modelcontextprotocol/server-github"
      ],
      "env": {
        "GITHUB_TOKEN": "your_personal_access_token"
      }
    }
  }
}
```

---

## 🔐 認証情報の管理

### 必須事項
- ✅ `.gitignore` で認証情報ファイルを除外（設定済み）
- ⚠️ 認証情報はローカルにのみ保存
- ⚠️ GitHubにプッシュする前に個人情報を確認

### 認証情報の取得手順

#### Google Drive API
1. Google Cloud Consoleでプロジェクト作成
2. Google Drive APIを有効化
3. 認証情報（JSON）をダウンロード
4. ローカルに保存（`~/.config/cursor/google-drive-credentials.json` など）

#### GitHub Personal Access Token
1. GitHub Settings → Developer settings → Personal access tokens
2. 「Generate new token (classic)」を選択
3. スコープ: `repo`, `read:org`（必要に応じて）
4. トークンをコピー（一度しか表示されないので注意）

---

## 💡 次のステップ

1. **今すぐ:** Git初期化・GitHub連携
2. **承認後:** Google Drive MCP設定（STEP 2実装前に必須）
3. **任意:** GitHub MCP設定（効率化のため）
