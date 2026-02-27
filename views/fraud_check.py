import streamlit as st
from logic.fraud_engine import calculate_risk_score

def show_fraud_check():
    st.title("🔍 Real-time Transaction Auditor")
    st.write("Manually verify a transaction against the Guardian AI weighting engine.")
    
    col1, col2 = st.columns([1, 1])

    with col1:
        st.subheader("Transaction Metadata")
        with st.form("fraud_form"):
            amount = st.number_input("Transaction Amount ($)", min_value=0.0, value=1250.0, step=50.0)
            channel = st.selectbox("Payment Channel", ["UPI", "Card", "Wallet", "Net Banking"])
            location_anomaly = st.radio("Is this a new location for user?", ["No", "Yes"])
            new_device = st.radio("Is this a new device?", ["No", "Yes"])
            time_hour = st.slider("Time of Day (24h Format)", 0, 23, 14)
            
            submitted = st.form_submit_button("Run Risk Assessment")

    with col2:
        st.subheader("Guardian AI Result")
        if submitted:
            score, status, color = calculate_risk_score(amount, channel, location_anomaly, new_device, time_hour)
            
            st.markdown(f"""
                <div style="padding:30px; border-radius:10px; background-color:{color}; color:white; text-align:center;">
                    <h1 style="color:white; margin:0;">{score}/100</h1>
                    <h2 style="color:white; margin:0;">{status}</h2>
                </div>
            """, unsafe_allow_html=True)
            
            st.write("---")
            st.markdown("### Risk Breakdown")
            if score > 70:
                st.error("🚨 HIGH RISK: This transaction matches multiple fraud signatures. Immediate verification or block recommended.")
            elif score > 30:
                st.warning("⚠️ SUSPICIOUS: Unusual patterns detected. Trigger Step-up Authentication (OTP/Bio).")
            else:
                st.success("✅ SAFE: Transaction parameters are within normal behavioral bounds.")
                
            # Visualization of score
            st.progress(score / 100)
        else:
            st.info("Fill out the form and click 'Run Risk Assessment' to see the AI evaluation.")

    st.divider()
    st.markdown("""
    #### Quick Tips for Reviewers:
    - **UPI Transactions** are currently seeing a 4% higher fraud attempt rate.
    - **New Device** logins combined with high amounts (>5k) trigger mandatory suspension.
    - **Midnight transactions** (00:00 - 05:00) carry a 15-point risk penalty.
    """)
