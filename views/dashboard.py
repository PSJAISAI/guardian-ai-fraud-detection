import streamlit as st
import plotly.express as px
import pandas as pd

def show_dashboard(df):
    st.markdown("## 🛡️ Fraud Monitoring Command Center")
    st.markdown("Real-time summary of transaction health across all channels.")
    
    # Metrics Calculation
    total_tx = len(df)
    total_fraud = int(df['Is_Fraud'].sum())
    fraud_rate = (total_fraud / total_tx) * 100
    total_volume = df['Amount'].sum()
    fraud_volume = df[df['Is_Fraud'] == 1]['Amount'].sum()
    
    # KPI Row
    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Total Transactions", f"{total_tx:,}")
    c2.metric("Fraudulent Hits", f"{total_fraud:,}", delta=f"{fraud_rate:.2f}% Rate", delta_color="inverse")
    c3.metric("Total Volume", f"${total_volume/1e6:.2f}M")
    c4.metric("Prevented Loss", f"${fraud_volume/1e6:.2f}M", delta="High Risk", delta_color="off")
    
    st.divider()

    col_left, col_right = st.columns([1, 1])

    with col_left:
        st.subheader("Fraud Events by Channel")
        # Aggregating fraud by channel
        fraud_df = df[df['Is_Fraud'] == 1].groupby('Channel').size().reset_index(name='Fraud Count')
        fig_bar = px.bar(
            fraud_df, 
            x='Channel', 
            y='Fraud Count', 
            color='Channel',
            color_discrete_sequence=px.colors.qualitative.Prism,
            template="plotly_white",
            text_auto=True
        )
        st.plotly_chart(fig_bar, use_container_width=True)

    with col_right:
        st.subheader("Fraud vs Safe Volume (USD)")
        # Area chart over time
        df_daily = df.copy()
        df_daily['Date'] = df_daily['Timestamp'].dt.date
        volume_trend = df_daily.groupby(['Date', 'Is_Fraud'])['Amount'].sum().reset_index()
        volume_trend['Status'] = volume_trend['Is_Fraud'].map({0: 'Safe', 1: 'Fraudulent'})
        
        fig_area = px.area(
            volume_trend, 
            x='Date', 
            y='Amount', 
            color='Status',
            color_discrete_map={'Safe': '#003366', 'Fraudulent': '#ff4b4b'},
            template="plotly_white"
        )
        st.plotly_chart(fig_area, use_container_width=True)

    st.subheader("Geographic Fraud Density")
    geo_data = df[df['Is_Fraud'] == 1].groupby('Location').size().reset_index(name='Alerts')
    fig_geo = px.scatter(
        geo_data, 
        x='Location', 
        y='Alerts', 
        size='Alerts', 
        color='Location', 
        hover_name='Location',
        size_max=60,
        template="plotly_white"
    )
    st.plotly_chart(fig_geo, use_container_width=True)
