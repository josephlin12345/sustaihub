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

      docker run -d --name scraper scraper