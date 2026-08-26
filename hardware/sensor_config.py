"""Configuration for Raspberry Pi sensors."""

# GPIO Pins Configuration
GPIO_CONFIG = {
    'DHT22_PIN': 17,  # Temperature/Humidity sensor
    'GAS_SENSOR_ADC': 0x48,  # I2C address for ADS1115 (Gas sensor)
    'PRESSURE_SENSOR_ADC': 0x76,  # I2C address for BMP280
    'VIBRATION_SENSOR_CHANNEL': 1,  # Analog channel for vibration
}

# Sensor Calibration
SENSOR_CALIBRATION = {
    'gas_sensor': {
        'offset': 0,
        'scale': 1.0,
        'unit': 'ppm',
        'model': 'MQ-2'
    },
    'temperature_sensor': {
        'offset': 0,
        'scale': 1.0,
        'unit': 'Celsius',
        'model': 'DHT22'
    },
    'humidity_sensor': {
        'offset': 0,
        'scale': 1.0,
        'unit': 'Percent',
        'model': 'DHT22'
    },
    'vibration_sensor': {
        'offset': 0,
        'scale': 1.0,
        'unit': 'mm/s',
        'model': 'ADXL345'
    },
    'pressure_sensor': {
        'offset': 0,
        'scale': 1.0,
        'unit': 'hPa',
        'model': 'BMP280'
    }
}

# Safe Operating Ranges
SAFE_RANGES = {
    'gas_level': {'min': 0, 'max': 1000, 'critical': 2500},
    'temperature': {'min': 15, 'max': 32, 'critical': 40},
    'humidity': {'min': 30, 'max': 80, 'critical': 90},
    'vibration': {'min': 0, 'max': 2.0, 'critical': 5.0},
    'pressure': {'min': 98, 'max': 105, 'critical': 110},
}

# Zone Configuration
ZONE_CONFIG = {
    'ZONE A': {'node_id': 1, 'description': 'Mining Area 1'},
    'ZONE B': {'node_id': 2, 'description': 'Mining Area 2'},
    'ZONE C': {'node_id': 3, 'description': 'Mining Area 3'},
    'ZONE D': {'node_id': 4, 'description': 'Mining Area 4'},
    'ZONE E': {'node_id': 5, 'description': 'Mining Area 5'},
}

# Data Collection Settings
DATA_COLLECTION = {
    'read_interval_seconds': 5,
    'batch_size': 100,
    'upload_interval_minutes': 30,
    'local_storage_path': 'data/raw/sensor_data.csv'
}

# Alert Thresholds
ALERT_THRESHOLDS = {
    'warning': {
        'gas_level': 1000,
        'temperature': 28,
        'vibration': 2.5,
    },
    'critical': {
        'gas_level': 2000,
        'temperature': 35,
        'vibration': 4.0,
    }
}
