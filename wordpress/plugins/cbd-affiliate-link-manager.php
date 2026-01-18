<?php
/**
 * Plugin Name: CBDアフィリエイトリンク管理
 * Description: Googleスプレッドシートでアフィリエイトリンクを一元管理し、WordPress記事に簡単に挿入
 * Version: 1.0.0
 * Author: CBD WORLD
 */

// プラグインが直接アクセスされた場合のセキュリティ
if (!defined('ABSPATH')) {
    exit;
}

// 設定
define('CBD_AFFILIATE_CACHE_TIME', 3600); // 1時間キャッシュ
define('CBD_AFFILIATE_SPREADSHEET_ID', ''); // スプレッドシートIDを設定

/**
 * Google Sheets APIから商品データを取得
 */
function cbd_get_affiliate_data($product_id) {
    // キャッシュキー
    $cache_key = 'cbd_affiliate_' . $product_id;
    $cached_data = get_transient($cache_key);
    
    if ($cached_data !== false) {
        return $cached_data;
    }
    
    // スプレッドシートIDが設定されていない場合
    if (empty(CBD_AFFILIATE_SPREADSHEET_ID)) {
        return null;
    }
    
    // Google Sheets APIを使用してデータを取得
    // 注: 実際の実装では、Google Sheets APIの認証が必要
    // ここでは簡易版として、WordPressオプションに保存されたデータを使用
    
    $all_products = get_option('cbd_affiliate_products', array());
    
    if (isset($all_products[$product_id])) {
        $product_data = $all_products[$product_id];
        set_transient($cache_key, $product_data, CBD_AFFILIATE_CACHE_TIME);
        return $product_data;
    }
    
    return null;
}

/**
 * アフィリエイトリンクショートコード
 * 使用方法: [affiliate id="商品ID"]
 */
function cbd_affiliate_link_shortcode($atts) {
    $atts = shortcode_atts(array(
        'id' => '',
        'text' => '',
        'class' => 'affiliate-link',
        'target' => '_blank',
        'rel' => 'nofollow sponsored'
    ), $atts);
    
    if (empty($atts['id'])) {
        return '<span style="color:red;">[affiliate] エラー: id属性が必要です</span>';
    }
    
    // 商品データを取得
    $product_data = cbd_get_affiliate_data($atts['id']);
    
    if (!$product_data) {
        return '<span style="color:red;">[affiliate] エラー: 商品ID "' . esc_html($atts['id']) . '" が見つかりません</span>';
    }
    
    // リンクテキストを決定
    $link_text = !empty($atts['text']) ? $atts['text'] : $product_data['name'];
    
    // アフィリエイトURLを取得
    $affiliate_url = $product_data['affiliate_url'];
    
    // アフィリエイトサービスのドメインを検出
    $domain = parse_url($affiliate_url, PHP_URL_HOST);
    $affiliate_service = $product_data['service'];
    
    // データ属性を追加（GA4連携用）
    $data_attrs = sprintf(
        'data-affiliate="true" data-affiliate-service="%s" data-affiliate-id="%s" data-affiliate-domain="%s"',
        esc_attr($affiliate_service),
        esc_attr($atts['id']),
        esc_attr($domain)
    );
    
    // リンクを生成
    $output = sprintf(
        '<a href="%s" class="%s" target="%s" rel="%s" %s>%s</a>',
        esc_url($affiliate_url),
        esc_attr($atts['class']),
        esc_attr($atts['target']),
        esc_attr($atts['rel']),
        $data_attrs,
        esc_html($link_text)
    );
    
    return $output;
}
add_shortcode('affiliate', 'cbd_affiliate_link_shortcode');

/**
 * スタイルの追加
 */
function cbd_affiliate_link_styles() {
    ?>
    <style>
        .affiliate-link {
            display: inline-block;
            padding: 8px 16px;
            background-color: #4CAF50;
            color: white;
            text-decoration: none;
            border-radius: 4px;
            transition: background-color 0.3s;
            font-weight: 500;
        }
        .affiliate-link:hover {
            background-color: #45a049;
            color: white;
        }
    </style>
    <?php
}
add_action('wp_head', 'cbd_affiliate_link_styles');

/**
 * 管理画面にメニューを追加
 */
function cbd_affiliate_admin_menu() {
    add_menu_page(
        'アフィリエイトリンク管理',
        'アフィリエイトリンク',
        'manage_options',
        'cbd-affiliate-links',
        'cbd_affiliate_admin_page'
    );
}
add_action('admin_menu', 'cbd_affiliate_admin_menu');

/**
 * 管理画面のページ
 */
function cbd_affiliate_admin_page() {
    ?>
    <div class="wrap">
        <h1>アフィリエイトリンク管理</h1>
        <p>Googleスプレッドシートでアフィリエイトリンクを管理します。</p>
        
        <h2>スプレッドシート</h2>
        <p>以下のスプレッドシートで商品を管理してください:</p>
        <p><a href="https://docs.google.com/spreadsheets/d/<?php echo esc_attr(CBD_AFFILIATE_SPREADSHEET_ID); ?>/edit" target="_blank">スプレッドシートを開く</a></p>
        
        <h2>使用方法</h2>
        <p>記事編集画面で以下のショートコードを使用してください:</p>
        <code>[affiliate id="商品ID"]</code>
        
        <h2>設定</h2>
        <form method="post" action="options.php">
            <?php settings_fields('cbd_affiliate_settings'); ?>
            <?php do_settings_sections('cbd_affiliate_settings'); ?>
            <table class="form-table">
                <tr>
                    <th scope="row">スプレッドシートID</th>
                    <td>
                        <input type="text" name="cbd_affiliate_spreadsheet_id" value="<?php echo esc_attr(get_option('cbd_affiliate_spreadsheet_id', '')); ?>" class="regular-text" />
                        <p class="description">GoogleスプレッドシートのIDを入力してください</p>
                    </td>
                </tr>
            </table>
            <?php submit_button(); ?>
        </form>
    </div>
    <?php
}

/**
 * 設定を登録
 */
function cbd_affiliate_register_settings() {
    register_setting('cbd_affiliate_settings', 'cbd_affiliate_spreadsheet_id');
}
add_action('admin_init', 'cbd_affiliate_register_settings');
