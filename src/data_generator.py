"""Generate realistic mine safety sensor data in simulation mode."""

import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import random

class MineDataGenerator:
    """Generate realistic sensor data for underground mine safety monitoring."""
    
    def __init__(self, mode='simulation'):
        self.mode = mode
        self.zones = ['Zone A', 'Zone B', 'Zone C', 'Zone D', 'Zone E']
        self.equipment_status = ['NORMAL', 'WARNING', 'CRITICAL']
        
        # Safe thresholds
        self.safe_gas_level = 1000  # ppm
        self.safe_temperature = 25  # Celsius
        self.safe_vibration = 2.0  # mm/s
        
    def generate_sensor_readings(self, num_records=10000, days=30):
        """Generate realistic sensor readings with relationships between variables."""
        
        records = []
        start_date = datetime.now() - timedelta(days=days)
        
        for i in range(num_records):
            # Distribute timestamps across the period
            timestamp = start_date + timedelta(minutes=i * (days * 24 * 60 / num_records))
            zone = random.choice(self.zones)
            hour_of_day = timestamp.hour
            
            # Create realistic patterns
            # Peak activity hours: 6-14 and 14-22
            is_active_hour = 6 <= hour_of_day < 22
            activity_factor = 1.5 if is_active_hour else 0.5
            
            # Gas levels - correlate with activity
            base_gas = np.random.normal(800, 100)
            gas_level = base_gas * activity_factor + np.random.normal(0, 50)
            gas_level = np.clip(gas_level, 100, 3000)
            
            # Add occasional gas spikes (anomalies - 5% chance)
            if random.random() < 0.05:
                gas_level = np.random.uniform(2000, 3000)
            
            # Temperature - correlate with gas and activity
            base_temp = 22 + (gas_level - 800) * 0.005
            temperature = base_temp + np.random.normal(0, 2)
            temperature = np.clip(temperature, 15, 40)
            
            # Humidity - inverse relationship with temperature
            humidity = 70 - (temperature - 20) * 2 + np.random.normal(0, 5)
            humidity = np.clip(humidity, 30, 90)
            
            # Vibration - correlate with activity and gas
            base_vibration = 1.0 * activity_factor + (gas_level - 800) * 0.0005
            vibration = base_vibration + np.random.normal(0, 0.3)
            vibration = np.clip(vibration, 0.1, 8.0)
            
            # Pressure - relatively stable
            pressure = 101.3 + np.random.normal(0, 1)
            pressure = np.clip(pressure, 98, 105)
            
            # Smoke level
            smoke_level = 0.1 * activity_factor + np.random.normal(0, 0.05)
            smoke_level = np.clip(smoke_level, 0, 0.5)
            
            # Worker count - higher during active hours
            worker_count = random.randint(3, 15) if is_active_hour else random.randint(0, 5)
            
            # Equipment status
            equipment_status = random.choices(
                self.equipment_status,
                weights=[0.85, 0.10, 0.05],
                k=1
            )[0]
            
            # Incident flag - higher when multiple conditions are bad
            incident_risk = 0
            if gas_level > self.safe_gas_level:
                incident_risk += 0.3
            if temperature > 32:
                incident_risk += 0.2
            if vibration > 3.0:
                incident_risk += 0.3
            if equipment_status == 'CRITICAL':
                incident_risk += 0.2
            
            incident_flag = 1 if random.random() < incident_risk else 0
            
            # Risk level based on sensor values
            if gas_level > 2500 or temperature > 35 or vibration > 5.0:
                risk_level = 'CRITICAL'
            elif gas_level > 1500 or temperature > 30 or vibration > 3.5:
                risk_level = 'HIGH'
            elif gas_level > 1000 or temperature > 27 or vibration > 2.5:
                risk_level = 'MEDIUM'
            else:
                risk_level = 'LOW'
            
            record = {
                'timestamp': timestamp.isoformat(),
                'mine_zone': zone,
                'gas_level': round(gas_level, 2),
                'temperature': round(temperature, 2),
                'humidity': round(humidity, 2),
                'vibration': round(vibration, 2),
                'pressure': round(pressure, 2),
                'smoke_level': round(smoke_level, 4),
                'worker_count': worker_count,
                'equipment_status': equipment_status,
                'incident_flag': incident_flag,
                'risk_level': risk_level
            }
            records.append(record)
        
        return pd.DataFrame(records)
    
    def save_raw_data(self, df, filepath='data/raw/mine_safety_raw.csv'):
        """Save generated data to CSV."""
        df.to_csv(filepath, index=False)
        print(f"Raw data saved to {filepath}")
        print(f"Records generated: {len(df)}")
        print(f"Date range: {df['timestamp'].min()} to {df['timestamp'].max()}")
        return filepath


if __name__ == "__main__":
    # Generate sample data
    generator = MineDataGenerator(mode='simulation')
    df = generator.generate_sensor_readings(num_records=10000, days=30)
    generator.save_raw_data(df)
    print("\nData Summary:")
    print(df.describe())
    print("\nRisk Level Distribution:")
    print(df['risk_level'].value_counts())
