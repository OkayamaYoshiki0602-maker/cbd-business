# ディレクトリ構成ルール

## 📁 プロジェクト構造

```
cursor/
├── .cursorrules              # Cursor最適化ルール（ルートに配置）
├── .gitignore                # Git除外設定（ルートに配置）
├── README.md                 # プロジェクト概要（ルートに配置）
├── identity.md               # ユーザープロフィール（ルートに配置）
│
├── docs/                     # ドキュメント類
│   ├── PROJECT_PLAN.md       # 詳細プロジェクト計画
│   ├── WORKFLOW.md           # ワークフロー・自動化手順
│   ├── DIAGNOSIS_LOGIC_PROPOSAL.md  # 診断ロジック案
│   ├── SETUP_GUIDE.md        # 開発環境セットアップガイド
│   ├── SETUP_ACTION_PLAN.md  # セットアップ実行プラン
│   ├── SETUP_STEP_BY_STEP.md # MCP連携詳細手順
│   ├── MCP_INTEGRATION_PLAN.md  # MCP連携プラン
│   ├── MCP_SETUP_INSTRUCTIONS.md  # MCP設定手順
│   ├── GITHUB_REPO_SETUP.md  # GitHubリポジトリ作成手順
│   ├── QUICK_START.md        # クイックスタートガイド
│   ├── NEXT_STEPS.md         # 次のステップガイド
│   └── DIRECTORY_STRUCTURE.md  # このファイル
│
├── config/                   # 設定ファイル・テンプレート
│   ├── mcp_settings_template.json  # MCP設定テンプレート
│   └── credentials/          # 認証情報（.gitignoreで除外）
│       └── .gitkeep          # ディレクトリを保持
│
└── scripts/                  # 自動化スクリプト
    └── setup_mcp.sh          # MCP設定自動化スクリプト
```

---

## 📋 分類ルール

### ルート直下（プロジェクトの根幹）

以下のファイルは**ルートに配置**します：

- **`.cursorrules`** - Cursor最適化ルール（Cursorが自動読み込み）
- **`.gitignore`** - Git除外設定（Gitが自動読み込み）
- **`README.md`** - プロジェクト概要（GitHubで自動表示）
- **`identity.md`** - ユーザープロフィール（プロジェクトの根幹情報）

**理由:** 各ツールがルート直下で自動的に読み込むため

---

### `docs/` ディレクトリ（ドキュメント類）

以下のファイルは**`docs/`ディレクトリに配置**します：

- **プロジェクト計画・戦略関連:**
  - `PROJECT_PLAN.md` - 詳細プロジェクト計画
  - `WORKFLOW.md` - ワークフロー・自動化手順
  - `DIAGNOSIS_LOGIC_PROPOSAL.md` - 診断ロジック案

- **セットアップ・導入関連:**
  - `SETUP_GUIDE.md` - 開発環境セットアップガイド
  - `SETUP_ACTION_PLAN.md` - セットアップ実行プラン
  - `SETUP_STEP_BY_STEP.md` - MCP連携詳細手順
  - `GITHUB_REPO_SETUP.md` - GitHubリポジトリ作成手順
  - `QUICK_START.md` - クイックスタートガイド

- **MCP連携関連:**
  - `MCP_INTEGRATION_PLAN.md` - MCP連携プラン
  - `MCP_SETUP_INSTRUCTIONS.md` - MCP設定手順

- **その他:**
  - `NEXT_STEPS.md` - 次のステップガイド
  - `DIRECTORY_STRUCTURE.md` - ディレクトリ構成ルール（このファイル）

**理由:** ドキュメントを一箇所にまとめて管理しやすくするため

---

### `config/` ディレクトリ（設定ファイル・テンプレート）

以下のファイルは**`config/`ディレクトリに配置**します：

- **設定テンプレート:**
  - `mcp_settings_template.json` - MCP設定テンプレート

- **認証情報（`.gitignore`で除外）:**
  - `credentials/` - 認証情報を配置するディレクトリ
    - `.gitkeep` - ディレクトリをGitで保持（認証情報は除外）

**理由:** 設定ファイルとテンプレートを分類し、認証情報を安全に管理するため

**注意:** 認証情報は**絶対にGitにコミットしない**（`.gitignore`で除外済み）

---

### `scripts/` ディレクトリ（自動化スクリプト）

以下のファイルは**`scripts/`ディレクトリに配置**します：

- **自動化スクリプト:**
  - `setup_mcp.sh` - MCP設定自動化スクリプト

**理由:** 実行可能なスクリプトを分類し、管理しやすくするため

---

## 🔄 ファイル移動時の注意事項

### Git管理
- ファイル移動時は `git mv` を使用することで、Gitの履歴を保持できます
- 移動後、コミットして変更を記録します

### パスの更新
- 設定ファイルやスクリプト内のパス参照があれば、移動後に更新が必要です

---

## 🚀 将来的なディレクトリ構成

プロジェクトが成長したら、以下を追加：

```
cursor/
├── diagnosis-tools/    # 診断ツール関連コード（STEP 1）
│   └── cbd-personal-diagnosis.html
├── automation/         # 自動化スクリプト（Python/GAS）
│   ├── x-autopost/
│   └── article-generator/
└── wordpress-theme/    # WordPressテーマ関連
    └── swell-child/
```

---

## 📝 ファイル追加時のルール

### 新しいファイルを追加する時

1. **ドキュメント（`.md`）** → `docs/` に配置
2. **設定ファイル・テンプレート** → `config/` に配置
3. **スクリプト（`.sh`, `.py`等）** → `scripts/` に配置
4. **認証情報（`.json`, `.key`等）** → `config/credentials/` に配置（`.gitignore`で除外）
5. **プロジェクト根幹ファイル** → ルートに配置

### 例外

- `.cursorrules`, `.gitignore`, `README.md`, `identity.md` は**常にルート**に配置

---

## ✅ チェックリスト

ファイル移動時：
- [ ] 適切なディレクトリに配置したか確認
- [ ] `git mv` を使用して移動したか確認
- [ ] パス参照を更新したか確認
- [ ] コミットしたか確認
