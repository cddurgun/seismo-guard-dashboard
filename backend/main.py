"""
SEISMO-GUARD Backend API
FastAPI server providing earthquake data and risk assessment endpoints
"""

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
import uvicorn
from datetime import datetime, timedelta
from typing import List, Dict, Optional
import asyncio
from pydantic import BaseModel

from .data_fetcher import AFADDataFetcher, EMSCDataFetcher, USGSDataFetcher
from .data_processor import SeismicDataProcessor
from .risk_analyzer import RiskAnalyzer

app = FastAPI(title="SEISMO-GUARD API", version="1.0.0")

# CORS configuration for frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount static files - serve frontend directory
import os
frontend_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "frontend")
app.mount("/css", StaticFiles(directory=os.path.join(frontend_path, "css")), name="css")
app.mount("/js", StaticFiles(directory=os.path.join(frontend_path, "js")), name="js")

# Data models
class EarthquakeEvent(BaseModel):
    event_id: str
    timestamp: str
    latitude: float
    longitude: float
    depth_km: float
    magnitude: float
    magnitude_type: str
    location_name: str
    region: str
    source: str

class RiskAssessment(BaseModel):
    region: str
    risk_level: str
    probability_m5_7days: float
    probability_m6_30days: float
    confidence: int
    trend: str
    contributing_factors: List[str]
    recommendations: List[str]

# Initialize components
afad_fetcher = AFADDataFetcher()
emsc_fetcher = EMSCDataFetcher()
usgs_fetcher = USGSDataFetcher()
processor = SeismicDataProcessor()
risk_analyzer = RiskAnalyzer()

# Cache
cache = {
    'events': [],
    'last_update': None,
    'risk_assessments': {}
}

@app.get("/")
async def root():
    """Serve the main dashboard"""
    frontend_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "frontend", "index.html")
    return FileResponse(frontend_path)

@app.get("/api/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "timestamp": datetime.now().isoformat(),
        "cache_age_minutes": (datetime.now() - cache['last_update']).total_seconds() / 60 if cache['last_update'] else None
    }

@app.get("/api/earthquakes/recent")
async def get_recent_earthquakes(hours: int = 24, min_magnitude: float = 0.0, region: Optional[str] = None):
    """
    Get recent earthquakes from AFAD and EMSC

    Parameters:
    - hours: Look back period (default: 24)
    - min_magnitude: Minimum magnitude filter (default: 0.0)
    - region: Filter by region (Istanbul, Marmara, Aegean, etc.)
    """
    try:
        # Check cache age
        if cache['last_update'] and (datetime.now() - cache['last_update']).total_seconds() < 300:
            # Use cached data if less than 5 minutes old
            events = cache['events']
        else:
            # Fetch fresh data from multiple sources
            afad_events = await afad_fetcher.get_recent_earthquakes(hours=hours)
            emsc_events = await emsc_fetcher.get_events_fdsn(hours=hours)
            usgs_events = await usgs_fetcher.get_earthquakes(hours=hours)

            # Normalize and merge from all sources
            all_source_events = afad_events + emsc_events + usgs_events
            events = processor.normalize_and_merge(afad_events, emsc_events)

            # Add USGS events
            for usgs_event in usgs_events:
                normalized = processor._normalize_event(usgs_event)
                if normalized and normalized not in events:
                    normalized['region'] = processor._classify_region(
                        normalized['latitude'],
                        normalized['longitude']
                    )
                    events.append(normalized)

            # Update cache
            cache['events'] = events
            cache['last_update'] = datetime.now()

        # Apply filters
        filtered_events = [
            e for e in events
            if e['magnitude'] >= min_magnitude
            and (not region or e['region'] == region)
        ]

        return {
            "count": len(filtered_events),
            "events": filtered_events,
            "last_update": cache['last_update'].isoformat() if cache['last_update'] else None,
            "sources": {
                "afad": len([e for e in filtered_events if e['source'] in ['AFAD', 'MERGED']]),
                "emsc": len([e for e in filtered_events if e['source'] in ['EMSC', 'MERGED']]),
                "usgs": len([e for e in filtered_events if e['source'] == 'USGS'])
            }
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/risk-assessment/{region}")
async def get_risk_assessment(region: str):
    """
    Get current risk assessment for a specific region

    Regions: Istanbul, Marmara, Aegean, Eastern_Anatolia, etc.
    """
    try:
        # Check cache
        cache_key = f"{region}_{datetime.now().strftime('%Y%m%d_%H')}"
        if cache_key in cache['risk_assessments']:
            return cache['risk_assessments'][cache_key]

        # Get recent events for the region
        if not cache['events'] or not cache['last_update']:
            afad_events = await afad_fetcher.get_recent_earthquakes(hours=168)  # 7 days
            emsc_events = await emsc_fetcher.get_events_fdsn(hours=168)
            cache['events'] = processor.normalize_and_merge(afad_events, emsc_events)
            cache['last_update'] = datetime.now()

        region_events = [e for e in cache['events'] if e['region'] == region]

        # Perform risk analysis
        assessment = risk_analyzer.calculate_risk_assessment(region, region_events)

        # Cache result
        cache['risk_assessments'][cache_key] = assessment

        return assessment
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/statistics/summary")
async def get_statistics_summary():
    """
    Get overall statistics summary for dashboard
    """
    try:
        if not cache['events'] or not cache['last_update']:
            afad_events = await afad_fetcher.get_recent_earthquakes(hours=24)
            emsc_events = await emsc_fetcher.get_events_fdsn(hours=24)
            cache['events'] = processor.normalize_and_merge(afad_events, emsc_events)
            cache['last_update'] = datetime.now()

        events = cache['events']

        # Calculate statistics
        stats = {
            "total_events_24h": len(events),
            "max_magnitude_24h": max([e['magnitude'] for e in events]) if events else 0,
            "avg_depth_km": sum([e['depth_km'] for e in events]) / len(events) if events else 0,
            "events_by_region": {},
            "magnitude_distribution": {
                "0-2": 0, "2-3": 0, "3-4": 0, "4-5": 0, "5+": 0
            },
            "depth_distribution": {
                "0-10km": 0, "10-20km": 0, "20-40km": 0, "40+km": 0
            },
            "last_significant_event": None
        }

        # Count by region
        for event in events:
            region = event['region']
            stats['events_by_region'][region] = stats['events_by_region'].get(region, 0) + 1

            # Magnitude distribution
            mag = event['magnitude']
            if mag < 2:
                stats['magnitude_distribution']['0-2'] += 1
            elif mag < 3:
                stats['magnitude_distribution']['2-3'] += 1
            elif mag < 4:
                stats['magnitude_distribution']['3-4'] += 1
            elif mag < 5:
                stats['magnitude_distribution']['4-5'] += 1
            else:
                stats['magnitude_distribution']['5+'] += 1

            # Depth distribution
            depth = event['depth_km']
            if depth < 10:
                stats['depth_distribution']['0-10km'] += 1
            elif depth < 20:
                stats['depth_distribution']['10-20km'] += 1
            elif depth < 40:
                stats['depth_distribution']['20-40km'] += 1
            else:
                stats['depth_distribution']['40+km'] += 1

        # Find last significant event (M >= 4.0)
        significant_events = [e for e in events if e['magnitude'] >= 4.0]
        if significant_events:
            significant_events.sort(key=lambda x: x['timestamp'], reverse=True)
            stats['last_significant_event'] = significant_events[0]

        return stats
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/analysis/patterns")
async def get_pattern_analysis():
    """
    Get detected seismic patterns (clusters, swarms, sequences)
    """
    try:
        if not cache['events']:
            afad_events = await afad_fetcher.get_recent_earthquakes(hours=168)
            emsc_events = await emsc_fetcher.get_events_fdsn(hours=168)
            cache['events'] = processor.normalize_and_merge(afad_events, emsc_events)

        patterns = processor.detect_patterns(cache['events'])

        return {
            "temporal_patterns": patterns.get('temporal', []),
            "spatial_clusters": patterns.get('spatial', []),
            "anomalies": patterns.get('anomalies', []),
            "analysis_timestamp": datetime.now().isoformat()
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/regions")
async def get_regions():
    """
    Get list of monitored regions with basic info
    """
    return {
        "regions": [
            {
                "name": "Istanbul",
                "bbox": {"lat_min": 40.8, "lat_max": 41.3, "lon_min": 28.5, "lon_max": 29.5},
                "population_millions": 15.5,
                "risk_context": "High seismic hazard zone - North Anatolian Fault proximity"
            },
            {
                "name": "Marmara",
                "bbox": {"lat_min": 40.4, "lat_max": 41.0, "lon_min": 27.0, "lon_max": 29.5},
                "population_millions": 2.5,
                "risk_context": "Critical seismic gap - NAF Marmara segment (259-year gap)"
            },
            {
                "name": "Aegean",
                "bbox": {"lat_min": 37.0, "lat_max": 40.0, "lon_min": 26.0, "lon_max": 29.0},
                "population_millions": 5.2,
                "risk_context": "Active seismic zone - Aegean extensional regime"
            },
            {
                "name": "Eastern_Anatolia",
                "bbox": {"lat_min": 38.0, "lat_max": 41.0, "lon_min": 38.0, "lon_max": 44.0},
                "population_millions": 3.8,
                "risk_context": "East Anatolian Fault - recent major events (2023)"
            }
        ]
    }

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000, reload=True)
