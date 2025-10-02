#!/usr/bin/env python
"""
Startup script for Railway deployment
Reads PORT from environment and starts uvicorn
"""
import os
import uvicorn

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8000))
    print(f"🌍 Starting SEISMO-GUARD on port {port}")

    uvicorn.run(
        "backend.main:app",
        host="0.0.0.0",
        port=port,
        log_level="info"
    )
