"""
Generate explanatory report for Public School Data Analysis
This script creates additional explanatory materials to help interpret the visualizations
"""

import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import os
import seaborn as sns
from matplotlib.colors import LinearSegmentedColormap
import matplotlib.patches as mpatches
from DMProject import df_merge  # Import the merged dataframe from main script

def ensure_output_dir():
    """Create output directory if it doesn't exist"""
    os.makedirs("../output", exist_ok=True)

def generate_annotated_correlation_matrix():
    """Generate an annotated correlation matrix with key insights highlighted"""
    # Create figure
    plt.figure(figsize=(14, 12))
    
    # Create correlation matrix
    corr = df_merge.corr()
    
    # Generate mask for upper triangle
    mask = np.triu(np.ones_like(corr, dtype=bool))
    
    # Draw heatmap with annotations
    ax = sns.heatmap(corr, annot=True, fmt=".2f", cmap="coolwarm", 
                    mask=mask, vmin=-1, vmax=1, annot_kws={"size": 8})
    
    # Add title and explanation
    plt.title("Correlation Matrix with Key Insights", fontsize=16, pad=20)
    
    # Highlight key correlations with annotations
    # Test Scores and SED relationship
    plt.annotate("Strong negative correlation between\nsocioeconomic disadvantage and test scores",
                xy=(10, 7), xytext=(10, 3),
                arrowprops=dict(facecolor='black', shrink=0.05, width=1.5),
                horizontalalignment='center', fontsize=9)
    
    # Teacher salary and test scores
    plt.annotate("Modest positive correlation between\nteacher salaries and test scores",
                xy=(3, 8), xytext=(3, 4),
                arrowprops=dict(facecolor='black', shrink=0.05, width=1.5),
                horizontalalignment='center', fontsize=9)
    
    # Chronic absence and test scores
    plt.annotate("Negative correlation between\nabsence rates and test scores",
                xy=(11, 8), xytext=(11, 4),
                arrowprops=dict(facecolor='black', shrink=0.05, width=1.5),
                horizontalalignment='center', fontsize=9)
    
    plt.tight_layout()
    plt.savefig("../output/annotated_correlation_matrix.png", dpi=300)
    plt.close()

def generate_key_findings_summary():
    """Generate a visual summary of key findings"""
    plt.figure(figsize=(12, 10))
    plt.text(0.5, 0.95, "Key Findings from Public School Data Analysis", 
             horizontalalignment='center', fontsize=20, weight='bold')
    
    # Finding 1
    plt.text(0.5, 0.85, "1. Socioeconomic Status Impact", fontsize=16, weight='bold', 
             horizontalalignment='center')
    plt.text(0.5, 0.80, 
             "Schools with higher percentages of socioeconomically disadvantaged students\n"
             "show significantly lower test scores in both Math and English Language Arts.\n"
             "The correlation values range from -0.76 to -0.84.",
             horizontalalignment='center', fontsize=12)
    
    # Finding 2
    plt.text(0.5, 0.70, "2. Teacher Salary Relationship", fontsize=16, weight='bold', 
             horizontalalignment='center')
    plt.text(0.5, 0.65, 
             "Higher teacher salaries show a modest positive correlation with test scores.\n"
             "High-level teacher salaries correlate at approximately 0.18 with test scores,\n"
             "suggesting that competitive compensation may contribute to student achievement.",
             horizontalalignment='center', fontsize=12)
    
    # Finding 3
    plt.text(0.5, 0.55, "3. Chronic Absence Impact", fontsize=16, weight='bold', 
             horizontalalignment='center')
    plt.text(0.5, 0.50, 
             "Higher chronic absence rates strongly correlate with lower test scores.\n"
             "The correlation values range from -0.39 to -0.48, indicating that\n"
             "regular attendance is an important factor in student achievement.",
             horizontalalignment='center', fontsize=12)
    
    # Finding 4
    plt.text(0.5, 0.40, "4. Salary Structure Observations", fontsize=16, weight='bold', 
             horizontalalignment='center')
    plt.text(0.5, 0.35, 
             "There's a strong correlation (0.72-0.76) between beginning, mid-career, and high-level\n"
             "teacher salaries, suggesting districts with higher starting salaries\n"
             "tend to maintain competitive compensation throughout career progression.",
             horizontalalignment='center', fontsize=12)
    
    # Finding 5
    plt.text(0.5, 0.25, "5. Absence Rate Patterns", fontsize=16, weight='bold', 
             horizontalalignment='center')
    plt.text(0.5, 0.20, 
             "Absence rates strongly correlate across different student groups (0.76-0.95),\n"
             "suggesting that absence issues tend to affect entire school populations\n"
             "rather than being isolated to specific demographic groups.",
             horizontalalignment='center', fontsize=12)
    
    # Sources
    plt.text(0.5, 0.05, 
             "These findings are derived from correlation analysis of California public school data\n"
             "including expenditures, salaries, test scores, and chronic absence information.",
             horizontalalignment='center', fontsize=10, style='italic')
    
    plt.axis('off')
    plt.tight_layout()
    plt.savefig("../output/key_findings_summary.png", dpi=300)
    plt.close()

def generate_variable_explanation():
    """Generate a reference guide explaining the variables in the dataset"""
    fig, ax = plt.subplots(figsize=(12, 14))
    
    variables = [
        ("CDSCODE", "Unique identifier for California schools"),
        ("DSAL", "District Salary (Normalized)"),
        ("STSAL", "State Salary (Normalized)"),
        ("BTCHSAL", "Beginning Teacher Salary (Normalized)"),
        ("MTCHSAL", "Mid-career Teacher Salary (Normalized)"),
        ("HTCHSAL", "High-level Teacher Salary (Normalized)"),
        ("SELA_Y2", "State English Language Arts Test Score"),
        ("SMATH_Y2", "State Mathematics Test Score"),
        ("DELA_Y2", "District English Language Arts Test Score"),
        ("DMATH_Y2", "District Mathematics Test Score"),
        ("PERSD", "Percentage of Socioeconomically Disadvantaged Students"),
        ("RALL", "Chronic Absence Rate - All Students"),
        ("REL", "Chronic Absence Rate - English Learners"),
        ("RSED", "Chronic Absence Rate - Socioeconomically Disadvantaged Students")
    ]
    
    plt.title("Variable Reference Guide", fontsize=18, pad=20)
    
    # Create variable explanation table
    table_data = []
    colors = []
    for var in variables:
        table_data.append([var[0], var[1]])
        if "Salary" in var[1]:
            colors.append(["#FFD699", "#FFD699"])  # Light orange for salary
        elif "Test Score" in var[1]:
            colors.append(["#B3E6B3", "#B3E6B3"])  # Light green for test scores
        elif "Absence" in var[1]:
            colors.append(["#FFC2C2", "#FFC2C2"])  # Light red for absence
        elif "Percentage" in var[1] or "Socioeconomically" in var[1]:
            colors.append(["#C2C2FF", "#C2C2FF"])  # Light blue for SED
        else:
            colors.append(["#F5F5F5", "#F5F5F5"])  # Light gray for others
    
    table = ax.table(cellText=table_data, colLabels=["Variable", "Description"], 
                     loc="center", cellLoc="left", colWidths=[0.2, 0.7])
    
    # Apply colors to cells
    for (row, col), cell in table.get_celld().items():
        if row == 0:  # Header row
            cell.set_facecolor("#4C72B0")
            cell.set_text_props(weight='bold', color='white')
        else:
            cell.set_facecolor(colors[row-1][col])
        
        cell.set_height(0.06)
        cell.set_text_props(fontsize=12)
    
    # Add legend for variable grouping
    salary_patch = mpatches.Patch(color='#FFD699', label='Salary Variables')
    score_patch = mpatches.Patch(color='#B3E6B3', label='Test Score Variables')
    absence_patch = mpatches.Patch(color='#FFC2C2', label='Absence Rate Variables')
    sed_patch = mpatches.Patch(color='#C2C2FF', label='Socioeconomic Variables')
    
    plt.legend(handles=[salary_patch, score_patch, absence_patch, sed_patch],
               loc='upper center', bbox_to_anchor=(0.5, 0.1), ncol=2)
    
    # Remove axes
    ax.axis('off')
    
    plt.figtext(0.5, 0.05, "Use this reference guide to interpret the correlation matrix and other visualizations", 
                ha="center", fontsize=10, style='italic')
    
    plt.tight_layout()
    plt.savefig("../output/variable_reference_guide.png", dpi=300)
    plt.close()

def create_explanatory_report():
    """Generate all explanatory materials"""
    ensure_output_dir()
    print("Generating annotated correlation matrix...")
    generate_annotated_correlation_matrix()
    print("Generating key findings summary...")
    generate_key_findings_summary()
    print("Generating variable explanation guide...")
    generate_variable_explanation()
    print("Report generation complete!")
    
if __name__ == "__main__":
    create_explanatory_report()
