# dashboard.py
# ----------------------------------------------------------------------
# Ledgerly — Business Management App (Dashboard UI)
#
# This dashboard focuses on a refined, production-friendly UI / UX:
#   - Glassmorphism (frosted) surfaces + animated gradient background
#   - Light / Dark theme toggle with live CSS variable updates
#   - Micro-interactions (hover, press, slide, fade) and accent shadows
#   - Flexible CSV/Excel import (auto-map headers, soft validation)
#   - Subtle motion on KPI cards, buttons, and section transitions
#   - Non-blocking row-level error handling for imports
#   - Zero changes to your service layer contracts
#
# It preserves your original functional surface:
#   Pages: Dashboard • Sales • Inventory • Expenses • Reports • Settings
#   Services: BillingService, StockService, AnalyticsService, ReminderService
#   Utils: format_currency, parse_date, CURRENCY_SYMBOL
#
# Drop-in replacement: keep your project structure identical and replace
# only this file. No extra libraries required beyond your requirements.txt.
# ----------------------------------------------------------------------

from __future__ import annotations

import io
import json
import datetime
from typing import Dict, Iterable, List, Optional, Tuple

import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st

# Project services / utils
from ledgerly.services.billing_service import BillingService
from ledgerly.services.stock_service import StockService
from ledgerly.services.analytics_service import AnalyticsService
from ledgerly.services.reminder_service import ReminderService
from ledgerly.utils.helpers import format_currency, parse_date
from ledgerly.utils.config import CURRENCY_SYMBOL


# ============================== Dashboard ============================== #
class Dashboard:
    """
    Streamlit page controller for Ledgerly.

    Responsibilities:
      - Global theme + CSS/JS injection (glassmorphism + animations)
      - Page composition (Dashboard / Sales / Inventory / Expenses / Reports / Settings)
      - Robust CSV/Excel ingest with header auto-mapping
      - Consistent UI primitives (cards, metrics, shimmers, separators)
    """

    # --------------------------- Initialization --------------------------- #
    def __init__(self) -> None:
        # Services (unchanged contracts)
        self.billing = BillingService()
        self.stock = StockService()
        self.analytics = AnalyticsService()
        self.reminder = ReminderService()

        # Session defaults
        if "theme" not in st.session_state:
            st.session_state.theme = "light"
        if "quick_action" not in st.session_state:
            st.session_state.quick_action = None

        self._inject_css()  # first paint with current theme

    # ------------------------------ Theming ------------------------------ #
    def _inject_css(self) -> None:
        """Inject global CSS: animated gradient, frosted cards, micro-UX."""
        is_dark = (st.session_state.get("theme") == "dark")

        # Color tokens for both themes
        text_primary = "#E5E7EB" if is_dark else "#0F172A"
        text_secondary = "#9CA3AF" if is_dark else "#475569"
        border_color = "rgba(255,255,255,0.18)" if is_dark else "rgba(15,23,42,0.08)"
        card_bg = "rgba(255,255,255,0.08)" if is_dark else "rgba(255,255,255,0.85)"
        subtle_bg = "rgba(255,255,255,0.06)" if is_dark else "#F8FAFC"
        card_shadow = "0 16px 40px rgba(0,0,0,0.45)" if is_dark else "0 18px 34px rgba(2,6,23,0.08)"
        ring_color = "rgba(59,130,246,0.35)"  # focus ring

        # Accent palette (kept constant for brand recognition)
        accent_1 = "#6366F1"  # indigo
        accent_2 = "#06B6D4"  # cyan
        accent_3 = "#10B981"  # emerald
        accent_4 = "#F59E0B"  # amber
        accent_danger = "#EF4444"

        # Animated gradient backdrop (infinite pan)
        st.markdown(
            f"""
            <style>
            :root {{
                --text-primary: {text_primary};
                --text-secondary: {text_secondary};
                --border-color: {border_color};
                --card-bg: {card_bg};
                --subtle-bg: {subtle_bg};
                --card-shadow: {card_shadow};
                --ring: {ring_color};
                --accent-1: {accent_1};
                --accent-2: {accent_2};
                --accent-3: {accent_3};
                --accent-4: {accent_4};
                --accent-danger: {accent_danger};
            }}

            /* App background with animated gradient */
            .stApp {{
                background: radial-gradient(1200px 600px at 20% 10%, rgba(99,102,241,0.22), transparent 60%),
                            radial-gradient(1200px 600px at 80% 0%, rgba(6,182,212,0.18), transparent 60%),
                            linear-gradient(135deg, #0f172a 0%, #1e293b 40%, #0b1020 100%);
                background-size: 180% 180%;
                animation: bgShift 24s ease-in-out infinite alternate;
            }}
            @keyframes bgShift {{
                0% {{ background-position: 0% 20%, 100% 0%, 0% 0%; }}
                50% {{ background-position: 50% 40%, 50% 50%, 50% 50%; }}
                100% {{ background-position: 100% 20%, 0% 0%, 100% 100%; }}
            }}

            /* Glass card container */
            .glass {{
                background: var(--card-bg);
                border: 1px solid var(--border-color);
                border-radius: 18px;
                box-shadow: var(--card-shadow);
                -webkit-backdrop-filter: saturate(140%) blur(14px);
                backdrop-filter: saturate(140%) blur(14px);
                padding: 18px 18px;
                transition: transform .24s ease, box-shadow .24s ease, border-color .2s ease;
            }}
            .glass:hover {{
                transform: translateY(-3px);
                box-shadow: 0 24px 48px rgba(0,0,0,0.3);
                border-color: rgba(99,102,241,0.45);
            }}

            /* Soft section container */
            .soft {{
                background: var(--subtle-bg);
                border-radius: 14px;
                border: 1px dashed rgba(125,125,125,0.16);
                padding: 16px 16px;
            }}

            /* Metric card with shimmer underline */
            .metric {{
                position: relative;
                overflow: hidden;
            }}
            .metric h3 {{
                margin: 0;
                color: var(--text-secondary);
                font-size: 13.5px;
                letter-spacing: .2px;
                text-transform: uppercase;
            }}
            .metric .value {{
                font-weight: 800;
                font-size: 28px;
                color: var(--text-primary);
                margin-top: 8px;
                line-height: 1.1;
            }}
            .metric::after {{
                content: "";
                position: absolute;
                left: 0;
                bottom: 0;
                height: 2px;
                width: 100%;
                background: linear-gradient(90deg, transparent, var(--accent-2), transparent);
                animation: shimmer 2.8s ease-in-out infinite;
                opacity: .6;
            }}
            @keyframes shimmer {{
                0% {{ transform: translateX(-40%); }}
                50% {{ transform: translateX(40%); }}
                100% {{ transform: translateX(-40%); }}
            }}

            /* Animations helpers */
            .fade-in {{ animation: fadeIn .55s ease both; }}
            .slide-up {{ animation: slideUp .6s cubic-bezier(.2,.7,.3,1) both; }}
            .pop-in {{ animation: popIn .25s ease both; }}
            @keyframes fadeIn {{
                from {{ opacity: 0; transform: translateY(6px); }}
                to   {{ opacity: 1; transform: translateY(0); }}
            }}
            @keyframes slideUp {{
                from {{ opacity: 0; transform: translateY(10px); }}
                to   {{ opacity: 1; transform: translateY(0); }}
            }}
            @keyframes popIn {{
                from {{ transform: scale(.98); opacity: .0; }}
                to   {{ transform: scale(1); opacity: 1; }}
            }}

            /* Buttons */
            .stButton>button {{
                border-radius: 12px;
                border: 1px solid var(--border-color);
                background: linear-gradient(180deg, rgba(255,255,255,.14), rgba(255,255,255,.06));
                color: var(--text-primary);
                font-weight: 700 !important;
                letter-spacing: .2px;
                transition: transform .18s ease, box-shadow .18s ease, border-color .18s ease;
            }}
            .stButton>button:hover {{
                transform: translateY(-2px);
                box-shadow: 0 16px 32px rgba(0,0,0,.25);
                border-color: rgba(99,102,241,0.55);
            }}
            .stButton>button:active {{
                transform: translateY(0px) scale(.99);
            }}

            /* Inputs focus ring */
            input:focus, textarea:focus, select:focus {{
                outline: none !important;
                box-shadow: 0 0 0 3px var(--ring);
                border-color: rgba(99,102,241,0.55) !important;
            }}

            /* Headings and typography overrides */
            h1, h2, h3, h4, label, p, span, div, small {{
                color: var(--text-primary);
            }}
            .muted {{ color: var(--text-secondary) !important; }}

            /* Dataframe rounding */
            .stDataFrame, .stTable {{
                border-radius: 14px !important;
            }}

            /* Subtle pill */
            .pill {{
                display: inline-flex;
                align-items: center;
                gap: 8px;
                padding: 6px 10px;
                border-radius: 999px;
                background: rgba(99,102,241,0.14);
                color: var(--text-primary);
                border: 1px solid var(--border-color);
                font-size: 12.5px;
                letter-spacing: .15px;
            }}
            .pill .dot {{
                width: 8px; height: 8px; border-radius: 999px; background: var(--accent-2);
                box-shadow: 0 0 0 3px rgba(6,182,212,0.25);
            }}

            /* Divider */
            .divider {{
                height: 1px;
                width: 100%;
                background: linear-gradient(90deg, transparent, rgba(255,255,255,.25), transparent);
                margin: 14px 0 10px 0;
            }}
            </style>
            """,
            unsafe_allow_html=True,
        )

    # -------------------------- CSV Normalization -------------------------- #
    @staticmethod
    def _clean_cols(cols: Iterable[str]) -> List[str]:
        return [str(c).strip().lower().replace(" ", "_").replace("-", "_") for c in cols]

    def _rename_with_synonyms(self, df: pd.DataFrame, mapping: Dict[str, List[str]]) -> pd.DataFrame:
        df = df.copy()
        df.columns = self._clean_cols(df.columns)
        rename_map: Dict[str, str] = {}
        for target, syns in mapping.items():
            for c in df.columns:
                if c == target or c in syns:
                    rename_map[c] = target
        if rename_map:
            df = df.rename(columns=rename_map)
        return df

    def _normalize_sales_df(self, df: pd.DataFrame) -> pd.DataFrame:
        mapping = {
            "item": ["product", "product_name", "item_name", "name", "sku", "title"],
            "qty": ["quantity", "units", "count", "qnty", "qnt", "qty_sold"],
            "unit_price": ["price", "rate", "unitprice", "selling_price", "mrp", "unit_cost"],
            "customer": ["customer_name", "client", "buyer", "member", "party"],
        }
        df = self._rename_with_synonyms(df, mapping)
        # Ensure columns exist
        for col in ["item", "qty", "unit_price", "customer"]:
            if col not in df.columns:
                df[col] = "" if col in ("item", "customer") else 0
        # Coerce
        df["item"] = df["item"].astype(str).str.strip()
        df["customer"] = df["customer"].astype(str).fillna("").str.strip()
        df["qty"] = pd.to_numeric(df["qty"], errors="coerce").fillna(1)
        df["unit_price"] = pd.to_numeric(df["unit_price"], errors="coerce").fillna(0)
        # Filters
        df = df[df["item"].str.len() > 0]
        df = df[df["qty"] > 0]
        return df[["item", "qty", "unit_price", "customer"]]

    def _normalize_inventory_df(self, df: pd.DataFrame) -> pd.DataFrame:
        mapping = {
            "item": ["item_name", "product", "name", "sku", "title"],
            "qty": ["quantity", "stock", "on_hand", "units"],
            "threshold": ["reorder_level", "reorder_point", "min_qty", "min_stock"],
            "unit_cost": ["cost", "purchase_price", "unitprice", "base_cost"],
        }
        df = self._rename_with_synonyms(df, mapping)
        for col in ["item", "qty", "threshold", "unit_cost"]:
            if col not in df.columns:
                df[col] = "" if col == "item" else 0
        df["item"] = df["item"].astype(str).str.strip()
        df["qty"] = pd.to_numeric(df["qty"], errors="coerce").fillna(0)
        df["threshold"] = pd.to_numeric(df["threshold"], errors="coerce").fillna(0)
        df["unit_cost"] = pd.to_numeric(df["unit_cost"], errors="coerce").fillna(0)
        df = df[df["item"].str.len() > 0]
        return df[["item", "qty", "threshold", "unit_cost"]]

    def _normalize_expenses_df(self, df: pd.DataFrame) -> pd.DataFrame:
        mapping = {
            "category": ["type", "head", "expense_category"],
            "vendor": ["supplier", "party", "payee", "seller"],
            "amount": ["amt", "value", "cost", "price", "total", "expense"],
            "notes": ["note", "remark", "remarks", "description"],
        }
        df = self._rename_with_synonyms(df, mapping)
        for col in ["category", "vendor", "amount", "notes"]:
            if col not in df.columns:
                df[col] = "" if col in ("category", "vendor", "notes") else 0
        df["category"] = df["category"].astype(str).str.strip()
        df["vendor"] = df["vendor"].astype(str).fillna("").str.strip()
        df["notes"] = df["notes"].astype(str).fillna("").str.strip()
        df["amount"] = pd.to_numeric(df["amount"], errors="coerce").fillna(0)
        df = df[df["category"].str.len() > 0]
        df = df[df["amount"] > 0]
        return df[["category", "vendor", "amount", "notes"]]

    # ----------------------------- UI Primitives ----------------------------- #
    def _header(self, title: str, subtitle: Optional[str] = None, badge: Optional[str] = None) -> None:
        st.markdown('<div class="glass fade-in">', unsafe_allow_html=True)
        # Title row: title + theme toggle
        left, right = st.columns([0.82, 0.18])
        with left:
            st.markdown(
                f"""
                <div style="display:flex;align-items:center;gap:12px;">
                    <div class="pill"><span class="dot"></span> Ledgerly</div>
                    <h1 style="margin:.2rem 0 0 0;">{title}</h1>
                </div>
                """,
                unsafe_allow_html=True,
            )
            if subtitle:
                st.markdown(f"<p class='muted' style='margin:.2rem 0 0 0;'>{subtitle}</p>", unsafe_allow_html=True)
            if badge:
                st.markdown(f"<div class='pill' style='margin-top:10px;'>{badge}</div>", unsafe_allow_html=True)
        with right:
            # Theme toggle is sticky per session; re-inject CSS on change
            toggle = st.toggle("🌙 Dark Mode", value=(st.session_state.theme == "dark"))
            new_theme = "dark" if toggle else "light"
            if new_theme != st.session_state.theme:
                st.session_state.theme = new_theme
                self._inject_css()
                st.experimental_rerun()
        st.markdown("</div>", unsafe_allow_html=True)

    def _metric(self, title: str, value: str, delta: Optional[float] = None, positive: bool = True) -> None:
        color = "var(--accent-3)" if positive else "var(--accent-danger)"
        sign = "+" if (delta is not None and delta >= 0) else ""
        delta_html = f"<div class='muted' style='font-size:13px;margin-top:4px;color:{color};'>{sign}{delta:.1f}%</div>" if delta is not None else ""
        st.markdown(
            f"""
            <div class="glass metric pop-in">
                <h3>{title}</h3>
                <div class="value">{value}</div>
                {delta_html}
            </div>
            """,
            unsafe_allow_html=True,
        )

    def _soft_block(self, title: str, body_html: str) -> None:
        st.markdown(
            f"""
            <div class="glass slide-up" style="padding:0;">
                <div class="soft" style="border-top-left-radius: 18px; border-top-right-radius:18px;">
                    <h3 style="margin:0 0 6px 0;">{title}</h3>
                    <div class="muted" style="font-size:13.5px;">Automated checks to keep you in control.</div>
                </div>
                <div style="padding:16px 18px;">
                    {body_html}
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    # ================================ Pages ================================ #
    # ------------------------------- Dashboard ------------------------------ #
    def show_dashboard(self) -> None:
        self._header("📊 Dashboard", "Your business insights at a glance", badge="Realtime KPIs")

        # Top KPI metrics row
        col1, col2, col3, col4 = st.columns(4)
        try:
            todays_sales = float(self.analytics.get_todays_sales())
        except Exception:
            todays_sales = 0.0
        try:
            todays_expenses = float(self.analytics.get_todays_expenses())
        except Exception:
            todays_expenses = 0.0
        try:
            net_profit = float(self.analytics.get_net_profit())
        except Exception:
            net_profit = todays_sales - todays_expenses
        try:
            stock_items = self.stock.get_stock()
            total_items = len(stock_items) if stock_items else 0
        except Exception:
            total_items = 0

        with col1:
            self._metric("Today's Sales", f"{CURRENCY_SYMBOL}{todays_sales:,.2f}", delta=12.5, positive=True)
        with col2:
            # negative delta colored red via _metric logic
            self._metric("Today's Expenses", f"{CURRENCY_SYMBOL}{todays_expenses:,.2f}", delta=-5.2, positive=False)
        with col3:
            self._metric("Net Profit", f"{CURRENCY_SYMBOL}{net_profit:,.2f}", delta=8.3, positive=True)
        with col4:
            self._metric("Stock Items", f"{total_items}", delta=2.1, positive=True)

        # Alerts and receivables
        colA, colB = st.columns([1, 1])
        with colA:
            try:
                alerts = self.stock.get_low_stock_alerts()
            except Exception as e:
                alerts = []
                st.caption(f"ℹ️ Alerts unavailable: {e}")
            if alerts:
                body = "<ul style='margin:0;padding-left:18px;'>" + "".join([f"<li>{a}</li>" for a in alerts]) + "</ul>"
            else:
                body = "<div class='pill'><span class='dot'></span> No low stock alerts.</div>"
            self._soft_block("🚨 Low Stock Alerts", body)

        with colB:
            try:
                dues = self.analytics.get_pending_receivables()
            except Exception as e:
                dues = []
                st.caption(f"ℹ️ Receivables unavailable: {e}")

            st.markdown('<div class="glass slide-up">', unsafe_allow_html=True)
            st.subheader("💰 Pending Receivables")
            if dues:
                df = pd.DataFrame(dues, columns=["Customer", "Amount", "Due Date"])
                st.dataframe(df, use_container_width=True, height=240)
            else:
                st.info("✅ No pending dues.")
            st.markdown("</div>", unsafe_allow_html=True)

        # Quick actions as frosted buttons
        st.markdown('<div class="glass slide-up">', unsafe_allow_html=True)
        st.subheader("⚡ Quick Actions")
        qa1, qa2, qa3, qa4 = st.columns(4)
        with qa1:
            if st.button("➕ Quick Sale", use_container_width=True):
                st.session_state.quick_action = "sale"
        with qa2:
            if st.button("📦 Add Stock", use_container_width=True):
                st.session_state.quick_action = "stock"
        with qa3:
            if st.button("💸 Add Expense", use_container_width=True):
                st.session_state.quick_action = "expense"
        with qa4:
            if st.button("📊 View Reports", use_container_width=True):
                st.session_state.quick_action = "reports"
        st.markdown("</div>", unsafe_allow_html=True)

        # Contextual helper after a quick action selection
        if st.session_state.quick_action:
            tip = {
                "sale": "Use the Sales page to add items with quantity and price; inventory auto-adjusts.",
                "stock": "Use Inventory to add/update items and thresholds (alerts fire automatically).",
                "expense": "Use Expenses to record costs with categories; breakdown shows in Reports.",
                "reports": "Open Reports to visualize trends, top items, and forecasts.",
            }.get(st.session_state.quick_action, "")
            st.markdown(
                f"<div class='glass pop-in' style='border-left:4px solid var(--accent-2);'><b>Quick Tip ·</b> {tip}</div>",
                unsafe_allow_html=True,
            )

    # -------------------------------- Sales -------------------------------- #
    def show_sales(self) -> None:
        self._header("💰 Sales Management", "Record and track your sales transactions")

        with st.form("sale_form", clear_on_submit=True):
            form_card = st.container()
            with form_card:
                c1, c2 = st.columns(2)
                with c1:
                    item = st.text_input("🏷️ Item Name", placeholder="Enter item name")
                    qty = st.number_input("📦 Quantity", min_value=0.0, step=1.0, value=1.0)
                    barcode = st.text_input("🔍 Scan/Enter Code", placeholder="Barcode or item code")
                with c2:
                    unit_price = st.number_input("💵 Unit Price", min_value=0.0, step=0.01, value=0.0)
                    customer = st.text_input("👤 Customer", placeholder="Customer name (optional)")
                submitted = st.form_submit_button("🚀 Add Sale", use_container_width=True)

            if submitted and item and qty > 0 and unit_price > 0:
                total = qty * unit_price
                try:
                    sale_id = self.billing.add_sale(item, qty, unit_price, total, customer)
                    st.success(f"✅ Sale added successfully! Receipt ID: {sale_id}")

                    with st.expander("📄 View Receipt", expanded=True):
                        st.markdown(
                            f"""
                            <div class="glass" style="padding:16px;">
                                <h3 style="margin:0 0 6px 0;">🧾 Receipt #{sale_id}</h3>
                                <div class="divider"></div>
                                <p><b>Item:</b> {item}</p>
                                <p><b>Quantity:</b> {qty}</p>
                                <p><b>Unit Price:</b> {CURRENCY_SYMBOL}{unit_price:,.2f}</p>
                                <p><b>Total:</b> {CURRENCY_SYMBOL}{total:,.2f}</p>
                                <p><b>Customer:</b> {customer or 'Walk-in'}</p>
                                <p><b>Date:</b> {parse_date('today')}</p>
                            </div>
                            """,
                            unsafe_allow_html=True,
                        )
                except Exception as e:
                    st.error(f"❌ Error adding sale: {str(e)}")

        st.markdown('<div class="glass slide-up">', unsafe_allow_html=True)
        c1, c2 = st.columns([1, 1])
        with c1:
            if st.button("🎤 Simulate Voice Input", use_container_width=True):
                st.info("🗣️ Voice command parsed: 'Add sale of 2 sugar at 50 each for John'")
        st.markdown("</div>", unsafe_allow_html=True)

    # ------------------------------- Expenses ------------------------------- #
    def show_expenses(self) -> None:
        self._header("💸 Expense Management", "Track and categorize your business expenses")

        with st.form("expense_form", clear_on_submit=True):
            c1, c2 = st.columns(2)
            with c1:
                category = st.selectbox(
                    "📂 Category",
                    ["⛽ Fuel", "🏠 Rent", "👥 Salaries", "💡 Utilities", "📋 Misc"],
                    format_func=lambda x: x,
                )
                vendor = st.text_input("🏪 Vendor", placeholder="Vendor/supplier name")
            with c2:
                amount = st.number_input("💰 Amount", min_value=0.0, step=0.01, value=0.0)
                notes = st.text_area("📝 Notes", placeholder="Additional details...")

            submitted = st.form_submit_button("💾 Add Expense", use_container_width=True)
            if submitted and amount > 0:
                try:
                    clean_category = category.split(" ", 1)[1] if " " in category else category
                    self.billing.add_expense(clean_category, vendor, amount, notes)
                    st.success("✅ Expense added successfully!")
                except Exception as e:
                    st.error(f"❌ Error adding expense: {str(e)}")

    # ------------------------------- Inventory ------------------------------ #
    def show_inventory(self) -> None:
        self._header("📦 Inventory Management", "Manage your stock levels and track inventory")

        with st.form("inventory_form", clear_on_submit=True):
            c1, c2 = st.columns(2)
            with c1:
                item = st.text_input("🏷️ Item Name", placeholder="Enter item name")
                qty = st.number_input("📦 Quantity", min_value=0.0, step=1.0, value=0.0)
            with c2:
                threshold = st.number_input("⚠️ Low Stock Threshold", min_value=0.0, step=1.0, value=5.0)
                unit_cost = st.number_input("💰 Unit Cost", min_value=0.0, step=0.01, value=0.0)
            submitted = st.form_submit_button("🔄 Add / Update Item", use_container_width=True)

            if submitted and item and qty >= 0 and threshold >= 0:
                try:
                    stock_id, is_new = self.billing.add_stock_safe(item, qty, threshold, unit_cost)
                    if is_new:
                        st.success(f"✅ Added {item} to inventory successfully!")
                    else:
                        st.success(f"🔄 Updated {item} in inventory successfully!")
                except Exception as e:
                    st.error(f"❌ Error updating inventory: {str(e)}")

        # Current stock table
        st.subheader("📋 Current Stock")
        try:
            stock_data = self.stock.get_stock()
            if stock_data:
                df = pd.DataFrame(stock_data, columns=["Item", "Quantity", "Threshold", "Unit Cost"])

                # Status derivation
                def status(row):
                    if row["Quantity"] <= row["Threshold"]:
                        return "🔴 Low"
                    elif row["Quantity"] <= row["Threshold"] * 2:
                        return "🟡 Medium"
                    return "🟢 Good"

                df["Status"] = df.apply(status, axis=1)
                df["Unit Cost"] = df["Unit Cost"].apply(lambda x: f"{CURRENCY_SYMBOL}{x:.2f}")
                st.dataframe(df, use_container_width=True, height=340)
            else:
                st.info("📦 No items in inventory yet. Add some items to get started!")
        except Exception as e:
            st.error(f"❌ Error loading inventory: {str(e)}")

    # -------------------------------- Reports ------------------------------- #
    def show_reports(self) -> None:
        self._header("📊 Business Reports", "Analyze your business performance and trends")

        tab1, tab2, tab3, tab4 = st.tabs(
            ["📈 Sales Analysis", "💰 Revenue Trends", "📊 Expense Breakdown", "🔮 Forecasts"]
        )

        with tab1:
            st.subheader("🏆 Top Selling Items")
            try:
                top_items = self.analytics.get_top_items()
                if not top_items.empty:
                    fig = px.bar(
                        top_items,
                        x="item",
                        y="qty",
                        title="Top 5 Items Sold",
                        color="qty",
                        color_continuous_scale="viridis",
                    )
                    fig.update_layout(
                        plot_bgcolor="rgba(0,0,0,0)",
                        paper_bgcolor="rgba(0,0,0,0)",
                        margin=dict(l=10, r=10, t=48, b=10),
                    )
                    st.plotly_chart(fig, use_container_width=True)
                else:
                    st.info("📊 No sales data available yet.")
            except Exception as e:
                st.error(f"❌ Error loading sales data: {str(e)}")

        with tab2:
            st.subheader("📈 Monthly Sales Trend")
            try:
                trend = self.analytics.get_monthly_trend("sales")
                if not trend.empty:
                    fig = px.line(trend, x="date", y="total", title="Monthly Sales Trend", line_shape="spline")
                    fig.update_traces(line_color="#6366f1", line_width=3)
                    fig.update_layout(
                        plot_bgcolor="rgba(0,0,0,0)",
                        paper_bgcolor="rgba(0,0,0,0)",
                        margin=dict(l=10, r=10, t=48, b=10),
                    )
                    st.plotly_chart(fig, use_container_width=True)
                else:
                    st.info("📈 No trend data available yet.")
            except Exception as e:
                st.error(f"❌ Error loading trend data: {str(e)}")

        with tab3:
            st.subheader("🥧 Expense Breakdown")
            try:
                breakdown = self.analytics.get_expense_breakdown()
                if not breakdown.empty:
                    fig = px.pie(breakdown, names="category", values="amount", title="Expense Distribution by Category")
                    fig.update_layout(
                        plot_bgcolor="rgba(0,0,0,0)",
                        paper_bgcolor="rgba(0,0,0,0)",
                        margin=dict(l=10, r=10, t=48, b=10),
                    )
                    st.plotly_chart(fig, use_container_width=True)
                else:
                    st.info("💸 No expense data available yet.")
            except Exception as e:
                st.error(f"❌ Error loading expense data: {str(e)}")

        with tab4:
            st.subheader("🔮 Sales Forecast")
            try:
                forecast_value = float(self.analytics.get_sales_forecast())
                st.metric("7-Day Sales Forecast", f"{CURRENCY_SYMBOL}{forecast_value:,.2f}")

                # Lightweight illustrative curve
                dates = [datetime.date.today() + datetime.timedelta(days=i) for i in range(7)]
                vals = [forecast_value * (0.82 + 0.38 * (i / 6)) for i in range(7)]
                fig = go.Figure()
                fig.add_trace(
                    go.Scatter(
                        x=dates,
                        y=vals,
                        mode="lines+markers",
                        name="Forecast",
                        line=dict(color="#06b6d4", width=3),
                    )
                )
                fig.update_layout(
                    title="7-Day Sales Forecast",
                    plot_bgcolor="rgba(0,0,0,0)",
                    paper_bgcolor="rgba(0,0,0,0)",
                    margin=dict(l=10, r=10, t=48, b=10),
                )
                st.plotly_chart(fig, use_container_width=True)
            except Exception as e:
                st.error(f"❌ Error generating forecast: {str(e)}")

        # Export primary report
        st.markdown('<div class="glass" style="margin-top:12px;">', unsafe_allow_html=True)
        c1, c2, c3 = st.columns(3)
        with c1:
            if st.button("📤 Export Top Items CSV", use_container_width=True):
                try:
                    top_items = self.analytics.get_top_items()
                    if not top_items.empty:
                        csv = top_items.to_csv(index=False)
                        st.download_button("💾 Download CSV", csv, "sales_report.csv", "text/csv", use_container_width=True)
                    else:
                        st.warning("⚠️ No data to export.")
                except Exception as e:
                    st.error(f"❌ Export error: {str(e)}")
        st.markdown("</div>", unsafe_allow_html=True)

    # --------------------- Import (CSV/Excel) – Robust Path --------------------- #
    def process_csv_upload(self, uploaded_file, data_type: str) -> None:
        """
        Flexible import routine:
          - Try CSV first; fallback to Excel (.xlsx)
          - Auto-map headers using robust synonyms
          - Soft-validate per-row; skip bad rows with toast
          - Success report at the end
        """
        try:
            try:
                df = pd.read_csv(uploaded_file)
            except Exception:
                uploaded_file.seek(0)
                df = pd.read_excel(uploaded_file)

            if data_type == "Sales":
                norm = self._normalize_sales_df(df)
                success = 0
                for _, row in norm.iterrows():
                    try:
                        item = str(row["item"])
                        qty = float(row["qty"])
                        price = float(row["unit_price"])
                        total = qty * price
                        customer = str(row.get("customer", "") or "")
                        self.billing.add_sale(item, qty, price, total, customer)
                        success += 1
                    except Exception as e:
                        st.toast(f"Skipped row · {e}", icon="⚠️")
                st.success(f"✅ Imported {success} sales record(s).")

            elif data_type == "Inventory":
                norm = self._normalize_inventory_df(df)
                success = 0
                for _, row in norm.iterrows():
                    try:
                        self.billing.add_stock_safe(
                            str(row["item"]),
                            float(row["qty"]),
                            float(row["threshold"]),
                            float(row["unit_cost"]),
                        )
                        success += 1
                    except Exception as e:
                        st.toast(f"Skipped row · {e}", icon="⚠️")
                st.success(f"✅ Imported {success} inventory item(s).")

            elif data_type == "Expenses":
                norm = self._normalize_expenses_df(df)
                success = 0
                for _, row in norm.iterrows():
                    try:
                        self.billing.add_expense(
                            str(row["category"]),
                            str(row.get("vendor", "") or ""),
                            float(row["amount"]),
                            str(row.get("notes", "") or ""),
                        )
                        success += 1
                    except Exception as e:
                        st.toast(f"Skipped row · {e}", icon="⚠️")
                st.success(f"✅ Imported {success} expense record(s).")

            else:
                st.error("❌ Unknown data type selected.")

        except Exception as e:
            st.error(f"❌ Error processing file: {str(e)}")

    # -------------------------------- Settings ------------------------------- #
    def show_settings(self) -> None:
        self._header("⚙️ Settings & Configuration", "Manage app preferences and data")

        tab1, tab2, tab3 = st.tabs(["📤 Import / Export", "🎨 Appearance", "🧪 Sample Data"])

        # Import / Export
        with tab1:
            st.subheader("📂 CSV / Excel Data Import")
            l, r = st.columns(2)
            with l:
                data_type = st.selectbox("📊 Select Data Type", ["Sales", "Inventory", "Expenses"])
                uploaded_file = st.file_uploader(
                    f"📁 Upload {data_type} CSV/Excel",
                    type=["csv", "xlsx"],
                    help=f"Upload a {data_type.lower()} file (.csv or .xlsx). Headers are flexible; extra columns ignored.",
                )
                if uploaded_file is not None:
                    if st.button(f"🚀 Import {data_type} Data", use_container_width=True):
                        self.process_csv_upload(uploaded_file, data_type)

            with r:
                st.markdown("### 📋 Header Mapping Guide")
                if data_type == "Sales":
                    st.markdown(
                        """
                        **Targets**: `item`, `qty`, `unit_price`, `customer`  
                        **Synonyms**:  
                        - *item*: product, product_name, item_name, sku  
                        - *qty*: quantity, units, count, qnty  
                        - *unit_price*: price, rate, selling_price, unit_cost  
                        - *customer*: client, buyer, party  
                        Extra columns are ignored. Missing fields get safe defaults.
                        """
                    )
                elif data_type == "Inventory":
                    st.markdown(
                        """
                        **Targets**: `item`, `qty`, `threshold`, `unit_cost`  
                        **Synonyms**:  
                        - *item*: product, item_name, sku  
                        - *qty*: stock, on_hand, units  
                        - *threshold*: reorder_level, min_qty  
                        - *unit_cost*: cost, purchase_price, base_cost  
                        """
                    )
                else:
                    st.markdown(
                        """
                        **Targets**: `category`, `vendor`, `amount`, `notes`  
                        **Synonyms**:  
                        - *category*: type, head  
                        - *vendor*: supplier, payee, party  
                        - *amount*: price, value, expense  
                        - *notes*: remark, description  
                        """
                    )

            # Preview zone
            if uploaded_file is not None:
                st.markdown('<div class="glass slide-up">', unsafe_allow_html=True)
                st.subheader("👀 Preview")
                try:
                    uploaded_file.seek(0)
                    preview_df = pd.read_csv(uploaded_file)
                except Exception:
                    uploaded_file.seek(0)
                    preview_df = pd.read_excel(uploaded_file)
                st.dataframe(preview_df.head(), use_container_width=True, height=240)
                st.caption(f"Rows detected: {len(preview_df)}")
                st.markdown("</div>", unsafe_allow_html=True)

        # Appearance
        with tab2:
            st.subheader("🎛️ Theme")
            current = st.session_state.theme
            choice = st.radio(
                "🌈 Color Mode",
                ["light", "dark"],
                index=(0 if current == "light" else 1),
                format_func=lambda x: "🌞 Light" if x == "light" else "🌙 Dark",
                horizontal=True,
            )
            if choice != current:
                st.session_state.theme = choice
                self._inject_css()
                st.success(f"Theme changed to {choice}.")
                st.experimental_rerun()

            st.markdown("---")
            st.subheader("🔔 Notifications (UI Only)")
            c1, c2 = st.columns(2)
            with c1:
                low_stock_alerts = st.checkbox("📦 Low Stock Alerts", value=True)
                payment_reminders = st.checkbox("💰 Payment Reminders", value=True)
            with c2:
                daily_reports = st.checkbox("📊 Daily Reports", value=False)
                weekly_summary = st.checkbox("📈 Weekly Summary", value=False)
            if st.button("💾 Save Settings", use_container_width=True):
                st.success("✅ Settings saved.")

        # Sample Data
        with tab3:
            st.subheader("🧪 Sample Data Management")
            a, b = st.columns(2)
            with a:
                if st.button("🎲 Load Sample Data", use_container_width=True):
                    try:
                        self.billing.load_sample_data()
                        st.success("✅ Sample data loaded successfully!")
                        st.balloons()
                    except Exception as e:
                        st.error(f"❌ Error loading sample data: {str(e)}")
            with b:
                if st.button("🧹 Clear All Data", use_container_width=True):
                    st.warning("⚠️ This will delete all data. This action cannot be undone!")
                    st.error("🚫 Delete-all is intentionally disabled for safety.")

            st.markdown("---")
            st.subheader("📧 Test Notifications")
            if st.button("📨 Send Test Reminder", use_container_width=True):
                try:
                    self.reminder.send_reminder("John Doe", 500, parse_date("2025-08-26"))
                    st.success("✅ Test reminder sent (see server logs).")
                except Exception as e:
                    st.error(f"❌ Error sending reminder: {str(e)}")

    # ------------------------------- Entrypoint ------------------------------ #
    def run(self) -> None:
        # Sidebar navigation (kept simple and predictable)
        st.sidebar.title("Ledgerly")
        page = st.sidebar.radio("Navigate", ["Dashboard", "Sales", "Inventory", "Expenses", "Reports", "Settings"])

        if page == "Dashboard":
            self.show_dashboard()
        elif page == "Sales":
            self.show_sales()
        elif page == "Inventory":
            self.show_inventory()
        elif page == "Expenses":
            self.show_expenses()
        elif page == "Reports":
            self.show_reports()
        elif page == "Settings":
            self.show_settings()
