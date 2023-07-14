from sqlalchemy import Column, Integer, String, create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

Base = declarative_base()
engine_url = 'sqlite:///data.db'
engine = create_engine(engine_url)
session = sessionmaker(engine)

class Item(Base):
  __tablename__ = 'item'
  id = Column(Integer, primary_key=True, autoincrement=True)
  股票代號 = Column(String)
  股票名稱 = Column(String)
  上市_上櫃 = Column(String)
  決議日期 = Column(String)
  發行總額 = Column(String)
  發行價格 = Column(String)
  發行期間 = Column(String)
  擔保品 = Column(String)
  發行用途 = Column(String)
  承銷方式 = Column(String)
  受託人 = Column(String)
  承銷 = Column(String)
  轉換基準日 = Column(String)

if __name__ == '__main__':
  Base.metadata.drop_all(engine)
  Base.metadata.create_all(engine)