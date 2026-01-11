# Google Tag Manager設定ガイド（アフィリエイトリンクGA4連携）

## 🎯 目的

アフィリエイトリンクのクリックを自動でGA4に送信し、コンバージョンを測定できるようにする。

---

## 📋 前提条件

- Google Tag Managerアカウントを作成済み
- GA4の測定IDを取得済み
- WordPressサイトにGoogle Tag Managerコードを追加済み

---

## 🚀 設定手順

### Step 1: Google Tag Managerアカウントの作成（未作成の場合）

1. **Google Tag Managerにアクセス**
   - URL: https://tagmanager.google.com/
   - Googleアカウントでログイン

2. **コンテナを作成**
   - 「コンテナを作成」をクリック
   - コンテナ名: `CBD WORLD`
   - ターゲットプラットフォーム: **Web**
   - 「作成」をクリック

3. **GTMコードを取得**
   - コンテナ作成後、GTMコードが表示される
   - 例: `GTM-XXXXXXX`

---

### Step 2: WordPressにGoogle Tag Managerコードを追加

#### 方法A: SWELLテーマの設定から追加（推奨）

1. **WordPress管理画面 → 外観 → カスタマイズ**
2. **「その他」または「カスタムコード」を選択**
3. **「head内に出力」にGTMコードを追加**

```html
<!-- Google Tag Manager -->
<script>(function(w,d,s,l,i){w[l]=w[l]||[];w[l].push({'gtm.start':
new Date().getTime(),event:'gtm.js'});var f=d.getElementsByTagName(s)[0],
j=d.createElement(s),dl=l!='dataLayer'?'&l='+l:'';j.async=true;j.src=
'https://www.googletagmanager.com/gtm.js?id='+i+dl;f.parentNode.insertBefore(j,f);
})(window,document,'script','dataLayer','GTM-XXXXXXX');</script>
<!-- End Google Tag Manager -->
```

4. **「body開始タグ直後に出力」にGTMコードを追加**

```html
<!-- Google Tag Manager (noscript) -->
<noscript><iframe src="https://www.googletagmanager.com/ns.html?id=GTM-XXXXXXX"
height="0" width="0" style="display:none;visibility:hidden"></iframe></noscript>
<!-- End Google Tag Manager (noscript) -->
```

#### 方法B: 子テーマのheader.phpとfooter.phpに追加

1. **子テーマの`header.php`を編集**
   - `<head>`タグの直後にGTMコードを追加

2. **子テーマの`footer.php`を編集**
   - `<body>`タグの直後にGTMコードを追加

---

### Step 3: GA4連携タグの作成

1. **Google Tag Manager → タグ → 新規**

2. **タグの設定**
   - **タグ名**: `GA4 - アフィリエイトリンククリック`
   - **タグタイプ**: **Google アナリティクス: GA4 イベント**
   - **測定ID**: GA4の測定IDを入力（例: `G-XXXXXXXXXX`）
   - **イベント名**: `affiliate_link_click`

3. **イベントパラメータの追加**
   - **パラメータ名**: `affiliate_domain`
   - **値**: `{{Click Element}}` → `data-affiliate-domain`属性を選択
   
   - **パラメータ名**: `link_url`
   - **値**: `{{Click URL}}`
   
   - **パラメータ名**: `link_text`
   - **値**: `{{Click Text}}`

4. **トリガーの設定**
   - **トリガーを選択**: 「新規」をクリック
   - **トリガー名**: `アフィリエイトリンククリック`
   - **トリガータイプ**: **クリック - すべての要素**
   - **このトリガーの発生場所**: **一部のクリック**
   - **条件**: 
     - **変数**: `Click Element`
     - **演算子**: **正規表現に一致**
     - **値**: `data-affiliate="true"`

5. **保存**

---

### Step 4: テスト

1. **Google Tag Manager → プレビュー**
2. **サイトのURLを入力**
3. **「接続」をクリック**
4. **サイトを訪問**
5. **アフィリエイトリンクをクリック**
6. **Google Tag Managerのプレビューでイベントが送信されているか確認**

---

### Step 5: GA4でコンバージョンとして設定

1. **GA4管理画面 → 「設定」→ 「イベント」**
2. **`affiliate_link_click`イベントを探す**
3. **「コンバージョンとしてマーク」をONにする**

---

## 📊 確認方法

### Google Tag Managerで確認

1. **Google Tag Manager → タグ**
2. **「GA4 - アフィリエイトリンククリック」を確認**
3. **「プレビュー」でテスト**

### GA4で確認

1. **GA4管理画面 → 「レポート」→ 「リアルタイム」**
2. **サイトを訪問**
3. **アフィリエイトリンクをクリック**
4. **イベントが表示されるか確認**

---

## 🔧 トラブルシューティング

### イベントが送信されない場合

1. **Google Tag Managerのプレビューで確認**
   - タグが発火しているか確認
   - エラーがないか確認

2. **データ属性が正しく設定されているか確認**
   - アフィリエイトリンクに`data-affiliate="true"`が含まれているか
   - ブラウザの開発者ツールで確認

3. **GA4の測定IDが正しいか確認**
   - 測定ID: `G-XXXXXXXXXX` の形式

---

## 📝 参考情報

### Google Tag Manager公式ドキュメント
- [Google Tag Manager公式サイト](https://tagmanager.google.com/)
- [GA4 イベント計測](https://developers.google.com/analytics/devguides/collection/ga4/events)

### WordPressショートコード
- [WordPress Codex: Shortcode API](https://codex.wordpress.org/Shortcode_API)
