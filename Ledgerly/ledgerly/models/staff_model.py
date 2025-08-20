
from sqlalchemy import Column, Integer, String, Float, Date
from ledgerly.models.sales_model import Base

class Staff(Base):
    __tablename__ = "staff"
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    role = Column(String, nullable=False)
    salary = Column(Float, nullable=False)
    hire_date = Column(Date, nullable=False)
