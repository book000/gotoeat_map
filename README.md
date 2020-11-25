# gotoeat_map

[農林水産省が実施しているGoToEatキャンペーン](https://gotoeat.maff.go.jp/)の加盟飲食店を[OpenStreetMap](https://www.openstreetmap.org)を用いて地図として見られるようにするプロジェクトです。  
つまり、[book000/gotoeat-map_yamanashi](https://github.com/book000/gotoeat-map_yamanashi)の全国版です。

気が向いたときに作っているので、完成するかはわかりません。

- https://book000.github.io/gotoeat_map/

## 追記 2020/11/20

2020/10/26の時点ですでに企業レベルでGo To Eat MAPというサービスが開始されていたようです。こちらの方が使いやすいかも。  
このプロジェクトも多少バグフィックスは継続するつもりですが、新規利用開始の更新まで対応するかは未定です。

- [Go To Eat MAP (α)](https://go-to-eat-map.com/)
- [jiji.comによる記事](https://www.jiji.com/jc/article?k=000000002.000057162&g=prt)
- [AME&Company株式会社によるプレスリリース](https://prtimes.jp/main/html/rd/p/000000002.000057162.html)

## 取得処理仕様

3時間毎に、6都道府県ずつに分けた都道府県グループをそれぞれ実行する。
例として、0,1,2時なら`1_hokkaido`, `2_aomori`, `3_iwate`, `4_miyagi`, `5_akita`, `6_yamagata`の6都道府県。

## データ

- 参考: [農林水産省 食事券発行事業 各地域の状況一覧](https://www.maff.go.jp/j/shokusan/gaisyoku/attach/shokujiken.pdf)

|  |  | 都道府県 | 実装日 | 元データ形式 | 取得データ種類 | 公式サイト | 生成マップ | 備考 |
|-|-|-|-|-|-|-|-|-|
| 1 | 00～02時 | 北海道 | 2020/11/25 | HTML (リスト) | 店名・店ジャンル・エリア・住所・電話番号 | [Link](https://gotoeat-hokkaido.jp/) | [Link](https://book000.github.io/gotoeat_map/1_hokkaido/) |  |
| 2 | 00～02時 | 青森県 |  |  |  | [Link](https://gotoeat-aomori.com/) |  | 販売・利用開始 2020/12/01 |
| 3 | 00～02時 | 岩手県 | 2020/11/04 | HTML | 店名・店ジャンル・住所・電話番号 | [Link](https://www.iwate-gotoeat.jp) | [Link](https://book000.github.io/gotoeat_map/3_iwate/) |  |
| 4 | 00～02時 | 宮城県 | 2020/11/25 | HTML | 店名・店ジャンル・エリア・住所・郵便番号・電話番号 | [Link](https://gte-miyagi.jp) | [Link](https://book000.github.io/gotoeat_map/4_miyagi/) |  |
| 5 | 00～02時 | 秋田県 | 2020/10/28 | CSV | 店名・エリア・住所・電話番号・URL | [Link](https://www.gotoeat-akita.com/) | [Link](https://book000.github.io/gotoeat_map/5_akita/) |  |
| 6 | 00～02時 | 山形県 | 2020/11/25 | JSON (HTML) | 店名・店ジャンル・エリア・住所・郵便番号・電話番号 | [Link](https://yamagata-gotoeat.com/) | [Link](https://book000.github.io/gotoeat_map/6_yamagata/) |  |
| 7 | 03～05時 | 福島県 | 2020/10/28 | HTML (リスト) | 店名・店ジャンル・住所 | [Link](https://gotoeat-fukushima.jp) | [Link](https://book000.github.io/gotoeat_map/7_fukushima/) |  |
| 8 | 03～05時 | 茨城県 | 2020/10/28 | HTML (テーブル) | 店名・店ジャンル・住所・電話番号 | [Link](https://gotoeat-ibaraki.com/) | [Link](https://book000.github.io/gotoeat_map/8_ibaraki/) |  |
| 9 | 03～05時 | 栃木県 | 2020/10/28 | HTML (リスト) | 店名・店ジャンル・住所・郵便番号・電話番号 | [Link](https://www.gotoeat-tochigi.jp/) | [Link](https://book000.github.io/gotoeat_map/9_tochigi/) |  |
| 10 | 03～05時 | 群馬県 | 2020/10/28 | HTML | 店名・店ジャンル・住所・郵便番号・電話番号 | [Link](https://gunma-gotoeat-campaign.com/) | [Link](https://book000.github.io/gotoeat_map/10_gunma/) |  |
| 11 | 03～05時 | 埼玉県 | 2020/10/28 | HTML | 店名・住所・郵便番号 | [Link](https://saitama-goto-eat.com) | [Link](https://book000.github.io/gotoeat_map/11_saitama/) |  |
| 12 | 03～05時 | 千葉県 | 2020/10/28 | JSON | 店名・住所・電話番号・緯度・経度 | [Link](https://www.chiba-gte.jp/) | [Link](https://book000.github.io/gotoeat_map/12_chiba/) | 公式マップ提供有 |
| 13 | 06～08時 | 東京都 |  |  |  | [Link](https://r.gnavi.co.jp/plan/campaign/gotoeat-tokyo/) | [Link](https://book000.github.io/gotoeat_map/13_tokyo/) | あまりにもスクレイピングしにくい(データが分散しすぎ・量が多すぎる)ので見送り |
| 14 | 06～08時 | 神奈川県 | 2020/11/04 | JSON | 店名・住所・電話番号・緯度・経度 | [Link](https://www.kanagawa-gte.jp/) | [Link](https://book000.github.io/gotoeat_map/14_kanagawa/) | 公式マップ提供有 |
| 15 | 06～08時 | 新潟県 | 2020/10/29 | HTML | 店名・店ジャンル・エリア・住所・郵便番号・電話番号 | [Link](https://niigata-gte.com/) | [Link](https://book000.github.io/gotoeat_map/15_niigata/) |  |
| 16 | 06～08時 | 富山県 | 2020/10/29 | HTML (リスト) | 店名・店ジャンル・住所・電話番号・営業時間・定休日 | [Link](https://toyamagotoeat.jp/) | [Link](https://book000.github.io/gotoeat_map/16_toyama/) |  |
| 17 | 06～08時 | 石川県 | 2020/11/25 | HTML (リスト) | 店名・店ジャンル・住所・郵便番号・電話番号 | [Link](https://ishikawa-gotoeat-cpn.com/) | [Link](https://book000.github.io/gotoeat_map/17_ishikawa/) |  |
| 18 | 06～08時 | 福井県 | 2020/10/29 | HTML | 店名・店ジャンル・エリア・住所・電話番号 | [Link](https://gotoeat-fukui.com/) | [Link](https://book000.github.io/gotoeat_map/18_fukui/) |  |
| 19 | 09～11時 | 山梨県 | 2020/10/27 | HTML (テーブル) | 店名・店ジャンル・住所・電話番号 | [Link](https://www.gotoeat-yamanashi.jp) | [Link](https://book000.github.io/gotoeat_map/19_yamanashi/) | 別リポジトリでホスト (リダイレクト) |
| 20 | 09～11時 | 長野県 |  |  |  | [Link](https://shinshu-gotoeat.com/) |  | 販売・利用開始 2020/11/09 |
| 21 | 09～11時 | 岐阜県 |  |  |  | [Link](https://gotoeat-gifu.jp) |  | あまりにもスクレイピングしにくい(店舗毎に別ページは厳しい)ので見送り |
| 22 | 09～11時 | 静岡県 | 2020/10/29 | HTML | 店名・店ジャンル・住所・郵便番号・電話番号 | [Link](https://premium-gift.jp/fujinokunigotoeat/) | [Link](https://book000.github.io/gotoeat_map/22_shizuoka/) |  |
| 22 | 09～11時 | 静岡県 | 2020/10/29 | HTML (リスト) | 店名・店ジャンル・住所・電話番号・営業時間・定休日 | [Link](https://gotoeat-shizuoka.com/) | [Link](https://book000.github.io/gotoeat_map/22_/) |  |
| 23 | 09～11時 | 愛知県 | 2020/10/29 | HTML (リスト) | 店名・店ジャンル・住所・郵便番号・電話番号 | [Link](https://gotoeat-aichi.jp/) | [Link](https://book000.github.io/gotoeat_map/23_aichi/) |  |
| 24 | 09～11時 | 三重県 |  |  |  | [Link](https://gotoeat-mie.com/) |  | あまりにもスクレイピングしにくい(店舗毎に別ページは厳しい)ので見送り |
| 25 | 12～14時 | 滋賀県 |  | PDF |  | [Link](https://www.shiga-gte.jp/) |  | PDFファイルによる配布のため、スクレイピングできないので見送り |
| 26 | 12～14時 | 京都府 | 2020/10/30 | JSON | 店名・店ジャンル・住所・郵便番号・電話番号・営業時間・定休日 | [Link](https://premium-gift.jp/kyoto-eat) | [Link](https://book000.github.io/gotoeat_map/26_kyoto/) |  |
| 27 | 12～14時 | 大阪府 | 2020/11/04 | HTML (リスト) | 店名・店ジャンル・住所・郵便番号・電話番号・営業時間・定休日 | [Link](https://goto-eat.weare.osaka-info.jp/) | [Link](https://book000.github.io/gotoeat_map/27_osaka/) |  |
| 28 | 12～14時 | 兵庫県 | 2020/11/04 | HTML (リスト) | 店名・住所・郵便番号・電話番号 | [Link](https://gotoeat-hyogo.com/) | [Link](https://book000.github.io/gotoeat_map/28_hyogo/) |  |
| 29 | 12～14時 | 奈良県 | 2020/11/04 | HTML | 店名・店ジャンル・住所・郵便番号・電話番号 | [Link](https://premium-gift.jp/nara-eat) | [Link](https://book000.github.io/gotoeat_map/29_nara/) |  |
| 30 | 12～14時 | 和歌山県 |  |  |  | [Link](https://gotoeat-wakayama.com/) |  |  |
| 31 | 15～17時 | 鳥取県 |  |  |  | [Link](https://tottori-gotoeat.jp/) |  | あまりにもスクレイピングしにくい(店舗毎に別ページは厳しい)ので見送り |
| 32 | 15～17時 | 島根県 |  |  |  | [Link](https://www.gotoeat-shimane.jp/) |  | あまりにもスクレイピングしにくい(店舗毎に別ページは厳しい)ので見送り |
| 33 | 15～17時 | 岡山県 | 2020/11/04 | JSON | 店名・店ジャンル・住所・電話番号・定休日・緯度・経度 | [Link](https://gotoeat-okayama.com/) | [Link](https://book000.github.io/gotoeat_map/33_okayama/) | 公式マップ提供有 |
| 34 | 15～17時 | 広島県 | 2020/11/04 | HTML | 店名・店ジャンル・住所 | [Link](https://gotoeat.hiroshima.jp/) | [Link](https://book000.github.io/gotoeat_map/34_hiroshima/) |  |
| 35 | 15～17時 | 山口県 | 2020/11/04 | HTML (リスト) | 店名・店ジャンル・住所・営業時間・定休日・電話番号・コロナ対策 | [Link](https://gotoeat-yamaguchi.com/) | [Link](https://book000.github.io/gotoeat_map/35_yamaguchi/) |  |
| 36 | 15～17時 | 徳島県 | 2020/11/04 | HTML | 店名・住所・営業時間・定休日・電話番号 | [Link](https://gotoeat.tokushima.jp) | [Link](https://book000.github.io/gotoeat_map/36_tokushima/) |  |
| 37 | 18～20時 | 香川県 | 2020/11/04 | HTML | 店名・店ジャンル・エリア・住所・電話番号 | [Link](https://www.kagawa-gotoeat.com) | [Link](https://book000.github.io/gotoeat_map/37_kagawa/) |  |
| 38 | 18～20時 | 愛媛県 | 2020/11/04 | HTML (リスト) | 店名・店ジャンル・住所・電話番号 | [Link](https://www.goto-eat-ehime.com) | [Link](https://book000.github.io/gotoeat_map/38_ehime/) |  |
| 39 | 18～20時 | 高知県 | 2020/11/04 | JSON | 店名・店ジャンル・エリア・住所・電話番号 | [Link](https://www.gotoeat-kochi.com/) | [Link](https://book000.github.io/gotoeat_map/39_kochi/) |  |
| 40 | 18～20時 | 福岡県 | 2020/11/04 | CSV | 店名・店ジャンル・エリア・住所・郵便番号・電話番号 | [Link](https://gotoeat-fukuoka.jp/) | [Link](https://book000.github.io/gotoeat_map/40_fukuoka/) |  |
| 41 | 18～20時 | 佐賀県 | 2020/11/04 | HTML | 店名・店ジャンル・住所・営業時間・定休日・電話番号 | [Link](https://gotoeat-saga.jp/) | [Link](https://book000.github.io/gotoeat_map/41_saga/) |  |
| 42 | 18～20時 | 長崎県 | 2020/11/04 | HTML | 店名・店ジャンル・エリア・住所・電話番号 | [Link](https://www.gotoeat-nagasaki.jp/) | [Link](https://book000.github.io/gotoeat_map/42_nagasaki/) |  |
| 43 | 21～23時 | 熊本県 | 2020/11/04 | HTML | 店名・エリア・住所・郵便番号 | [Link](https://gotoeat-kumamoto.jp/) | [Link](https://book000.github.io/gotoeat_map/43_kumamoto/) |  |
| 44 | 21～23時 | 大分県 |  | (Firestore) |  | [Link](https://oita-gotoeat.com/) |  | Firestoreからデータ持ってきていてスクレイピングしにくいため見送り |
| 45 | 21～23時 | 宮崎県 | 2020/11/04 | HTML | 店名・店ジャンル・住所・郵便番号・電話番号 | [Link](https://premium-gift.jp/gotoeatmiyazaki/) | [Link](https://book000.github.io/gotoeat_map/45_miyazaki/) |  |
| 46 | 21～23時 | 鹿児島県 |  | PDF |  | [Link](http://www.kagoshima-cci.or.jp/) |  | PDFファイルによる配布のため、スクレイピングできないので見送り |
| 46 | 21～23時 | 鹿児島県 |  | PDF |  | [Link](https://r.goope.jp/srp-46) |  | PDFファイルによる配布のため、スクレイピングできないので見送り |
| 47 | 21～23時 | 沖縄県 |  |  |  | [Link](https://gotoeat.okinawa.jp/) |  | 販売・利用開始 2020/11/17 |

## 注意・免責事項

このプロジェクトを使用したことによって引き起こされた問題に関して開発者は一切の責任を負いません。  
また、本プロジェクトはGoToEatキャンペーンを利用する店舗を探す際の手助けとなることを目的として作られたものです。

## 問い合わせ先

当プロジェクトに関する問い合わせは[Twitter@book000](https://twitter.com/book000)で受け付けます。

## ライセンス

このプロジェクトのライセンスは[MIT License](https://github.com/book000/gotoeat-map_yamanashi/blob/master/LICENSE)です。
