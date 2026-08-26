#include <iostream>
#include <string>
#include <cmath>
#include <iomanip>

// Structure for sensor data
struct SensorReading {
    double gas_level;
    double temperature;
    double vibration;
    std::string equipment_status;
};

// Structure for risk output
struct RiskAssessment {
    std::string risk_level;  // NORMAL, WARNING, CRITICAL
    int risk_score;          // 0-100
    std::string reason;
};

// Function to assess risk based on sensor readings
RiskAssessment assessRisk(const SensorReading& reading) {
    RiskAssessment assessment;
    int risk_score = 0;
    std::string reason = "";
    
    // Gas level assessment (0-40 points)
    if (reading.gas_level > 2500) {
        risk_score += 40;
        reason += "Dangerous gas levels. ";
    } else if (reading.gas_level > 1500) {
        risk_score += 30;
        reason += "High gas levels. ";
    } else if (reading.gas_level > 1000) {
        risk_score += 15;
        reason += "Elevated gas levels. ";
    }
    
    // Temperature assessment (0-30 points)
    if (reading.temperature > 35) {
        risk_score += 30;
        reason += "Extreme temperature. ";
    } else if (reading.temperature > 30) {
        risk_score += 20;
        reason += "High temperature. ";
    } else if (reading.temperature > 27) {
        risk_score += 10;
        reason += "Elevated temperature. ";
    }
    
    // Vibration assessment (0-20 points)
    if (reading.vibration > 5.0) {
        risk_score += 20;
        reason += "Severe vibration. ";
    } else if (reading.vibration > 3.5) {
        risk_score += 15;
        reason += "High vibration. ";
    } else if (reading.vibration > 2.5) {
        risk_score += 8;
        reason += "Elevated vibration. ";
    }
    
    // Equipment status assessment (0-10 points)
    if (reading.equipment_status == "CRITICAL") {
        risk_score += 10;
        reason += "Critical equipment status. ";
    } else if (reading.equipment_status == "WARNING") {
        risk_score += 5;
        reason += "Equipment warning. ";
    }
    
    // Cap risk score at 100
    if (risk_score > 100) risk_score = 100;
    
    // Determine risk level
    if (risk_score >= 70) {
        assessment.risk_level = "CRITICAL";
    } else if (risk_score >= 50) {
        assessment.risk_level = "WARNING";
    } else {
        assessment.risk_level = "NORMAL";
    }
    
    assessment.risk_score = risk_score;
    assessment.reason = reason.empty() ? "All parameters within safe range." : reason;
    
    return assessment;
}

// Function to validate sensor readings
bool validateReading(const SensorReading& reading) {
    if (reading.gas_level < 0 || reading.gas_level > 5000) return false;
    if (reading.temperature < -10 || reading.temperature > 50) return false;
    if (reading.vibration < 0 || reading.vibration > 20) return false;
    return true;
}

// Main function - demonstrates usage
int main(int argc, char* argv[]) {
    // Example 1: Safe conditions
    SensorReading safe_reading = {800.0, 22.5, 1.2, "NORMAL"};
    RiskAssessment safe_result = assessRisk(safe_reading);
    
    std::cout << "\n=== MINE SAFETY SENSOR PROCESSOR ===";
    std::cout << "\n\nExample 1: Safe Conditions";
    std::cout << "\nGas Level: " << safe_reading.gas_level << " ppm";
    std::cout << "\nTemperature: " << safe_reading.temperature << "C";
    std::cout << "\nVibration: " << safe_reading.vibration << " mm/s";
    std::cout << "\nEquipment: " << safe_reading.equipment_status;
    std::cout << "\n\nRisk Assessment:";
    std::cout << "\n  Risk Level: " << safe_result.risk_level;
    std::cout << "\n  Risk Score: " << safe_result.risk_score << "/100";
    std::cout << "\n  Reason: " << safe_result.reason;
    
    // Example 2: Warning conditions
    SensorReading warning_reading = {1200.0, 28.0, 2.8, "WARNING"};
    RiskAssessment warning_result = assessRisk(warning_reading);
    
    std::cout << "\n\n\nExample 2: Warning Conditions";
    std::cout << "\nGas Level: " << warning_reading.gas_level << " ppm";
    std::cout << "\nTemperature: " << warning_reading.temperature << "C";
    std::cout << "\nVibration: " << warning_reading.vibration << " mm/s";
    std::cout << "\nEquipment: " << warning_reading.equipment_status;
    std::cout << "\n\nRisk Assessment:";
    std::cout << "\n  Risk Level: " << warning_result.risk_level;
    std::cout << "\n  Risk Score: " << warning_result.risk_score << "/100";
    std::cout << "\n  Reason: " << warning_result.reason;
    
    // Example 3: Critical conditions
    SensorReading critical_reading = {2800.0, 36.0, 5.5, "CRITICAL"};
    RiskAssessment critical_result = assessRisk(critical_reading);
    
    std::cout << "\n\n\nExample 3: Critical Conditions";
    std::cout << "\nGas Level: " << critical_reading.gas_level << " ppm";
    std::cout << "\nTemperature: " << critical_reading.temperature << "C";
    std::cout << "\nVibration: " << critical_reading.vibration << " mm/s";
    std::cout << "\nEquipment: " << critical_reading.equipment_status;
    std::cout << "\n\nRisk Assessment:";
    std::cout << "\n  Risk Level: " << critical_result.risk_level;
    std::cout << "\n  Risk Score: " << critical_result.risk_score << "/100";
    std::cout << "\n  Reason: " << critical_result.reason;
    
    std::cout << "\n\n===================================\n";
    
    return 0;
}

/*
COMPILATION INSTRUCTIONS:

On Linux/Mac:
  g++ -o sensor_processor sensor_processor.cpp
  ./sensor_processor

On Windows (MinGW):
  g++ -o sensor_processor.exe sensor_processor.cpp
  sensor_processor.exe

The C++ executable can be called from Python using subprocess module:
  import subprocess
  result = subprocess.run(['./sensor_processor'], capture_output=True, text=True)
  print(result.stdout)
*/
