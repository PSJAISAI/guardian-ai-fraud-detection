def calculate_risk_score(amount, channel, location_anomaly, new_device, time_of_day):
    """
    Logic engine to calculate risk score (0-100) based on weighted features.
    Returns: (score, status_label, color)
    """
    score = 0
    
    # 1. Amount Weighting (Max 40 points)
    if amount > 50000: score += 40
    elif amount > 10000: score += 25
    elif amount > 5000: score += 15
        
    # 2. Channel Risk (Max 15 points)
    if channel == 'UPI': score += 15
    elif channel == 'Net Banking': score += 10
    elif channel == 'Wallet': score += 5
        
    # 3. Behavioral Risks (Max 30 points)
    if new_device == 'Yes': score += 20
    if location_anomaly == 'Yes': score += 10
        
    # 4. Temporal Risk (Max 15 points)
    # Late night hours (12 AM - 5 AM)
    if 0 <= time_of_day <= 5:
        score += 15
        
    # Ensure score stays within bounds
    score = min(score, 100)
    
    # Classification logic
    if score < 30:
        return score, "SAFE", "#28a745" # Green
    elif score < 65:
        return score, "SUSPICIOUS", "#fd7e14" # Orange
    else:
        return score, "HIGH RISK / FRAUD", "#dc3545" # Red
