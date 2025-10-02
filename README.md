# 🌍 SEISMO-GUARD Dashboard

**AI-Powered Real-Time Earthquake Risk Monitoring System**

SEISMO-GUARD is a comprehensive web dashboard for monitoring seismic activity across Turkey, with primary focus on Istanbul and the Marmara region. The system integrates real-time data from AFAD (Turkey's Disaster and Emergency Management Authority) and EMSC (European-Mediterranean Seismological Centre) to provide risk assessments, pattern detection, and predictive analysis.

![Dashboard Preview](docs/preview.png)

## 🚨 Critical Context

**Istanbul is in a HIGH seismic hazard zone** with >20% probability of experiencing a damaging earthquake within the next 50 years due to the North Anatolian Fault Zone beneath the Marmara Sea (259-year seismic gap).

---

## ✨ Features

### 📊 Real-Time Monitoring
- **Live earthquake data** from AFAD and EMSC APIs
- **Interactive map visualization** with Leaflet showing event locations
- **Automatic data refresh** every 5 minutes
- **Multi-source data fusion** with deduplication

### 🎯 Risk Assessment
- **Regional risk levels** (LOW/MEDIUM/HIGH) with confidence scores
- **Probabilistic forecasting** (7-day M5+ and 30-day M6+ probabilities)
- **Trend analysis** (Increasing/Stable/Decreasing)
- **Context-aware recommendations** based on fault proximity and historical patterns

### 🔍 Pattern Detection
- **Temporal patterns**: Foreshock-mainshock-aftershock sequences, swarms
- **Spatial clustering**: Geographic concentration of events
- **Anomaly detection**: Unusual depth distributions, magnitude patterns
- **b-value calculations** (Gutenberg-Richter law)

### 📈 Data Visualization
- **Interactive earthquake map** with magnitude-based markers
- **Magnitude distribution charts** (bar charts)
- **Depth distribution** (doughnut charts)
- **7-day timeline** showing seismic activity trends
- **Recent significant events table**

### 🌐 Regional Coverage
- **Istanbul** - Critical monitoring due to NAF proximity
- **Marmara Sea** - 259-year seismic gap
- **Aegean** - Active extensional zone
- **Eastern Anatolia** - Recent major events (2023 M7.8)
- **Central Anatolia** - Background monitoring

---

## 🏗️ Architecture

```
seismo-guard-dashboard/
├── backend/
│   ├── main.py                 # FastAPI application
│   ├── data_fetcher.py         # AFAD & EMSC data fetchers
│   ├── data_processor.py       # Normalization & pattern detection
│   └── risk_analyzer.py        # Risk assessment engine
├── frontend/
│   ├── index.html              # Main dashboard HTML
│   ├── css/
│   │   └── styles.css          # Dashboard styling
│   └── js/
│       └── dashboard.js        # Interactive visualization logic
├── data/                       # Data storage (cached events)
├── docs/                       # Documentation
├── Dockerfile                  # Container configuration
├── docker-compose.yml          # Orchestration
├── requirements.txt            # Python dependencies
└── README.md                   # This file
```

### Technology Stack

**Backend:**
- FastAPI - Modern async web framework
- httpx - Async HTTP client for API calls
- Pandas/NumPy - Data processing
- Pydantic - Data validation

**Frontend:**
- HTML5/CSS3/JavaScript (Vanilla)
- Leaflet.js - Interactive maps
- Chart.js - Data visualization
- Responsive design

**Deployment:**
- Docker & Docker Compose
- Health checks and auto-restart

---

## 🚀 Quick Start

### Prerequisites
- Python 3.11+
- Docker & Docker Compose (for containerized deployment)
- 2GB RAM minimum
- Internet connection for API access

### Option 1: Docker Deployment (Recommended)

```bash
# Clone or navigate to the project directory
cd seismo-guard-dashboard

# Build and start the container
docker-compose up -d

# Check logs
docker-compose logs -f

# Access dashboard
open http://localhost:8000
```

### Option 2: Local Development

```bash
# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Run the server
cd backend
python main.py

# Access dashboard
open http://localhost:8000
```

---

## 📡 API Endpoints

### Health Check
```
GET /api/health
```

### Recent Earthquakes
```
GET /api/earthquakes/recent?hours=24&min_magnitude=0.0&region=Istanbul
```

### Risk Assessment
```
GET /api/risk-assessment/{region}
```

### Statistics Summary
```
GET /api/statistics/summary
```

### Pattern Analysis
```
GET /api/analysis/patterns
```

### Monitored Regions
```
GET /api/regions
```

---

## 🎨 Dashboard Components

### 1. **Header Status Bar**
- System status indicator (Active/Inactive)
- Last update timestamp
- Manual refresh button

### 2. **Key Metrics Cards**
- Total events (24h)
- Maximum magnitude
- Average depth
- Istanbul risk level

### 3. **Interactive Map**
- Color-coded earthquake markers by magnitude
- Fault line overlays (NAF, EAF)
- Region/magnitude filters
- Popup details for each event

### 4. **Risk Assessment Panel**
- Current risk level with confidence
- Probabilistic forecasts
- Contributing factors
- Safety recommendations

### 5. **Distribution Charts**
- Magnitude distribution (bar chart)
- Depth distribution (doughnut chart)

### 6. **Timeline Chart**
- 7-day seismic activity visualization
- Event count per day

### 7. **Recent Events Table**
- Significant earthquakes (M ≥ 2.5)
- Sorted by magnitude
- Time, location, depth, region

### 8. **Pattern Detection**
- Detected sequences and clusters
- Anomalies and warnings

---

## ⚙️ Configuration

### Environment Variables

Create a `.env` file (optional):

```env
# API Configuration
AFAD_API_URL=https://deprem.afad.gov.tr/apiv2/event
EMSC_API_URL=https://www.seismicportal.eu/fdsnws/event/1/query

# Refresh Settings
AUTO_REFRESH_INTERVAL=300000  # 5 minutes in milliseconds
CACHE_TTL=300  # 5 minutes in seconds

# Server
HOST=0.0.0.0
PORT=8000
```

---

## 📊 Data Sources

### AFAD (Disaster and Emergency Management Authority)
- **URL**: https://deprem.afad.gov.tr/
- **Coverage**: Turkey
- **Update Frequency**: Near real-time
- **Magnitude Type**: Ml (Local magnitude)

### EMSC (European-Mediterranean Seismological Centre)
- **URL**: https://www.seismicportal.eu/
- **Coverage**: Euro-Mediterranean region
- **Update Frequency**: Real-time
- **Magnitude Type**: ML, Mw

### Data Processing
- **Deduplication**: Events within 10km and 5 minutes are merged
- **Source Agreement**: AFAD and EMSC data are cross-validated
- **Normalization**: Unified timestamp, coordinate, and magnitude formats

---

## 🔬 Risk Assessment Methodology

### Risk Calculation Components

1. **Event Rate Score (30%)**
   - Events per day in the region
   - Compared to historical baseline

2. **Magnitude Score (30%)**
   - Maximum recent magnitude
   - Count of significant events (M ≥ 4.0)

3. **Pattern Score (20%)**
   - Spatial clustering coefficient
   - Rate increase detection

4. **Temporal Score (20%)**
   - Inter-event time analysis
   - Sequence identification

### Risk Levels
- **HIGH**: Elevated activity or critical fault proximity
- **MEDIUM**: Moderate activity or active seismic zones
- **LOW**: Background seismicity

### Confidence Scores
Based on:
- Data source agreement (AFAD ↔ EMSC)
- Event count (more data = higher confidence)
- Score extremes (clear signals)

---

## ⚠️ Important Disclaimers

1. **No Deterministic Predictions**
   - This system provides RISK ASSESSMENTS, not earthquake predictions
   - No technology can predict exact time/location of earthquakes

2. **Probabilistic Nature**
   - All forecasts are probabilistic and include uncertainty
   - Confidence scores reflect reliability, not certainty

3. **Preparedness Focus**
   - System emphasizes preparedness, not panic
   - Recommendations align with official building codes and emergency guidelines

4. **Long-Term Context**
   - Istanbul's high risk is based on 50-year probability, not imminent danger
   - Continuous monitoring and preparedness are essential

---

## 🛠️ Development

### Running Tests
```bash
# Backend tests
pytest backend/tests/

# API testing
curl http://localhost:8000/api/health
```

### Adding New Features

1. **New Data Source**
   - Create fetcher class in `data_fetcher.py`
   - Add normalization logic in `data_processor.py`

2. **New Risk Metric**
   - Add calculation method in `risk_analyzer.py`
   - Update API endpoint in `main.py`

3. **New Visualization**
   - Add chart function in `dashboard.js`
   - Update HTML structure in `index.html`

---

## 📈 Roadmap

- [ ] WebSocket support for real-time updates
- [ ] PostgreSQL + PostGIS for persistent storage
- [ ] Machine learning anomaly detection (Isolation Forest)
- [ ] SMS/Email alerting system
- [ ] Multi-language support (Turkish, English)
- [ ] Mobile-responsive improvements
- [ ] Historical data analysis (5+ years)
- [ ] Stress transfer modeling (Coulomb)
- [ ] Integration with seismic station networks

---

## 🤝 Contributing

Contributions are welcome! Please follow these guidelines:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

---

## 📄 License

This project is licensed under the MIT License.

---

## 📞 Support

For issues, questions, or suggestions:
- Open an issue on GitHub
- Contact: seismo-guard@example.com

---

## 🙏 Acknowledgments

- **AFAD** (Turkey Disaster and Emergency Management Authority) for earthquake data
- **EMSC** (European-Mediterranean Seismological Centre) for real-time feeds
- **Leaflet.js** for interactive mapping
- **Chart.js** for data visualization
- **FastAPI** for the robust backend framework

---

## 📚 References

1. Stein, R. S., Barka, A. A., & Dieterich, J. H. (1997). Progressive failure on the North Anatolian fault since 1939 by earthquake stress triggering. *Geophysical Journal International*.

2. Parsons, T. (2004). Recalculated probability of M ≥ 7 earthquakes beneath the Sea of Marmara, Turkey. *Journal of Geophysical Research*.

3. AFAD Official Website: https://deprem.afad.gov.tr/

4. EMSC Portal: https://www.seismicportal.eu/

---

**⚠️ Remember: Stay prepared. Stay safe. Istanbul's high seismic risk requires continuous vigilance and readiness.**

© 2025 SEISMO-GUARD | AI Earthquake Risk Monitoring System v1.0.0
