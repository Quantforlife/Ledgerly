
import os
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from ledgerly.models.sales_model import Base
from ledgerly.models.expenses_model import Expense
from ledgerly.models.receivables_model import Receivable
from ledgerly.models.stock_model import Stock

def get_engine():
    """Get database engine"""
    from .config import DB_PATH
    # Ensure data directory exists
    os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
    return create_engine(f"sqlite:///{DB_PATH}")

def init_db(db_path):
    """Initialize database with all tables"""
    engine = get_engine()
    Base.metadata.create_all(engine)
