#!/bin/bash

echo "🚀 Testing Render.com Configuration Locally"
echo "=========================================="

# Check if requirements are installed
echo "📦 Installing requirements..."
pip install -r requirements.txt

echo ""
echo "🧪 Testing with Gunicorn (Render's production server)..."
echo "🌐 Your app will be available at: http://localhost:8000"
echo "🛑 Press Ctrl+C to stop the server"
echo ""

# Start with gunicorn (same as Render)
PORT=8000 gunicorn --bind 0.0.0.0:8000 --timeout 120 app:app