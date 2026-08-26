-- Mine Safety Monitoring Database Schema

-- Raw Sensor Readings Table
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
    risk_level TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Processed Data Table (with Features)
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
    is_night_shift INTEGER,
    gas_risk_score REAL,
    temperature_risk_score REAL,
    vibration_risk_score REAL,
    humidity_risk_score REAL,
    combined_risk_score REAL,
    abnormal_gas_flag INTEGER,
    abnormal_temperature_flag INTEGER,
    abnormal_vibration_flag INTEGER,
    total_anomalies INTEGER,
    anomaly_flag INTEGER,
    anomaly_type TEXT,
    equipment_risk REAL,
    zone_risk_baseline REAL,
    incident_risk REAL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Safety Incidents Table
CREATE TABLE IF NOT EXISTS safety_incidents (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    incident_timestamp TEXT NOT NULL,
    zone TEXT NOT NULL,
    incident_type TEXT,
    severity TEXT,
    description TEXT,
    affected_workers INTEGER,
    resolution_time INTEGER,
    status TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Anomalies Table
CREATE TABLE IF NOT EXISTS anomalies (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    timestamp TEXT NOT NULL,
    zone TEXT NOT NULL,
    anomaly_type TEXT,
    sensor_name TEXT,
    value REAL,
    expected_value REAL,
    severity_score REAL,
    detected_by TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- ML Predictions Table
CREATE TABLE IF NOT EXISTS predictions (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    timestamp TEXT NOT NULL,
    zone TEXT NOT NULL,
    predicted_risk INTEGER,
    risk_probability REAL,
    actual_risk INTEGER,
    model_version TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Create Indexes for Performance
CREATE INDEX IF NOT EXISTS idx_sensor_readings_timestamp ON sensor_readings(timestamp);
CREATE INDEX IF NOT EXISTS idx_sensor_readings_zone ON sensor_readings(mine_zone);
CREATE INDEX IF NOT EXISTS idx_processed_data_timestamp ON processed_data(timestamp);
CREATE INDEX IF NOT EXISTS idx_processed_data_zone ON processed_data(mine_zone);
CREATE INDEX IF NOT EXISTS idx_incidents_timestamp ON safety_incidents(incident_timestamp);
CREATE INDEX IF NOT EXISTS idx_incidents_zone ON safety_incidents(zone);
CREATE INDEX IF NOT EXISTS idx_anomalies_timestamp ON anomalies(timestamp);
CREATE INDEX IF NOT EXISTS idx_predictions_timestamp ON predictions(timestamp);
