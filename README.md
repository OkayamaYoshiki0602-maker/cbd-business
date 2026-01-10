# CBD Side Business Ecosystem

CursorとAIを活用し、CBDアフィリエイトサイトの収益化と、各SNS・ツールを連携させた自動収益化エコシステムの構築を目指すプロジェクト。

## 📁 プロジェクト構造

```
cursor/
├── .cursorrules              # Cursor最適化ルール
├── .gitignore                # Git除外設定
├── README.md                 # このファイル
├── identity.md               # ユーザープロフィール・ビジョン
├── DIRECTORY_STRUCTURE.md    # ディレクトリ構成ルール
│
├── docs/                     # ドキュメント類
│   ├── PROJECT_PLAN.md       # 詳細プロジェクト計画
│   ├── WORKFLOW.md           # ワークフロー・自動化手順
│   ├── DIAGNOSIS_LOGIC_PROPOSAL.md  # 診断ロジック案
│   ├── SETUP_GUIDE.md        # 開発環境セットアップガイド
│   └── ...                   # その他ドキュメント
│
├── config/                   # 設定ファイル・テンプレート
│   ├── mcp_settings_template.json  # MCP設定テンプレート
│   └── credentials/          # 認証情報（.gitignoreで除外）
│
└── scripts/                  # 自動化スクリプト
    └── setup_mcp.sh          # MCP設定自動化スクリプト
```

詳細は [`DIRECTORY_STRUCTURE.md`](DIRECTORY_STRUCTURE.md) を参照。

## プロジェクト概要

### 目標
- **短期（2024 Q1-Q2）:** 固定費（約10万円）の完全回収
- **中期（2024 End）:** 副業収益で本業（月50万円）を上回る
- **長期（2027, Age 30）:** 総資産1,000万円突破

### 戦略
現在のCBDサイト（PV: 約10/日）で、CVR 10%を達成すれば毎日1件成約 → 固定費回収可能

## システム構成

### コアツール連携
| ツール | 役割 | 自動化内容 |
|--------|------|-----------|
| **WordPress (SWELL)** | 収益の柱 | 診断ツール実装、SEO記事自動生成 |
| **GitHub** | ソース管理 | テーマコード、診断ロジック、Pythonスクリプト |
| **Google Drive (MCP)** | 知識基盤 | スプレッドシートをDB化（診断ロジック・投稿ネタ管理） |
| **X (Twitter)** | 集客・拡散 | 記事公開連動の自動ツイート（1,000フォロワー活用） |
| **TikTok/Instagram** | 認知拡大 | AIによる動画台本作成、画像自動生成、予約投稿 |
| **LINE Official** | CVR向上 | 診断ツールからの誘導、パーソナル提案 |

## 開発・運用ルール

### 必須原則
1. **承認制:** 全ての実行（ファイル作成、コード反映、デプロイ）前に承認を得ること
2. **データドリブン:** 提案には数値的根拠または図解イメージを含める
3. **自動化優先:** 単発施策ではなく「仕組み化」を最優先
4. **Identity参照:** 常に `@identity.md` を参照し、ユーザーの背景を反映

### 開発フロー
1. 提案作成（数値・図解付き）
2. ユーザー承認待ち
3. 実装
4. GitHubへコミット（すべてのコードはGitHub管理）
5. 動作確認・ドキュメント更新

## 短期マイルストーン（2024 Q1-Q2）

- [ ] 診断ツールのロジック確定とプロトタイプ作成
- [ ] WordPressテーマコードのGitHubリポジトリ化
- [ ] Google Drive上のスプレッドシートとCursorのMCP連携最適化
- [ ] X自動投稿システムのプロトタイプ作成

## クイックスタート

### セットアップ
1. [`docs/SETUP_GUIDE.md`](docs/SETUP_GUIDE.md) を参照
2. [`docs/QUICK_START.md`](docs/QUICK_START.md) を参照

### MCP連携
1. [`docs/MCP_SETUP_INSTRUCTIONS.md`](docs/MCP_SETUP_INSTRUCTIONS.md) を参照
2. [`docs/SETUP_STEP_BY_STEP.md`](docs/SETUP_STEP_BY_STEP.md) を参照

### GitHubリポジトリ作成
1. [`docs/GITHUB_REPO_SETUP.md`](docs/GITHUB_REPO_SETUP.md) を参照

## 参考情報

- **サイト:** https://cbd-no-hito.com/
- **X:** @yo_nandakanda (1,000 followers)
- **TikTok:** 1,200 followers
- **スキルセット:** SQL, GCP, Python, WordPress, データコンサル

## 関連ドキュメント

- [`identity.md`](identity.md) - ユーザープロフィール・ビジョン
- [`DIRECTORY_STRUCTURE.md`](DIRECTORY_STRUCTURE.md) - ディレクトリ構成ルール
- [`docs/PROJECT_PLAN.md`](docs/PROJECT_PLAN.md) - 詳細プロジェクト計画
- [`docs/WORKFLOW.md`](docs/WORKFLOW.md) - ワークフロー・自動化手順
- [`docs/NEXT_STEPS.md`](docs/NEXT_STEPS.md) - 次のステップガイド
