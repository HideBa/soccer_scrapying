# 運用手順

## Scrapyの実行
### 必要ライブラリのインストール
`pip install scrapy`

JavaScriptによって生成されるページはScrapyだけではデータ取得できないため以下のライブラリもインストールする。

`pip install selenium`

### ドライバのインストール
Seleniumでブラウザを使うためのインストールをする

[Chrome driver](https://sites.google.com/a/chromium.org/chromedriver/downloads)へアクセスし、該当するChromeのバージョンに応じたドライバをインストールする。
（Firefoxを使う場合はgeckodriverを使う。

### 実行手順
* U18の試合結果を取得
`scrapy crawl SoccerSpider -o directory_name/filename.csv`　でCSV出力
* U15の試合結果を取得
`scrapy crawl u15`
* U12の試合結果を取得
`scrapy crawl u12`
* U15の各年の試合結果取得
`scrapy crawl u15_2007`
* 取得結果サマリーを作成(必要に応じて欲しい関数の事項部分をコメントアウト、解除)
`python success_rate_pd'