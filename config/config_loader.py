"""Configuration loader for mine safety monitoring system.

Supports loading configuration from:
1. config.json (base configuration)
2. Environment variables (.env file or system env)
3. Runtime overrides

Environment variables override config.json values.
"""

import json
import os
import logging
from typing import Any, Dict, Optional
from pathlib import Path

try:
    from dotenv import load_dotenv
except ImportError:
    def load_dotenv(path):
        pass

logger = logging.getLogger(__name__)


class ConfigLoader:
    """Load and manage configuration from multiple sources."""
    
    def __init__(self, config_path: str = "config.json", env_path: str = ".env"):
        """
        Initialize configuration loader.
        
        Args:
            config_path: Path to config.json file
            env_path: Path to .env file
        """
        self.config_path = Path(config_path)
        self.env_path = Path(env_path)
        self.config: Dict[str, Any] = {}
        
        # Load environment variables first
        if self.env_path.exists():
            load_dotenv(str(self.env_path))
            logger.info(f"Loaded environment from {self.env_path}")
        else:
            logger.debug(f"Environment file not found: {self.env_path}")
        
        # Load configuration
        self._load_config()
        
        # Apply environment variable overrides
        self._apply_env_overrides()
    
    def _load_config(self) -> None:
        """Load configuration from JSON file."""
        if not self.config_path.exists():
            logger.warning(f"Config file not found: {self.config_path}")
            self.config = self._get_default_config()
            return
        
        try:
            with open(self.config_path, 'r') as f:
                self.config = json.load(f)
            logger.info(f"Loaded configuration from {self.config_path}")
        except json.JSONDecodeError as e:
            logger.error(f"Failed to parse config.json: {e}")
            self.config = self._get_default_config()
        except Exception as e:
            logger.error(f"Error loading config: {e}")
            self.config = self._get_default_config()
    
    def _apply_env_overrides(self) -> None:
        """Apply environment variable overrides to configuration."""
        # System settings
        if os.getenv("SYSTEM_MODE"):
            self.config["system"]["mode"] = os.getenv("SYSTEM_MODE")
        if os.getenv("LOG_LEVEL"):
            self.config["system"]["log_level"] = os.getenv("LOG_LEVEL")
        
        # Database settings
        if os.getenv("DB_TYPE"):
            self.config["database"]["type"] = os.getenv("DB_TYPE")
        if os.getenv("DB_SQLITE_PATH"):
            self.config["database"]["sqlite"]["path"] = os.getenv("DB_SQLITE_PATH")
        if os.getenv("DB_POSTGRESQL_HOST"):
            self.config["database"]["postgresql"]["host"] = os.getenv("DB_POSTGRESQL_HOST")
        if os.getenv("DB_POSTGRESQL_PORT"):
            self.config["database"]["postgresql"]["port"] = int(os.getenv("DB_POSTGRESQL_PORT"))
        if os.getenv("DB_POSTGRESQL_DATABASE"):
            self.config["database"]["postgresql"]["database"] = os.getenv("DB_POSTGRESQL_DATABASE")
        if os.getenv("DB_POSTGRESQL_USER"):
            self.config["database"]["postgresql"]["user"] = os.getenv("DB_POSTGRESQL_USER")
        if os.getenv("DB_POSTGRESQL_PASSWORD"):
            self.config["database"]["postgresql"]["password"] = os.getenv("DB_POSTGRESQL_PASSWORD")
        
        # API settings
        if os.getenv("API_HOST"):
            self.config["api"]["host"] = os.getenv("API_HOST")
        if os.getenv("API_PORT"):
            self.config["api"]["port"] = int(os.getenv("API_PORT"))
        if os.getenv("API_DEBUG"):
            self.config["api"]["debug"] = os.getenv("API_DEBUG").lower() == "true"
        
        # Hardware settings
        if os.getenv("HARDWARE_MODE"):
            self.config["hardware"]["simulation"]["enabled"] = os.getenv("HARDWARE_MODE") == "simulation"
        if os.getenv("RASPBERRY_PI_ENABLED"):
            self.config["hardware"]["raspberry_pi"]["enabled"] = os.getenv("RASPBERRY_PI_ENABLED").lower() == "true"
        
        # Sensor enable/disable
        if os.getenv("SENSOR_GAS_ENABLED"):
            self.config["sensors"]["enabled_sensors"]["gas"] = os.getenv("SENSOR_GAS_ENABLED").lower() == "true"
        if os.getenv("SENSOR_TEMPERATURE_ENABLED"):
            self.config["sensors"]["enabled_sensors"]["temperature"] = os.getenv("SENSOR_TEMPERATURE_ENABLED").lower() == "true"
        if os.getenv("SENSOR_HUMIDITY_ENABLED"):
            self.config["sensors"]["enabled_sensors"]["humidity"] = os.getenv("SENSOR_HUMIDITY_ENABLED").lower() == "true"
        
        # Monitoring intervals
        if os.getenv("SENSOR_READ_INTERVAL"):
            self.config["monitoring"]["sensor_read_interval"] = int(os.getenv("SENSOR_READ_INTERVAL"))
        
        # Risk thresholds
        if os.getenv("RISK_THRESHOLD_LOW"):
            self.config["risk_engine"]["risk_thresholds"]["low"] = float(os.getenv("RISK_THRESHOLD_LOW"))
        if os.getenv("RISK_THRESHOLD_MEDIUM"):
            self.config["risk_engine"]["risk_thresholds"]["medium"] = float(os.getenv("RISK_THRESHOLD_MEDIUM"))
        if os.getenv("RISK_THRESHOLD_HIGH"):
            self.config["risk_engine"]["risk_thresholds"]["high"] = float(os.getenv("RISK_THRESHOLD_HIGH"))
    
    @staticmethod
    def _get_default_config() -> Dict[str, Any]:
        """Return default configuration if file not found."""
        return {
            "system": {
                "mode": "simulation",
                "log_level": "INFO",
                "timezone": "UTC"
            },
            "database": {
                "type": "sqlite",
                "sqlite": {"path": "data/mine_safety.db"},
                "postgresql": {
                    "host": "localhost",
                    "port": 5432,
                    "database": "mine_safety",
                    "user": "mine_user",
                    "password": "PLACEHOLDER"
                }
            },
            "sensors": {
                "enabled_sensors": {
                    "gas": True,
                    "temperature": True,
                    "humidity": True,
                    "vibration": True,
                    "pressure": True,
                    "smoke": True,
                    "motion": True
                }
            },
            "monitoring": {
                "sensor_read_interval": 5,
                "buffer_size": 100,
                "data_validation_enabled": True
            },
            "risk_engine": {
                "risk_thresholds": {
                    "low": 25,
                    "medium": 50,
                    "high": 75
                }
            },
            "api": {
                "host": "localhost",
                "port": 8000,
                "debug": False
            },
            "hardware": {
                "simulation": {"enabled": True},
                "raspberry_pi": {"enabled": False}
            },
            "features": {
                "enable_risk_explanation": True,
                "enable_what_if_simulation": True,
                "enable_forecasting": True
            }
        }
    
    def get(self, key: str, default: Any = None) -> Any:
        """
        Get configuration value by dot-notation key.
        
        Examples:
            get("system.mode")
            get("sensors.gas.safe_threshold")
            get("database.postgresql.host")
        
        Args:
            key: Configuration key in dot notation
            default: Default value if key not found
        
        Returns:
            Configuration value or default
        """
        keys = key.split(".")
        value = self.config
        
        for k in keys:
            if isinstance(value, dict):
                value = value.get(k)
                if value is None:
                    return default
            else:
                return default
        
        return value if value is not None else default
    
    def get_section(self, section: str) -> Dict[str, Any]:
        """
        Get entire configuration section.
        
        Args:
            section: Section name (e.g., "sensors", "database")
        
        Returns:
            Configuration section as dictionary
        """
        return self.config.get(section, {})
    
    def get_full_config(self) -> Dict[str, Any]:
        """Get the complete configuration dictionary."""
        return self.config.copy()
    
    def is_enabled(self, feature: str) -> bool:
        """
        Check if a feature is enabled.
        
        Args:
            feature: Feature key (e.g., "forecasting", "anomaly_detection")
        
        Returns:
            True if feature is enabled, False otherwise
        """
        # Check in features section
        if self.config.get("features", {}).get(f"enable_{feature}"):
            return True
        
        # Check in specific subsections
        if feature == "forecasting":
            return self.config.get("forecasting", {}).get("enabled", False)
        elif feature == "anomaly_detection":
            return self.config.get("risk_engine", {}).get("anomaly_detection", {}).get("enabled", False)
        elif feature == "alerts":
            return self.config.get("alerts", {}).get("enabled", False)
        
        return False
    
    def print_config(self) -> None:
        """Print configuration (for debugging, excludes passwords)."""
        config_copy = json.loads(json.dumps(self.config))
        
        # Mask sensitive values
        if "database" in config_copy and "postgresql" in config_copy["database"]:
            config_copy["database"]["postgresql"]["password"] = "***MASKED***"
        
        print("\n" + "="*60)
        print("CONFIGURATION")
        print("="*60)
        print(json.dumps(config_copy, indent=2))
        print("="*60 + "\n")


# Singleton instance
_config_instance: Optional[ConfigLoader] = None


def get_config() -> ConfigLoader:
    """
    Get singleton configuration instance.
    
    Returns:
        ConfigLoader instance
    """
    global _config_instance
    if _config_instance is None:
        _config_instance = ConfigLoader()
    return _config_instance


if __name__ == "__main__":
    # Test configuration loading
    config = ConfigLoader()
    config.print_config()
    
    # Test getting values
    print(f"System mode: {config.get('system.mode')}")
    print(f"Gas safe threshold: {config.get('sensors.gas.safe_threshold')}")
    print(f"Forecasting enabled: {config.is_enabled('forecasting')}")
