
import streamlit as st
from streamlit_option_menu import option_menu
import base64
from main import LedgerlyApp

def load_css():
    """Load and inject custom CSS with theme support"""
    return """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');
    
    /* Base Variables */
    :root {
        --primary-color: #6366f1;
        --secondary-color: #8b5cf6;
        --accent-color: #06b6d4;
        --text-primary: #1f2937;
        --text-secondary: #6b7280;
        --bg-primary: #ffffff;
        --bg-secondary: #f8fafc;
        --border-color: #e5e7eb;
        --shadow: 0 1px 3px 0 rgba(0, 0, 0, 0.1);
    }
    
    .dark-theme {
        --primary-color: #8b5cf6;
        --secondary-color: #6366f1;
        --accent-color: #06b6d4;
        --text-primary: #f9fafb;
        --text-secondary: #d1d5db;
        --bg-primary: #111827;
        --bg-secondary: #1f2937;
        --border-color: #374151;
        --shadow: 0 1px 3px 0 rgba(0, 0, 0, 0.3);
    }
    
    /* Animated Gradient Background */
    .main-container {
        background: linear-gradient(-45deg, #6366f1, #8b5cf6, #06b6d4, #3b82f6);
        background-size: 400% 400%;
        animation: gradientShift 10s ease infinite;
        min-height: 100vh;
        position: relative;
    }
    
    .dark-theme .main-container {
        background: linear-gradient(-45deg, #1e1b4b, #312e81, #1e3a8a, #1e40af);
        background-size: 400% 400%;
        animation: gradientShift 10s ease infinite;
    }
    
    @keyframes gradientShift {
        0% { background-position: 0% 50%; }
        50% { background-position: 100% 50%; }
        100% { background-position: 0% 50%; }
    }
    
    /* Theme Toggle Button */
    .theme-toggle {
        position: fixed;
        top: 20px;
        right: 20px;
        z-index: 1000;
        background: var(--bg-primary);
        border: 2px solid var(--border-color);
        border-radius: 50px;
        padding: 8px 16px;
        cursor: pointer;
        box-shadow: var(--shadow);
        transition: all 0.3s ease;
        font-size: 18px;
        color: var(--text-primary);
    }
    
    .theme-toggle:hover {
        transform: scale(1.05);
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
    }
    
    /* Content Overlay */
    .content-overlay {
        background: rgba(255, 255, 255, 0.95);
        backdrop-filter: blur(10px);
        border-radius: 20px;
        margin: 20px;
        padding: 30px;
        box-shadow: 0 8px 32px rgba(31, 38, 135, 0.37);
        border: 1px solid rgba(255, 255, 255, 0.18);
        min-height: calc(100vh - 40px);
    }
    
    .dark-theme .content-overlay {
        background: rgba(31, 41, 55, 0.95);
        border: 1px solid rgba(107, 114, 128, 0.18);
    }
    
    /* Streamlit Customizations */
    .stApp {
        font-family: 'Inter', sans-serif;
    }
    
    .main .block-container {
        padding: 0;
        max-width: none;
    }
    
    /* Sidebar Styling */
    .css-1d391kg {
        background: var(--bg-secondary);
        border-right: 1px solid var(--border-color);
    }
    
    /* Metrics Cards */
    .metric-card {
        background: var(--bg-primary);
        padding: 20px;
        border-radius: 12px;
        border: 1px solid var(--border-color);
        box-shadow: var(--shadow);
        text-align: center;
        transition: transform 0.2s ease, box-shadow 0.2s ease;
    }
    
    .metric-card:hover {
        transform: translateY(-2px);
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
    }
    
    /* Form Styling */
    .stTextInput > div > div > input,
    .stNumberInput > div > div > input,
    .stSelectbox > div > div > select,
    .stTextArea > div > div > textarea {
        border-radius: 8px !important;
        border: 2px solid var(--border-color) !important;
        background: var(--bg-primary) !important;
        color: var(--text-primary) !important;
        transition: all 0.3s ease !important;
    }
    
    .stTextInput > div > div > input:focus,
    .stNumberInput > div > div > input:focus,
    .stSelectbox > div > div > select:focus,
    .stTextArea > div > div > textarea:focus {
        border-color: var(--primary-color) !important;
        box-shadow: 0 0 0 3px rgba(99, 102, 241, 0.1) !important;
    }
    
    /* Button Styling */
    .stButton > button {
        background: linear-gradient(135deg, var(--primary-color), var(--secondary-color)) !important;
        color: white !important;
        border: none !important;
        border-radius: 8px !important;
        padding: 12px 24px !important;
        font-weight: 500 !important;
        transition: all 0.3s ease !important;
        box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1) !important;
    }
    
    .stButton > button:hover {
        transform: translateY(-1px) !important;
        box-shadow: 0 4px 12px rgba(99, 102, 241, 0.3) !important;
    }
    
    /* Dataframe Styling */
    .stDataFrame {
        border-radius: 12px !important;
        overflow: hidden !important;
        box-shadow: var(--shadow) !important;
    }
    
    /* Alert Styling */
    .stAlert {
        border-radius: 8px !important;
        border: none !important;
        box-shadow: var(--shadow) !important;
    }
    
    /* Animation Classes */
    .fade-in {
        animation: fadeIn 0.6s ease-in;
    }
    
    @keyframes fadeIn {
        from { opacity: 0; transform: translateY(20px); }
        to { opacity: 1; transform: translateY(0); }
    }
    
    .slide-up {
        animation: slideUp 0.4s ease-out;
    }
    
    @keyframes slideUp {
        from { transform: translateY(30px); opacity: 0; }
        to { transform: translateY(0); opacity: 1; }
    }
    
    /* Responsive Design */
    @media (max-width: 768px) {
        .content-overlay {
            margin: 10px;
            padding: 20px;
            border-radius: 15px;
        }
        
        .theme-toggle {
            top: 10px;
            right: 10px;
            padding: 6px 12px;
            font-size: 16px;
        }
    }
    
    /* Hide Streamlit Branding */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    .stDeployButton {display:none;}
    </style>
    """

def main():
    st.set_page_config(
        page_title="Ledgerly - Business Management",
        page_icon="📊",
        layout="wide",
        initial_sidebar_state="expanded"
    )
    
    # Initialize theme in session state
    if 'theme' not in st.session_state:
        st.session_state.theme = 'light'
    
    # Load CSS
    st.markdown(load_css(), unsafe_allow_html=True)
    
    # Theme toggle
    col1, col2 = st.columns([10, 1])
    with col2:
        theme_icon = "🌙" if st.session_state.theme == 'light' else "🌞"
        if st.button(theme_icon, key="theme_toggle", help="Toggle theme"):
            st.session_state.theme = 'dark' if st.session_state.theme == 'light' else 'light'
            st.rerun()
    
    # Apply theme class
    theme_class = "dark-theme" if st.session_state.theme == 'dark' else ""
    
    # Main container with animated gradient
    st.markdown(f"""
        <div class="main-container {theme_class}">
            <div class="content-overlay fade-in">
    """, unsafe_allow_html=True)
    
    # Initialize and run app
    app = LedgerlyApp()
    app.run()
    
    # Close container
    st.markdown("</div></div>", unsafe_allow_html=True)

if __name__ == "__main__":
    main()
