"""Analytics and statistical analysis of mine safety data."""

import pandas as pd
import numpy as np
from scipy import stats
import warnings
warnings.filterwarnings('ignore')

class MineAnalytics:
    """Perform comprehensive analytics on mine safety data."""
    
    def __init__(self, df):
        self.df = df.copy()
        self.df['timestamp'] = pd.to_datetime(self.df['timestamp'])
        self.analytics_results = {}
    
    # ============ GAS ANALYTICS ============
    def analyze_gas(self):
        """Analyze gas levels and trends."""
        gas_analysis = {
            'avg_gas_level': self.df['gas_level'].mean(),
            'max_gas_level': self.df['gas_level'].max(),
            'min_gas_level': self.df['gas_level'].min(),
            'std_gas_level': self.df['gas_level'].std(),
            'median_gas_level': self.df['gas_level'].median(),
            'dangerous_readings': len(self.df[self.df['gas_level'] > 2000]),
            'warning_readings': len(self.df[(self.df['gas_level'] > 1000) & (self.df['gas_level'] <= 2000)]),
            'safe_readings': len(self.df[self.df['gas_level'] <= 1000]),
        }
        
        # Gas by zone
        gas_by_zone = self.df.groupby('mine_zone')['gas_level'].agg([
            ('avg', 'mean'),
            ('max', 'max'),
            ('min', 'min'),
            ('std', 'std')
        ]).round(2)
        gas_analysis['by_zone'] = gas_by_zone.to_dict()
        
        return gas_analysis
    
    # ============ TEMPERATURE ANALYTICS ============
    def analyze_temperature(self):
        """Analyze temperature patterns."""
        temp_analysis = {
            'avg_temperature': self.df['temperature'].mean(),
            'max_temperature': self.df['temperature'].max(),
            'min_temperature': self.df['temperature'].min(),
            'std_temperature': self.df['temperature'].std(),
            'median_temperature': self.df['temperature'].median(),
            'extreme_high': len(self.df[self.df['temperature'] > 32]),
            'high': len(self.df[(self.df['temperature'] > 27) & (self.df['temperature'] <= 32)]),
            'normal': len(self.df[(self.df['temperature'] > 20) & (self.df['temperature'] <= 27)]),
            'low': len(self.df[self.df['temperature'] <= 20]),
        }
        
        # Temperature by zone
        temp_by_zone = self.df.groupby('mine_zone')['temperature'].agg([
            ('avg', 'mean'),
            ('max', 'max'),
            ('min', 'min')
        ]).round(2)
        temp_analysis['by_zone'] = temp_by_zone.to_dict()
        
        return temp_analysis
    
    # ============ VIBRATION ANALYTICS ============
    def analyze_vibration(self):
        """Analyze vibration patterns and equipment status."""
        vib_analysis = {
            'avg_vibration': self.df['vibration'].mean(),
            'max_vibration': self.df['vibration'].max(),
            'min_vibration': self.df['vibration'].min(),
            'std_vibration': self.df['vibration'].std(),
            'critical_vibration': len(self.df[self.df['vibration'] > 5.0]),
            'high_vibration': len(self.df[(self.df['vibration'] > 3.0) & (self.df['vibration'] <= 5.0)]),
            'normal_vibration': len(self.df[self.df['vibration'] <= 3.0]),
        }
        
        # Vibration by zone
        vib_by_zone = self.df.groupby('mine_zone')['vibration'].agg([
            ('avg', 'mean'),
            ('max', 'max'),
            ('std', 'std')
        ]).round(2)
        vib_analysis['by_zone'] = vib_by_zone.to_dict()
        
        # Equipment status
        equipment_status = self.df['equipment_status'].value_counts().to_dict()
        vib_analysis['equipment_status'] = equipment_status
        
        return vib_analysis
    
    # ============ HUMIDITY ANALYTICS ============
    def analyze_humidity(self):
        """Analyze humidity patterns."""
        humidity_analysis = {
            'avg_humidity': self.df['humidity'].mean(),
            'max_humidity': self.df['humidity'].max(),
            'min_humidity': self.df['humidity'].min(),
            'optimal_range': len(self.df[(self.df['humidity'] >= 40) & (self.df['humidity'] <= 70)]),
            'too_low': len(self.df[self.df['humidity'] < 40]),
            'too_high': len(self.df[self.df['humidity'] > 70]),
        }
        return humidity_analysis
    
    # ============ INCIDENT ANALYTICS ============
    def analyze_incidents(self):
        """Analyze safety incidents."""
        incident_analysis = {
            'total_incidents': self.df['incident_flag'].sum(),
            'incident_percentage': (self.df['incident_flag'].sum() / len(self.df) * 100),
            'critical_risk_readings': len(self.df[self.df['combined_risk_score'] > 80]),
            'high_risk_readings': len(self.df[(self.df['combined_risk_score'] > 50) & (self.df['combined_risk_score'] <= 80)]),
            'medium_risk_readings': len(self.df[(self.df['combined_risk_score'] > 25) & (self.df['combined_risk_score'] <= 50)]),
            'low_risk_readings': len(self.df[self.df['combined_risk_score'] <= 25]),
        }
        
        # Incidents by zone
        incidents_by_zone = self.df.groupby('mine_zone').agg({
            'incident_flag': 'sum',
            'combined_risk_score': 'mean'
        }).round(2)
        incident_analysis['by_zone'] = incidents_by_zone.to_dict()
        
        # Incidents by hour
        incidents_by_hour = self.df.groupby('hour')['incident_flag'].sum().to_dict()
        incident_analysis['by_hour'] = incidents_by_hour
        
        return incident_analysis
    
    # ============ CORRELATION ANALYSIS ============
    def analyze_correlations(self):
        """Calculate correlation between sensor variables."""
        sensor_cols = ['gas_level', 'temperature', 'humidity', 'vibration', 'pressure', 'combined_risk_score']
        correlation_matrix = self.df[sensor_cols].corr().round(3)
        
        # Key correlations
        key_correlations = {
            'gas_temperature': correlation_matrix.loc['gas_level', 'temperature'],
            'gas_risk': correlation_matrix.loc['gas_level', 'combined_risk_score'],
            'temperature_risk': correlation_matrix.loc['temperature', 'combined_risk_score'],
            'vibration_risk': correlation_matrix.loc['vibration', 'combined_risk_score'],
            'humidity_temperature': correlation_matrix.loc['humidity', 'temperature'],
        }
        
        return {
            'correlation_matrix': correlation_matrix,
            'key_correlations': key_correlations
        }
    
    # ============ ZONE RISK RANKING ============
    def rank_zones_by_risk(self):
        """Rank mine zones by risk level."""
        zone_risk = self.df.groupby('mine_zone').agg({
            'combined_risk_score': ['mean', 'max'],
            'incident_flag': 'sum',
            'gas_level': 'mean',
            'temperature': 'mean',
            'vibration': 'mean'
        }).round(2)
        
        zone_risk.columns = ['avg_risk', 'max_risk', 'incident_count', 'avg_gas', 'avg_temp', 'avg_vibration']
        zone_risk = zone_risk.sort_values('avg_risk', ascending=False)
        
        return zone_risk
    
    # ============ ANOMALY STATISTICS ============
    def analyze_anomalies(self):
        """Analyze anomalous readings."""
        anomaly_analysis = {
            'total_anomalies': self.df['anomaly_flag'].sum(),
            'anomaly_percentage': (self.df['anomaly_flag'].sum() / len(self.df) * 100),
            'abnormal_gas': self.df['abnormal_gas_flag'].sum(),
            'abnormal_temperature': self.df['abnormal_temperature_flag'].sum(),
            'abnormal_vibration': self.df['abnormal_vibration_flag'].sum(),
            'abnormal_smoke': self.df['abnormal_smoke_flag'].sum(),
        }
        
        # Anomalies by zone
        anomalies_by_zone = self.df.groupby('mine_zone')['anomaly_flag'].sum().to_dict()
        anomaly_analysis['by_zone'] = anomalies_by_zone
        
        return anomaly_analysis
    
    # ============ STATISTICAL SUMMARY ============
    def statistical_summary(self):
        """Generate comprehensive statistical summary."""
        summary = {
            'total_readings': len(self.df),
            'date_range': f"{self.df['timestamp'].min().date()} to {self.df['timestamp'].max().date()}",
            'zones_monitored': self.df['mine_zone'].nunique(),
            'unique_zones': sorted(self.df['mine_zone'].unique().tolist()),
        }
        
        # Percentiles
        summary['gas_level_percentiles'] = {
            'p25': self.df['gas_level'].quantile(0.25),
            'p50': self.df['gas_level'].quantile(0.50),
            'p75': self.df['gas_level'].quantile(0.75),
            'p95': self.df['gas_level'].quantile(0.95),
            'p99': self.df['gas_level'].quantile(0.99),
        }
        
        return summary
    
    # ============ COMPLETE ANALYSIS REPORT ============
    def generate_complete_report(self):
        """Generate complete analytics report."""
        report = {
            'summary': self.statistical_summary(),
            'gas_analysis': self.analyze_gas(),
            'temperature_analysis': self.analyze_temperature(),
            'vibration_analysis': self.analyze_vibration(),
            'humidity_analysis': self.analyze_humidity(),
            'incident_analysis': self.analyze_incidents(),
            'anomaly_analysis': self.analyze_anomalies(),
            'correlation_analysis': self.analyze_correlations(),
            'zone_risk_ranking': self.rank_zones_by_risk().to_dict(),
        }
        return report


if __name__ == "__main__":
    df = pd.read_csv('data/processed/mine_safety_features.csv')
    analytics = MineAnalytics(df)
    report = analytics.generate_complete_report()
    print("Analytics report generated successfully!")
