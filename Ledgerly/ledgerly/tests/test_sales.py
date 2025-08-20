import pytest
from services.billing_service import BillingService
from services.stock_service import StockService
from utils.db import init_db
from utils.config import DB_PATH

@pytest.fixture
def setup_db():
    init_db(DB_PATH)
    yield

def test_add_sale_updates_stock(setup_db):
    billing = BillingService()
    stock = StockService()
    stock.update_stock("Sugar", 10, 5, 40)
    sale_id = billing.add_sale("Sugar", 2, 50, 100, "John")
    stock_data = stock.get_stock()
    assert any(item == "Sugar" and qty == 8 for item, qty, _, _ in stock_data)
    assert sale_id is not None