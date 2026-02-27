import streamlit as st
import plotly.express as px
import pandas as pd

def show_analytics(df):
    st.title("📊 Deep Dive Analytics")
    st.markdown("Granular breakdown of transaction patterns and systemic vulnerabilities.")

    # Filter Sidebar for Analytics
    st.sidebar.subheader("Analytics Filters")
    channel_filter = st.sidebar.multiselect("Select Channels", options=df['Channel'].unique(), default=df['Channel'].unique())
    location_filter = st.sidebar.multiselect("Select Locations", options=df['Location'].unique(), default=df['Location'].unique())
    
    filtered_df = df[(df['Channel'].isin(channel_filter)) & (df['Location'].isin(location_filter))]

    tab1, tab2, tab3 = st.tabs(["Temporal Distribution", "Amount Analysis", "Metric Correlations"])

    with tab1:
        st.subheader("Fraud Occurrences by Hour of Day")
        hour_data = filtered_df.groupby(['Hour', 'Is_Fraud']).size().reset_index(name='Count')
        hour_data['Status'] = hour_data['Is_Fraud'].map({0: 'Safe', 1: 'Fraud'})
        fig_hour = px.line(hour_data, x='Hour', y='Count', color='Status', markers=True,
                          title="Peak Fraud Hours", color_discrete_map={'Safe': 'grey', 'Fraud': 'red'})
        st.plotly_chart(fig_hour, use_container_width=True)
        st.info("Observation: Fraud attempts typically spike between 1 AM and 4 AM.")

    with tab2:
        st.subheader("Transaction Amount Distribution")
        fig_dist = px.histogram(filtered_df, x="Amount", color="Is_Fraud", nbins=50,
                               title="Transaction Amount Spread (Fraud vs Safe)",
                               color_discrete_map={0: '#003366', 1: '#ff4b4b'},
                               marginal="box", barmode="overlay")
        st.plotly_chart(fig_dist, use_container_width=True)

    with tab3:
        st.subheader("Fraud Rate Heatmap: Channel vs Location")
        heatmap_data = filtered_df.groupby(['Channel', 'Location'])['Is_Fraud'].mean().reset_index()
        heatmap_data_pivot = heatmap_data.pivot(index='Channel', columns='Location', values='Is_Fraud')
        
        fig_heat = px.imshow(heatmap_data_pivot, 
                            labels=dict(x="Location", y="Channel", color="Fraud Rate"),
                            color_continuous_scale='Reds',
                            title="Regional Risk Vectors")
        st.plotly_chart(fig_heat, use_container_width=True)
        
    st.subheader("Sample Raw Flagged Data")
    st.dataframe(filtered_df[filtered_df['Is_Fraud'] == 1].head(100), use_container_width=True)
