"""Create engineered features for analytics and machine learning."""

import pandas as pd
import numpy as np
from datetime import datetime

class FeatureEngineer:
    """Engineer features from sensor data."""
    
    def __init__(self):
        self.safe_thresholds = {
            'gas_level': 1000,
            'temperature': 25,
            'vibration': 2.0,
            'smoke_level': 0.2
        }
    
    def create_features(self, df):
        """Create all engineered features."""
        df = df.copy()
        df['timestamp'] = pd.to_datetime(df['timestamp'])
        
        # 1. Time-based features
        df['hour'] = df['timestamp'].dt.hour
        df['day'] = df['timestamp'].dt.day
        df['month'] = df['timestamp'].dt.month
        df['weekday'] = df['timestamp'].dt.dayofweek
        df['is_night_shift'] = ((df['hour'] >= 22) | (df['hour'] < 6)).astype(int)
        df['is_weekend'] = (df['weekday'].isin([5, 6])).astype(int)
        
        # 2. Risk scores (0-100 scale)
        df['gas_risk_score'] = self._calculate_gas_risk(df['gas_level'])
        df['temperature_risk_score'] = self._calculate_temperature_risk(df['temperature'])
        df['vibration_risk_score'] = self._calculate_vibration_risk(df['vibration'])
        df['humidity_risk_score'] = self._calculate_humidity_risk(df['humidity'])
        
        # 3. Combined risk score
        df['combined_risk_score'] = (
            df['gas_risk_score'] * 0.4 +
            df['temperature_risk_score'] * 0.3 +
            df['vibration_risk_score'] * 0.2 +
            df['humidity_risk_score'] * 0.1
        )
        
        # 4. Anomaly flags
        df['abnormal_gas_flag'] = (df['gas_level'] > self.safe_thresholds['gas_level']).astype(int)
        df['abnormal_temperature_flag'] = (df['temperature'] > self.safe_thresholds['temperature']).astype(int)
        df['abnormal_vibration_flag'] = (df['vibration'] > self.safe_thresholds['vibration']).astype(int)
        df['abnormal_smoke_flag'] = (df['smoke_level'] > self.safe_thresholds['smoke_level']).astype(int)
        
        # 5. Overall anomaly score
        df['total_anomalies'] = (
            df['abnormal_gas_flag'] +
            df['abnormal_temperature_flag'] +
            df['abnormal_vibration_flag'] +
            df['abnormal_smoke_flag']
        )
        df['anomaly_flag'] = (df['total_anomalies'] > 0).astype(int)
        
        # 6. Equipment risk
        df['equipment_risk'] = df['equipment_status'].map({
            'NORMAL': 0,
            'WARNING': 50,
            'CRITICAL': 100
        })
        
        # 7. Zone risk baseline (from historical data)
        zone_risk_map = {
            'ZONE A': 30,
            'ZONE B': 25,
            'ZONE C': 40,
            'ZONE D': 35,
            'ZONE E': 45
        }
        df['zone_risk_baseline'] = df['mine_zone'].map(zone_risk_map)
        
        # 8. Rolling averages (5-reading window)
        for col in ['gas_level', 'temperature', 'vibration']:
            df[f'{col}_rolling_avg'] = df.groupby('mine_zone')[col].transform(
                lambda x: x.rolling(window=5, min_periods=1).mean()
            )
        
        # 9. Change from rolling average
        df['gas_level_change'] = df['gas_level'] - df['gas_level_rolling_avg']
        df['temperature_change'] = df['temperature'] - df['temperature_rolling_avg']
        df['vibration_change'] = df['vibration'] - df['vibration_rolling_avg']
        
        # 10. Zone statistics
        zone_stats = df.groupby('mine_zone').agg({
            'gas_level': 'mean',
            'temperature': 'mean',
            'vibration': 'mean'
        }).round(2)
        df = df.merge(zone_stats.add_suffix('_zone_mean'), left_on='mine_zone', right_index=True)
        
        # 11. Safety incident risk
        df['incident_risk'] = df['combined_risk_score'] * 0.5 + df['equipment_risk'] * 0.3 + df['total_anomalies'] * 10
        df['incident_risk'] = df['incident_risk'].clip(0, 100)
        
        return df
    
    def _calculate_gas_risk(self, gas_level):
        """Calculate gas-related risk score (0-100)."""
        risk = np.zeros_like(gas_level, dtype=float)
        risk = np.where(gas_level < 800, 0, risk)
        risk = np.where((gas_level >= 800) & (gas_level < 1000), (gas_level - 800) / 2, risk)
        risk = np.where((gas_level >= 1000) & (gas_level < 1500), 10 + (gas_level - 1000) / 10, risk)
        risk = np.where((gas_level >= 1500) & (gas_level < 2000), 55 + (gas_level - 1500) / 10, risk)
        risk = np.where(gas_level >= 2000, 100, risk)
        return np.round(risk, 2)
    
    def _calculate_temperature_risk(self, temperature):
        """Calculate temperature-related risk score (0-100)."""
        risk = np.zeros_like(temperature, dtype=float)
        risk = np.where(temperature < 20, 0, risk)
        risk = np.where((temperature >= 20) & (temperature < 25), (temperature - 20) * 4, risk)
        risk = np.where((temperature >= 25) & (temperature < 30), 20 + (temperature - 25) * 12, risk)
        risk = np.where((temperature >= 30) & (temperature < 35), 80 + (temperature - 30) * 4, risk)
        risk = np.where(temperature >= 35, 100, risk)
        return np.round(risk, 2)
    
    def _calculate_vibration_risk(self, vibration):
        """Calculate vibration-related risk score (0-100)."""
        risk = np.zeros_like(vibration, dtype=float)
        risk = np.where(vibration < 1.5, 0, risk)
        risk = np.where((vibration >= 1.5) & (vibration < 2.5), (vibration - 1.5) * 20, risk)
        risk = np.where((vibration >= 2.5) & (vibration < 4.0), 20 + (vibration - 2.5) * 13.33, risk)
        risk = np.where((vibration >= 4.0) & (vibration < 6.0), 60 + (vibration - 4.0) * 20, risk)
        risk = np.where(vibration >= 6.0, 100, risk)
        return np.round(risk, 2)
    
    def _calculate_humidity_risk(self, humidity):
        """Calculate humidity-related risk score (0-100)."""
        # Too low or too high humidity is risky
        risk = np.zeros_like(humidity, dtype=float)
        optimal_low = 40
        optimal_high = 70
        
        # Below optimal: increases risk
        risk = np.where(humidity < optimal_low, (optimal_low - humidity) * 2, risk)
        # Above optimal: increases risk
        risk = np.where(humidity > optimal_high, (humidity - optimal_high) * 2, risk)
        
        return np.clip(risk, 0, 100).round(2)


if __name__ == "__main__":
    df = pd.read_csv('data/processed/mine_safety_clean.csv')
    engineer = FeatureEngineer()
    df_features = engineer.create_features(df)
    df_features.to_csv('data/processed/mine_safety_features.csv', index=False)
    print("Features engineered successfully!")
    print(f"Total features created: {df_features.shape[1]}")
