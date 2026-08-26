"""Professional Streamlit Dashboard for Mine Safety Analytics."""

import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots
import sys
from pathlib import Path

# Add src to path
sys.path.append(str(Path(__file__).parent / 'src'))

from data_generator import MineDataGenerator
from data_loader import DataLoader
from preprocessing import DataPreprocessor
from feature_engineering import FeatureEngineer
from analytics import MineAnalytics
from risk_analysis import RiskAnalyzer
from anomaly_detection import AnomalyDetector
from prediction import RiskPredictor
from visualization import MineVisualization

# ============ PAGE CONFIG ============
st.set_page_config(
    page_title="Mine Safety Monitoring System",
    page_icon="⛏️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ============ CUSTOM STYLING ============
st.markdown("""
    <style>
    [data-testid="stMetricValue"] {
        font-size: 32px !important;
        font-weight: bold;
    }
    .metric-card {
        background-color: #1e1e1e;
        border-radius: 10px;
        padding: 20px;
        color: #ffffff;
    }
    .safe-status { color: #00ff00; }
    .warning-status { color: #ffaa00; }
    .critical-status { color: #ff0000; }
    </style>
""", unsafe_allow_html=True)

# ============ CACHE DATA LOADING ============
@st.cache_resource
def load_data():
    """Load and process data."""
    try:
        # Try loading from CSV
        if Path('data/processed/mine_safety_features.csv').exists():
            df = pd.read_csv('data/processed/mine_safety_features.csv')
        else:
            # Generate fresh data
            st.info("Generating fresh data...")
            generator = MineDataGenerator(mode='simulation')
            df_raw = generator.generate_sensor_readings(num_records=5000, days=30)
            
            preprocessor = DataPreprocessor()
            df_clean = preprocessor.clean_data(df_raw)
            
            engineer = FeatureEngineer()
            df = engineer.create_features(df_clean)
            
            # Save
            df.to_csv('data/processed/mine_safety_features.csv', index=False)
        
        df['timestamp'] = pd.to_datetime(df['timestamp'])
        return df
    except Exception as e:
        st.error(f"Error loading data: {e}")
        return None

@st.cache_resource
def get_analytics(df):
    """Get analytics results."""
    return MineAnalytics(df)

@st.cache_resource
def get_risk_analyzer(df):
    """Get risk analyzer."""
    return RiskAnalyzer(df)

@st.cache_resource
def get_anomaly_detector(df):
    """Get anomaly detector."""
    return AnomalyDetector(df)

# ============ SIDEBAR NAVIGATION ============
st.sidebar.title("⛏️ Mine Safety System")
st.sidebar.markdown("---")

page = st.sidebar.radio(
    "Select Page:",
    ["🏢 Overview", "📊 Zone Analytics", "📈 Sensor Analytics", 
     "🚨 Incidents & Risk", "⚠️ Anomaly Detection", "🤖 ML Prediction", "📡 Live Monitoring"]
)

st.sidebar.markdown("---")
st.sidebar.markdown("**System Status:**")
st.sidebar.markdown("🟢 **SIMULATION MODE** - Running on synthetic data")

# ============ LOAD DATA ============
df = load_data()

if df is None:
    st.error("Failed to load data. Please check your data files.")
    st.stop()

analytics = get_analytics(df)
risk_analyzer = get_risk_analyzer(df)
anomaly_detector = get_anomaly_detector(df)

# ============ PAGE 1: OVERVIEW ============
if page == "🏢 Overview":
    st.title("⛏️ Underground Mine Safety Monitoring - Overview")
    st.markdown("Real-time safety status and key performance indicators")
    st.markdown("---")
    
    # Current Status Indicator
    col1, col2, col3, col4 = st.columns(4)
    
    avg_risk = df['combined_risk_score'].mean()
    critical_count = len(df[df['risk_level'] == 'CRITICAL'])
    high_count = len(df[df['risk_level'] == 'HIGH'])
    avg_gas = df['gas_level'].mean()
    
    if avg_risk > 60:
        status_color = "🔴"
        status_text = "CRITICAL"
    elif avg_risk > 40:
        status_color = "🟠"
        status_text = "HIGH RISK"
    elif avg_risk > 25:
        status_color = "🟡"
        status_text = "MEDIUM"
    else:
        status_color = "🟢"
        status_text = "SAFE"
    
    with col1:
        st.metric("Safety Status", status_text, status_color, delta=f"{avg_risk:.1f}%")
    with col2:
        st.metric("Avg Gas Level", f"{avg_gas:.0f} ppm", "-50" if avg_gas < 1000 else "+50")
    with col3:
        st.metric("Critical Events", critical_count, high_count)
    with col4:
        st.metric("Total Readings", len(df), "+142")
    
    st.markdown("---")
    
    # KPI Cards
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("🌡️ Avg Temperature", f"{df['temperature'].mean():.1f}°C")
    with col2:
        st.metric("📊 Avg Humidity", f"{df['humidity'].mean():.1f}%")
    with col3:
        st.metric("📈 Avg Vibration", f"{df['vibration'].mean():.2f} mm/s")
    with col4:
        st.metric("👥 Avg Workers", f"{df['worker_count'].mean():.0f}")
    
    st.markdown("---")
    
    # Charts
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Risk Distribution")
        risk_dist = df['risk_level'].value_counts()
        fig = px.pie(values=risk_dist.values, names=risk_dist.index,
                     color_discrete_map={'LOW': '#00ff00', 'MEDIUM': '#ffaa00', 
                                        'HIGH': '#ff6600', 'CRITICAL': '#ff0000'})
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        st.subheader("Risk Trend")
        daily_risk = df.groupby(df['timestamp'].dt.date)['combined_risk_score'].mean()
        fig = go.Figure()
        fig.add_trace(go.Scatter(x=daily_risk.index, y=daily_risk.values, mode='lines+markers'))
        fig.update_layout(title="Average Daily Risk Score", xaxis_title="Date", yaxis_title="Risk Score")
        st.plotly_chart(fig, use_container_width=True)
    
    # Incidents timeline
    st.subheader("Incidents Over Time")
    daily_incidents = df[df['incident_flag'] == 1].groupby(df['timestamp'].dt.date).size()
    fig = px.bar(x=daily_incidents.index, y=daily_incidents.values, labels={'x': 'Date', 'y': 'Incident Count'})
    st.plotly_chart(fig, use_container_width=True)
    
    # Alerts
    st.markdown("---")
    st.subheader("⚠️ Active Alerts")
    
    if critical_count > 0:
        st.error(f"🚨 {critical_count} CRITICAL readings detected")
    if high_count > 0:
        st.warning(f"⚠️ {high_count} HIGH-RISK readings detected")
    if avg_gas > 1500:
        st.warning(f"🔥 Elevated gas levels: {avg_gas:.0f} ppm")
    if df['temperature'].max() > 32:
        st.warning(f"🌡️ High temperature detected: {df['temperature'].max():.1f}°C")

# ============ PAGE 2: ZONE ANALYTICS ============
elif page == "📊 Zone Analytics":
    st.title("📊 Zone-wise Safety Analytics")
    st.markdown("Comparative analysis across all mine zones")
    st.markdown("---")
    
    zones = sorted(df['mine_zone'].unique())
    
    # Zone comparison metrics
    st.subheader("Zone Comparison Dashboard")
    
    zone_stats = df.groupby('mine_zone').agg({
        'gas_level': 'mean',
        'temperature': 'mean',
        'vibration': 'mean',
        'combined_risk_score': 'mean',
        'incident_flag': 'sum'
    }).round(2)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Average Gas Level by Zone")
        fig = px.bar(x=zone_stats.index, y=zone_stats['gas_level'],
                     color=zone_stats['gas_level'],
                     color_continuous_scale='Reds')
        fig.add_hline(y=1000, line_dash="dash", line_color="orange", annotation_text="Safe Limit")
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        st.subheader("Average Temperature by Zone")
        fig = px.bar(x=zone_stats.index, y=zone_stats['temperature'],
                     color=zone_stats['temperature'],
                     color_continuous_scale='RdYlBu_r')
        fig.add_hline(y=25, line_dash="dash", line_color="orange", annotation_text="Safe Limit")
        st.plotly_chart(fig, use_container_width=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Average Vibration by Zone")
        fig = px.bar(x=zone_stats.index, y=zone_stats['vibration'],
                     color=zone_stats['vibration'],
                     color_continuous_scale='Oranges')
        fig.add_hline(y=2.0, line_dash="dash", line_color="orange", annotation_text="Safe Limit")
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        st.subheader("Total Incidents by Zone")
        fig = px.bar(x=zone_stats.index, y=zone_stats['incident_flag'],
                     color=zone_stats['incident_flag'],
                     color_continuous_scale='Reds')
        st.plotly_chart(fig, use_container_width=True)
    
    # Zone ranking
    st.subheader("🚨 Most Dangerous Zones Ranking")
    zone_ranking = df.groupby('mine_zone').agg({
        'combined_risk_score': 'mean',
        'incident_flag': 'sum',
        'gas_level': 'mean',
        'temperature': 'mean',
        'vibration': 'mean'
    }).round(2).sort_values('combined_risk_score', ascending=False)
    
    zone_ranking.columns = ['Avg Risk Score', 'Total Incidents', 'Avg Gas', 'Avg Temp', 'Avg Vibration']
    
    # Add ranking number
    zone_ranking.insert(0, 'Rank', range(1, len(zone_ranking) + 1))
    st.dataframe(zone_ranking, use_container_width=True)

# ============ PAGE 3: SENSOR ANALYTICS ============
elif page == "📈 Sensor Analytics":
    st.title("📈 Detailed Sensor Analysis")
    st.markdown("Time-series analysis and trends for individual sensors")
    st.markdown("---")
    
    # Sensor selector
    col1, col2, col3 = st.columns(3)
    with col1:
        selected_sensor = st.selectbox("Select Sensor:", 
                                      ['gas_level', 'temperature', 'humidity', 'vibration', 'pressure'])
    with col2:
        selected_zone = st.selectbox("Select Zone:", ['All'] + sorted(df['mine_zone'].unique()))
    with col3:
        date_range = st.date_input("Date Range:", value=(df['timestamp'].min().date(), df['timestamp'].max().date()))
    
    # Filter data
    plot_df = df.copy()
    if selected_zone != 'All':
        plot_df = plot_df[plot_df['mine_zone'] == selected_zone]
    
    plot_df = plot_df[(plot_df['timestamp'].dt.date >= date_range[0]) & 
                      (plot_df['timestamp'].dt.date <= date_range[1])]
    
    # Time series plot
    st.subheader(f"{selected_sensor.replace('_', ' ').title()} Trend")
    fig = go.Figure()
    
    for zone in plot_df['mine_zone'].unique():
        zone_data = plot_df[plot_df['mine_zone'] == zone].sort_values('timestamp')
        fig.add_trace(go.Scatter(x=zone_data['timestamp'], y=zone_data[selected_sensor], 
                                mode='lines', name=zone, hovertemplate='%{y:.2f}<extra></extra>'))
    
    fig.update_layout(title=f"{selected_sensor.replace('_', ' ').title()} Over Time",
                     xaxis_title="Timestamp", yaxis_title=selected_sensor)
    st.plotly_chart(fig, use_container_width=True)
    
    # Statistics
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Average", f"{plot_df[selected_sensor].mean():.2f}")
    with col2:
        st.metric("Maximum", f"{plot_df[selected_sensor].max():.2f}")
    with col3:
        st.metric("Minimum", f"{plot_df[selected_sensor].min():.2f}")
    with col4:
        st.metric("Std Dev", f"{plot_df[selected_sensor].std():.2f}")
    
    # Distribution histogram
    st.subheader("Distribution")
    fig = px.histogram(plot_df, x=selected_sensor, nbins=30, title=f"{selected_sensor.replace('_', ' ').title()} Distribution")
    st.plotly_chart(fig, use_container_width=True)

# ============ PAGE 4: INCIDENTS & RISK ============
elif page == "🚨 Incidents & Risk":
    st.title("🚨 Incidents & Risk Analysis")
    st.markdown("Safety incident tracking and risk assessment")
    st.markdown("---")
    
    # Incident statistics
    total_incidents = df['incident_flag'].sum()
    incident_pct = (total_incidents / len(df)) * 100
    
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Total Incidents", int(total_incidents))
    with col2:
        st.metric("Incident Rate", f"{incident_pct:.2f}%")
    with col3:
        st.metric("Critical Events", len(df[df['combined_risk_score'] > 80]))
    with col4:
        st.metric("High Risk Events", len(df[(df['combined_risk_score'] > 50) & (df['combined_risk_score'] <= 80)]))
    
    st.markdown("---")
    
    # Risk by hour
    st.subheader("Risk Levels by Hour of Day")
    hourly_risk = df.groupby('hour').agg({
        'combined_risk_score': 'mean',
        'incident_flag': 'sum'
    })
    
    fig = make_subplots(specs=[[{"secondary_y": True}]])
    fig.add_trace(go.Bar(x=hourly_risk.index, y=hourly_risk['combined_risk_score'],
                         name='Avg Risk Score'), secondary_y=False)
    fig.add_trace(go.Scatter(x=hourly_risk.index, y=hourly_risk['incident_flag'],
                            name='Incident Count', mode='lines+markers'), secondary_y=True)
    fig.update_layout(title="Risk Metrics by Hour", xaxis_title="Hour of Day")
    st.plotly_chart(fig, use_container_width=True)
    
    # Incidents by zone
    st.subheader("Incidents by Zone")
    incidents_by_zone = df[df['incident_flag'] == 1].groupby('mine_zone').size()
    fig = px.bar(x=incidents_by_zone.index, y=incidents_by_zone.values,
                 color=incidents_by_zone.values, color_continuous_scale='Reds')
    st.plotly_chart(fig, use_container_width=True)
    
    # Risk threshold violations
    st.subheader("Threshold Violations")
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        gas_violations = len(df[df['gas_level'] > 1000])
        st.metric("Gas Violations", gas_violations, delta=f"{(gas_violations/len(df)*100):.1f}%")
    with col2:
        temp_violations = len(df[df['temperature'] > 32])
        st.metric("Temperature Violations", temp_violations, delta=f"{(temp_violations/len(df)*100):.1f}%")
    with col3:
        vib_violations = len(df[df['vibration'] > 3.0])
        st.metric("Vibration Violations", vib_violations, delta=f"{(vib_violations/len(df)*100):.1f}%")
    with col4:
        smoke_violations = len(df[df['smoke_level'] > 0.2])
        st.metric("Smoke Violations", smoke_violations, delta=f"{(smoke_violations/len(df)*100):.1f}%")

# ============ PAGE 5: ANOMALY DETECTION ============
elif page == "⚠️ Anomaly Detection":
    st.title("⚠️ Anomaly Detection Results")
    st.markdown("Abnormal readings and unusual patterns detected")
    st.markdown("---")
    
    # Generate anomaly report
    anomaly_combined = anomaly_detector.combine_anomaly_scores()
    anomaly_details = anomaly_detector.get_anomaly_details()
    
    # Metrics
    total_anomalies = anomaly_combined['is_anomaly'].sum()
    anomaly_pct = (total_anomalies / len(df)) * 100
    
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Total Anomalies", int(total_anomalies))
    with col2:
        st.metric("Anomaly Rate", f"{anomaly_pct:.2f}%")
    with col3:
        st.metric("High Severity", len(anomaly_combined[anomaly_combined['anomaly_severity'] == 'HIGH']))
    with col4:
        st.metric("Medium Severity", len(anomaly_combined[anomaly_combined['anomaly_severity'] == 'MEDIUM']))
    
    st.markdown("---")
    
    # Anomaly severity distribution
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Anomalies by Severity")
        severity_dist = anomaly_combined['anomaly_severity'].value_counts()
        fig = px.pie(values=severity_dist.values, names=severity_dist.index,
                     color_discrete_map={'HIGH': '#ff0000', 'MEDIUM': '#ffaa00', 'LOW': '#ffff00', 'NORMAL': '#00ff00'})
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        st.subheader("Anomalies by Zone")
        anomalies_by_zone = anomaly_combined[anomaly_combined['is_anomaly'] == 1].groupby(df['mine_zone']).size()
        fig = px.bar(x=anomalies_by_zone.index, y=anomalies_by_zone.values,
                     color=anomalies_by_zone.values, color_continuous_scale='Reds')
        st.plotly_chart(fig, use_container_width=True)
    
    # Anomaly details table
    st.subheader("Recent Anomalies")
    if len(anomaly_details) > 0:
        st.dataframe(anomaly_details.head(20), use_container_width=True)
    else:
        st.info("No anomalies detected.")
    
    # Anomaly timeline
    st.subheader("Anomaly Timeline")
    if len(anomaly_details) > 0:
        daily_anomalies = anomaly_details.groupby(anomaly_details['timestamp'].dt.date).size()
        fig = px.bar(x=daily_anomalies.index, y=daily_anomalies.values,
                     labels={'x': 'Date', 'y': 'Anomaly Count'})
        st.plotly_chart(fig, use_container_width=True)

# ============ PAGE 6: ML PREDICTION ============
elif page == "🤖 ML Prediction":
    st.title("🤖 Machine Learning Risk Prediction")
    st.markdown("AI-powered risk assessment and prediction")
    st.markdown("---")
    
    # Train model
    st.info("Training ML model...")
    predictor = RiskPredictor(df)
    predictor.train_model(model_type='random_forest')
    summary = predictor.get_model_summary()
    
    # Model performance metrics
    st.subheader("Model Performance")
    metrics = summary['performance_metrics']
    
    col1, col2, col3, col4, col5 = st.columns(5)
    with col1:
        st.metric("Accuracy", f"{metrics['test_accuracy']:.4f}")
    with col2:
        st.metric("Precision", f"{metrics['precision']:.4f}")
    with col3:
        st.metric("Recall", f"{metrics['recall']:.4f}")
    with col4:
        st.metric("F1-Score", f"{metrics['f1_score']:.4f}")
    with col5:
        st.metric("ROC-AUC", f"{metrics['roc_auc']:.4f}")
    
    st.markdown("---")
    
    # Confusion matrix
    st.subheader("Confusion Matrix")
    cm = metrics['confusion_matrix']
    fig = go.Figure(data=go.Heatmap(
        z=cm,
        x=['Predicted Safe', 'Predicted High-Risk'],
        y=['Actual Safe', 'Actual High-Risk'],
        text=cm,
        texttemplate='%{text}',
        colorscale='Blues'
    ))
    st.plotly_chart(fig, use_container_width=True)
    
    # Feature importance
    if summary['feature_importance'] is not None:
        st.subheader("Top Features Contributing to Risk Prediction")
        feature_df = summary['feature_importance'].head(10)
        fig = px.bar(feature_df, x='importance', y='feature', orientation='h')
        st.plotly_chart(fig, use_container_width=True)
    
    # Recent predictions
    st.subheader("Latest Risk Predictions")
    recent_predictions = predictor.predict_for_latest(n_records=10)
    st.dataframe(recent_predictions, use_container_width=True)

# ============ PAGE 7: LIVE MONITORING ============
elif page == "📡 Live Monitoring":
    st.title("📡 Real-Time Live Monitoring")
    st.markdown("Simulated real-time sensor data streaming")
    st.markdown("---")
    
    st.info("🔴 SIMULATION MODE - Displaying real-time simulated sensor data")
    
    # Live sensor values
    st.subheader("Current Sensor Readings")
    
    # Get latest reading from each zone
    latest_readings = df.loc[df.groupby('mine_zone')['timestamp'].idxmax()]
    
    cols = st.columns(5)
    zones = sorted(df['mine_zone'].unique())
    
    for idx, zone in enumerate(zones):
        with cols[idx % 5]:
            zone_data = latest_readings[latest_readings['mine_zone'] == zone].iloc[0]
            
            # Color based on risk
            if zone_data['risk_level'] == 'CRITICAL':
                st.error(f"### {zone}\n🔴 CRITICAL")
            elif zone_data['risk_level'] == 'HIGH':
                st.warning(f"### {zone}\n🟠 HIGH")
            elif zone_data['risk_level'] == 'MEDIUM':
                st.warning(f"### {zone}\n🟡 MEDIUM")
            else:
                st.success(f"### {zone}\n🟢 SAFE")
            
            st.metric("Gas", f"{zone_data['gas_level']:.0f} ppm")
            st.metric("Temp", f"{zone_data['temperature']:.1f}°C")
            st.metric("Vibration", f"{zone_data['vibration']:.2f} mm/s")
    
    st.markdown("---")
    
    # Auto-refresh controls
    col1, col2 = st.columns([3, 1])
    with col1:
        st.info("💡 In a real deployment, this would refresh every 5 seconds with live Raspberry Pi data.")
    with col2:
        if st.button("🔄 Refresh Now"):
            st.rerun()
    
    # Live gauge charts
    st.subheader("Live Sensor Gauges")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        avg_gas = df['gas_level'].tail(100).mean()
        fig = go.Figure(go.Indicator(
            mode="gauge+number",
            value=avg_gas,
            title={'text': "Gas Level (ppm)"},
            domain={'x': [0, 1], 'y': [0, 1]},
            gauge={
                'axis': {'range': [0, 3000]},
                'bar': {'color': "darkblue"},
                'steps': [
                    {'range': [0, 1000], 'color': "lightgreen"},
                    {'range': [1000, 2000], 'color': "lightyellow"},
                    {'range': [2000, 3000], 'color': "lightcoral"}
                ]
            }
        ))
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        avg_temp = df['temperature'].tail(100).mean()
        fig = go.Figure(go.Indicator(
            mode="gauge+number",
            value=avg_temp,
            title={'text': "Temperature (°C)"},
            domain={'x': [0, 1], 'y': [0, 1]},
            gauge={
                'axis': {'range': [10, 40]},
                'bar': {'color': "red"},
                'steps': [
                    {'range': [10, 25], 'color': "lightblue"},
                    {'range': [25, 30], 'color': "lightyellow"},
                    {'range': [30, 40], 'color': "lightcoral"}
                ]
            }
        ))
        st.plotly_chart(fig, use_container_width=True)
    
    with col3:
        avg_humidity = df['humidity'].tail(100).mean()
        fig = go.Figure(go.Indicator(
            mode="gauge+number",
            value=avg_humidity,
            title={'text': "Humidity (%)"},
            domain={'x': [0, 1], 'y': [0, 1]},
            gauge={
                'axis': {'range': [0, 100]},
                'bar': {'color': "blue"},
                'steps': [
                    {'range': [0, 40], 'color': "lightcoral"},
                    {'range': [40, 70], 'color': "lightgreen"},
                    {'range': [70, 100], 'color': "lightcoral"}
                ]
            }
        ))
        st.plotly_chart(fig, use_container_width=True)
    
    with col4:
        avg_vibration = df['vibration'].tail(100).mean()
        fig = go.Figure(go.Indicator(
            mode="gauge+number",
            value=avg_vibration,
            title={'text': "Vibration (mm/s)"},
            domain={'x': [0, 1], 'y': [0, 1]},
            gauge={
                'axis': {'range': [0, 8]},
                'bar': {'color': "orange"},
                'steps': [
                    {'range': [0, 2], 'color': "lightgreen"},
                    {'range': [2, 4], 'color': "lightyellow"},
                    {'range': [4, 8], 'color': "lightcoral"}
                ]
            }
        ))
        st.plotly_chart(fig, use_container_width=True)

st.markdown("---")
st.markdown("<p style='text-align: center; color: gray;'>Underground Mine Safety Monitoring & Analytics System | Data Period: {} to {}</p>".format(
    df['timestamp'].min().strftime('%Y-%m-%d'), df['timestamp'].max().strftime('%Y-%m-%d')
), unsafe_allow_html=True)
