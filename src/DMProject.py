#CSCI 185 - Web and Data Mining

#Use Agg backend which doesn't require a GUI
import matplotlib
matplotlib.use('Agg')  # Set this before importing pyplot
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import os

# Import the data preparation module
from data_preparation import load_data

# Load and prepare data using the data_preparation module
print("Loading and preparing data...")
df_merge = load_data()

if df_merge is None:
    print("Error loading data. Please check the logs for details.")
    exit(1)

# Print data types to verify they're all numeric
print("Verifying data types after processing:")
print(df_merge.dtypes)

# Utility function to normalize PERSD column to 0-1 scale
def normalize_persd(df):
    """Normalize the PERSD column to a 0-1 scale for consistent categorization."""
    if df['PERSD'].max() > 1:
        return df['PERSD'] / 100
    return df['PERSD']

def plot_correlation_matrix(df, output_path):
    """Plot and save the correlation matrix heatmap."""
    # Compute the correlation matrix for all numeric columns
    fig, ax = plt.subplots(figsize=(12, 10))
    corr = df.corr()
    # Display the correlation matrix as a heatmap
    heatmap = ax.matshow(corr, cmap=plt.cm.coolwarm)
    ax.set_title("Correlation Matrix of School Data Variables", fontsize=16, pad=20)
    plt.colorbar(heatmap, ax=ax)
    labels = corr.columns
    # Set axis ticks and labels for all variables
    ax.set_xticks(range(len(labels)))
    ax.set_yticks(range(len(labels)))
    ax.set_xticklabels(labels, rotation=90, fontsize=8)
    ax.set_yticklabels(labels, fontsize=8)
    # Annotate each cell with the correlation value
    for i in range(len(corr.columns)):
        for j in range(len(corr.columns)):
            ax.text(i, j, f"{corr.iloc[i, j]:.2f}", ha="center", va="center", color="white" if abs(corr.iloc[i, j]) > 0.5 else "black", fontsize=7)
    plt.tight_layout()
    # Save the heatmap to the specified output path
    plt.savefig(output_path, dpi=300)
    plt.close()

def plot_test_score_relationships(df, output_path):
    """Create a 2x2 grid of scatter plots for test scores vs. key factors."""
    fig, axs = plt.subplots(2, 2, figsize=(20, 15))
    # --- Top left: High Teacher Salary vs State Math Scores ---
    axs[0,0].scatter(df['HTCHSAL'], df['SMATH_Y2'], alpha=0.4, c='blue', s=15)
    axs[0,0].set_title('High Teacher Salary vs. State Math Scores', fontsize=16)
    axs[0,0].set_xlabel('High Teacher Salary (Normalized)', fontsize=12)
    axs[0,0].set_ylabel('State Math Scores', fontsize=12)
    axs[0,0].grid(True, alpha=0.3)
    axs[0,0].tick_params(axis='both', which='major', labelsize=10)
    axs[0,0].set_ylim(0, 100)
    # Fit and plot a linear trend line
    z = np.polyfit(df['HTCHSAL'], df['SMATH_Y2'], 1)
    p = np.poly1d(z)
    axs[0,0].plot(np.linspace(0, 1, 100), p(np.linspace(0, 1, 100)), "r-", linewidth=2, label=f'Trend (r={df["HTCHSAL"].corr(df["SMATH_Y2"]):.2f})')
    axs[0,0].legend(fontsize=10)
    # --- Top right: High Teacher Salary vs State ELA Scores ---
    axs[0,1].scatter(df['HTCHSAL'], df['SELA_Y2'], alpha=0.4, c='green', s=15)
    axs[0,1].set_title('High Teacher Salary vs. State ELA Scores', fontsize=16)
    axs[0,1].set_xlabel('High Teacher Salary (Normalized)', fontsize=12)
    axs[0,1].set_ylabel('State ELA Scores', fontsize=12)
    axs[0,1].grid(True, alpha=0.3)
    axs[0,1].tick_params(axis='both', which='major', labelsize=10)
    axs[0,1].set_ylim(0, 100)
    # Fit and plot a linear trend line
    z = np.polyfit(df['HTCHSAL'], df['SELA_Y2'], 1)
    p = np.poly1d(z)
    axs[0,1].plot(np.linspace(0, 1, 100), p(np.linspace(0, 1, 100)), "r-", linewidth=2, label=f'Trend (r={df["HTCHSAL"].corr(df["SELA_Y2"]):.2f})')
    axs[0,1].legend(fontsize=10)
    # --- Bottom left: Chronic Absence Rate vs State Math Scores ---
    axs[1,0].scatter(df['RALL'], df['SMATH_Y2'], alpha=0.4, c='red', s=15)
    axs[1,0].set_title('Chronic Absence Rate vs. State Math Scores', fontsize=16)
    axs[1,0].set_xlabel('Chronic Absence Rate (All Students %)', fontsize=12)
    axs[1,0].set_ylabel('State Math Scores', fontsize=12)
    axs[1,0].grid(True, alpha=0.3)
    axs[1,0].tick_params(axis='both', which='major', labelsize=10)
    axs[1,0].set_ylim(0, 100)
    # Fit and plot a linear trend line
    z = np.polyfit(df['RALL'], df['SMATH_Y2'], 1)
    p = np.poly1d(z)
    axs[1,0].plot(np.linspace(0, 100, 100), p(np.linspace(0, 100, 100)), "r-", linewidth=2, label=f'Trend (r={df["RALL"].corr(df["SMATH_Y2"]):.2f})')
    axs[1,0].legend(fontsize=10)
    # --- Bottom right: Chronic Absence Rate vs State ELA Scores ---
    axs[1,1].scatter(df['RALL'], df['SELA_Y2'], alpha=0.4, c='purple', s=15)
    axs[1,1].set_title('Chronic Absence Rate vs. State ELA Scores', fontsize=16)
    axs[1,1].set_xlabel('Chronic Absence Rate (All Students %)', fontsize=12)
    axs[1,1].set_ylabel('State ELA Scores', fontsize=12)
    axs[1,1].grid(True, alpha=0.3)
    axs[1,1].tick_params(axis='both', which='major', labelsize=10)
    axs[1,1].set_ylim(0, 100)
    # Fit and plot a linear trend line
    z = np.polyfit(df['RALL'], df['SELA_Y2'], 1)
    p = np.poly1d(z)
    axs[1,1].plot(np.linspace(0, 100, 100), p(np.linspace(0, 100, 100)), "r-", linewidth=2, label=f'Trend (r={df["RALL"].corr(df["SELA_Y2"]):.2f})')
    axs[1,1].legend(fontsize=10)
    plt.tight_layout()
    # Save the 2x2 grid of plots
    plt.savefig(output_path, dpi=300)
    plt.close()

def plot_scores_by_sed(df, output_path):
    """Plot bar charts for average test scores by SED category."""
    # Normalize PERSD for consistent binning (0-1 scale)
    df['PERSD_normalized'] = normalize_persd(df)
    # Bin SED into 4 categories: 0-25%, 25-50%, 50-75%, 75-100%
    df['SED_Category'] = pd.cut(df['PERSD_normalized'], bins=[0, 0.25, 0.5, 0.75, 1.0], labels=['0-25%', '25-50%', '50-75%', '75-100%'], include_lowest=True)
    # Group by SED category and compute mean test scores
    sed_groups = df.groupby('SED_Category', observed=True)[['SELA_Y2', 'SMATH_Y2', 'DELA_Y2', 'DMATH_Y2']].mean()
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(14, 12))
    # Plot state test scores by SED category
    sed_groups[['SELA_Y2', 'SMATH_Y2']].plot(kind='bar', ax=ax1, rot=0, colormap='viridis')
    ax1.set_title("State Test Scores by Socioeconomically Disadvantaged Student Percentage", fontsize=16, fontweight='bold')
    ax1.set_xlabel('Percentage of Socioeconomically Disadvantaged Students', fontsize=12)
    ax1.set_ylabel('Average Test Score', fontsize=12)
    ax1.grid(True, axis='y', alpha=0.3)
    ax1.legend(['ELA Scores', 'Math Scores'], fontsize=10)
    ax1.tick_params(axis='both', which='major', labelsize=10)
    # Annotate bars with values
    for container in ax1.containers:
        ax1.bar_label(container, fmt='%.1f', fontsize=9)
    # Plot district test scores by SED category
    sed_groups[['DELA_Y2', 'DMATH_Y2']].plot(kind='bar', ax=ax2, rot=0, colormap='viridis')
    ax2.set_title("District Test Scores by Socioeconomically Disadvantaged Student Percentage", fontsize=16, fontweight='bold')
    ax2.set_xlabel('Percentage of Socioeconomically Disadvantaged Students', fontsize=12)
    ax2.set_ylabel('Average Test Score', fontsize=12)
    ax2.grid(True, axis='y', alpha=0.3)
    ax2.legend(['ELA Scores', 'Math Scores'], fontsize=10)
    ax2.tick_params(axis='both', which='major', labelsize=10)
    # Annotate bars with values
    for container in ax2.containers:
        ax2.bar_label(container, fmt='%.1f', fontsize=9)
    plt.tight_layout()
    # Save the bar charts
    plt.savefig(output_path, dpi=300)
    plt.close()

def plot_sed_vs_math(df, output_path):
    """Plot relationship between SED percentage and math scores."""
    # Prepare a DataFrame with SED and Math Score columns
    plot_df = df[['PERSD', 'SMATH_Y2']].copy()
    # Normalize SED to percent scale for plotting
    if plot_df['PERSD'].max() > 100:
        plot_df['PERSD_PCT'] = plot_df['PERSD'].clip(upper=100)
    elif plot_df['PERSD'].max() <= 1:
        plot_df['PERSD_PCT'] = plot_df['PERSD'] * 100
    else:
        plot_df['PERSD_PCT'] = plot_df['PERSD']
    plot_df = plot_df.dropna()
    plt.figure(figsize=(10, 8))
    if len(plot_df) == 0:
        # If no data, display a message on the plot
        plt.text(50, 50, "NO VALID DATA AVAILABLE", ha='center', va='center', fontsize=20, color='red')
        plt.title('No Data Available for Visualization', fontsize=16)
    else:
        # Scatter plot of SED % vs Math Scores
        plt.scatter(plot_df['PERSD_PCT'], plot_df['SMATH_Y2'], s=80, alpha=0.6, color='blue', edgecolor='black', linewidth=1, label='Schools')
        # Fit and plot a linear trend line
        z = np.polyfit(plot_df['PERSD_PCT'], plot_df['SMATH_Y2'], 1)
        p = np.poly1d(z)
        x_range = np.linspace(plot_df['PERSD_PCT'].min(), plot_df['PERSD_PCT'].max(), 100)
        plt.plot(x_range, p(x_range), 'r-', linewidth=2, label=f'Trend Line (y={z[0]:.3f}x+{z[1]:.1f})')
        # Annotate with correlation coefficient
        corr = plot_df['PERSD_PCT'].corr(plot_df['SMATH_Y2'])
        plt.annotate(f"Correlation: {corr:.2f}", xy=(0.05, 0.95), xycoords='axes fraction', bbox=dict(boxstyle="round,pad=0.3", fc="white", alpha=0.8), fontsize=12)
        plt.title('Relationship Between Socioeconomic Status and Math Scores', fontsize=16)
        plt.xlabel('Percentage of Socioeconomically Disadvantaged Students', fontsize=12)
        plt.ylabel('State Math Scores', fontsize=12)
        plt.grid(True, alpha=0.3)
        plt.legend(fontsize=10)
    plt.xlim(0, 100)
    plt.tight_layout()
    # Save the scatter plot
    plt.savefig(output_path, dpi=300)
    plt.close()

# Adding a main guard to make the script directly executable
if __name__ == "__main__":
    # Main script entry point
    print("Running Public School Data Analysis...")
    plt.style.use('seaborn-v0_8-whitegrid')
    # Generate and save all visualizations
    plot_correlation_matrix(df_merge, "output/correlation_matrix.png")
    plot_test_score_relationships(df_merge, "output/test_scores_relationships.png")
    plot_scores_by_sed(df_merge, "output/test_scores_by_sed.png")
    plot_sed_vs_math(df_merge, "output/sed_mathscores_relationship.png")
    print("All visualizations have been saved to the output directory.")
    plt.ioff()  # Turn off interactive mode at the end

