import streamlit as st

def show_model_info():
    st.title("🧠 Guardian AI Logic & Feature Weights")
    
    st.markdown("""
    ### System Overview
    The Digital Payment Fraud Detection System uses a **Weighted Risk Score Engine**. 
    While many production systems use XGBoost or Random Forest models, this transparent engine allows 
    compliance officers to understand exactly *why* a transaction was flagged.
    
    ---
    
    ### Weighted Feature Logic
    Below are the current weights assigned to the real-time scoring engine:
    """)

    col1, col2 = st.columns(2)
    
    with col1:
        st.info("**Category: Transaction Magnitude**")
        st.write("- **>$50,000:** +40 Points")
        st.write("- **>$10,000:** +25 Points")
        st.write("- **>$5,000:** +15 Points")
        
        st.info("**Category: Channel Risk**")
        st.write("- **UPI:** +15 Points (High Velocity Risk)")
        st.write("- **Net Banking:** +10 Points")
        st.write("- **Digital Wallet:** +5 Points")

    with col2:
        st.info("**Category: Behavioral Context**")
        st.write("- **New Device Fingerprint:** +20 Points")
        st.write("- **Geographic Anomaly:** +10 Points")
        
        st.info("**Category: Temporal Context**")
        st.write("- **Midnight Window (00:00-05:00):** +15 Points")

    st.divider()

    st.markdown("""
    ### How Thresholds are Set
    1.  **Green (0-30):** Auto-Approved. Transaction follows normal user persona.
    2.  **Orange (31-65):** Soft-Flag. Redirects user to Multi-Factor Authentication (MFA). 
    3.  **Red (66-100):** Hard-Flag. Transaction blocked. Sent to manual review queue.

    ### Performance Metrics (Simulated)
    - **Precision:** 94.2%
    - **Recall:** 88.5%
    - **False Positive Rate:** 1.2%
    - **Latency:** < 45ms
    """)

    st.warning("⚠️ **Note:** Weights are adjusted weekly based on feedback loops from the human-in-the-loop review team.")
