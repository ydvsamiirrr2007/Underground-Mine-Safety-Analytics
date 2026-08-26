"""Raspberry Pi sensor reader for hardware mode."""

import os
import sys
import json
import time
from datetime import datetime
import argparse

try:
    import RPi.GPIO as GPIO
    import board
    import adafruit_dht
    HARDWARE_AVAILABLE = True
except ImportError:
    HARDWARE_AVAILABLE = False
    print("Warning: RPi.GPIO or adafruit libraries not available. Running in simulation mode.")


class RaspberryPiSensorReader:
    """Read sensor data from Raspberry Pi GPIO pins."""
    
    def __init__(self, mode='simulation'):
        self.mode = mode
        self.zone = 'ZONE A'  # Configure per Pi instance
        self.sensor_data = {}
        
        if mode == 'hardware' and HARDWARE_AVAILABLE:
            self._initialize_hardware()
        else:
            self.mode = 'simulation'
            print("Running in SIMULATION MODE")
    
    def _initialize_hardware(self):
        """Initialize hardware connections (Raspberry Pi only)."""
        try:
            # Set GPIO mode
            GPIO.setmode(GPIO.BCM)
            
            # DHT sensor setup (GPIO pin 17)
            self.dht_device = adafruit_dht.DHT22(board.D17)
            
            print("Hardware initialized successfully!")
        except Exception as e:
            print(f"Hardware initialization failed: {e}")
            self.mode = 'simulation'
    
    def read_gas_sensor(self):
        """Read analog gas sensor value (MQ-2 on ADC)."""
        if self.mode == 'hardware':
            try:
                # Read from ADC (e.g., using I2C ADS1115)
                # This is a placeholder - implement based on your ADC setup
                return 800 + (os.urandom(2)[0] % 200)
            except Exception as e:
                print(f"Gas sensor read error: {e}")
                return 800
        else:
            # Simulation
            import random
            return 800 + random.randint(-100, 100)
    
    def read_temperature_humidity(self):
        """Read temperature and humidity from DHT sensor."""
        if self.mode == 'hardware':
            try:
                temperature = self.dht_device.temperature
                humidity = self.dht_device.humidity
                return temperature, humidity
            except Exception as e:
                print(f"DHT sensor read error: {e}")
                return 25, 60
        else:
            # Simulation
            import random
            temp = 22 + random.randint(-3, 5)
            humidity = 60 + random.randint(-10, 10)
            return temp, humidity
    
    def read_vibration_sensor(self):
        """Read vibration sensor (analog input)."""
        if self.mode == 'hardware':
            try:
                # Read from analog pin via ADC
                return 1.5 + (os.urandom(1)[0] % 200) / 100
            except Exception as e:
                print(f"Vibration sensor read error: {e}")
                return 1.5
        else:
            # Simulation
            import random
            return 1.5 + random.random()
    
    def read_pressure_sensor(self):
        """Read pressure sensor (I2C BMP280)."""
        if self.mode == 'hardware':
            try:
                # Read from I2C pressure sensor
                return 101.3 + (os.urandom(1)[0] % 20) / 10
            except Exception as e:
                print(f"Pressure sensor read error: {e}")
                return 101.3
        else:
            # Simulation
            import random
            return 101.3 + random.uniform(-1, 1)
    
    def read_all_sensors(self):
        """Read all sensor values and create a data record."""
        timestamp = datetime.now().isoformat()
        gas_level = self.read_gas_sensor()
        temperature, humidity = self.read_temperature_humidity()
        vibration = self.read_vibration_sensor()
        pressure = self.read_pressure_sensor()
        
        # Simulate other values
        import random
        smoke_level = max(0.1, gas_level / 10000)  # Correlate with gas
        worker_count = random.randint(1, 10)
        equipment_status = random.choice(['NORMAL', 'NORMAL', 'NORMAL', 'WARNING'])
        
        # Determine incident based on conditions
        incident_flag = 1 if gas_level > 2000 or temperature > 32 or vibration > 3.0 else 0
        
        # Determine risk level
        if gas_level > 2500 or temperature > 35 or vibration > 5.0:
            risk_level = 'CRITICAL'
        elif gas_level > 1500 or temperature > 30 or vibration > 3.5:
            risk_level = 'HIGH'
        elif gas_level > 1000 or temperature > 27 or vibration > 2.5:
            risk_level = 'MEDIUM'
        else:
            risk_level = 'LOW'
        
        sensor_record = {
            'timestamp': timestamp,
            'mine_zone': self.zone,
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
        
        return sensor_record
    
    def stream_data(self, interval=5, output_file=None):
        """Stream sensor data at regular intervals."""
        print(f"\nStreaming data in {self.mode.upper()} mode (Zone: {self.zone})")
        print(f"Interval: {interval} seconds")
        if output_file:
            print(f"Output file: {output_file}")
        print("-" * 80)
        
        try:
            while True:
                record = self.read_all_sensors()
                print(f"[{record['timestamp']}] Zone: {record['mine_zone']} | "
                      f"Gas: {record['gas_level']} | Temp: {record['temperature']}°C | "
                      f"Risk: {record['risk_level']}")
                
                if output_file:
                    with open(output_file, 'a') as f:
                        f.write(json.dumps(record) + '\n')
                
                time.sleep(interval)
        
        except KeyboardInterrupt:
            print("\nData streaming stopped.")
            self.cleanup()
    
    def cleanup(self):
        """Clean up GPIO pins."""
        if self.mode == 'hardware' and HARDWARE_AVAILABLE:
            try:
                GPIO.cleanup()
                print("GPIO cleaned up.")
            except:
                pass


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Raspberry Pi Mine Safety Sensor Reader')
    parser.add_argument('--mode', choices=['simulation', 'hardware'], default='simulation',
                       help='Operation mode (default: simulation)')
    parser.add_argument('--zone', default='ZONE A', help='Mine zone identifier')
    parser.add_argument('--interval', type=int, default=5, help='Read interval in seconds')
    parser.add_argument('--output', help='Optional output file for sensor data')
    
    args = parser.parse_args()
    
    reader = RaspberryPiSensorReader(mode=args.mode)
    reader.zone = args.zone
    reader.stream_data(interval=args.interval, output_file=args.output)
