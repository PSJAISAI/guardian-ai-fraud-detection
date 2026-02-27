import pandas as pd
import numpy as np
import datetime

def generate_mock_data(n=75000):
    """
    Simulates a secure transaction dataset for demo purposes.
    Generates realistic features including timestamps, amounts, channels, and locations.
    """
    np.random.seed(42)
    start_date = datetime.datetime.now() - datetime.timedelta(days=30)
    
    # Core features
    dates = [start_date + datetime.timedelta(minutes=np.random.randint(0, 43200)) for _ in range(n)]
    amounts = np.random.exponential(scale=1000, size=n) + 10 
    channels = np.random.choice(['UPI', 'Card', 'Wallet', 'Net Banking'], size=n, p=[0.4, 0.3, 0.2, 0.1])
    locations = np.random.choice(['Mumbai', 'Delhi', 'Bangalore', 'London', 'New York', 'Singapore', 'Dubai'], size=n)
    hours = [d.hour for d in dates]
    device_types = np.random.choice(['Mobile App', 'Web Browser', 'POS Terminal'], size=n, p=[0.6, 0.3, 0.1])
    
    # Fraud Simulation Logic (Rule-based probability)
    fraud_prob = np.zeros(n)
    for i in range(n):
        p = 0.01  # Base fraud rate (1%)
        
        # High amount risk
        if amounts[i] > 8000: p += 0.15
        elif amounts[i] > 3000: p += 0.05
        
        # Channel risk
        if channels[i] == 'UPI': p += 0.04
        
        # Time risk (Late night transactions)
        if hours[i] < 5 or hours[i] > 23: p += 0.08
        
        # Location risk (Cross-border simulation)
        if locations[i] in ['London', 'New York', 'Singapore'] and np.random.rand() > 0.8:
            p += 0.10
            
        fraud_prob[i] = min(p, 0.95) # Cap at 95%
    
    # Assign fraud labels based on probability
    is_fraud = np.random.binomial(1, fraud_prob)
    
    df = pd.DataFrame({
        'Timestamp': dates,
        'Amount': amounts,
        'Channel': channels,
        'Location': locations,
        'Hour': hours,
        'Device': device_types,
        'Is_Fraud': is_fraud
    })
    
    # Clean up: sort by time
    df = df.sort_values('Timestamp').reset_index(drop=True)
    return df
