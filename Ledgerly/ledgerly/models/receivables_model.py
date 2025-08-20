
from sqlalchemy import Column, Integer, String, Float, Date
from ledgerly.models.sales_model import Base

class Receivable(Base):
    __tablename__ = "receivables"
    id = Column(Integer, primary_key=True)
    customer = Column(String, nullable=False)
    amount = Column(Float, nullable=False)
    due_date = Column(Date, nullable=False)
    status = Column(String, default="pending")
