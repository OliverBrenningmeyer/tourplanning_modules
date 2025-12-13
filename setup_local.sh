#!/bin/bash
# Quick setup script for local execution

echo "=========================================="
echo "Tour Planning - Local Setup"
echo "=========================================="
echo ""

# Check Python
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 not found. Please install Python 3.8+"
    exit 1
fi
echo "✓ Python found: $(python3 --version)"

# Install dependencies
echo ""
echo "Installing dependencies..."
pip install -q -r requirements.txt
echo "✓ Dependencies installed"

# Create data directory structure
echo ""
echo "Creating data directory structure..."
mkdir -p data/{kemmler,stark,Wigger,Obi_Buchholz,laminatdepot,generic_tourplanning}/depots
echo "✓ Data directories created"

# Check for API key
echo ""
if [ -z "$HERE_API_KEY" ]; then
    echo "⚠️  HERE_API_KEY not set"
    echo ""
    echo "Please set your API key:"
    echo "  export HERE_API_KEY='your_key_here'"
    echo ""
    echo "Or create a .env file:"
    echo "  echo 'HERE_API_KEY=your_key_here' > .env"
    echo ""
    echo "You can get your API key from: https://developer.here.com/"
else
    echo "✓ HERE_API_KEY is set"
fi

# Check for data files
echo ""
echo "Checking for data files..."
if [ -f "data/kemmler/depots/Depots_geocoded.xlsx" ]; then
    echo "✓ Depots file found"
else
    echo "⚠️  Depots file not found at: data/kemmler/depots/Depots_geocoded.xlsx"
    echo "   Please copy your Depots_geocoded.xlsx file to this location"
fi

if [ -f "data/kemmler/orders.xlsx" ]; then
    echo "✓ Orders file found"
else
    echo "⚠️  Orders file not found at: data/kemmler/orders.xlsx"
    echo "   Please copy your orders Excel file to this location"
fi

echo ""
echo "=========================================="
echo "Setup complete!"
echo "=========================================="
echo ""
echo "Next steps:"
echo "1. Set your HERE_API_KEY (if not already set)"
echo "2. Copy your data files to the data/ directory"
echo "3. Update paths in run_tour_planning.py if needed"
echo "4. Run: python run_tour_planning.py"
echo ""

