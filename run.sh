#!/bin/bash

# SEISMO-GUARD Quick Start Script

echo "🌍 SEISMO-GUARD Earthquake Monitoring Dashboard"
echo "================================================"
echo ""

# Check if Docker is installed
if command -v docker &> /dev/null; then
    echo "✓ Docker found"

    if command -v docker-compose &> /dev/null; then
        echo "✓ Docker Compose found"
        echo ""
        echo "🚀 Starting SEISMO-GUARD with Docker..."
        echo ""

        # Start with Docker Compose
        docker-compose up -d

        echo ""
        echo "✅ SEISMO-GUARD is starting up!"
        echo ""
        echo "📊 Dashboard will be available at: http://localhost:8000"
        echo ""
        echo "⏳ Please wait 10-15 seconds for the server to start..."
        sleep 15

        # Try to open in browser
        if command -v open &> /dev/null; then
            open http://localhost:8000
        elif command -v xdg-open &> /dev/null; then
            xdg-open http://localhost:8000
        else
            echo "Please open http://localhost:8000 in your browser"
        fi

        echo ""
        echo "📋 Useful commands:"
        echo "   View logs:    docker-compose logs -f"
        echo "   Stop server:  docker-compose stop"
        echo "   Restart:      docker-compose restart"
        echo ""

    else
        echo "❌ Docker Compose not found"
        echo "Please install Docker Compose: https://docs.docker.com/compose/install/"
        exit 1
    fi

else
    echo "❌ Docker not found"
    echo ""
    echo "Starting with Python instead..."
    echo ""

    # Check if Python is installed
    if command -v python3 &> /dev/null; then
        echo "✓ Python found"

        # Check if virtual environment exists
        if [ ! -d "venv" ]; then
            echo "Creating virtual environment..."
            python3 -m venv venv
        fi

        # Activate virtual environment
        source venv/bin/activate

        # Install dependencies
        echo "Installing dependencies..."
        pip install -q -r requirements.txt

        echo ""
        echo "🚀 Starting SEISMO-GUARD..."
        echo ""

        # Start server
        python -m uvicorn backend.main:app --host 0.0.0.0 --port 8000 &
        SERVER_PID=$!

        sleep 10

        echo ""
        echo "✅ SEISMO-GUARD is running!"
        echo "📊 Dashboard: http://localhost:8000"
        echo ""

        # Try to open in browser
        if command -v open &> /dev/null; then
            open http://localhost:8000
        elif command -v xdg-open &> /dev/null; then
            xdg-open http://localhost:8000
        fi

        echo ""
        echo "Press Ctrl+C to stop the server"
        echo ""

        # Wait for Ctrl+C
        wait $SERVER_PID

    else
        echo "❌ Python not found"
        echo ""
        echo "Please install Python 3.11+ or Docker to run SEISMO-GUARD"
        echo "Python: https://www.python.org/downloads/"
        echo "Docker: https://www.docker.com/products/docker-desktop"
        exit 1
    fi
fi
