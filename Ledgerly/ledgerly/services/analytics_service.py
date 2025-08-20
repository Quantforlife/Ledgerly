
from sqlalchemy.orm import sessionmaker
from sqlalchemy import func
from ledgerly.models.sales_model import Sale
from ledgerly.models.expenses_model import Expense
from ledgerly.models.receivables_model import Receivable
from ledgerly.utils.db import get_engine
from ledgerly.utils.helpers import parse_date
import pandas as pd
from datetime import datetime, timedelta

class AnalyticsService:
    def __init__(self):
        self.engine = get_engine()
        self.Session = sessionmaker(bind=self.engine)

    def get_todays_sales(self):
        session = self.Session()
        try:
            today = parse_date("today")
            result = session.query(func.sum(Sale.total)).filter(Sale.date == today).scalar()
            return result or 0.0
        finally:
            session.close()

    def get_todays_expenses(self):
        session = self.Session()
        try:
            today = parse_date("today")
            result = session.query(func.sum(Expense.amount)).filter(Expense.date == today).scalar()
            return result or 0.0
        finally:
            session.close()

    def get_net_profit(self):
        return self.get_todays_sales() - self.get_todays_expenses()

    def get_pending_receivables(self):
        session = self.Session()
        try:
            receivables = session.query(Receivable).filter(Receivable.status == "pending").all()
            return [(r.customer, r.amount, r.due_date) for r in receivables]
        finally:
            session.close()

    def get_top_items(self):
        session = self.Session()
        try:
            result = session.query(Sale.item, func.sum(Sale.qty).label('qty')).group_by(Sale.item).order_by(func.sum(Sale.qty).desc()).limit(5).all()
            return pd.DataFrame(result, columns=['item', 'qty'])
        finally:
            session.close()

    def get_monthly_trend(self, data_type="sales"):
        session = self.Session()
        try:
            if data_type == "sales":
                result = session.query(Sale.date, func.sum(Sale.total).label('total')).group_by(Sale.date).order_by(Sale.date).all()
            else:
                result = session.query(Expense.date, func.sum(Expense.amount).label('total')).group_by(Expense.date).order_by(Expense.date).all()
            return pd.DataFrame(result, columns=['date', 'total'])
        finally:
            session.close()

    def get_expense_breakdown(self):
        session = self.Session()
        try:
            result = session.query(Expense.category, func.sum(Expense.amount).label('amount')).group_by(Expense.category).all()
            return pd.DataFrame(result, columns=['category', 'amount'])
        finally:
            session.close()

    def get_sales_forecast(self):
        # Simple 7-day forecast based on recent average
        session = self.Session()
        try:
            seven_days_ago = parse_date("today") - timedelta(days=7)
            result = session.query(func.avg(Sale.total)).filter(Sale.date >= seven_days_ago).scalar()
            return (result or 0.0) * 7
        finally:
            session.close()
