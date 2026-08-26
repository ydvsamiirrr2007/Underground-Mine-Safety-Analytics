-- Mine Safety Analytics SQL Queries

-- ============ BASIC STATISTICS ============

-- Total sensor readings
SELECT COUNT(*) as total_readings FROM sensor_readings;

-- Date range of data
SELECT 
    MIN(timestamp) as earliest_reading,
    MAX(timestamp) as latest_reading,
    julianday(MAX(timestamp)) - julianday(MIN(timestamp)) as days_of_data
FROM sensor_readings;

-- ============ GAS LEVEL ANALYTICS ============

-- Average gas level by zone
SELECT 
    mine_zone,
    ROUND(AVG(gas_level), 2) as avg_gas,
    ROUND(MAX(gas_level), 2) as max_gas,
    ROUND(MIN(gas_level), 2) as min_gas,
    COUNT(*) as readings_count
FROM sensor_readings
GROUP BY mine_zone
ORDER BY avg_gas DESC;

-- Gas level threshold violations
SELECT 
    mine_zone,
    COUNT(*) as violation_count,
    ROUND(AVG(gas_level), 2) as avg_violation_level
FROM sensor_readings
WHERE gas_level > 1000
GROUP BY mine_zone
ORDER BY violation_count DESC;

-- ============ TEMPERATURE ANALYTICS ============

-- Average temperature by zone
SELECT 
    mine_zone,
    ROUND(AVG(temperature), 2) as avg_temp,
    ROUND(MAX(temperature), 2) as max_temp,
    ROUND(MIN(temperature), 2) as min_temp
FROM sensor_readings
GROUP BY mine_zone
ORDER BY avg_temp DESC;

-- Extreme temperature events
SELECT 
    timestamp,
    mine_zone,
    temperature,
    risk_level
FROM sensor_readings
WHERE temperature > 32
ORDER BY temperature DESC
LIMIT 20;

-- ============ HUMIDITY ANALYTICS ============

-- Average humidity
SELECT 
    ROUND(AVG(humidity), 2) as avg_humidity,
    ROUND(MAX(humidity), 2) as max_humidity,
    ROUND(MIN(humidity), 2) as min_humidity
FROM sensor_readings;

-- Humidity levels by zone
SELECT 
    mine_zone,
    ROUND(AVG(humidity), 2) as avg_humidity,
    COUNT(*) as readings
FROM sensor_readings
GROUP BY mine_zone;

-- ============ VIBRATION ANALYTICS ============

-- Average vibration by zone
SELECT 
    mine_zone,
    ROUND(AVG(vibration), 2) as avg_vibration,
    ROUND(MAX(vibration), 2) as max_vibration,
    COUNT(*) as readings
FROM sensor_readings
GROUP BY mine_zone
ORDER BY avg_vibration DESC;

-- Abnormal vibration events
SELECT 
    timestamp,
    mine_zone,
    vibration,
    equipment_status
FROM sensor_readings
WHERE vibration > 3.0
ORDER BY vibration DESC
LIMIT 20;

-- ============ INCIDENT ANALYTICS ============

-- Total incidents by zone
SELECT 
    mine_zone,
    SUM(incident_flag) as total_incidents,
    ROUND(100.0 * SUM(incident_flag) / COUNT(*), 2) as incident_percentage
FROM sensor_readings
GROUP BY mine_zone
ORDER BY total_incidents DESC;

-- Daily incident count
SELECT 
    DATE(timestamp) as incident_date,
    SUM(incident_flag) as incident_count,
    COUNT(*) as total_readings
FROM sensor_readings
GROUP BY DATE(timestamp)
ORDER BY incident_date DESC;

-- Incidents by hour of day
SELECT 
    CAST(strftime('%H', timestamp) AS INTEGER) as hour,
    SUM(incident_flag) as incident_count,
    COUNT(*) as total_readings
FROM sensor_readings
GROUP BY hour
ORDER BY incident_count DESC;

-- ============ RISK ANALYTICS ============

-- Risk level distribution
SELECT 
    risk_level,
    COUNT(*) as count,
    ROUND(100.0 * COUNT(*) / (SELECT COUNT(*) FROM sensor_readings), 2) as percentage
FROM sensor_readings
GROUP BY risk_level
ORDER BY count DESC;

-- Critical and high-risk readings
SELECT 
    COUNT(*) as critical_high_risk_count,
    ROUND(100.0 * COUNT(*) / (SELECT COUNT(*) FROM sensor_readings), 2) as percentage
FROM sensor_readings
WHERE risk_level IN ('CRITICAL', 'HIGH');

-- ============ MOST DANGEROUS ZONES ============

-- Zones ranked by risk
SELECT 
    mine_zone,
    ROUND(AVG(
        CASE 
            WHEN risk_level = 'CRITICAL' THEN 100
            WHEN risk_level = 'HIGH' THEN 75
            WHEN risk_level = 'MEDIUM' THEN 50
            ELSE 25
        END
    ), 2) as avg_risk_score,
    SUM(CASE WHEN risk_level IN ('CRITICAL', 'HIGH') THEN 1 ELSE 0 END) as high_risk_count,
    COUNT(*) as total_readings
FROM sensor_readings
GROUP BY mine_zone
ORDER BY avg_risk_score DESC;

-- ============ EQUIPMENT STATUS ============

-- Equipment status summary
SELECT 
    equipment_status,
    COUNT(*) as count,
    ROUND(100.0 * COUNT(*) / (SELECT COUNT(*) FROM sensor_readings), 2) as percentage
FROM sensor_readings
GROUP BY equipment_status;

-- Equipment status by zone
SELECT 
    mine_zone,
    equipment_status,
    COUNT(*) as count
FROM sensor_readings
GROUP BY mine_zone, equipment_status
ORDER BY mine_zone, count DESC;

-- ============ WORKER SAFETY ============

-- Average workers by zone
SELECT 
    mine_zone,
    ROUND(AVG(worker_count), 1) as avg_workers,
    MAX(worker_count) as max_workers,
    MIN(worker_count) as min_workers
FROM sensor_readings
GROUP BY mine_zone;

-- ============ PRESSURE ANALYTICS ============

-- Average pressure
SELECT 
    ROUND(AVG(pressure), 2) as avg_pressure,
    ROUND(MAX(pressure), 2) as max_pressure,
    ROUND(MIN(pressure), 2) as min_pressure
FROM sensor_readings;

-- ============ PROCESSED DATA QUERIES ============

-- Risk score distribution
SELECT 
    mine_zone,
    ROUND(AVG(combined_risk_score), 2) as avg_risk_score,
    ROUND(MAX(combined_risk_score), 2) as max_risk_score,
    ROUND(MIN(combined_risk_score), 2) as min_risk_score
FROM processed_data
GROUP BY mine_zone
ORDER BY avg_risk_score DESC;

-- Anomaly detection results
SELECT 
    anomaly_type,
    COUNT(*) as anomaly_count,
    ROUND(100.0 * COUNT(*) / (SELECT COUNT(*) FROM processed_data WHERE anomaly_flag = 1), 2) as percentage
FROM processed_data
WHERE anomaly_flag = 1
GROUP BY anomaly_type
ORDER BY anomaly_count DESC;

-- High-risk periods
SELECT 
    hour,
    COUNT(*) as high_risk_readings,
    ROUND(AVG(combined_risk_score), 2) as avg_risk
FROM processed_data
WHERE combined_risk_score > 50
GROUP BY hour
ORDER BY avg_risk DESC;

-- Night shift vs Day shift comparison
SELECT 
    CASE WHEN is_night_shift = 1 THEN 'Night Shift' ELSE 'Day Shift' END as shift,
    COUNT(*) as readings,
    ROUND(AVG(combined_risk_score), 2) as avg_risk,
    SUM(incident_flag) as incident_count
FROM processed_data
GROUP BY is_night_shift;
