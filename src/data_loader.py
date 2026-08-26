"""Load sensor data from CSV or database."""

import pandas as pd
import sqlite3
from pathlib import Path
import os

class DataLoader:
    """Load and manage data from various sources."""
    
    def __init__(self, db_path='database/mine_safety.db'):
        self.db_path = db_path
        self.ensure_db_exists()
    
    def ensure_db_exists(self):
        """Ensure database and tables exist."""
        os.makedirs(os.path.dirname(self.db_path), exist_ok=True)
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Create tables if they don't exist
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS sensor_readings (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp TEXT NOT NULL,
                mine_zone TEXT NOT NULL,
                gas_level REAL,
                temperature REAL,
                humidity REAL,
                vibration REAL,
                pressure REAL,
                smoke_level REAL,
                worker_count INTEGER,
                equipment_status TEXT,
                incident_flag INTEGER,
                risk_level TEXT
            )
        ''')
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS processed_data (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp TEXT NOT NULL,
                mine_zone TEXT NOT NULL,
                gas_level REAL,
                temperature REAL,
                humidity REAL,
                vibration REAL,
                pressure REAL,
                smoke_level REAL,
                worker_count INTEGER,
                equipment_status TEXT,
                incident_flag INTEGER,
                risk_level TEXT,
                hour INTEGER,
                day INTEGER,
                month INTEGER,
                weekday INTEGER,
                gas_risk_score REAL,
                temperature_risk_score REAL,
                vibration_risk_score REAL,
                combined_risk_score REAL,
                anomaly_flag INTEGER,
                anomaly_type TEXT
            )
        ''')
        
        conn.commit()
        conn.close()
    
    def load_csv(self, filepath):
        """Load data from CSV file."""
        df = pd.read_csv(filepath)
        df['timestamp'] = pd.to_datetime(df['timestamp'])
        return df
    
    def save_to_db(self, df, table_name='sensor_readings'):
        """Save dataframe to SQLite database."""
        conn = sqlite3.connect(self.db_path)
        df.to_sql(table_name, conn, if_exists='append', index=False)
        conn.close()
    
    def load_from_db(self, table_name='processed_data', limit=None):
        """Load data from SQLite database."""
        conn = sqlite3.connect(self.db_path)
        query = f"SELECT * FROM {table_name}"
        if limit:
            query += f" LIMIT {limit}"
        df = pd.read_sql_query(query, conn)
        conn.close()
        if 'timestamp' in df.columns:
            df['timestamp'] = pd.to_datetime(df['timestamp'])
        return df
    
    def execute_query(self, query):
        """Execute custom SQL query."""
        conn = sqlite3.connect(self.db_path)
        result = pd.read_sql_query(query, conn)
        conn.close()
        return result


if __name__ == "__main__":
    loader = DataLoader()
    print("Database initialized successfully!")
