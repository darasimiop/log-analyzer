#!/bin/bash

echo "🚀 Setting up Log Analyzer..."

# Step 1: Update system
echo "🔄 Updating system packages..."
sudo apt update -y && sudo apt install -y python3 python3-venv python3-pip

# Step 2: Clone repository
if [ ! -d "log-analyzer" ]; then
    echo "📥 Cloning repository..."
    git clone https://github.com/darasimiop/log-analyzer.git
fi
cd log-analyzer

# Step 3: Setup Python virtual environment
echo "🐍 Creating virtual environment..."
python3 -m venv venv
source venv/bin/activate

# Step 4: Install dependencies
echo "📦 Installing dependencies..."
pip install -r requirements.txt

# Step 5: Copy system log file (Linux only)
echo "📂 Copying auth.log (Requires sudo access)..."
sudo cp /var/log/auth.log ./auth.log

echo "✅ Setup complete! Run 'python log_analyzer.py -f auth.log' to start analysis."


