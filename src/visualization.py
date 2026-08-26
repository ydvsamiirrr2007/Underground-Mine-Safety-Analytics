"""Visualization functions for mine safety analytics."""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots

class MineVisualization:
    """Create visualizations for mine safety data."""
    
    def __init__(self, df):
        self.df = df.copy()
        self.df['timestamp'] = pd.to_datetime(self.df['timestamp'])
        sns.set_style("whitegrid")
        plt.rcParams['figure.figsize'] = (14, 6)
    
    def plot_sensor_trends(self, figsize=(16, 10)):
        """Plot trends for all key sensors."""
        fig, axes = plt.subplots(2, 2, figsize=figsize)
        
        # Gas level trend
        self.df.groupby(self.df['timestamp'].dt.date)['gas_level'].mean().plot(ax=axes[0, 0], color='red', linewidth=2)
        axes[0, 0].set_title('Average Gas Level Over Time', fontsize=12, fontweight='bold')
        axes[0, 0].set_ylabel('Gas Level (ppm)')
        axes[0, 0].axhline(y=1000, color='orange', linestyle='--', label='Safe Threshold')
        axes[0, 0].legend()
        
        # Temperature trend
        self.df.groupby(self.df['timestamp'].dt.date)['temperature'].mean().plot(ax=axes[0, 1], color='blue', linewidth=2)
        axes[0, 1].set_title('Average Temperature Over Time', fontsize=12, fontweight='bold')
        axes[0, 1].set_ylabel('Temperature (°C)')
        axes[0, 1].axhline(y=25, color='orange', linestyle='--', label='Safe Threshold')
        axes[0, 1].legend()
        
        # Vibration trend
        self.df.groupby(self.df['timestamp'].dt.date)['vibration'].mean().plot(ax=axes[1, 0], color='green', linewidth=2)
        axes[1, 0].set_title('Average Vibration Over Time', fontsize=12, fontweight='bold')
        axes[1, 0].set_ylabel('Vibration (mm/s)')
        axes[1, 0].axhline(y=2.0, color='orange', linestyle='--', label='Safe Threshold')
        axes[1, 0].legend()
        
        # Humidity trend
        self.df.groupby(self.df['timestamp'].dt.date)['humidity'].mean().plot(ax=axes[1, 1], color='purple', linewidth=2)
        axes[1, 1].set_title('Average Humidity Over Time', fontsize=12, fontweight='bold')
        axes[1, 1].set_ylabel('Humidity (%)')
        axes[1, 1].axhline(y=50, color='orange', linestyle='--', label='Optimal')
        axes[1, 1].legend()
        
        plt.tight_layout()
        return fig
    
    def plot_zone_comparison(self):
        """Compare sensors across zones."""
        fig, axes = plt.subplots(2, 2, figsize=(14, 10))
        
        # Gas by zone
        zone_gas = self.df.groupby('mine_zone')['gas_level'].mean().sort_values(ascending=False)
        zone_gas.plot(kind='bar', ax=axes[0, 0], color='red', alpha=0.7)
        axes[0, 0].set_title('Average Gas Level by Zone', fontsize=12, fontweight='bold')
        axes[0, 0].set_ylabel('Gas Level (ppm)')
        axes[0, 0].axhline(y=1000, color='orange', linestyle='--', linewidth=2)
        
        # Temperature by zone
        zone_temp = self.df.groupby('mine_zone')['temperature'].mean().sort_values(ascending=False)
        zone_temp.plot(kind='bar', ax=axes[0, 1], color='blue', alpha=0.7)
        axes[0, 1].set_title('Average Temperature by Zone', fontsize=12, fontweight='bold')
        axes[0, 1].set_ylabel('Temperature (°C)')
        axes[0, 1].axhline(y=25, color='orange', linestyle='--', linewidth=2)
        
        # Vibration by zone
        zone_vib = self.df.groupby('mine_zone')['vibration'].mean().sort_values(ascending=False)
        zone_vib.plot(kind='bar', ax=axes[1, 0], color='green', alpha=0.7)
        axes[1, 0].set_title('Average Vibration by Zone', fontsize=12, fontweight='bold')
        axes[1, 0].set_ylabel('Vibration (mm/s)')
        axes[1, 0].axhline(y=2.0, color='orange', linestyle='--', linewidth=2)
        
        # Incident count by zone
        zone_incidents = self.df.groupby('mine_zone')['incident_flag'].sum().sort_values(ascending=False)
        zone_incidents.plot(kind='bar', ax=axes[1, 1], color='red', alpha=0.7)
        axes[1, 1].set_title('Total Incidents by Zone', fontsize=12, fontweight='bold')
        axes[1, 1].set_ylabel('Incident Count')
        
        plt.tight_layout()
        return fig
    
    def plot_correlation_heatmap(self):
        """Plot correlation heatmap of sensors."""
        sensor_cols = ['gas_level', 'temperature', 'humidity', 'vibration', 'pressure', 'combined_risk_score']
        corr_matrix = self.df[sensor_cols].corr()
        
        plt.figure(figsize=(10, 8))
        sns.heatmap(corr_matrix, annot=True, cmap='coolwarm', center=0, 
                    square=True, linewidths=1, cbar_kws={"shrink": 0.8})
        plt.title('Sensor Correlation Heatmap', fontsize=14, fontweight='bold')
        plt.tight_layout()
        return plt.gcf()
    
    def plot_risk_distribution(self):
        """Plot risk level distribution."""
        fig, axes = plt.subplots(1, 2, figsize=(14, 5))
        
        # Risk level counts
        risk_counts = self.df['risk_level'].value_counts()
        colors = {'LOW': 'green', 'MEDIUM': 'yellow', 'HIGH': 'orange', 'CRITICAL': 'red'}
        risk_colors = [colors.get(level, 'gray') for level in risk_counts.index]
        risk_counts.plot(kind='bar', ax=axes[0], color=risk_colors, alpha=0.7)
        axes[0].set_title('Risk Level Distribution', fontsize=12, fontweight='bold')
        axes[0].set_ylabel('Count')
        axes[0].set_xlabel('Risk Level')
        
        # Risk score distribution
        axes[1].hist(self.df['combined_risk_score'], bins=30, color='purple', alpha=0.7, edgecolor='black')
        axes[1].set_title('Combined Risk Score Distribution', fontsize=12, fontweight='bold')
        axes[1].set_xlabel('Risk Score')
        axes[1].set_ylabel('Frequency')
        axes[1].axvline(x=50, color='red', linestyle='--', linewidth=2, label='High Risk Threshold')
        axes[1].legend()
        
        plt.tight_layout()
        return fig
    
    def plot_anomalies_by_hour(self):
        """Plot anomalies distribution by hour."""
        anomalies_by_hour = self.df.groupby('hour')['anomaly_flag'].sum()
        
        fig = go.Figure()
        fig.add_trace(go.Bar(x=anomalies_by_hour.index, y=anomalies_by_hour.values,
                            marker=dict(color='red', opacity=0.7)))
        fig.update_layout(title='Anomalies Detected by Hour',
                         xaxis_title='Hour of Day',
                         yaxis_title='Anomaly Count',
                         hovermode='x unified')
        return fig
    
    def plot_interactive_sensor_timeseries(self, sensor='gas_level'):
        """Create interactive sensor time series plot."""
        fig = go.Figure()
        
        for zone in self.df['mine_zone'].unique():
            zone_data = self.df[self.df['mine_zone'] == zone].sort_values('timestamp')
            fig.add_trace(go.Scatter(
                x=zone_data['timestamp'],
                y=zone_data[sensor],
                mode='lines',
                name=zone
            ))
        
        fig.update_layout(title=f'{sensor.replace("_", " ").title()} Over Time',
                         xaxis_title='Timestamp',
                         yaxis_title=sensor,
                         hovermode='x unified',
                         height=500)
        return fig
    
    def plot_incident_timeline(self):
        """Plot incident timeline."""
        incidents = self.df[self.df['incident_flag'] == 1].copy()
        incidents['date'] = incidents['timestamp'].dt.date
        
        daily_incidents = incidents.groupby('date').size()
        
        fig = go.Figure()
        fig.add_trace(go.Bar(x=daily_incidents.index, y=daily_incidents.values,
                            marker=dict(color='red', opacity=0.7)))
        fig.update_layout(title='Daily Incident Count',
                         xaxis_title='Date',
                         yaxis_title='Incident Count',
                         hovermode='x unified')
        return fig


if __name__ == "__main__":
    df = pd.read_csv('data/processed/mine_safety_features.csv')
    viz = MineVisualization(df)
    print("Visualization module loaded successfully!")
