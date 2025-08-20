
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from ledgerly.models.sales_model import Sale
from ledgerly.models.expenses_model import Expense
from ledgerly.models.receivables_model import Receivable
from ledgerly.models.stock_model import Stock
from ledgerly.utils.db import get_engine
from ledgerly.utils.helpers import parse_date
import pandas as pd

class BillingService:
    def __init__(self):
        self.engine = get_engine()
        self.Session = sessionmaker(bind=self.engine)

    def add_sale(self, item, qty, unit_price, total, customer):
        session = self.Session()
        try:
            sale = Sale(item=item, qty=qty, unit_price=unit_price, total=total, customer=customer, date=parse_date("today"))
            session.add(sale)
            # Update stock
            stock = session.query(Stock).filter_by(item=item).first()
            if stock:
                stock.qty -= qty
                stock.last_updated = parse_date("today")
            session.commit()
            return sale.id
        except Exception as e:
            session.rollback()
            raise e
        finally:
            session.close()

    def add_expense(self, category, vendor, amount, notes):
        session = self.Session()
        try:
            expense = Expense(category=category, vendor=vendor, amount=amount, date=parse_date("today"), notes=notes)
            session.add(expense)
            session.commit()
        except Exception as e:
            session.rollback()
            raise e
        finally:
            session.close()

    def add_stock_safe(self, item, qty, threshold, unit_cost):
        """Safely add or update stock without duplicates"""
        session = self.Session()
        try:
            existing_stock = session.query(Stock).filter_by(item=item).first()
            if existing_stock:
                # Update existing stock
                existing_stock.qty = qty
                existing_stock.threshold = threshold
                existing_stock.unit_cost = unit_cost
                existing_stock.last_updated = parse_date("today")
                session.commit()
                return existing_stock.id, False  # False indicates update
            else:
                # Add new stock
                new_stock = Stock(
                    item=item, 
                    qty=qty, 
                    threshold=threshold, 
                    unit_cost=unit_cost,
                    last_updated=parse_date("today")
                )
                session.add(new_stock)
                session.commit()
                return new_stock.id, True  # True indicates new addition
        except Exception as e:
            session.rollback()
            raise e
        finally:
            session.close()

    def load_sample_data(self):
        session = self.Session()
        try:
            # Sample sales data
            sample_sales = [
                {"item": "Sugar", "qty": 2, "unit_price": 50, "total": 100, "customer": "John", "date": "2025-01-15"},
                {"item": "Rice", "qty": 1, "unit_price": 60, "total": 60, "customer": "Mary", "date": "2025-01-15"},
                {"item": "Tea", "qty": 5, "unit_price": 10, "total": 50, "customer": "Bob", "date": "2025-01-16"},
            ]
            
            for data in sample_sales:
                existing_sale = session.query(Sale).filter_by(
                    item=data["item"], 
                    customer=data["customer"], 
                    date=parse_date(data["date"])
                ).first()
                if not existing_sale:
                    sale = Sale(**{**data, "date": parse_date(data["date"])})
                    session.add(sale)
            
            # Sample stock data
            stock_data = [
                {"item": "Sugar", "qty": 100, "threshold": 10, "unit_cost": 40, "last_updated": parse_date("2025-01-15")},
                {"item": "Rice", "qty": 50, "threshold": 5, "unit_cost": 60, "last_updated": parse_date("2025-01-15")},
                {"item": "Tea", "qty": 200, "threshold": 20, "unit_cost": 8, "last_updated": parse_date("2025-01-15")},
            ]
            for data in stock_data:
                existing_stock = session.query(Stock).filter_by(item=data["item"]).first()
                if existing_stock:
                    # Update existing stock
                    existing_stock.qty = data["qty"]
                    existing_stock.threshold = data["threshold"]
                    existing_stock.unit_cost = data["unit_cost"]
                    existing_stock.last_updated = data["last_updated"]
                else:
                    # Add new stock
                    stock = Stock(**data)
                    session.add(stock)
            session.commit()
        except Exception as e:
            session.rollback()
            raise e
        finally:
            session.close()
