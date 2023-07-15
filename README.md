# 程式說明

**環境:**

python 3.6或以上

**執行步驟:**

以下所有步驟指令均在資料夾下執行

* step 1:

  安裝需要的套件

      pip install - r requirements.txt

* step 2:

  建立資料庫

      python database.py

* step 3:

  抓取資料

      python scraper.py

**利用Docker執行:**

* step 1:

  在資料夾中下輸入指令建立docker image

      docker build -t scraper .

* step 2:

  建立容器並在背景執行

      docker run -d --name=scraper scraper

* step 3:

  查看執行log

      docker logs scraper

**程式執行流程:**

* step 1:

  使用多線程從網站爬取各年度清單

* step 2:

  從清單爬取個項目詳細資料並過濾出需要的資料

* step 3:

  加入splite資料庫

* 遇到的問題:

  正常執行會輸出爬取到的資料，但網站會限制爬取資料頻率，程式中被限制時會持續重試，如果持續被限制會一直沒有輸出

  有嘗試將線程數改為1、被限制時過幾秒再重試，解除註解scraper.py中以下3行程式碼以嘗試
  
      import time
      time.sleep(0.1)
      executor._max_workers = 1
