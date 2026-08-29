# Underground Mine Safety Analytics & Decision Support System

A comprehensive **SIH 2026** prototype implementing an integrated approach to convert **reactive mine safety monitoring into predictive safety decision support**.

## 🎯 Project Innovation

### Traditional Approach (Reactive)
```
Sensor Reading → Threshold Check → Alarm
```

### Our Approach (Predictive Decision Support)
```
Sensor Reading
    ↓
Sensor Validation & Health Check
    ↓
Anomaly Detection (Isolation Forest)
    ↓
Risk Scoring (0-100 scale)
    ↓
Risk Forecasting (+5, +10, +15 minutes)
    ↓
Risk Explanation (Risk DNA - Feature Contribution)
    ↓
What-If Scenario Simulation (Counterfactual)
    ↓
Safety Recommendation
    ↓
Alert & Visualization
```

This system answers four critical questions:
1. **Is the mine currently at risk?** (Risk Score)
2. **Is the risk increasing or decreasing?** (Forecast)
3. **Why is the risk high?** (Risk DNA)
4. **What action could reduce predicted risk?** (Simulation & Recommendation)

---

## 🏗️ System Architecture

```
┌─────────────────────────────────────────────────────────┐
│           HARDWARE LAYER (Raspberry Pi)                 │
│  ┌──────┬──────┬──────┬──────┬──────┬──────┬──────┐    │
│  │ Gas  │ Temp │Humid │ Vib  │Press │Smoke │Motion│   │
│  │ MQ-2 │ DHT  │ DHT  │ Acc  │ BMP  │ ----┤ PIR  │   │
│  └──────┴──────┴──────┴──────┴──────┴──────┴──────┘    │
└─────────────────────────────────────────────────────────┘
                        ↓
┌─────────────────────────────────────────────────────────┐
│      EDGE PROCESSING (Raspberry Pi / Python)            │
│  ┌─────────┐ ┌──────────┐ ┌────────┐ ┌────────┐       │
│  │ Sensor  │→│ Validation│→│ Health │→│Feature │       │
│  │ Reading │ │ & Clean   │ │ Score  │ │Engineer│       │
│  └─────────┘ └──────────┘ └────────┘ └────────┘       │
└─────────────────────────────────────────────────────────┘
                        ↓
┌─────────────────────────────────────────────────────────┐
│         AI/ML PROCESSING (Python - Scikit-learn)       │
│  ┌──────────┐ ┌──────┐ ┌─────────┐ ┌────────┐         │
│  │ Anomaly  │→│ Risk │→│Forecst  │→│Explain │         │
│  │ Detection│ │Engine│ │(ARIMA)  │ │(SHAP)  │         │
│  │(Iso.For)│ │      │ │         │ │        │         │
│  └──────────┘ └──────┘ └─────────┘ └────────┘         │
│  ┌──────────────────────────────────────────┐          │
│  │ What-If Simulation (Counterfactual)      │          │
│  │ Recommendation Engine                    │          │
│  └──────────────────────────────────────────┘          │
└─────────────────────────────────────────────────────────┘
                        ↓
┌─────────────────────────────────────────────────────────┐
│         DATABASE LAYER (PostgreSQL / SQLite)            │
│  ┌─────────────┐ ┌───────────┐ ┌──────────────┐       │
│  │   Sensor    │ │    Risk   │ │  Anomalies   │       │
│  │  Readings   │ │Predictions│ │   & Alerts   │       │
│  └─────────────┘ └───────────┘ └──────────────┘       │
└─────────────────────────────────────────────────────────┘
                        ↓
┌─────────────────────────────────────────────────────────┐
│      API LAYER (FastAPI - REST endpoints)              │
│  GET /sensors/latest    GET /risk/current              │
│  GET /risk/forecast     GET /risk/explanation          │
│  POST /what-if          GET /anomalies                 │
│  POST /recommendation   GET /alerts                    │
└─────────────────────────────────────────────────────────┘
                        ↓
┌─────────────────────────────────────────────────────────┐
│    FRONTEND LAYER (React.js + Recharts)                │
│  ┌─────────────┐ ┌────────────┐ ┌──────────────┐      │
│  │ Current     │ │ Risk DNA   │ │ What-If      │      │
│  │ Status      │ │ Breakdown  │ │ Simulator    │      │
│  ├─────────────┤ ├────────────┤ ├──────────────┤      │
│  │ Live Sensor │ │ Forecast   │ │ Recommend.   │      │
│  │ Cards       │ │ Chart      │ │              │      │
│  └─────────────┘ └────────────┘ └──────────────┘      │
└─────────────────────────────────────────────────────────┘
                        ↓
┌─────────────────────────────────────────────────────────┐
│    ALERT & NOTIFICATION LAYER                          │
│  ┌──────────────┐ ┌────────────┐ ┌──────────────┐     │
│  │ Buzzer Alarm │ │ LED Status │ │ Dashboard    │     │
│  │ (GPIO Pin)   │ │ Indicators │ │ Notifications│     │
│  └──────────────┘ └────────────┘ └──────────────┘     │
└─────────────────────────────────────────────────────────┘
```

---

## 📋 Tech Stack

| Layer | Technology | Purpose |
|-------|-----------|---------|
| **Hardware** | Raspberry Pi, MQ-2, DHT, BMP, Accelerometer | Sensor data acquisition |
| **Edge Processing** | Python 3.12, Pandas, NumPy | Real-time data processing |
| **ML/AI** | Scikit-learn, Isolation Forest | Anomaly detection, risk scoring |
| **Forecasting** | ARIMA, Exponential Smoothing | Time-series prediction |
| **Database** | PostgreSQL, SQLite | Data persistence |
| **API** | FastAPI, Pydantic | REST endpoints |
| **Frontend** | React.js, Recharts, TypeScript | Interactive dashboard |
| **Deployment** | Docker, Docker Compose | Containerization |

---

## 🚀 Quick Start

### Prerequisites
- Python 3.12+
- Node.js 18+ (for React frontend)
- PostgreSQL 13+ (or SQLite for development)
- Raspberry Pi (optional - simulation mode works on Windows/Mac)

### Installation

1. **Clone Repository**
   ```bash
   git clone https://github.com/ydvsamiirrr2007/Underground-Mine-Safety-Analytics.git
   cd Underground-Mine-Safety-Analytics
   ```

2. **Setup Python Environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   pip install -r requirements.txt
   ```

3. **Configure System**
   ```bash
   cp .env.example .env
   # Edit .env with your settings
   ```

4. **Run in Simulation Mode (No Hardware Needed)**
   ```bash
   python tests/test_config.py  # Verify configuration
   python src/data_generator.py  # Generate test data
   streamlit run dashboard/app.py  # View dashboard
   ```

5. **Setup Frontend (React)**
   ```bash
   cd frontend
   npm install
   npm start  # Runs on http://localhost:3000
   ```

---

## 📁 Project Structure

```
Underground-Mine-Safety-Analytics/
├── config.json                 # System configuration
├── .env.example               # Environment template
├── config/
│   ├── __init__.py
│   └── config_loader.py       # Configuration management
├── hardware/
│   ├── sensors.py             # Sensor abstraction
│   ├── gpio.py                # GPIO control
│   ├── alerts.py              # Buzzer & LED alerts
│   └── sensor_config.py       # Hardware configuration
├── processing/
│   ├── cleaner.py             # Data validation
│   ├── feature_engineering.py # Feature creation
│   ├── sensor_fusion.py       # Multi-sensor fusion
│   └── sensor_health.py       # Sensor reliability
├── ai/
│   ├── anomaly.py             # Isolation Forest anomaly detection
│   ├── risk_engine.py         # Risk scoring
│   ├── forecasting.py         # Risk forecasting
│   ├── risk_explanation.py    # Risk DNA / Feature contribution
│   ├── counterfactual.py      # What-if simulation
│   ├── recommendation.py      # Safety recommendations
│   ├── train.py               # Model training
│   └── predict.py             # Predictions
├── database/
│   ├── database.py            # Database connection
│   ├── models.py              # ORM models
│   └── schema.sql             # Database schema
├── api/
│   ├── server.py              # FastAPI application
│   ├── schemas.py             # Pydantic models
│   └── services.py            # Business logic
├── src/
│   ├── analytics.py           # Statistical analysis
│   ├── anomaly_detection.py   # Anomaly detection
│   ├── risk_analysis.py       # Risk analysis
│   ├── feature_engineering.py # Feature engineering
│   ├── data_generator.py      # Test data generation
│   ├── preprocessing.py       # Data preprocessing
│   └── prediction.py          # Risk prediction
├── dashboard/
│   └── app.py                 # Streamlit dashboard
├── frontend/
│   ├── src/
│   │   ├── components/        # React components
│   │   ├── pages/             # Page components
│   │   ├── services/          # API services
│   │   └── App.jsx            # Main app
│   └── package.json
├── tests/
│   ├── test_config.py         # Configuration tests
│   └── ...                    # Other tests
├── docs/
│   ├── PHASE_2_CONFIGURATION.md
│   ├── architecture.md        # Architecture docs
│   ├── innovation.md          # Innovation explanation
│   └── demo_script.md         # Demo walkthrough
├── requirements.txt           # Python dependencies
└── main.py                    # Entry point
```

---

## 🔧 Configuration

### Quick Config Reference

**System Mode** (simulation vs hardware):
```bash
export SYSTEM_MODE=simulation  # Use simulated data
export SYSTEM_MODE=hardware    # Use Raspberry Pi sensors
```

**Database** (SQLite vs PostgreSQL):
```bash
export DB_TYPE=sqlite          # Development
export DB_TYPE=postgresql      # Production
export DB_POSTGRESQL_HOST=your_host
export DB_POSTGRESQL_PASSWORD=your_password
```

**Risk Thresholds** (customize for your mine):
```bash
export RISK_THRESHOLD_LOW=25
export RISK_THRESHOLD_MEDIUM=50
export RISK_THRESHOLD_HIGH=75
```

See [PHASE_2_CONFIGURATION.md](docs/PHASE_2_CONFIGURATION.md) for complete configuration guide.

---

## 📊 Dashboard Features

### 1. Current Status Overview
- Real-time risk level (LOW/MEDIUM/HIGH/CRITICAL)
- Live sensor readings (gas, temperature, humidity, vibration, pressure)
- Latest anomalies detected
- Active alerts

### 2. Risk Analysis
- Current risk score (0-100)
- Risk trend chart (past 24 hours)
- Risk by zone comparison
- Threshold violation statistics

### 3. Risk DNA / Explanation
- Feature contribution breakdown (%)
- Which factors drive current risk?
- Visual attribution analysis
- Historical trend of each factor

### 4. Risk Forecasting
- Estimated risk 5, 10, 15 minutes ahead
- Trend direction (increasing/decreasing)
- Forecast confidence interval
- "Insufficient data" warning if needed

### 5. What-If Simulator
- Simulate safety interventions:
  - Increase ventilation (0-100%)
  - Reduce worker exposure
  - Equipment shutdown
  - Zone evacuation
- Compare current risk vs simulated risk
- Visualize impact of each scenario

### 6. Anomaly Detection
- Recent anomalies with severity levels
- Anomaly timeline chart
- Anomalies by zone breakdown
- Detection methods used (Isolation Forest, IQR, Z-score)

### 7. Live Monitoring
- Real-time sensor gauges
- Zone-by-zone status indicators
- Data streaming (simulated or hardware)
- Alert notifications

---

## 🤖 ML Pipeline

### 1. Anomaly Detection (Isolation Forest)
- **Algorithm:** Scikit-learn Isolation Forest
- **Input:** Current sensor readings + historical context
- **Output:** Anomaly flag, anomaly score
- **Interpretation:** Unusual sensor pattern (not necessarily dangerous)

### 2. Risk Engine
- **Input:** Gas, temperature, humidity, vibration levels
- **Weights:** Gas 40%, Temperature 30%, Vibration 20%, Humidity 10%
- **Output:** Risk score 0-100
- **Levels:** LOW (0-25), MEDIUM (25-50), HIGH (50-75), CRITICAL (75-100)
- **Note:** Prototype thresholds - not regulatory compliance

### 3. Risk Forecasting
- **Method:** ARIMA / Exponential Smoothing
- **Horizon:** +5, +10, +15 minutes
- **Input:** Historical risk scores, trend
- **Output:** Forecast with confidence intervals
- **Caveat:** "Insufficient data for reliable forecast" if <30 readings

### 4. Risk Explanation (Risk DNA)
- **Method:** Feature importance / SHAP-like attribution
- **Shows:** What % each factor contributes to current risk
- **Example:** Gas 44%, Smoke 25%, Temperature 13%, Humidity 10%, Other 8%
- **Purpose:** Answer "Why is risk high?"

### 5. What-If Simulation
- **Method:** Modify input features, recalculate risk
- **Scenarios:**
  - Ventilation increase: reduces gas/smoke
  - Worker evacuation: reduces exposure risk
  - Equipment shutdown: reduces vibration/heat
- **Purpose:** Evaluate safety actions before implementation
- **Important:** Simulation - not guaranteed outcome

### 6. Recommendation Engine
- **Logic:** Combines risk, forecast, Risk DNA, simulation results
- **Example:** "Risk HIGH. Increasing ventilation estimated to reduce risk from 68 to 45. RECOMMENDED: Increase ventilation and inspect Zone C."
- **Disclaimer:** Prototype decision support, not substitute for certified procedures

---

## 🔋 Offline-First Design

The Raspberry Pi can operate autonomously:

✓ **Runs locally without internet:**
- Sensor reading
- Validation
- Anomaly detection
- Risk calculation
- Alert generation

✓ **Buffered locally when disconnected:**
- All data stored locally
- Alerts still trigger
- Safety functions unaffected

✓ **Syncs when connected:**
- Uploads buffered data to server
- Pulls updated models if needed
- Bidirectional sync

---

## 🧪 Testing

### Run All Tests
```bash
pytest tests/
```

### Run Configuration Tests
```bash
python tests/test_config.py
```

### Run with Coverage
```bash
pytest --cov=. tests/
```

### Test Simulation Scenarios
```python
from src.data_generator import MineDataGenerator
gen = MineDataGenerator(scenario="gas_rising")
data = gen.generate_sensor_readings(num_records=1000)
```

---

## 📈 Demo Scenario

See [docs/demo_script.md](docs/demo_script.md) for complete walkthrough.

**Quick Demo:**
1. Start dashboard: `streamlit run dashboard/app.py`
2. Select "Live Monitoring" tab
3. System shows LOW risk (all sensors normal)
4. Trigger gas spike: Backend shifts to "gas_rising" scenario
5. Anomaly detected → Risk increases to MEDIUM
6. Forecast shows risk trending to HIGH
7. Risk DNA shows gas is main contributor (65%)
8. Open What-If: Simulate ventilation +30%
9. Projected risk drops to MEDIUM (54)
10. Recommendation: "Increase ventilation - estimated impact: -14 risk points"
11. If critical threshold (85+): Buzzer sounds, red LED on

---

## 🛠️ Development Status

### ✅ Completed (Phases 1-2)
- [x] Codebase audit
- [x] Configuration system (JSON + Environment)
- [x] Sensor data models
- [x] Data validation & cleaning
- [x] Feature engineering
- [x] Anomaly detection (Isolation Forest)
- [x] Risk scoring engine
- [x] Analytics & statistical analysis
- [x] Streamlit dashboard
- [x] Hardware abstraction (simulation mode)

### 🚀 In Progress / Planned (Phases 3-20)
- [ ] Sensor data model standardization (Phase 3)
- [ ] Sensor health assessment (Phase 6)
- [ ] Risk forecasting (Phase 5)
- [ ] Risk explanation / Risk DNA (Phase 6)
- [ ] What-if simulation (Phase 7)
- [ ] Recommendation engine (Phase 8)
- [ ] FastAPI backend (Phase 9)
- [ ] React frontend (Phase 10)
- [ ] PostgreSQL migration (Phase 11)
- [ ] Hardware alerts (buzzer/LEDs) (Phase 12)
- [ ] Comprehensive testing suite (Phase 13)
- [ ] main.py orchestration (Phase 14)
- [ ] Complete documentation (Phase 15)

---

## 📚 Documentation

- **[PHASE_2_CONFIGURATION.md](docs/PHASE_2_CONFIGURATION.md)** - Configuration system guide
- **[architecture.md](docs/architecture.md)** - System architecture details
- **[innovation.md](docs/innovation.md)** - Innovation explanation for judges
- **[demo_script.md](docs/demo_script.md)** - Step-by-step demo walkthrough

---

## ⚖️ Important Disclaimers

### This is a Prototype for SIH 2026

**NOT a certified mine safety system.**

This system:
- ✓ Demonstrates integrated approach to mine safety analytics
- ✓ Shows predictive decision support concept
- ✓ Provides prototype risk scoring
- ✓ Illustrates what-if simulation capability

This system is NOT:
- ✗ Regulatory compliance certified
- ✗ Guaranteed accurate risk prediction
- ✗ Certified evacuation system
- ✗ Replacement for certified mine safety procedures
- ✗ Production-ready without regulatory review

**Use terminology:**
- "Estimated risk" (not "actual risk")
- "Prototype decision support" (not "certified system")
- "Simulated scenario" (not "guaranteed outcome")
- "Model prediction" (not "guarantee")

---

## 👥 Team

- **Samir** - Hardware (Sensors, GPIO, Alerts)
- **Arshiya** - Backend (FastAPI, REST APIs)
- **Nishtha** - Database (PostgreSQL, SQL)
- **Anirudh** - AI/ML (Anomaly, Risk, Forecasting, Simulation)
- **Aman** - Frontend (React Dashboard)
- **Zonaira** - Documentation & Presentation

---

## 📞 Support & Contact

For questions about this SIH 2026 prototype:
- Repository: https://github.com/ydvsamiirrr2007/Underground-Mine-Safety-Analytics
- Issues: Use GitHub Issues
- Documentation: See `/docs` folder

---

## 📄 License

This project is part of SIH 2026 competition.

---

**Last Updated:** Phase 2 - Configuration System Complete ✓

**Next Phase:** Phase 3 - Sensor Data Model Standardization
