"""Anomaly detection using multiple methods."""

import pandas as pd
import numpy as np
from sklearn.ensemble import IsolationForest
from scipy import stats

class AnomalyDetector:
    """Detect anomalies in sensor data."""
    
    def __init__(self, df):
        self.df = df.copy()
        self.df['timestamp'] = pd.to_datetime(self.df['timestamp'])
        self.anomalies = []
    
    def detect_iqr_anomalies(self, columns=['gas_level', 'temperature', 'vibration'], multiplier=1.5):
        """Detect anomalies using Interquartile Range (IQR) method."""
        anomaly_scores = pd.DataFrame(index=self.df.index)
        
        for col in columns:
            Q1 = self.df[col].quantile(0.25)
            Q3 = self.df[col].quantile(0.75)
            IQR = Q3 - Q1
            
            lower_bound = Q1 - multiplier * IQR
            upper_bound = Q3 + multiplier * IQR
            
            is_anomaly = (self.df[col] < lower_bound) | (self.df[col] > upper_bound)
            anomaly_scores[f'{col}_iqr'] = is_anomaly.astype(int)
        
        return anomaly_scores
    
    def detect_zscore_anomalies(self, columns=['gas_level', 'temperature', 'vibration'], threshold=3):
        """Detect anomalies using Z-score method."""
        anomaly_scores = pd.DataFrame(index=self.df.index)
        
        for col in columns:
            z_scores = np.abs(stats.zscore(self.df[col]))
            is_anomaly = z_scores > threshold
            anomaly_scores[f'{col}_zscore'] = is_anomaly.astype(int)
        
        return anomaly_scores
    
    def detect_isolation_forest_anomalies(self, columns=['gas_level', 'temperature', 'humidity', 'vibration'], contamination=0.05):
        """Detect anomalies using Isolation Forest algorithm."""
        iso_forest = IsolationForest(contamination=contamination, random_state=42)
        X = self.df[columns].fillna(self.df[columns].mean())
        predictions = iso_forest.fit_predict(X)
        anomaly_scores = (predictions == -1).astype(int)
        
        return pd.DataFrame({f'isolation_forest': anomaly_scores}, index=self.df.index)
    
    def detect_statistical_anomalies(self):
        """Detect anomalies based on statistical outliers in combinations."""
        # Detect readings with multiple abnormal conditions
        anomaly_flags = pd.DataFrame(index=self.df.index)
        
        # Gas anomaly
        gas_anomaly = self.df['gas_level'] > self.df['gas_level'].quantile(0.95)
        anomaly_flags['gas_anomaly'] = gas_anomaly.astype(int)
        
        # Temperature anomaly
        temp_anomaly = (self.df['temperature'] > self.df['temperature'].quantile(0.95)) | \
                       (self.df['temperature'] < self.df['temperature'].quantile(0.05))
        anomaly_flags['temp_anomaly'] = temp_anomaly.astype(int)
        
        # Vibration anomaly
        vib_anomaly = self.df['vibration'] > self.df['vibration'].quantile(0.95)
        anomaly_flags['vib_anomaly'] = vib_anomaly.astype(int)
        
        # Humidity anomaly (too dry or too humid)
        humidity_anomaly = (self.df['humidity'] > self.df['humidity'].quantile(0.95)) | \
                          (self.df['humidity'] < self.df['humidity'].quantile(0.05))
        anomaly_flags['humidity_anomaly'] = humidity_anomaly.astype(int)
        
        # Combined anomaly (multiple conditions)
        anomaly_flags['combined_anomaly'] = (anomaly_flags.sum(axis=1) >= 2).astype(int)
        
        return anomaly_flags
    
    def detect_zone_anomalies(self):
        """Detect anomalies specific to each zone."""
        zone_anomalies = []
        
        for zone in self.df['mine_zone'].unique():
            zone_data = self.df[self.df['mine_zone'] == zone]
            
            for sensor in ['gas_level', 'temperature', 'vibration']:
                mean = zone_data[sensor].mean()
                std = zone_data[sensor].std()
                
                # Anomalies beyond 3 standard deviations
                anomalous_indices = zone_data[
                    (zone_data[sensor] > mean + 3*std) | (zone_data[sensor] < mean - 3*std)
                ].index
                
                for idx in anomalous_indices:
                    zone_anomalies.append({
                        'index': idx,
                        'zone': zone,
                        'sensor': sensor,
                        'value': self.df.loc[idx, sensor],
                        'mean': mean,
                        'std': std,
                        'z_score': (self.df.loc[idx, sensor] - mean) / std if std > 0 else 0
                    })
        
        return pd.DataFrame(zone_anomalies) if zone_anomalies else pd.DataFrame()
    
    def combine_anomaly_scores(self):
        """Combine multiple anomaly detection methods."""
        iqr = self.detect_iqr_anomalies()
        zscore = self.detect_zscore_anomalies()
        iso_forest = self.detect_isolation_forest_anomalies()
        statistical = self.detect_statistical_anomalies()
        
        # Combine all methods
        combined = pd.concat([iqr, zscore, iso_forest, statistical], axis=1)
        combined['anomaly_score'] = combined.sum(axis=1)
        combined['is_anomaly'] = (combined['anomaly_score'] > 0).astype(int)
        combined['anomaly_severity'] = combined['anomaly_score'].apply(
            lambda x: 'LOW' if x == 1 else 'MEDIUM' if x == 2 else 'HIGH' if x >= 3 else 'NORMAL'
        )
        
        return combined
    
    def get_anomaly_details(self):
        """Get detailed information about anomalies."""
        combined = self.combine_anomaly_scores()
        anomalies = combined[combined['is_anomaly'] == 1]
        
        details = pd.DataFrame({
            'timestamp': self.df.loc[anomalies.index, 'timestamp'],
            'zone': self.df.loc[anomalies.index, 'mine_zone'],
            'gas_level': self.df.loc[anomalies.index, 'gas_level'],
            'temperature': self.df.loc[anomalies.index, 'temperature'],
            'vibration': self.df.loc[anomalies.index, 'vibration'],
            'anomaly_score': anomalies['anomaly_score'],
            'severity': anomalies['anomaly_severity']
        })
        
        return details.sort_values('anomaly_score', ascending=False)
    
    def generate_anomaly_report(self):
        """Generate comprehensive anomaly detection report."""
        combined = self.combine_anomaly_scores()
        anomaly_details = self.get_anomaly_details()
        zone_anomalies = self.detect_zone_anomalies()
        
        report = {
            'total_anomalies': combined['is_anomaly'].sum(),
            'anomaly_percentage': (combined['is_anomaly'].sum() / len(self.df) * 100),
            'anomaly_by_severity': combined['anomaly_severity'].value_counts().to_dict(),
            'anomalies_by_zone': combined['is_anomaly'].groupby(self.df['mine_zone']).sum().to_dict(),
            'anomaly_methods_agreement': combined[[c for c in combined.columns if c not in ['anomaly_score', 'is_anomaly', 'anomaly_severity']]].sum().to_dict(),
            'anomaly_details': anomaly_details.to_dict(),
            'zone_specific_anomalies': zone_anomalies.to_dict() if len(zone_anomalies) > 0 else {},
        }
        
        return report


if __name__ == "__main__":
    df = pd.read_csv('data/processed/mine_safety_features.csv')
    detector = AnomalyDetector(df)
    report = detector.generate_anomaly_report()
    print("Anomaly detection report generated successfully!")
