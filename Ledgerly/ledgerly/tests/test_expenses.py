import pytest
from services.billing_service import BillingService
from utils.db import init_db
from utils.config import DB_PATH

@pytest.fixture
def setup_db():
    init_db(DB_PATH)
    yield

def test_add_expense(setup_db):
    billing = BillingService()
    billing.add_expense("Fuel", "VendorX", 100, "Fuel cost")
    # Assuming we can query expenses table; minimal check for non-error