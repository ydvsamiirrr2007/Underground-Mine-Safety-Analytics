"""Risk analysis and classification for mine safety."""

import pandas as pd
import numpy as np

class RiskAnalyzer:
    """Analyze and classify safety risks."""
    
    def __init__(self, df):
        self.df = df.copy()
        self.df['timestamp'] = pd.to_datetime(self.df['timestamp'])
    
    def classify_risk_level(self):
        """Classify risk levels based on sensor readings and scores."""
        self.df['risk_classification'] = 'LOW'
        
        # Critical conditions
        critical_mask = (
            (self.df['gas_level'] > 2500) |
            (self.df['temperature'] > 35) |
            (self.df['vibration'] > 5.0) |
            (self.df['combined_risk_score'] > 80) |
            (self.df['equipment_status'] == 'CRITICAL')
        )
        self.df.loc[critical_mask, 'risk_classification'] = 'CRITICAL'
        
        # High risk conditions
        high_mask = (
            ~critical_mask &
            (
                (self.df['gas_level'] > 1500) |
                (self.df['temperature'] > 30) |
                (self.df['vibration'] > 3.5) |
                (self.df['combined_risk_score'] > 50) |
                (self.df['equipment_status'] == 'WARNING')
            )
        )
        self.df.loc[high_mask, 'risk_classification'] = 'HIGH'
        
        # Medium risk conditions
        medium_mask = (
            ~critical_mask &
            ~high_mask &
            (
                (self.df['gas_level'] > 1000) |
                (self.df['temperature'] > 27) |
                (self.df['vibration'] > 2.5) |
                (self.df['combined_risk_score'] > 25) |
                (self.df['total_anomalies'] >= 2)
            )
        )
        self.df.loc[medium_mask, 'risk_classification'] = 'MEDIUM'
        
        return self.df
    
    def identify_critical_zones(self, threshold=70):
        """Identify zones with high average risk."""
        zone_risk = self.df.groupby('mine_zone').agg({
            'combined_risk_score': 'mean',
            'incident_flag': 'sum',
            'gas_level': 'mean',
            'temperature': 'mean',
            'vibration': 'mean'
        }).round(2)
        
        critical_zones = zone_risk[zone_risk['combined_risk_score'] > threshold]
        return critical_zones.sort_values('combined_risk_score', ascending=False)
    
    def identify_high_risk_periods(self):
        """Identify time periods with elevated risk."""
        high_risk = self.df[self.df['combined_risk_score'] > 60]
        
        if len(high_risk) == 0:
            return pd.DataFrame()
        
        high_risk_periods = high_risk.groupby('hour').agg({
            'combined_risk_score': 'mean',
            'incident_flag': 'sum'
        }).round(2).sort_values('combined_risk_score', ascending=False)
        
        return high_risk_periods
    
    def identify_threshold_violations(self):
        """Identify sensor threshold violations."""
        violations = {
            'gas_violations': len(self.df[self.df['gas_level'] > 1000]),
            'temperature_violations': len(self.df[self.df['temperature'] > 32]),
            'vibration_violations': len(self.df[self.df['vibration'] > 3.0]),
            'smoke_violations': len(self.df[self.df['smoke_level'] > 0.2]),
        }
        
        # By zone
        gas_violations_by_zone = self.df[self.df['gas_level'] > 1000].groupby('mine_zone').size().to_dict()
        temp_violations_by_zone = self.df[self.df['temperature'] > 32].groupby('mine_zone').size().to_dict()
        
        violations['gas_violations_by_zone'] = gas_violations_by_zone
        violations['temperature_violations_by_zone'] = temp_violations_by_zone
        
        return violations
    
    def risk_trend_analysis(self):
        """Analyze risk trends over time."""
        self.df['date'] = self.df['timestamp'].dt.date
        
        daily_risk = self.df.groupby('date').agg({
            'combined_risk_score': ['mean', 'max', 'min'],
            'incident_flag': 'sum',
            'anomaly_flag': 'sum'
        }).round(2)
        
        daily_risk.columns = ['avg_risk', 'max_risk', 'min_risk', 'incidents', 'anomalies']
        
        return daily_risk
    
    def worker_safety_assessment(self):
        """Assess safety conditions for workers in each zone."""
        worker_safety = self.df.groupby('mine_zone').agg({
            'worker_count': 'mean',
            'combined_risk_score': 'mean',
            'incident_flag': 'sum',
            'equipment_status': lambda x: (x == 'CRITICAL').sum()
        }).round(2)
        
        worker_safety.columns = ['avg_workers', 'avg_risk', 'total_incidents', 'critical_equipment']
        worker_safety['safety_score'] = 100 - worker_safety['avg_risk']
        
        return worker_safety
    
    def generate_risk_report(self):
        """Generate comprehensive risk analysis report."""
        # Classify risks
        self.classify_risk_level()
        
        report = {
            'risk_distribution': self.df['risk_classification'].value_counts().to_dict(),
            'critical_zones': self.identify_critical_zones().to_dict(),
            'high_risk_periods': self.identify_high_risk_periods().to_dict(),
            'threshold_violations': self.identify_threshold_violations(),
            'risk_trends': self.risk_trend_analysis().to_dict(),
            'worker_safety': self.worker_safety_assessment().to_dict(),
        }
        
        return report


if __name__ == "__main__":
    df = pd.read_csv('data/processed/mine_safety_features.csv')
    risk_analyzer = RiskAnalyzer(df)
    report = risk_analyzer.generate_risk_report()
    print("Risk analysis report generated successfully!")
