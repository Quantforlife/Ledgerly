
from sqlalchemy.orm import sessionmaker
from ledgerly.models.stock_model import Stock
from ledgerly.utils.db import get_engine
from ledgerly.utils.helpers import parse_date

class StockService:
    def __init__(self):
        self.engine = get_engine()
        self.Session = sessionmaker(bind=self.engine)

    def get_stock(self):
        """Get all stock items"""
        session = self.Session()
        try:
            stocks = session.query(Stock).all()
            return [[stock.item, stock.qty, stock.threshold, stock.unit_cost] for stock in stocks]
        except Exception as e:
            raise e
        finally:
            session.close()

    def update_stock(self, item, qty, threshold, unit_cost):
        """Update or add stock item"""
        session = self.Session()
        try:
            existing_stock = session.query(Stock).filter_by(item=item).first()
            if existing_stock:
                existing_stock.qty = qty
                existing_stock.threshold = threshold
                existing_stock.unit_cost = unit_cost
                existing_stock.last_updated = parse_date("today")
            else:
                new_stock = Stock(
                    item=item,
                    qty=qty,
                    threshold=threshold,
                    unit_cost=unit_cost,
                    last_updated=parse_date("today")
                )
                session.add(new_stock)
            session.commit()
        except Exception as e:
            session.rollback()
            raise e
        finally:
            session.close()

    def get_low_stock_alerts(self):
        """Get items with low stock"""
        session = self.Session()
        try:
            low_stock_items = session.query(Stock).filter(Stock.qty <= Stock.threshold).all()
            alerts = []
            for item in low_stock_items:
                alerts.append(f"⚠️ {item.item}: Only {item.qty} left (threshold: {item.threshold})")
            return alerts
        except Exception as e:
            return [f"Error loading stock alerts: {str(e)}"]
        finally:
            session.close()

class StockService:
    def __init__(self):
        self.engine = get_engine()
        self.Session = sessionmaker(bind=self.engine)

    def update_stock(self, item, qty, threshold, unit_cost):
        session = self.Session()
        try:
            stock = session.query(Stock).filter_by(item=item).first()
            if stock:
                stock.qty = qty
                stock.threshold = threshold
                stock.unit_cost = unit_cost
                stock.last_updated = parse_date("today")
            else:
                stock = Stock(item=item, qty=qty, threshold=threshold, unit_cost=unit_cost, last_updated=parse_date("today"))
                session.add(stock)
            session.commit()
        except Exception as e:
            session.rollback()
            raise e
        finally:
            session.close()

    def get_stock(self):
        session = self.Session()
        try:
            return [(s.item, s.qty, s.threshold, s.unit_cost) for s in session.query(Stock).all()]
        finally:
            session.close()

    def get_low_stock_alerts(self):
        session = self.Session()
        try:
            alerts = []
            for stock in session.query(Stock).all():
                if stock.qty <= stock.threshold:
                    alerts.append(f"{stock.item}: {stock.qty} left; threshold {stock.threshold}")
            return alerts
        finally:
            session.close()
