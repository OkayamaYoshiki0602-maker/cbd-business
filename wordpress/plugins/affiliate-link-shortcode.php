<?php
/**
 * Plugin Name: アフィリエイトリンクショートコード
 * Description: アフィリエイトリンクを簡単に挿入し、GA4連携を自動化
 * Version: 1.0.0
 * Author: CBD WORLD
 */

// アフィリエイトリンクショートコード
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
        'a8.to',
        'af.moshimo.com',
        'moshimo.com'
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
        $data_attrs = 'data-affiliate="true" data-affiliate-domain="' . esc_attr($domain) . '" data-affiliate-url="' . esc_attr($atts['url']) . '"';
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

// スタイルの追加（オプション）
function affiliate_link_styles() {
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
        }
        .affiliate-link:hover {
            background-color: #45a049;
        }
    </style>
    <?php
}
add_action('wp_head', 'affiliate_link_styles');
