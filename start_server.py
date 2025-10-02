#!/usr/bin/env python3
"""
SEISMO-GUARD Server Startup Script
Starts the FastAPI server with proper configuration
"""

import sys
import os

# Add backend directory to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'backend'))

if __name__ == "__main__":
    import uvicorn
    from backend.main import app

    print("🌍 Starting SEISMO-GUARD Earthquake Monitoring Dashboard")
    print("=" * 60)
    print()
    print("📊 Dashboard URL: http://localhost:8000")
    print("📡 API Documentation: http://localhost:8000/docs")
    print()
    print("Press CTRL+C to stop the server")
    print()

    # Start server
    uvicorn.run(
        "backend.main:app",
        host="0.0.0.0",
        port=8000,
        reload=False,
        log_level="info"
    )
