<?php
/**
 * Plugin Name: CBD Affiliate GA4 Tracker
 * Description: アフィリエイトリンクのクリックを自動でGA4に送信するプラグイン
 * Version: 1.0.0
 * Author: CBDの人
 */

// アフィリエイトリンクの自動検出とGA4トラッキング
function cbd_affiliate_ga4_tracker() {
    // GA4測定IDを取得（環境変数またはオプションから）
    $ga4_measurement_id = get_option('cbd_ga4_measurement_id', '');
    
    if (empty($ga4_measurement_id)) {
        return;
    }
    
    ?>
    <script>
    (function() {
        // アフィリエイトリンクのパターン
        const affiliatePatterns = [
            /a8\.net/i,
            /px\.a8\.net/i,
            /rakuten\.co\.jp/i,
            /hb\.afl\.rakuten\.co\.jp/i,
            /moshimo\.com/i,
            /af\.moshimo\.com/i,
            /amazon\.co\.jp.*[?&](tag=|linkCode=)/i,
            /amzn\.to/i
        ];
        
        // アフィリエイトタイプを判定
        function getAffiliateType(url) {
            if (/a8\.net/i.test(url)) return 'A8.net';
            if (/rakuten\.co\.jp/i.test(url)) return '楽天アフィリエイト';
            if (/moshimo\.com/i.test(url)) return 'もしもアフィリエイト';
            if (/amazon\.co\.jp/i.test(url) || /amzn\.to/i.test(url)) return 'Amazonアソシエイト';
            return 'unknown';
        }
        
        // アフィリエイトリンクかチェック
        function isAffiliateLink(url) {
            return affiliatePatterns.some(pattern => pattern.test(url));
        }
        
        // ページ内のすべてのリンクにイベントリスナーを追加
        document.addEventListener('DOMContentLoaded', function() {
            const links = document.querySelectorAll('a[href]');
            
            links.forEach(function(link) {
                const href = link.getAttribute('href');
                
                if (href && isAffiliateLink(href)) {
                    // データ属性を追加
                    link.setAttribute('data-affiliate-link', 'true');
                    link.setAttribute('data-affiliate-type', getAffiliateType(href));
                    
                    // クリックイベントリスナーを追加
                    link.addEventListener('click', function(e) {
                        const linkText = link.textContent.trim() || link.innerText.trim();
                        const affiliateType = getAffiliateType(href);
                        
                        // GA4イベントを送信
                        if (typeof gtag !== 'undefined') {
                            gtag('event', 'affiliate_click', {
                                'event_category': 'affiliate',
                                'event_label': linkText,
                                'affiliate_type': affiliateType,
                                'link_url': href,
                                'link_text': linkText,
                                'page_title': document.title,
                                'page_url': window.location.href
                            });
                        } else {
                            // gtagがない場合、dataLayerに送信（GTM経由）
                            console.log('gtag not found, using dataLayer');
                        }
                        
                        // Google Tag ManagerのdataLayerにも送信（GTMを使用している場合）
                        if (typeof dataLayer !== 'undefined') {
                            dataLayer.push({
                                'event': 'affiliate_click',
                                'affiliate_type': affiliateType,
                                'link_url': href,
                                'link_text': linkText,
                                'page_title': document.title,
                                'page_url': window.location.href
                            });
                        }
                    });
                }
            });
        });
    })();
    </script>
    <?php
}
add_action('wp_footer', 'cbd_affiliate_ga4_tracker');

// 管理画面でGA4測定IDを設定
function cbd_affiliate_ga4_settings_page() {
    add_options_page(
        'CBD Affiliate GA4 Tracker設定',
        'CBD Affiliate GA4',
        'manage_options',
        'cbd-affiliate-ga4',
        'cbd_affiliate_ga4_settings_page_content'
    );
}
add_action('admin_menu', 'cbd_affiliate_ga4_settings_page');

function cbd_affiliate_ga4_settings_page_content() {
    if (isset($_POST['submit'])) {
        update_option('cbd_ga4_measurement_id', sanitize_text_field($_POST['ga4_measurement_id']));
        echo '<div class="notice notice-success"><p>設定を保存しました。</p></div>';
    }
    
    $ga4_measurement_id = get_option('cbd_ga4_measurement_id', '');
    ?>
    <div class="wrap">
        <h1>CBD Affiliate GA4 Tracker設定</h1>
        <form method="post" action="">
            <table class="form-table">
                <tr>
                    <th scope="row">
                        <label for="ga4_measurement_id">GA4測定ID</label>
                    </th>
                    <td>
                        <input type="text" 
                               id="ga4_measurement_id" 
                               name="ga4_measurement_id" 
                               value="<?php echo esc_attr($ga4_measurement_id); ?>" 
                               class="regular-text"
                               placeholder="G-XXXXXXXXXX">
                        <p class="description">GA4の測定IDを入力してください（例: G-XXXXXXXXXX）</p>
                    </td>
                </tr>
            </table>
            <?php submit_button(); ?>
        </form>
        
        <h2>使い方</h2>
        <ol>
            <li>GA4測定IDを入力してください</li>
            <li>このプラグインが自動でアフィリエイトリンクを検出し、クリック時にGA4イベントを送信します</li>
            <li>GA4の管理画面で<code>affiliate_click</code>イベントをコンバージョンとして設定してください</li>
        </ol>
        
        <h2>対応しているアフィリエイトサービス</h2>
        <ul>
            <li>A8.net</li>
            <li>楽天アフィリエイト</li>
            <li>もしもアフィリエイト</li>
            <li>Amazonアソシエイト</li>
        </ul>
    </div>
    <?php
}
