# WordPress GitHub同期前のバックアップガイド

## 📋 概要

WordPressからGitHubに同期する前に、既存のファイルをバックアップする方法です。

GitHubでバックアップを管理できるため、簡単かつ安全です。

---

## 🎯 バックアップ方法

### 方法1: Gitで現在の状態をコミット（推奨）⭐

最も簡単で安全な方法です。現在の状態をGitにコミットすることで、いつでも元に戻せます。

#### Step 1: 現在の状態を確認

```bash
cd "/Users/okayamayoshiki/Library/CloudStorage/GoogleDrive-okayamayoshiki0602o@gmail.com/マイドライブ/cursor"
git status
```

#### Step 2: 変更がある場合はコミット

```bash
# 変更を確認
git status

# 変更がある場合、コミットしてバックアップ
git add .
git commit -m "Backup before syncing from WordPress"

# GitHubにプッシュ
git push origin main
```

これで、現在の状態がGitHubに保存され、いつでも元に戻せます。

---

### 方法2: バックアップブランチを作成（より安全）⭐⭐

既存のファイルを別ブランチにバックアップする方法です。

#### Step 1: 現在の状態をコミット

```bash
git status
git add .
git commit -m "Current state before WordPress sync"
```

#### Step 2: バックアップブランチを作成

```bash
# バックアップブランチを作成
git checkout -b backup-before-wordpress-sync

# バックアップブランチをGitHubにプッシュ
git push origin backup-before-wordpress-sync

# 元のブランチ（main）に戻る
git checkout main
```

これで、`backup-before-wordpress-sync`ブランチに現在の状態が保存されます。

---

## 🔄 完全な作業フロー（推奨）

### Step 1: 現在の状態をバックアップ

```bash
cd "/Users/okayamayoshiki/Library/CloudStorage/GoogleDrive-okayamayoshiki0602o@gmail.com/マイドライブ/cursor"

# 現在の状態を確認
git status

# 変更がある場合、コミット
git add .
git commit -m "Backup: Before WordPress sync"
git push origin main
```

### Step 2: WordPressから同期

```bash
# WordPressから同期スクリプトを実行
python3 automation/scripts/sync_from_wordpress.py
```

### Step 3: 変更を確認

```bash
# どのファイルが変更・追加されたか確認
git status

# 具体的な変更内容を確認（オプション）
git diff wordpress/posts/
git diff wordpress/pages/
```

### Step 4: 変更をコミット・プッシュ

```bash
# ファイルを追加
git add wordpress/posts/ wordpress/pages/

# コミット
git commit -m "Sync posts and pages from WordPress"

# GitHubにプッシュ
git push origin main
```

---

## 🔙 元に戻す方法

### 方法1: Gitで特定のファイルを元に戻す

```bash
# 特定のファイルを元に戻す
git checkout HEAD -- wordpress/posts/specific-file.html

# または、すべてのファイルを元に戻す
git checkout HEAD -- wordpress/posts/ wordpress/pages/
```

### 方法2: 直前のコミットを取り消す

```bash
# 直前のコミットを取り消す（ファイルは変更状態のまま）
git reset HEAD~1

# 変更を破棄する場合
git reset --hard HEAD~1
```

**注意:** `--hard`オプションは変更を完全に削除するため、慎重に使用してください。

### 方法3: バックアップブランチから復元

```bash
# バックアップブランチからファイルを復元
git checkout backup-before-wordpress-sync -- wordpress/posts/ wordpress/pages/

# 変更をコミット
git add wordpress/posts/ wordpress/pages/
git commit -m "Restore from backup branch"
```

---

## 📝 Git履歴でバックアップポイントを確認

```bash
# コミット履歴を確認
git log --oneline

# 特定のコミットの内容を確認
git show [コミットハッシュ]

# 特定のコミット時点のファイルを確認
git checkout [コミットハッシュ] -- wordpress/posts/
```

---

## ⚠️ 注意事項

### Gitのバックアップの特徴

**メリット:**
- ✅ GitHubに保存されるため、ローカルファイルが失われても復元可能
- ✅ 変更履歴を完全に記録
- ✅ 特定の時点に簡単に戻れる
- ✅ ブランチで複数のバックアップを管理可能

**デメリット:**
- ⚠️ 大きなファイルを保存するとリポジトリサイズが大きくなる
- ⚠️ コミット履歴が増える

### 推奨事項

1. **同期前に必ずコミット** - 現在の状態をGitHubに保存
2. **変更を確認してからコミット** - 同期後の変更内容を確認
3. **重要な変更はバックアップブランチを作成** - より安全

---

## 🔗 参考情報

- `docs/WORDPRESS_TO_GITHUB_SYNC.md` - WordPressからGitHubへの同期ガイド
- `docs/GITHUB_PUSH_GUIDE.md` - GitHubへのプッシュ方法

---

## 📋 クイックリファレンス

```bash
# バックアップ（現在の状態をコミット）
git add .
git commit -m "Backup: Before WordPress sync"
git push origin main

# WordPressから同期
python3 automation/scripts/sync_from_wordpress.py

# 変更を確認
git status

# 変更をコミット
git add wordpress/posts/ wordpress/pages/
git commit -m "Sync posts and pages from WordPress"
git push origin main

# 元に戻す（必要に応じて）
git checkout HEAD -- wordpress/posts/ wordpress/pages/
```
