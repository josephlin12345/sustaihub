import re
from concurrent.futures.thread import ThreadPoolExecutor
from datetime import datetime

import requests
from bs4 import BeautifulSoup

from database import Item, session


def query(url, data):
  try:
    response = requests.post(url, data)
    # 被擋下就重試
    if 'Too many query requests from your ip, please wait and try again later!!' in response.text:
      raise
  except:
    return query(url, data)
  return BeautifulSoup(response.text, 'html.parser')

def get_items(kind, year):
  data = {
    'month1': 0,
    'Stp': 4,
    'r1': 1,
    'keyWord': '轉換公司債',
    'KIND': kind,
    'year': year
  }
  page = query(items_url, data)
  items = []
  # 找出詳細資料按鈕
  for button in page.find_all('input', type='button', value='詳細資料'):
    # 從按鈕onclick的程式碼中擷取數值
    seq_no, spoke_time, spoke_date, _, co_id, _ = re.findall('"([^"]+)"', button['onclick'])
    items.append({
      'seq_no': seq_no,
      'spoke_time': spoke_time,
      'spoke_date': spoke_date,
      'co_id': co_id
    })
  return items

def get_details(item):
  data = {
    'firstin': 1,
    'step': 2
  }
  data.update(item)
  page = query(details_url, data)
  # 找出需要的資料
  title = page.find('td', class_='compName').text
  content = re.sub('\n\s', '', page.find_all('pre')[-1].text)
  try:
    上市_上櫃, 股票代號, 股票名稱 = re.findall('本資料由\s\((.+)\)\s(\d+)\s+(\S+)\s+公司提供', title)[0]
    return {
      '股票代號': 股票代號,
      '股票名稱': 股票名稱,
      '上市_上櫃': 上市_上櫃,
      '決議日期': re.findall('決議日期\s*:\s*(.*)', content)[0],
      '發行總額': re.findall('發行總額\s*:\s*(.*)', content)[0],
      '發行價格': re.findall('發行價格\s*:\s*(.*)', content)[0],
      '發行期間': re.findall('發行期間\s*:\s*(.*)', content)[0],
      '擔保品': re.findall('擔保品之種類、名稱、金額及約定事項\s*:\s*(.*)', content)[0],
      '發行用途': re.findall('募得價款之用途及運用計畫\s*:\s*(.*)', content)[0],
      '承銷方式': re.findall('承銷方式\s*:\s*(.*)', content)[0],
      '受託人': re.findall('公司債受託人\s*:\s*(.*)', content)[0],
      '承銷': re.findall('承銷或代銷機構\s*:\s*(.*)', content)[0],
      '轉換基準日': re.findall('附有轉換、交換或認股者，其換股基準日\s*:\s*(.*)', content)[0],
    }
  # 找不到對應資料
  except IndexError:
    pass

base_url = 'https://mops.twse.com.tw/mops/web/'
items_url = base_url + 'ajax_t51sb10'
details_url = base_url + 'ajax_t05st01'
db = session()

with ThreadPoolExecutor() as executor:
  # 取得清單，kind:上市/上櫃、year:0~今年
  for items in executor.map(lambda p: get_items(*p), [(kind, year) for kind in ['L', 'O'] for year in range(1, datetime.now().year - 1911 + 1)]):
    # 取得每個項目的詳細資料
    for details in executor.map(get_details, items):
      # 加到資料庫
      if details:
        print(details)
        db.add(Item(**details))
        db.commit()

db.close()