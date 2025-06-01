#!/bin/bash

# Ensure we're in the project root directory
cd "$(dirname "$0")"

# Ensure output directory exists
mkdir -p output

# Run the analysis
echo "Starting Public School Data Analysis..."
python src/DMProject.py

# Add an optional flag to generate additional explanatory materials
if [ "$1" == "--with-report" ]; then
  echo "Generating explanatory report..."
  python src/generate_report.py
fi

echo "Analysis complete. Check the output directory for visualization results."
echo "To generate additional explanatory materials, run: ./run.sh --with-report"
