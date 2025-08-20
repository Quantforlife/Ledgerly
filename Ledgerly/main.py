
import streamlit as st
from streamlit_option_menu import option_menu
from dashboard import Dashboard
from ledgerly.utils.db import init_db
from ledgerly.utils.config import DB_PATH

class LedgerlyApp:
    def __init__(self):
        try:
            init_db(DB_PATH)  # Initialize database on startup
            self.dashboard = Dashboard()
        except Exception as e:
            st.error(f"❌ Database initialization error: {str(e)}")
            st.stop()

    def run(self):
        # Sidebar navigation with icons
        with st.sidebar:
            st.markdown("""
                <div style="text-align: center; margin-bottom: 30px;">
                    <h1 style="color: var(--primary-color); margin-bottom: 5px;">📊 Ledgerly</h1>
                    <p style="color: var(--text-secondary); font-size: 14px;">Business Management Suite</p>
                </div>
            """, unsafe_allow_html=True)
            
            page = option_menu(
                menu_title=None,
                options=[
                    "Dashboard", 
                    "Sales", 
                    "Expenses", 
                    "Inventory", 
                    "Reports", 
                    "Settings"
                ],
                icons=[
                    "house-fill", 
                    "cart-plus-fill", 
                    "credit-card-fill", 
                    "box-seam-fill", 
                    "graph-up", 
                    "gear-fill"
                ],
                menu_icon="cast",
                default_index=0,
                orientation="vertical",
                styles={
                    "container": {
                        "padding": "0!important",
                        "background-color": "transparent"
                    },
                    "icon": {
                        "color": "var(--text-secondary)", 
                        "font-size": "18px"
                    },
                    "nav-link": {
                        "font-size": "16px",
                        "text-align": "left",
                        "margin": "5px 0",
                        "padding": "10px 15px",
                        "border-radius": "8px",
                        "color": "var(--text-primary)",
                        "background-color": "transparent",
                        "transition": "all 0.3s ease"
                    },
                    "nav-link-selected": {
                        "background": "linear-gradient(135deg, var(--primary-color), var(--secondary-color))",
                        "color": "white",
                        "box-shadow": "0 2px 4px rgba(0, 0, 0, 0.1)"
                    },
                }
            )
        
        # Route to appropriate page
        try:
            if page == "Dashboard":
                self.dashboard.show_dashboard()
            elif page == "Sales":
                self.dashboard.show_sales()
            elif page == "Expenses":
                self.dashboard.show_expenses()
            elif page == "Inventory":
                self.dashboard.show_inventory()
            elif page == "Reports":
                self.dashboard.show_reports()
            elif page == "Settings":
                self.dashboard.show_settings()
        except Exception as e:
            st.error(f"❌ An error occurred: {str(e)}")
            st.info("🔄 Please refresh the page or contact support if the issue persists.")
