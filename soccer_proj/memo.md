`extract()`で該当要素すべて
`extract_first`で該当するものの最初のオブジェクト
`::text`がないと、文字列だけでなく要素も返してくれる
`.extract()`がないとセレクターのXpathを返してくれる。

`res.css('div#main>div)`だと直下
`res.css('div#main div)`たど直下だけでなく子要素すべて