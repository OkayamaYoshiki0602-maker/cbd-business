# アフィリエイトリンク自動化・GA4連携提案

## 🎯 目的

1. **アフィリエイトリンクの作成・貼り付けを簡略化**
2. **アフィリエイトリンクのクリックを自動でGA4に送信**

---

## 📋 現状の課題

- 毎回アフィリエイトリンクを作成して貼り付けている
- 手作業でGA4連携を設定する必要がある
- 時間がかかる

---

## 🚀 解決策

### 方法A: WordPressショートコード + Google Tag Manager（推奨）

#### メリット
- ✅ コードを書かずに実装可能
- ✅ 管理が簡単
- ✅ アフィリエイトリンクを簡単に挿入できる
- ✅ GA4連携が自動化される

#### 実装内容

1. **WordPressショートコードの作成**
   - ショートコード: `[affiliate url="商品URL" text="リンクテキスト"]`
   - 使用例: `[affiliate url="https://amazon.co.jp/dp/XXXXX" text="おすすめCBDオイル"]`

2. **Google Tag Managerの設定**
   - アフィリエイトリンクのクリックを自動検出
   - GA4にイベントを自動送信

---

### 方法B: WordPressプラグイン（MonsterInsights等）

#### メリット
- ✅ プラグインをインストールするだけ
- ✅ 設定が簡単
- ✅ 既存のプラグインを活用

#### デメリット
- ⚠️ 有料プラグインの場合がある
- ⚠️ カスタマイズの自由度が低い

---

### 方法C: カスタムWordPressプラグイン（完全自動化）

#### メリット
- ✅ 完全にカスタマイズ可能
- ✅ アフィリエイトリンクの管理が一元化
- ✅ GA4連携が自動化される

#### デメリット
- ⚠️ 開発時間がかかる
- ⚠️ メンテナンスが必要

---

## 🎯 推奨アプローチ：方法A（WordPressショートコード + Google Tag Manager）

### Phase 1: WordPressショートコードの作成（30分）

#### Step 1: 子テーマのfunctions.phpに追加

```php
<?php
/**
 * アフィリエイトリンクショートコード
 * 使用方法: [affiliate url="商品URL" text="リンクテキスト" class="custom-class"]
 */
function affiliate_link_shortcode($atts) {
    $atts = shortcode_atts(array(
        'url' => '',
        'text' => '商品を見る',
        'class' => 'affiliate-link',
        'target' => '_blank',
        'rel' => 'nofollow sponsored'
    ), $atts);
    
    if (empty($atts['url'])) {
        return '<span style="color:red;">[affiliate] エラー: url属性が必要です</span>';
    }
    
    // アフィリエイトリンクのドメインを検出
    $domain = parse_url($atts['url'], PHP_URL_HOST);
    $affiliate_domains = array(
        'amazon.co.jp',
        'amzn.to',
        'rakuten.co.jp',
        'r10.to',
        'a8.net',
        'a8.to'
    );
    
    $is_affiliate = false;
    foreach ($affiliate_domains as $affiliate_domain) {
        if (strpos($domain, $affiliate_domain) !== false) {
            $is_affiliate = true;
            break;
        }
    }
    
    // データ属性を追加（GA4連携用）
    $data_attrs = '';
    if ($is_affiliate) {
        $data_attrs = 'data-affiliate="true" data-affiliate-domain="' . esc_attr($domain) . '"';
    }
    
    $output = sprintf(
        '<a href="%s" class="%s" target="%s" rel="%s" %s>%s</a>',
        esc_url($atts['url']),
        esc_attr($atts['class']),
        esc_attr($atts['target']),
        esc_attr($atts['rel']),
        $data_attrs,
        esc_html($atts['text'])
    );
    
    return $output;
}
add_shortcode('affiliate', 'affiliate_link_shortcode');
```

#### Step 2: 使用方法

記事編集画面で以下のように入力：

```
[affiliate url="https://amazon.co.jp/dp/XXXXX" text="おすすめCBDオイル"]
```

または、より詳細な設定：

```
[affiliate url="https://amazon.co.jp/dp/XXXXX" text="おすすめCBDオイル" class="btn-primary"]
```

---

### Phase 2: Google Tag Managerの設定（30分）

#### Step 1: Google Tag ManagerをWordPressに追加

1. **Google Tag Managerアカウントを作成**
   - URL: https://tagmanager.google.com/
   - コンテナを作成

2. **WordPressにGoogle Tag Managerコードを追加**
   - 子テーマの`header.php`または`footer.php`に追加
   - または、SWELLテーマの設定から追加

#### Step 2: GA4連携タグの作成

1. **Google Tag Manager → タグ → 新規**
2. **タグの設定**
   - タグタイプ: Google アナリティクス: GA4 イベント
   - 測定ID: GA4の測定IDを入力
   - イベント名: `affiliate_link_click`

3. **トリガーの設定**
   - トリガータイプ: クリック - すべての要素
   - 条件: `{{Click Element}}` に `data-affiliate="true"` が含まれる

4. **カスタムパラメータの追加**
   - `affiliate_domain`: `{{Click Element}}` の `data-affiliate-domain` 属性
   - `link_url`: `{{Click URL}}`
   - `link_text`: `{{Click Text}}`

#### Step 3: テスト

1. **Google Tag Manager → プレビュー**
2. **サイトを訪問**
3. **アフィリエイトリンクをクリック**
4. **イベントが送信されているか確認**

---

### Phase 3: GA4でコンバージョンとして設定（10分）

1. **GA4管理画面 → 「設定」→ 「イベント」**
2. **`affiliate_link_click`イベントを探す**
3. **「コンバージョンとしてマーク」をONにする**

---

## 📊 実装後の効果

### 作業時間の短縮
- **従来**: アフィリエイトリンク作成 + 貼り付け + GA4設定 = 5-10分/記事
- **実装後**: ショートコード入力 = 10秒/記事
- **削減時間**: 約95%削減

### GA4連携の自動化
- ✅ すべてのアフィリエイトリンクのクリックが自動でGA4に送信
- ✅ コンバージョン率を自動で測定
- ✅ どの商品が人気か自動で分析可能

---

## 🔧 追加機能（オプション）

### 1. アフィリエイトリンクの管理画面

WordPress管理画面でアフィリエイトリンクを一元管理：

```php
// 管理画面にメニューを追加
function add_affiliate_links_menu() {
    add_menu_page(
        'アフィリエイトリンク管理',
        'アフィリエイトリンク',
        'manage_options',
        'affiliate-links',
        'affiliate_links_admin_page'
    );
}
add_action('admin_menu', 'add_affiliate_links_menu');
```

### 2. アフィリエイトリンクの統計表示

GA4データを取得して、アフィリエイトリンクのクリック数を表示：

```php
// GA4 APIを使用して統計を取得
function get_affiliate_link_stats($link_url) {
    // GA4 API呼び出し
    // クリック数、コンバージョン数を返す
}
```

### 3. アフィリエイトリンクの自動検出

記事内の既存のアフィリエイトリンクを自動検出して、GA4連携を追加：

```php
// 記事保存時に自動でアフィリエイトリンクを検出
function auto_detect_affiliate_links($post_id) {
    $content = get_post_field('post_content', $post_id);
    // アフィリエイトリンクを検出
    // 自動でdata属性を追加
}
add_action('save_post', 'auto_detect_affiliate_links');
```

---

## 📝 実装手順（まとめ）

### すぐに実装できること（1時間）

1. **WordPressショートコードの作成**（30分）
   - `functions.php`にコードを追加
   - テスト

2. **Google Tag Managerの設定**（30分）
   - GTMアカウント作成
   - WordPressにGTMコードを追加
   - GA4連携タグの作成
   - テスト

### 次のステップ（オプション）

3. **GA4でコンバージョンとして設定**（10分）
4. **アフィリエイトリンクの管理画面作成**（1-2時間）
5. **統計表示機能の追加**（1-2時間）

---

## ✅ 確認事項

### 実装前に確認

1. **WordPressの子テーマは作成済みか？**
   - SWELLテーマを使用している場合、子テーマが必要

2. **Google Tag Managerアカウントは作成済みか？**
   - 未作成の場合は作成が必要

3. **GA4の測定IDは確認済みか？**
   - 測定ID: `G-XXXXXXXXXX` の形式

---

## 🚀 次のアクション

1. **WordPressショートコードの実装**
   - 子テーマの`functions.php`にコードを追加
   - テスト

2. **Google Tag Managerの設定**
   - GTMアカウント作成
   - WordPressにGTMコードを追加
   - GA4連携タグの作成

3. **既存記事のアフィリエイトリンクをショートコードに置き換え**
   - 既存のアフィリエイトリンクをショートコード形式に変更

---

## 📚 参考情報

### WordPressショートコード
- [WordPress Codex: Shortcode API](https://codex.wordpress.org/Shortcode_API)

### Google Tag Manager
- [Google Tag Manager公式ドキュメント](https://support.google.com/tagmanager)

### GA4連携
- [GA4 イベント計測](https://developers.google.com/analytics/devguides/collection/ga4/events)
