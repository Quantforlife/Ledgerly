import pytest
from services.stock_service import StockService
from utils.db import init_db
from utils.config import DB_PATH

@pytest.fixture
def setup_db():
    init_db(DB_PATH)
    yield

def test_low_stock_alert(setup_db):
    stock = StockService()
    stock.update_stock("Sugar", 5, 10, 40)
    alerts = stock.get_low_stock_alerts()
    assert any("Sugar: 5 left; threshold 10" in alert for alert in alerts)