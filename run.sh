#!/bin/bash

# Ensure we're in the project root directory
cd "$(dirname "$0")"

# Ensure output directory exists
mkdir -p output

# Check for '--html-report' flag
HTML_REPORT=false

for arg in "$@"
do
    if [ "$arg" == "--html-report" ]; then
        HTML_REPORT=true
    fi
done

# Activate virtual environment if it exists
if [ -d ".venv" ]; then
    source .venv/bin/activate
fi

echo "Starting Public School Data Analysis..."

# Run the main analysis script
python src/DMProject.py

# If --html-report flag is provided, generate the HTML report
if [ "$HTML_REPORT" = true ]; then
    echo "Generating HTML report..."
    python src/generate_html_report.py

    # Copy the HTML report to Vercel's public directory
    mkdir -p public
    cp output/school_data_report.html public/index.html
    echo "Copied HTML report to public/index.html for Vercel deployment."

    # Copy all PNG visualizations to public for Vercel deployment
    cp output/*.png public/
    echo "Copied PNG visualizations to public/ for Vercel deployment."
fi

echo "Analysis complete. Check the output directory for visualization results."

# Open the output files with the default application
if [ "$(uname)" == "Darwin" ]; then  # macOS
    echo "Opening generated visualizations..."
    open output/*.png
elif [ "$(expr substr $(uname -s) 1 5)" == "Linux" ]; then  # Linux
    echo "Opening generated visualizations..."
    xdg-open output/*.png 2>/dev/null || true
elif [ "$(expr substr $(uname -s) 1 10)" == "MINGW32_NT" ]; then  # Windows with GitBash
    echo "Opening generated visualizations..."
    start output/*.png
fi

echo "To generate HTML report, run: ./run.sh --html-report"


