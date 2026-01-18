# WordPress追加CSSのGitHub自動管理

## 📋 実現可能性の調査結果

### 現状

WordPress REST APIには、**追加CSSを取得/更新する標準エンドポイントがありません**。

### 実現方法の比較

#### 方法1: WordPress REST API（標準機能） ❌ 不可

- WordPress REST APIの標準エンドポイントには、追加CSSを取得/更新する機能がない
- テーマカスタマイザーの設定はREST APIで直接操作できない

#### 方法2: カスタムプラグインを作成 ⚠️ 可能だが複雑

**実装内容:**
- WordPressプラグインを作成
- REST APIエンドポイントを追加
- 追加CSSを取得/更新するAPIを実装

**必要な作業:**
- プラグインの開発（PHP）
- WordPressサーバーへのインストール
- メンテナンスが必要

**評価:**
- ⭐⭐ 実現可能だが、開発・メンテナンスコストが高い
- 自動化のメリットより、手動コピー＆ペーストの方が効率的な場合が多い

#### 方法3: WordPress CLIを使用 ⚠️ 可能だがサーバーアクセス必要

**実装内容:**
- WordPress CLI (`wp`) を使用
- SSHアクセスが必要
- コマンドラインから追加CSSを取得/更新

**必要な作業:**
- サーバーにSSHアクセス
- WordPress CLIのインストール
- スクリプトの作成

**評価:**
- ⭐⭐ 実現可能だが、SSHアクセスが必要
- ConoHa WINGではSSHアクセスが制限されている可能性

#### 方法4: ファイルとして管理（推奨） ✅ シンプルで確実

**実装内容:**
- `wordpress/custom-css.css` ファイルとして管理
- 手動でコピー＆ペースト（または簡単なスクリプト）

**必要な作業:**
- CSSファイルを作成
- WordPressに手動でコピー＆ペースト

**評価:**
- ⭐⭐⭐⭐⭐ 最もシンプルで確実
- 自動化のコストを考えると、この方法が最適
- GitHubでバージョン管理は可能

---

## 🎯 推奨アプローチ

### 現時点での推奨: ファイルとして管理

**理由:**
1. **コスト対効果**: 自動化の開発コスト > 手動コピー＆ペーストの時間コスト
2. **確実性**: ファイルとして管理すれば、GitHubで完全にバージョン管理できる
3. **シンプルさ**: 複雑なプラグイン開発が不要

**運用フロー:**
1. `wordpress/custom-css.css` を編集
2. Gitでコミット・プッシュ
3. WordPress管理画面でコピー＆ペースト（数分の作業）

---

## 🔄 将来的な自動化の可能性

### 条件が整った場合の自動化案

#### 条件1: SSHアクセスが可能になった場合

WordPress CLIを使用した自動同期スクリプトを作成可能：

```bash
# WordPressから追加CSSを取得
wp theme mod get custom_css > wordpress/custom-css.css

# GitHubからWordPressに同期
cat wordpress/custom-css.css | wp theme mod set custom_css
```

#### 条件2: カスタムプラグインの開発が可能になった場合

REST APIエンドポイントを追加するプラグインを作成可能：

```php
// プラグインでREST APIエンドポイントを追加
add_action('rest_api_init', function() {
    register_rest_route('custom/v1', '/css', array(
        'methods' => 'GET',
        'callback' => 'get_custom_css',
    ));
    register_rest_route('custom/v1', '/css', array(
        'methods' => 'POST',
        'callback' => 'update_custom_css',
        'permission_callback' => 'is_user_logged_in',
    ));
});
```

---

## 📝 結論

### 現時点での推奨

**ファイルとして管理（手動コピー＆ペースト）** を推奨します。

**理由:**
- ✅ GitHubでバージョン管理可能
- ✅ シンプルで確実
- ✅ 開発コストが低い
- ✅ 自動化のメリットが限定的（CSSの変更頻度は低い）

### 自動化を検討する条件

以下の条件が整った場合、自動化を検討する価値があります：

1. CSSの変更頻度が非常に高い（週に複数回など）
2. SSHアクセスが可能になった
3. カスタムプラグインの開発・メンテナンスが可能になった

---

## 🔗 参考情報

- `docs/WORDPRESS_CSS_SYNC.md` - WordPress追加CSSのGitHub管理ガイド（手動版）
