
from sqlalchemy import Column, Integer, String, Float, Date
from ledgerly.models.sales_model import Base

class Stock(Base):
    __tablename__ = "stock"
    id = Column(Integer, primary_key=True)
    item = Column(String, unique=True, nullable=False)
    qty = Column(Float, nullable=False)
    threshold = Column(Float, nullable=False)
    unit_cost = Column(Float, nullable=False)
    last_updated = Column(Date, nullable=False)
