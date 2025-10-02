#!/bin/bash
# Startup script for Railway deployment

# Set default port if not provided
PORT=${PORT:-8000}

echo "Starting SEISMO-GUARD on port $PORT"

# Start uvicorn
exec uvicorn backend.main:app --host 0.0.0.0 --port $PORT
