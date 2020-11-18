# kamigamo-scraper (ベータ版)

上賀茂神社ー京都産業大学間を行き来する上賀茂シャトルバスの到着時刻を表示するツールです．ベータ版なので，予期せぬエラーが起こる可能性があります．

## 動作環境

Python 3.6.0 以降 (動作確認済み)

## 必要ライブラリ

- BeautifulSoup4

```
pip install bs4
```

## 使用例

コマンドライン引数に出発地点を入れてください．

- 神社発の時刻

```
python kamigamo-scraper.py from_shrine
```

- 大学発の時刻

```
python kamigamo-scraper.py from_univ
```
