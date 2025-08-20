from sqlalchemy import Column, Integer, String, Float, Date
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class Sale(Base):
    __tablename__ = "sales"
    id = Column(Integer, primary_key=True)
    item = Column(String, nullable=False)
    qty = Column(Float, nullable=False)
    unit_price = Column(Float, nullable=False)
    total = Column(Float, nullable=False)
    customer = Column(String)
    date = Column(Date, nullable=False)
