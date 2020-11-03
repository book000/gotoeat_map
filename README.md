# gotoeat_map

[農林水産省が実施しているGoToEatキャンペーン](https://gotoeat.maff.go.jp/)の加盟飲食店を[OpenStreetMap](https://www.openstreetmap.org)を用いて地図として見られるようにするプロジェクトです。  
つまり、[book000/gotoeat-map_yamanashi](https://github.com/book000/gotoeat-map_yamanashi)の全国版です。

気が向いたときに作っているので、完成するかはわかりません。

- https://book000.github.io/gotoeat_map/

## 取得処理仕様

3時間毎に、6都道府県ずつに分けた都道府県グループをそれぞれ実行する。
例として、0,1,2時なら`1_hokkaido`, `2_aomori`, `3_iwate`, `4_miyagi`, `5_akita`, `6_yamagata`の6都道府県。

## データ

- 参考: [農林水産省 食事券発行事業 各地域の状況一覧](https://www.maff.go.jp/j/shokusan/gaisyoku/attach/shokujiken.pdf)

|  | 都道府県 | 実装日 | 元データ形式 | 取得データ種類 | 公式サイトURL | マップURL | 備考 |
| :- | :- | :-: | :-: | :- | :- | :- | :- |
| 1 | 北海道 |  |  |  | https://gotoeat-hokkaido.jp/ |  | 販売・利用開始 2020/11/10 |
| 2 | 青森県 |  |  |  |  |  |  |
| 3 | 岩手県 |  |  |  | https://www.iwate-gotoeat.jp |  | 販売・利用開始 2020/11/01 |
| 4 | 宮城県 |  |  |  | https://gte-miyagi.jp |  | 販売・利用開始 2020/11/16 |
| 5 | 秋田県 | 2020/10/28 | CSV | 店名・エリア・住所・電話番号・URL | https://www.gotoeat-akita.com/ | https://book000.github.io/gotoeat_map/5_akita/ |  |
| 6 | 山形県 |  |  |  |  |  |  |
| 7 | 福島県 | 2020/10/28 | HTML (リスト) | 店名・店ジャンル・住所 | https://gotoeat-fukushima.jp | https://book000.github.io/gotoeat_map/7_fukushima/ |  |
| 8 | 茨城県 | 2020/10/28 | HTML (テーブル) | 店名・店ジャンル・住所・電話番号 | https://gotoeat-ibaraki.com/ | https://book000.github.io/gotoeat_map/8_ibaraki/ |  |
| 9 | 栃木県 | 2020/10/28 | HTML (リスト) | 店名・店ジャンル・住所・郵便番号・電話番号 | https://www.gotoeat-tochigi.jp/ | https://book000.github.io/gotoeat_map/9_tochigi/ |  |
| 10 | 群馬県 | 2020/10/28 | HTML | 店名・店ジャンル・住所・郵便番号・電話番号 | https://gunma-gotoeat-campaign.com/ | https://book000.github.io/gotoeat_map/10_gunma/ |  |
| 11 | 埼玉県 | 2020/10/28 | HTML | 店名・住所・郵便番号 | https://saitama-goto-eat.com | https://book000.github.io/gotoeat_map/11_saitama/ |  |
| 12 | 千葉県 | 2020/10/28 | JSON | 店名・住所・電話番号・緯度・経度 | https://www.chiba-gte.jp/ | https://book000.github.io/gotoeat_map/12_chiba/ |  |
| 13 | 東京都 |  |  |  | https://r.gnavi.co.jp/plan/campaign/gotoeat-tokyo/ |  | 販売・利用開始 2020/11/20 |
| 14 | 神奈川県 |  |  |  | https://www.kanagawa-gte.jp/ |  | 2020/11/02公開予定 |
| 15 | 新潟県 | 2020/10/29 | HTML | 店名・店ジャンル・エリア・住所・郵便番号・電話番号 | https://niigata-gte.com/ | https://book000.github.io/gotoeat_map/15_niigata/ |  |
| 16 | 富山県 | 2020/10/29 | HTML (リスト) | 店名・店ジャンル・住所・電話番号・営業時間・定休日 | https://toyamagotoeat.jp/ | https://book000.github.io/gotoeat_map/16_toyama/ |  |
| 17 | 石川県 |  | HTML (リスト) |  | https://ishikawa-gotoeat-cpn.com/ |  | 住所情報未提供のため見送り |
| 18 | 福井県 | 2020/10/29 | HTML | 店名・店ジャンル・エリア・住所・電話番号 | https://gotoeat-fukui.com/ | https://book000.github.io/gotoeat_map/18_fukui/ |  |
| 19 | 山梨県 | 2020/10/27 | HTML (テーブル) | 店名・店ジャンル・住所・電話番号 | https://www.gotoeat-yamanashi.jp | https://book000.github.io/gotoeat-map_yamanashi/ | 別リポジトリでホスト |
| 20 | 長野県 |  |  |  | https://shinshu-gotoeat.com/ |  | 販売・利用開始 2020/11/09 |
| 21 | 岐阜県 |  |  |  | https://gotoeat-gifu.jp |  | あまりにもスクレイピングしにくい(店舗毎に別ページは厳しい)ので見送り |
| 22 | 静岡県 | 2020/10/29 | HTML | 店名・店ジャンル・住所・郵便番号・電話番号 | https://premium-gift.jp/fujinokunigotoeat/ | https://book000.github.io/gotoeat_map/22_shizuoka/ |  |
| 22 | 静岡県 | 2020/10/29 | HTML (リスト) | 店名・店ジャンル・住所・電話番号・営業時間・定休日 | https://gotoeat-shizuoka.com/ | https://book000.github.io/gotoeat_map/22_/ |  |
| 23 | 愛知県 | 2020/10/29 | HTML (リスト) | 店名・店ジャンル・住所・郵便番号・電話番号 | https://gotoeat-aichi.jp/ | https://book000.github.io/gotoeat_map/23_aichi/ |  |
| 24 | 三重県 |  |  |  | https://gotoeat-mie.com/ |  | あまりにもスクレイピングしにくい(店舗毎に別ページは厳しい)ので見送り |
| 25 | 滋賀県 |  |  |  | https://www.shiga-gte.jp/ |  | PDFファイルによる配布のため、スクレイピングできないので見送り |
| 26 | 京都府 | 2020/10/30 | JSON | 店名・店ジャンル・住所・郵便番号・電話番号・営業時間・定休日 | https://premium-gift.jp/kyoto-eat | https://book000.github.io/gotoeat_map/26_kyoto/ |  |
| 27 | 大阪府 |  |  |  | https://goto-eat.weare.osaka-info.jp/ |  |  |
| 28 | 兵庫県 |  |  |  | https://gotoeat-hyogo.com/ |  |  |
| 29 | 奈良県 |  |  |  | https://premium-gift.jp/nara-eat |  |  |
| 30 | 和歌山県 |  |  |  |  |  |  |
| 31 | 鳥取県 |  |  |  | https://tottori-gotoeat.jp/ |  |  |
| 32 | 島根県 |  |  |  | https://www.gotoeat-shimane.jp/ |  |  |
| 33 | 岡山県 |  |  |  | https://gotoeat-okayama.com/ |  |  |
| 34 | 広島県 |  |  |  | https://gotoeat.hiroshima.jp/ |  |  |
| 35 | 山口県 |  |  |  | https://gotoeat-yamaguchi.com/ |  |  |
| 36 | 徳島県 |  |  |  | https://gotoeat.tokushima.jp |  |  |
| 37 | 香川県 |  |  |  | https://www.kagawa-gotoeat.com |  |  |
| 38 | 愛媛県 |  |  |  | https://www.goto-eat-ehime.com |  |  |
| 39 | 高知県 |  |  |  | https://www.gotoeat-kochi.com/ |  |  |
| 40 | 福岡県 |  |  |  | https://gotoeat-fukuoka.jp/ |  |  |
| 41 | 佐賀県 |  |  |  | https://gotoeat-saga.jp/ |  |  |
| 42 | 長崎県 |  |  |  | https://www.gotoeat-nagasaki.jp/ |  |  |
| 43 | 熊本県 |  |  |  | https://gotoeat-kumamoto.jp/ |  |  |
| 44 | 大分県 |  |  |  | https://oita-gotoeat.com/ |  |  |
| 45 | 宮崎県 |  |  |  | https://premium-gift.jp/gotoeatmiyazaki/ |  |  |
| 46 | 鹿児島県 |  |  |  | http://www.kagoshima-cci.or.jp/   ・ https://r.goope.jp/srp-46 |  |  |
| 47 | 沖縄県 |  |  |  | https://gotoeat.okinawa.jp/ |  |  |

## 注意・免責事項

このプロジェクトを使用したことによって引き起こされた問題に関して開発者は一切の責任を負いません。  
また、本プロジェクトはGoToEatキャンペーンを利用する店舗を探す際の手助けとなることを目的として作られたものです。

## 問い合わせ先

当プロジェクトに関する問い合わせは[Twitter@book000](https://twitter.com/book000)で受け付けます。

## ライセンス

このプロジェクトのライセンスは[MIT License](https://github.com/book000/gotoeat-map_yamanashi/blob/master/LICENSE)です。
