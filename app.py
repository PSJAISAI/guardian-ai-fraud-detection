import streamlit as st
from streamlit_option_menu import option_menu

# Local Logic Imports
from logic.data_generator import generate_mock_data

# View Imports
from views.dashboard import show_dashboard
from views.fraud_check import show_fraud_check
from views.analytics import show_analytics
from views.model_info import show_model_info

# Initial Web Page Configuration
st.set_page_config(
    layout="wide", 
    page_title="Guardian AI | Fraud Detection", 
    page_icon="🛡️"
)

# Custom Banking CSS
st.markdown("""
<style>
    /* Main Background and Text */
    .main {
        background-color: #f8f9fa;
    }
    
    /* Metrics Styling */
    div[data-testid="stMetricValue"] {
        font-size: 28px;
        color: #003366;
        font-weight: 700;
    }
    
    /* Sidebar Styling */
    section[data-testid="stSidebar"] {
        background-color: #ffffff;
        border-right: 1px solid #e0e0e0;
    }

    /* Primary Headers */
    h1, h2, h3 {
        color: #003366;
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
    }

    /* Custom Cards */
    .stMetric {
        background-color: white;
        padding: 20px !important;
        border-radius: 10px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.05);
        border-bottom: 4px solid #003366;
    }
    
    /* Buttons */
    .stButton>button {
        background-color: #003366;
        color: white;
        border-radius: 5px;
        width: 100%;
    }
</style>
""", unsafe_allow_html=True)

@st.cache_data(show_spinner="Generating Secure Simulation Data (75,000 records)...")
def get_cached_data():
    """Generates and caches the dataset for session performance."""
    return generate_mock_data(75000)

def main():
    # Sidebar Logo/Title
    with st.sidebar:
        st.markdown("<h1 style='text-align: center; color: #003366;'>🛡️ GUARDIAN AI</h1>", unsafe_allow_html=True)
        st.markdown("<p style='text-align: center; font-size: 0.8em;'>Secure Payment Intelligence</p>", unsafe_allow_html=True)
        st.divider()
        
        selected = option_menu(
            menu_title=None,
            options=["Dashboard", "Real-Time Check", "Deep Analytics", "Engine Specs"],
            icons=["grid-1x2", "shield-lock", "graph-up-arrow", "cpu"],
            menu_icon="cast",
            default_index=0,
            styles={
                "container": {"padding": "0!important", "background-color": "#ffffff"},
                "icon": {"color": "#003366", "font-size": "18px"}, 
                "nav-link": {"font-size": "16px", "text-align": "left", "margin":"5px", "--hover-color": "#f0f2f6"},
                "nav-link-selected": {"background-color": "#003366", "color": "white"},
            }
        )
        
        st.spacer = st.sidebar.empty()
        for _ in range(15): st.sidebar.write("") # Push info to bottom
        st.sidebar.info("Authorized Personnel Only\n\nVersion: 2.1.0-stable")

    # Load Data
    data = get_cached_data()

    # Application Routing Logic
    if selected == "Dashboard":
        show_dashboard(data)
    elif selected == "Real-Time Check":
        show_fraud_check()
    elif selected == "Deep Analytics":
        show_analytics(data)
    elif selected == "Engine Specs":
        show_model_info()

if __name__ == "__main__":
    main()
