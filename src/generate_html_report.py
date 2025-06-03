"""
Generate HTML reports for Public School Data Analysis
This script creates HTML reports that are more visually appealing than matplotlib-based reports

Features:
- Generates a complete HTML report with embedded visualizations
- Includes key findings summary
- Integrates variable reference guide for easy interpretation
- Dynamically finds visualization files across different path configurations
"""

import os
import pandas as pd
import numpy as np
import webbrowser
from pathlib import Path
from data_preparation import load_data
import base64
from datetime import datetime

def ensure_output_dir():
    """
    Create output directory if it doesn't exist
    
    Handles multiple possible directory structures to ensure compatibility
    across different environments and execution contexts.
    
    Returns:
        str: Path to the usable output directory
    """
    # Create both possible output directories to ensure compatibility
    os.makedirs("../output", exist_ok=True)
    os.makedirs("output", exist_ok=True)
    
    # Determine which directory to use
    if os.access("../output", os.W_OK):
        return "../output"
    elif os.access("output", os.W_OK):
        return "output"
    else:
        print("WARNING: Could not create or access output directory")
        return "../output"  # Default fallback

def get_image_base64(image_path):
    """Convert an image to base64 for embedding in HTML"""
    try:
        with open(image_path, "rb") as image_file:
            return base64.b64encode(image_file.read()).decode("utf-8")
    except Exception as e:
        print(f"Error loading image {image_path}: {e}")
        return ""

def generate_key_findings_html():
    """
    Generate an HTML version of the key findings summary with visualizations
    
    This is the main function that creates a comprehensive HTML report with:
    - Key findings from the analysis
    - Embedded data visualizations (converted to base64)
    - Integrated variable reference guide
    - Professional styling with responsive layout
    
    Returns:
        str: Path to the generated HTML file
    """
    output_dir = "output"
    os.makedirs(output_dir, exist_ok=True)
    
    # Check for visualization files in both possible output locations
    sed_math_img_paths = [
        f"{output_dir}/sed_mathscores_relationship.png",
        "output/sed_mathscores_relationship.png",
        "../output/sed_mathscores_relationship.png"
    ]
    
    correlation_img_paths = [
        f"{output_dir}/correlation_matrix.png",
        "output/correlation_matrix.png",
        "../output/correlation_matrix.png"
    ]
    
    test_scores_by_sed_img_paths = [
        f"{output_dir}/test_scores_by_sed.png",
        "output/test_scores_by_sed.png",
        "../output/test_scores_by_sed.png"
    ]
    test_scores_relationships_img_paths = [
        f"{output_dir}/test_scores_relationships.png",
        "output/test_scores_relationships.png",
        "../output/test_scores_relationships.png"
    ]
    
    # Find the first existing image path
    sed_math_img = next((path for path in sed_math_img_paths if os.path.exists(path)), None)
    correlation_img = next((path for path in correlation_img_paths if os.path.exists(path)), None)
    test_scores_by_sed_img = next((path for path in test_scores_by_sed_img_paths if os.path.exists(path)), None)
    test_scores_relationships_img = next((path for path in test_scores_relationships_img_paths if os.path.exists(path)), None)
    
    # Get base64 encoded versions of the images if they exist
    sed_math_b64 = get_image_base64(sed_math_img) if sed_math_img else ""
    correlation_b64 = get_image_base64(correlation_img) if correlation_img else ""
    test_scores_by_sed_b64 = get_image_base64(test_scores_by_sed_img) if test_scores_by_sed_img else ""
    test_scores_relationships_b64 = get_image_base64(test_scores_relationships_img) if test_scores_relationships_img else ""
    
    # Generate the current date for the report
    report_date = datetime.now().strftime("%B %d, %Y")
    
    # Variable definitions for the reference section
    variable_definitions = {
        # School identifier
        "CDSCODE": {"description": "Unique identifier for California schools", "category": "identifier"},
        
        # Salary variables (normalized 0-1)
        "DSAL": {"description": "District Salary (Normalized)", "category": "salary"},
        "STSAL": {"description": "State Salary (Normalized)", "category": "salary"},
        "BTCHSAL": {"description": "Beginning Teacher Salary (Normalized)", "category": "salary"},
        "MTCHSAL": {"description": "Mid-career Teacher Salary (Normalized)", "category": "salary"},
        "HTCHSAL": {"description": "High-level Teacher Salary (Normalized)", "category": "salary"},
        
        # Test score variables
        "SELA_Y2": {"description": "State English Language Arts Test Score", "category": "test_score"},
        "SMATH_Y2": {"description": "State Mathematics Test Score", "category": "test_score"},
        "DELA_Y2": {"description": "District English Language Arts Test Score", "category": "test_score"},
        "DMATH_Y2": {"description": "District Mathematics Test Score", "category": "test_score"},
        
        # Socioeconomic variables
        "PERSD": {"description": "Percentage of Socioeconomically Disadvantaged Students", "category": "socioeconomic"},
        
        # Absence rate variables
        "RALL": {"description": "Chronic Absence Rate - All Students", "category": "absence"},
        "REL": {"description": "Chronic Absence Rate - English Learners", "category": "absence"},
        "RSED": {"description": "Chronic Absence Rate - Socioeconomically Disadvantaged Students", "category": "absence"}
    }
    
    # Category colors for CSS
    category_colors = {
        "identifier": "#A9BCD0",  # Light blue-gray
        "salary": "#FFD699",      # Light orange
        "test_score": "#B8E0B8",  # Light green
        "socioeconomic": "#C5C0E5", # Light purple
        "absence": "#FAB3B3"      # Light red
    }
    
    # Generate the HTML content for variable reference table
    # This creates a clear, color-coded reference guide that helps users
    # understand all variables used in the analysis
    variable_reference_html = """
        <h2>Variable Reference Guide</h2>
        <p>This reference table explains the variables used in the analysis.</p>
        
        <div class="legend">
    """
    
    # Add legend items
    for category, color in category_colors.items():
        category_name = category.capitalize()
        variable_reference_html += f"""
            <div class="legend-item">
                <div class="color-box" style="background-color: {color};"></div>
                <span>{category_name} Variables</span>
            </div>
        """
    
    variable_reference_html += """
        </div>
        
        <table class="variable-table">
            <tr>
                <th>Variable</th>
                <th>Description</th>
            </tr>
    """
    
    # Add rows for each variable, grouped by category
    for category in ["identifier", "salary", "test_score", "socioeconomic", "absence"]:
        for var_name, info in variable_definitions.items():
            if info["category"] == category:
                variable_reference_html += f"""
                <tr style="background-color: {category_colors[category]};">
                    <td><strong>{var_name}</strong></td>
                    <td>{info["description"]}</td>
                </tr>
                """
    
    variable_reference_html += """
        </table>
    """
    
    html_content = f"""
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Public School Data Analysis Report</title>
        <style>
            body {{
                font-family: 'Segoe UI', Arial, sans-serif;
                line-height: 1.6;
                color: #333;
                max-width: 1000px;
                margin: 0 auto;
                padding: 20px;
                background-color: #f9f9f9;
            }}
            .container {{
                background-color: white;
                border-radius: 8px;
                box-shadow: 0 4px 6px rgba(0,0,0,0.1);
                padding: 30px;
                margin-bottom: 30px;
            }}
            h1, h2 {{
                color: #2c3e50;
            }}
            h1 {{
                text-align: center;
                font-size: 28px;
                margin-bottom: 30px;
                border-bottom: 2px solid #3498db;
                padding-bottom: 15px;
            }}
            h2 {{
                font-size: 22px;
                margin-top: 30px;
                margin-bottom: 15px;
            }}
            .findings-container {{
                margin-top: 30px;
            }}
            .finding {{
                margin-bottom: 25px;
                padding-left: 15px;
                border-left: 4px solid #3498db;
            }}
            .finding h3 {{
                color: #2c3e50;
                font-size: 20px;
                margin-bottom: 10px;
            }}
            .finding p {{
                color: #34495e;
                font-size: 16px;
                margin-left: 5px;
            }}
            .visualization {{
                margin: 30px 0;
                text-align: center;
            }}
            .visualization img {{
                max-width: 100%;
                box-shadow: 0 2px 4px rgba(0,0,0,0.1);
                border-radius: 4px;
            }}
            .caption {{
                font-style: italic;
                color: #666;
                margin-top: 10px;
                font-size: 14px;
            }}
            .footer {{
                margin-top: 40px;
                text-align: center;
                font-style: italic;
                color: #7f8c8d;
                font-size: 14px;
                border-top: 1px solid #e0e0e0;
                padding-top: 15px;
            }}
            .year {{
                margin-top: 10px;
                text-align: center;
                color: #3498db;
                font-weight: bold;
            }}
            .date {{
                text-align: right;
                font-size: 14px;
                color: #7f8c8d;
                margin-bottom: 20px;
            }}
            .summary {{
                background-color: #f8f9fa;
                padding: 15px;
                border-left: 4px solid #3498db;
                margin: 20px 0;
            }}
            /* Variable reference styles */
            .variable-table {{
                width: 100%;
                border-collapse: collapse;
                margin: 20px 0;
            }}
            .variable-table th, .variable-table td {{
                padding: 10px;
                text-align: left;
                border-bottom: 1px solid #ddd;
            }}
            .variable-table th {{
                background-color: #f2f2f2;
                font-weight: bold;
            }}
            .legend {{
                display: flex;
                flex-wrap: wrap;
                justify-content: center;
                margin: 20px 0;
            }}
            .legend-item {{
                display: flex;
                align-items: center;
                margin: 5px 10px;
            }}
            .color-box {{
                width: 20px;
                height: 20px;
                margin-right: 5px;
                border: 1px solid #ddd;
            }}
        </style>
    </head>
    <body>
        <div class="date">Generated on: {report_date}</div>
        
        <div class="container">
            <h1>Public School Data Analysis Report</h1>
            
            <div class="summary">
                <p>This report analyzes California public school data to explore relationships between socioeconomic factors, 
                teacher salaries, absence rates, and academic performance. The findings reveal several significant correlations 
                that provide insights for educational policy and resource allocation decisions.</p>
            </div>
            
            <h2>Key Findings</h2>
            <div class="findings-container">
                <div class="finding">
                    <h3>1. Socioeconomic Status Impact</h3>
                    <p>Schools with higher percentages of socioeconomically disadvantaged students 
                    show significantly lower test scores in both Math and English Language Arts. 
                    The correlation values range from -0.76 to -0.84.</p>
                </div>
                
                <div class="finding">
                    <h3>2. Teacher Salary Relationship</h3>
                    <p>Higher teacher compensation appears to be associated with slightly better 
                    academic outcomes, though the relationship is not strong. This may suggest that while pay
                    contributes to performance, other factors—like absenteeism or socioeconomic status—have greater 
                    influence.</p>
                </div>
                
                <div class="finding">
                    <h3>3. Chronic Absence Impact</h3>
                    <p>Higher chronic absence rates strongly correlate with lower test scores. 
                    The correlation values range from -0.39 to -0.48, indicating that 
                    regular attendance is an important factor in student achievement.</p>
                </div>
                
                <div class="finding">
                    <h3>4. English Learner Absence & Disadvantage</h3>
                    <p>Chronic absence rates among English Learners are moderately correlated with both the percentage of socioeconomically 
                    disadvantaged students (r ≈ 0.29) and lower test scores (r ≈ -0.39 for ELA, r ≈ -0.41 for Math). This suggests that schools with more disadvantaged students and higher English Learner absence face compounding challenges in academic achievement.</p>
                </div>
                
                <div class="finding">
                    <h3>5. Absence Rate Patterns</h3>
                    <p>Absence rates strongly correlate across different student groups (0.76-0.95), 
                    suggesting that absence issues tend to affect entire school populations 
                    rather than being isolated to specific demographic groups.</p>
                </div>
            </div>
            
            <h2>Data Visualizations</h2>
            {f'''
            <div class="visualization">
                <img src="data:image/png;base64,{sed_math_b64}" alt="Relationship between socioeconomic status and math scores">
                <p class="caption">Figure 1: Relationship between socioeconomic status and math scores showing a strong negative correlation.</p>
            </div>
            ''' if sed_math_b64 else '<p>Socioeconomic relationship visualization not available.</p>'}
            {f'''
            <div class="visualization">
                <img src="data:image/png;base64,{correlation_b64}" alt="Correlation matrix of key variables">
                <p class="caption">Figure 2: Correlation matrix showing relationships between various factors in the dataset.</p>
            </div>
            ''' if correlation_b64 else '<p>Correlation matrix visualization not available.</p>'}
            {f'''
            <div class="visualization">
                <img src="data:image/png;base64,{test_scores_by_sed_b64}" alt="Test scores by SED bins">
                <p class="caption">Figure 3: Average test scores by percentage of socioeconomically disadvantaged students (SED bins).</p>
            </div>
            ''' if test_scores_by_sed_b64 else '<p>Test scores by SED bins visualization not available.</p>'}
            {f'''
            <div class="visualization">
                <img src="data:image/png;base64,{test_scores_relationships_b64}" alt="Test score relationships">
                <p class="caption">Figure 4: Scatter plots showing relationships between teacher salaries, absence rates, and test scores.</p>
            </div>
            ''' if test_scores_relationships_b64 else '<p>Test score relationships visualization not available.</p>'}
            
            {variable_reference_html}
            
            <div class="footer">
                These findings are derived from correlation analysis of California public school data
                including expenditures, salaries, test scores, and chronic absence information.
            </div>
            
            <div class="year">
                Data period: 2022-23
            </div>
        </div>
    </body>
    </html>
    """
    
    # Write the HTML content to a file
    output_path = Path(f"{output_dir}/school_data_report.html")
    with open(output_path, "w") as f:
        f.write(html_content)
    
    print(f"HTML report generated: {output_path.resolve()}")
    return str(output_path.resolve())

def create_html_report():
    """Generate all HTML reports"""
    try:
        # Generate main report with embedded variable reference
        html_path = generate_key_findings_html()
        print(f"Report generation complete!")
        
        # Try to open the HTML file in the default browser
        try:
            webbrowser.open('file://' + html_path)
            print(f"Report opened in browser. If not, manually open: {html_path}")
        except:
            print(f"Could not open browser automatically. Please open: {html_path}")
            
    except Exception as e:
        print(f"Error generating HTML report: {e}")

if __name__ == "__main__":
    create_html_report()
