"""
Helper functions for creating advanced visualizations for the Public School Data project.
This module provides additional visualizations beyond those in the main script.
"""

import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import numpy as np
from matplotlib.colors import LinearSegmentedColormap
import os

def create_output_dir():
    """Create output directory if it doesn't exist"""
    os.makedirs("../output", exist_ok=True)

def plot_top_correlations(df, target_col, n=10):
    """
    Plot the top n correlations with a specific target column
    
    Parameters:
    -----------
    df : pandas DataFrame
        The dataframe containing the data
    target_col : str
        The target column to calculate correlations with
    n : int
        Number of top correlations to display
    """
    plt.figure(figsize=(12, 8))
    
    # Calculate correlations with target column
    correlations = df.corr()[target_col].sort_values(ascending=False)
    
    # Get top n correlations (excluding self-correlation)
    top_correlations = correlations[1:n+1]
    
    # Create horizontal bar chart
    ax = top_correlations.plot(kind='barh', color='skyblue')
    
    # Add values to the end of each bar
    for i, v in enumerate(top_correlations):
        ax.text(v + 0.01, i, f'{v:.2f}', va='center')
    
    plt.title(f'Top {n} Correlations with {target_col}', fontsize=16)
    plt.xlabel('Correlation Coefficient')
    plt.tight_layout()
    plt.savefig(f"../output/top_correlations_{target_col}.png", dpi=300)
    plt.show()

def plot_regression_analysis(df, x_col, y_col, color='blue'):
    """
    Create a scatter plot with regression line
    
    Parameters:
    -----------
    df : pandas DataFrame
        The dataframe containing the data
    x_col : str
        The column name for x-axis
    y_col : str
        The column name for y-axis
    color : str
        Color for the plot points
    """
    plt.figure(figsize=(10, 6))
    
    # Create scatter plot
    sns.regplot(x=df[x_col], y=df[y_col], color=color, scatter_kws={'alpha':0.5})
    
    # Add title and labels with correlation coefficient
    corr = df[[x_col, y_col]].corr().iloc[0,1]
    plt.title(f'Relationship between {x_col} and {y_col} (r = {corr:.2f})', fontsize=14)
    plt.xlabel(x_col)
    plt.ylabel(y_col)
    plt.grid(True, alpha=0.3)
    
    plt.tight_layout()
    plt.savefig(f"../output/regression_{x_col}_{y_col}.png", dpi=300)
    plt.show()

def create_dashboard(df):
    """
    Create a comprehensive dashboard of visualizations
    
    Parameters:
    -----------
    df : pandas DataFrame
        The dataframe containing the data
    """
    # Set aesthetics for all plots
    sns.set_style("whitegrid")
    plt.rcParams['font.family'] = 'sans-serif'
    plt.rcParams['font.sans-serif'] = ['Arial']
    
    # Create figure with subplots
    fig = plt.figure(figsize=(20, 16))
    fig.suptitle('Public School Data Analysis Dashboard', fontsize=24, y=0.98)
    
    # 1. Correlation heatmap - top left
    ax1 = plt.subplot2grid((3, 3), (0, 0), colspan=2, rowspan=1)
    mask = np.triu(np.ones_like(df.corr()))
    heatmap = sns.heatmap(df.corr(), mask=mask, annot=False, cmap='coolwarm', 
                         ax=ax1, cbar_kws={'shrink': .8})
    ax1.set_title('Correlation Heatmap', fontsize=16)
    
    # 2. Test score vs Salary scatter - top right
    ax2 = plt.subplot2grid((3, 3), (0, 2), colspan=1, rowspan=1)
    sns.scatterplot(x='HTCHSAL', y='SMATH_Y2', data=df, alpha=0.6, ax=ax2)
    ax2.set_title('Teacher Salary vs Math Scores', fontsize=14)
    ax2.set_xlabel('High Teacher Salary')
    ax2.set_ylabel('State Math Scores')
    
    # 3. SED vs Test Scores - middle row left
    ax3 = plt.subplot2grid((3, 3), (1, 0), colspan=1, rowspan=1)
    df.plot.scatter(x='PERSD', y='SMATH_Y2', c='RALL', 
                   cmap='viridis', alpha=0.6, ax=ax3, colorbar=False)
    ax3.set_title('SED % vs Math Scores', fontsize=14)
    ax3.set_xlabel('SED Percentage')
    ax3.set_ylabel('State Math Scores')
    
    # 4. Test Scores by Absence Rate - middle row center
    ax4 = plt.subplot2grid((3, 3), (1, 1), colspan=1, rowspan=1)
    sns.boxplot(x=pd.qcut(df['RALL'], 4, labels=['Low', 'Medium-Low', 'Medium-High', 'High']), 
               y='SMATH_Y2', data=df, ax=ax4)
    ax4.set_title('Math Scores by Absence Rate Quartiles', fontsize=14)
    ax4.set_xlabel('Chronic Absence Rate (Quartiles)')
    ax4.set_ylabel('State Math Scores')
    
    # 5. Beginning vs High Teacher Salary - middle row right
    ax5 = plt.subplot2grid((3, 3), (1, 2), colspan=1, rowspan=1)
    sns.scatterplot(x='BTCHSAL', y='HTCHSAL', data=df, 
                   hue='SMATH_Y2', palette='viridis', ax=ax5)
    ax5.set_title('Beginning vs High Teacher Salary', fontsize=14)
    ax5.set_xlabel('Beginning Teacher Salary')
    ax5.set_ylabel('High Teacher Salary')
    ax5.legend(title='Math Score', loc='upper left', bbox_to_anchor=(1, 1))
    
    # 6. Bottom row - 3 panels showing distributions
    # 6.1 SED Distribution
    ax6 = plt.subplot2grid((3, 3), (2, 0), colspan=1, rowspan=1)
    sns.histplot(df['PERSD'], kde=True, ax=ax6)
    ax6.set_title('SED % Distribution', fontsize=14)
    
    # 6.2 Test Scores Distribution
    ax7 = plt.subplot2grid((3, 3), (2, 1), colspan=1, rowspan=1)
    sns.kdeplot(df['SELA_Y2'], ax=ax7, label='ELA', fill=True, alpha=0.3)
    sns.kdeplot(df['SMATH_Y2'], ax=ax7, label='Math', fill=True, alpha=0.3)
    ax7.set_title('Test Score Distributions', fontsize=14)
    ax7.legend()
    
    # 6.3 Chronic Absence Rate Distribution
    ax8 = plt.subplot2grid((3, 3), (2, 2), colspan=1, rowspan=1)
    sns.histplot(df['RALL'], kde=True, ax=ax8, color='purple')
    ax8.set_title('Chronic Absence Rate Distribution', fontsize=14)
    
    plt.tight_layout(rect=[0, 0, 1, 0.96])
    plt.savefig("../output/school_data_dashboard.png", dpi=300)
    plt.show()

def generate_all_visualizations(df):
    """Generate all available visualizations for the dataset"""
    create_output_dir()
    
    # Generate visualizations
    plot_top_correlations(df, 'SMATH_Y2', n=8)
    plot_top_correlations(df, 'SELA_Y2', n=8)
    
    plot_regression_analysis(df, 'HTCHSAL', 'SMATH_Y2', 'blue')
    plot_regression_analysis(df, 'PERSD', 'SMATH_Y2', 'red')
    plot_regression_analysis(df, 'RALL', 'SMATH_Y2', 'green')
    
    create_dashboard(df)
    
    print("All visualizations generated successfully!")
    print("Visualizations saved to the '../output' directory")
