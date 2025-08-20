
from sqlalchemy import Column, Integer, String, Float, Date, Text
from ledgerly.models.sales_model import Base

class Expense(Base):
    __tablename__ = "expenses"
    id = Column(Integer, primary_key=True)
    category = Column(String, nullable=False)
    vendor = Column(String)
    amount = Column(Float, nullable=False)
    date = Column(Date, nullable=False)
    notes = Column(Text)
