#!/bin/bash
# Quick run script for Tour Planning
# Usage: ./run.sh

# Get the directory where this script is located
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
cd "$SCRIPT_DIR"

# Check if API key is set
if [ -z "$HERE_API_KEY" ]; then
    echo "⚠️  HERE_API_KEY not set!"
    echo ""
    echo "Please set it first:"
    echo "  export HERE_API_KEY='your_api_key_here'"
    echo ""
    echo "Or create a .env file with: HERE_API_KEY=your_key"
    exit 1
fi

# Run the script
echo "🚀 Running Tour Planning..."
python3 run_tour_planning_gdrive.py

