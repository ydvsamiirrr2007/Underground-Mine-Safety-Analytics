# PHASE 3: SENSOR DATA MODEL STANDARDIZATION - PLANNING

## 🎯 Objective

Establish a **unified sensor data schema** that all system modules will use for consistency, validation, and integration.

---

## 📋 Sensor Data Standard

### Core Schema

```python
{
    # Identification
    "timestamp": "2026-08-29T04:14:09Z",      # ISO 8601 UTC
    "sensor_id": "MQ2_01",                     # From config.json
    "zone": "ZONE_A",                          # Mine zone identifier
    
    # Sensor Readings (from configuration)
    "readings": {
        "gas": 820,                            # ppm (0-4000 typical)
        "temperature": 28.4,                   # celsius (-10 to 50)
        "humidity": 62.0,                      # % (0-100)
        "vibration": 1.8,                      # mm/s (0-10)
        "pressure": 101.2,                     # kPa (95-105 normal)
        "smoke": 0.08,                         # normalized (0-1)
        "motion": true                         # boolean
    },
    
    # Data Quality & Health
    "metadata": {
        "sensor_health": 95,                   # % (0-100, from Phase 6)
        "validation_status": "VALID",          # VALID, WARNING, ERROR
        "data_quality": "GOOD",                # EXCELLENT, GOOD, FAIR, POOR
        "reading_interval": 5                  # seconds
    },
    
    # Processing Status
    "processing": {
        "is_anomaly": false,                   # From Phase 8
        "anomaly_score": 0.12,                 # 0-1 (from Phase 8)
        "risk_score": 35,                      # 0-100 (from Phase 6)
        "risk_level": "MEDIUM"                 # LOW, MEDIUM, HIGH, CRITICAL
    }
}
```

### Advantages

✅ **Consistent Structure** - All modules work with same format
✅ **Configuration-Aware** - Uses sensor IDs, units, thresholds from config
✅ **Quality Indicators** - Health and validation status included
✅ **Extensible** - Easy to add new fields
✅ **Validation-Ready** - Can use Pydantic schema validation
✅ **Type-Safe** - Clear data types for each field
✅ **Timestamps** - All data can be correlated temporally
✅ **Metadata-Rich** - Includes processing information

---

## 📁 Files to Create in Phase 3

### 1. `models/sensor_data.py`
- Pydantic models for validation
- Type definitions
- Field constraints
- Default values

### 2. `models/sensor_reading.py`
- Individual sensor reading model
- Units and ranges
- Validation rules

### 3. `models/__init__.py`
- Export models

### 4. `tests/test_sensor_data.py`
- Schema validation tests
- Type checking tests
- Range validation tests
- JSON serialization tests

### 5. `docs/PHASE_3_SENSOR_DATA.md`
- Complete specification
- Usage examples
- Integration guide

---

## 🔄 Data Flow with Standard Schema

```
Hardware/Simulation (Phase 4)
    ↓
Sensor Reading [Raw]
    ↓
Validation (Phase 3)
    ├─ Type checking
    ├─ Range validation
    └─ Completeness check
    ↓
Sensor Data [Standard Schema]
    ↓
Feature Engineering (Phase 3)
    ├─ Moving averages
    ├─ Derivatives
    └─ Cross-sensor ratios
    ↓
Anomaly Detection (Phase 8)
    ├─ Check against normal range
    └─ Isolation Forest scoring
    ↓
Risk Calculation (Phase 6)
    ├─ Apply weights
    └─ Generate risk score
    ↓
Forecasting (Phase 5)
    └─ Predict next values
    ↓
Database Storage (Phase 14)
    ├─ Insert standardized data
    └─ Maintain temporal index
    ↓
API Response (Phase 9)
    └─ Return standard schema
    ↓
Frontend Display (Phase 10)
    └─ Render dashboards
```

---

## ✅ Phase 3 Deliverables

1. **Sensor Data Schema**
   - Core model definition
   - Type definitions
   - Validation constraints

2. **Implementation**
   - Pydantic models
   - Validation logic
   - Serialization/deserialization

3. **Testing**
   - Schema validation tests
   - Type checking tests
   - Integration tests

4. **Documentation**
   - Complete schema specification
   - Usage examples
   - Validation rules

---

## 🚀 Phase 3 is Ready to Start

After Phase 2 (Configuration System), we can immediately start Phase 3 because:

✅ Configuration system provides sensor metadata
✅ All sensor types are defined in config.json
✅ Data quality standards are established
✅ Integration points are documented

**Estimated Duration:** 2-3 hours
**Complexity:** Medium
**Dependencies:** Phase 2 (Complete)
**Blocking:** Phases 4, 5, 6, 7, 8, 9, 10

---

## 📝 Next Steps

1. Create sensor data models with Pydantic
2. Implement validation logic
3. Add comprehensive tests
4. Document schema thoroughly
5. Ready for Phase 4 (Hardware Abstraction)

---

**Phase 2 Complete** ✅  
**Phase 3 Queued** 📋  
**Ready to Begin:** YES ✓
