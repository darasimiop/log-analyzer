#!/bin/bash

echo "🚀 Starting Log Analyzer..."

# Activate virtual environment
source venv/bin/activate

# Start Flask Web App
python3 app.py &

# Start Log Monitoring
python3 log_analyzer.py &

echo "✅ Log Analyzer & Web App Running!"
