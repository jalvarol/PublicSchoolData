"""
Variable Reference Guide for Public School Data Analysis

This module provides documentation and descriptions for all variables
used in the Public School Data Analysis project.

Usage:
    - Import this module to access variable definitions
    - Run directly to generate a visual reference guide
    - Use print_variable_descriptions() for console output
"""

import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors
from pathlib import Path
import os

# Define variable categories and their descriptions
VARIABLE_DEFINITIONS = {
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

# Define category colors for visualization
CATEGORY_COLORS = {
    "identifier": "#A9BCD0",  # Light blue-gray
    "salary": "#FFD699",      # Light orange
    "test_score": "#B8E0B8",  # Light green
    "socioeconomic": "#C5C0E5", # Light purple
    "absence": "#FAB3B3"      # Light red
}

def create_variable_reference_table():
    """Create a pandas DataFrame with variable reference information"""
    data = []
    for var_name, info in VARIABLE_DEFINITIONS.items():
        data.append({
            "Variable": var_name,
            "Description": info["description"],
            "Category": info["category"].capitalize()
        })
    return pd.DataFrame(data)

def generate_reference_guide(output_path=None):
    """
    Generate a visual reference guide for the variables
    
    This function creates a table visualization with color-coded categories
    for all variables in the dataset, making it easier to interpret results.
    
    Args:
        output_path: Optional path to save the image. If None, only displays the image.
    """
    # Create figure
    fig, ax = plt.subplots(figsize=(10, 12))
    ax.axis('tight')
    ax.axis('off')
    
    # Create DataFrame for table
    var_df = create_variable_reference_table()
    
    # Create category-based colors for rows
    category_colors = []
    for cat in var_df["Category"]:
        if cat.lower() in CATEGORY_COLORS:
            category_colors.append(CATEGORY_COLORS[cat.lower()])
        else:
            category_colors.append("#FFFFFF")  # White for unknown categories
    
    # Create table
    table = ax.table(
        cellText=var_df[["Variable", "Description"]].values,
        colLabels=["Variable", "Description"],
        loc="center",
        cellLoc="center",
        cellColours=[[c, c] for c in category_colors]
    )
    
    # Style the table
    table.auto_set_font_size(False)
    table.set_fontsize(10)
    table.scale(1, 1.5)  # Adjust row heights
    
    # Add title
    plt.suptitle("Variable Reference Guide", fontsize=16, y=0.95)
    
    # Add legend for categories
    legend_elements = []
    for cat, color in CATEGORY_COLORS.items():
        legend_elements.append(
            plt.Rectangle((0, 0), 1, 1, facecolor=color, 
                         edgecolor='gray', label=cat.capitalize())
        )
    legend = plt.legend(
        handles=legend_elements, 
        loc='upper center', 
        bbox_to_anchor=(0.5, 0.08),
        ncol=3,
        frameon=True,
        title="Variable Categories"
    )
    
    # Add footnote
    plt.figtext(0.5, 0.01, "Use this reference guide to interpret the correlation matrix and other visualizations",
               ha="center", fontsize=9, fontstyle="italic")
    
    # Save to file if path is provided
    if output_path:
        plt.savefig(output_path, bbox_inches='tight', dpi=300)
        print(f"Variable reference guide saved to: {output_path}")
    
    plt.tight_layout()
    plt.show()
    
def save_reference_guide_to_output():
    """
    Save the reference guide to the output directory
    
    Attempts to save to multiple possible output locations to handle
    different working directory configurations.
    
    Returns:
        str: Path where the file was saved, or None if saving failed
    """
    # Create output directory if it doesn't exist
    for output_dir in ["../output", "output"]:
        os.makedirs(output_dir, exist_ok=True)
        
        # Try to save to this directory
        try:
            output_path = Path(f"{output_dir}/variable_reference_guide.png")
            generate_reference_guide(output_path)
            return str(output_path)
        except Exception as e:
            print(f"Could not save to {output_dir}: {e}")
    
    return None

def print_variable_descriptions():
    """Print descriptions of all variables to the console"""
    var_df = create_variable_reference_table()
    print("\n" + "=" * 60)
    print("VARIABLE REFERENCE GUIDE".center(60))
    print("=" * 60)
    
    # Group by category
    for category in sorted(set(var_df["Category"])):
        print(f"\n{category} Variables:")
        print("-" * 60)
        category_vars = var_df[var_df["Category"] == category]
        for _, row in category_vars.iterrows():
            print(f"{row['Variable']:<10} : {row['Description']}")
    
    print("\n" + "=" * 60 + "\n")

if __name__ == "__main__":
    # Generate the reference guide
    save_reference_guide_to_output()
    
    # Also print to console
    print_variable_descriptions()
