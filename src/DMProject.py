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

# Create output directory at the beginning to avoid FileNotFoundError
os.makedirs("../output", exist_ok=True)

# Load and prepare data using the data_preparation module
print("Loading and preparing data...")
df_merge = load_data()

if df_merge is None:
    print("Error loading data. Please check the logs for details.")
    exit(1)

# Print data types to verify they're all numeric
print("Verifying data types after processing:")
print(df_merge.dtypes)

# Adding a main guard to make the script directly executable
if __name__ == "__main__":
    print("Running Public School Data Analysis...")
    
    # Set a more professional style for plots
    plt.style.use('seaborn-v0_8-whitegrid')
    
    # 1. Enhanced Correlation Matrix - Fix the tight_layout warning with proper figure setup
    fig, ax = plt.subplots(figsize=(12, 10))
    corr = df_merge.corr()
    
    # Use ax.matshow instead of plt.matshow to avoid tight_layout warning
    heatmap = ax.matshow(corr, cmap=plt.cm.coolwarm)
    ax.set_title("Correlation Matrix of School Data Variables", fontsize=16, pad=20)
    plt.colorbar(heatmap, ax=ax)
    
    # Improve readability of labels
    labels = corr.columns
    ax.set_xticks(range(len(labels)))
    ax.set_yticks(range(len(labels)))
    ax.set_xticklabels(labels, rotation=90, fontsize=8)
    ax.set_yticklabels(labels, fontsize=8)
    
    # Add correlation values
    for i in range(len(corr.columns)):
        for j in range(len(corr.columns)):
            ax.text(i, j, f"{corr.iloc[i, j]:.2f}", 
                   ha="center", va="center", 
                   color="white" if abs(corr.iloc[i, j]) > 0.5 else "black",
                   fontsize=7)
    
    plt.tight_layout()
    plt.savefig("../output/correlation_matrix.png", dpi=300)
    plt.close()  # Close the figure to free memory
    
    # 2. Create a pair plot to visualize relationships between test scores and key factors
    # Fix the scatter plots - better axis formatting and jitter to reveal density
    fig, axs = plt.subplots(2, 2, figsize=(20, 15))
    
    # Test scores vs Teacher salaries with improved readability
    axs[0,0].scatter(df_merge['HTCHSAL'], df_merge['SMATH_Y2'], alpha=0.4, c='blue', s=15)
    axs[0,0].set_title('High Teacher Salary vs. State Math Scores', fontsize=16)
    axs[0,0].set_xlabel('High Teacher Salary (Normalized)', fontsize=12)
    axs[0,0].set_ylabel('State Math Scores', fontsize=12)
    axs[0,0].grid(True, alpha=0.3)
    axs[0,0].tick_params(axis='both', which='major', labelsize=10)
    
    # Add a trend line
    z = np.polyfit(df_merge['HTCHSAL'], df_merge['SMATH_Y2'], 1)
    p = np.poly1d(z)
    axs[0,0].plot(np.linspace(0, 1, 100), p(np.linspace(0, 1, 100)), 
                 "r-", linewidth=2, label=f'Trend (r={df_merge["HTCHSAL"].corr(df_merge["SMATH_Y2"]):.2f})')
    axs[0,0].legend(fontsize=10)
    
    axs[0,1].scatter(df_merge['HTCHSAL'], df_merge['SELA_Y2'], alpha=0.4, c='green', s=15)
    axs[0,1].set_title('High Teacher Salary vs. State ELA Scores', fontsize=16)
    axs[0,1].set_xlabel('High Teacher Salary (Normalized)', fontsize=12)
    axs[0,1].set_ylabel('State ELA Scores', fontsize=12)
    axs[0,1].grid(True, alpha=0.3)
    axs[0,1].tick_params(axis='both', which='major', labelsize=10)
    
    # Add a trend line
    z = np.polyfit(df_merge['HTCHSAL'], df_merge['SELA_Y2'], 1)
    p = np.poly1d(z)
    axs[0,1].plot(np.linspace(0, 1, 100), p(np.linspace(0, 1, 100)), 
                 "r-", linewidth=2, label=f'Trend (r={df_merge["HTCHSAL"].corr(df_merge["SELA_Y2"]):.2f})')
    axs[0,1].legend(fontsize=10)
    
    # Test scores vs Chronic Absence Rate with improved formatting
    axs[1,0].scatter(df_merge['RALL'], df_merge['SMATH_Y2'], alpha=0.4, c='red', s=15)
    axs[1,0].set_title('Chronic Absence Rate vs. State Math Scores', fontsize=16)
    axs[1,0].set_xlabel('Chronic Absence Rate (All Students %)', fontsize=12)
    axs[1,0].set_ylabel('State Math Scores', fontsize=12)
    axs[1,0].grid(True, alpha=0.3)
    axs[1,0].tick_params(axis='both', which='major', labelsize=10)
    
    # Add a trend line
    z = np.polyfit(df_merge['RALL'], df_merge['SMATH_Y2'], 1)
    p = np.poly1d(z)
    axs[1,0].plot(np.linspace(0, 100, 100), p(np.linspace(0, 100, 100)), 
                "r-", linewidth=2, label=f'Trend (r={df_merge["RALL"].corr(df_merge["SMATH_Y2"]):.2f})')
    axs[1,0].legend(fontsize=10)
    
    axs[1,1].scatter(df_merge['RALL'], df_merge['SELA_Y2'], alpha=0.4, c='purple', s=15)
    axs[1,1].set_title('Chronic Absence Rate vs. State ELA Scores', fontsize=16)
    axs[1,1].set_xlabel('Chronic Absence Rate (All Students %)', fontsize=12)
    axs[1,1].set_ylabel('State ELA Scores', fontsize=12)
    axs[1,1].grid(True, alpha=0.3)
    axs[1,1].tick_params(axis='both', which='major', labelsize=10)
    
    # Add a trend line
    z = np.polyfit(df_merge['RALL'], df_merge['SELA_Y2'], 1)
    p = np.poly1d(z)
    axs[1,1].plot(np.linspace(0, 100, 100), p(np.linspace(0, 100, 100)), 
                "r-", linewidth=2, label=f'Trend (r={df_merge["RALL"].corr(df_merge["SELA_Y2"]):.2f})')
    axs[1,1].legend(fontsize=10)
    
    plt.tight_layout()
    plt.savefig("../output/test_scores_relationships.png", dpi=300)
    plt.close()  # Close the figure
    
    # 3. Bar charts for comparing average test scores by socioeconomic factors - Fix empty bars
    plt.figure(figsize=(14, 10))
    
    # Fix the PERSD values - ensure they're in 0-1 range for proper categorization
    # Check if PERSD is already in percentage form (>1) and convert if needed
    if df_merge['PERSD'].max() > 1:
        print("PERSD appears to be in percentage form (>1), converting to 0-1 scale for categorization")
        df_merge['PERSD_normalized'] = df_merge['PERSD'] / 100
    else:
        df_merge['PERSD_normalized'] = df_merge['PERSD']
    
    # Create SED categories using the normalized values
    df_merge['SED_Category'] = pd.cut(df_merge['PERSD_normalized'], 
                                      bins=[0, 0.25, 0.5, 0.75, 1.0], 
                                      labels=['0-25%', '25-50%', '50-75%', '75-100%'],
                                      include_lowest=True)
    
    # Verify we have data in each category
    sed_counts = df_merge['SED_Category'].value_counts()
    print("SED Category counts:")
    print(sed_counts)
    
    # Group by SED category and calculate mean test scores
    sed_groups = df_merge.groupby('SED_Category', observed=True)[['SELA_Y2', 'SMATH_Y2', 'DELA_Y2', 'DMATH_Y2']].mean()
    print("Mean scores by SED category:")
    print(sed_groups)
    
    # Create clearer bar charts with values
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(14, 12))
    
    # State scores
    state_bars = sed_groups[['SELA_Y2', 'SMATH_Y2']].plot(kind='bar', ax=ax1, rot=0, colormap='viridis')
    ax1.set_title('State Test Scores by Socioeconomically Disadvantaged Student Percentage', fontsize=16)
    ax1.set_xlabel('Percentage of Socioeconomically Disadvantaged Students', fontsize=12)
    ax1.set_ylabel('Average Test Score', fontsize=12)
    ax1.grid(True, axis='y', alpha=0.3)
    ax1.legend(['ELA Scores', 'Math Scores'], fontsize=10)
    ax1.tick_params(axis='both', which='major', labelsize=10)
    
    # Add value labels
    for container in ax1.containers:
        ax1.bar_label(container, fmt='%.1f', fontsize=9)
    
    # District scores
    district_bars = sed_groups[['DELA_Y2', 'DMATH_Y2']].plot(kind='bar', ax=ax2, rot=0, colormap='viridis')
    ax2.set_title('District Test Scores by Socioeconomically Disadvantaged Student Percentage', fontsize=16)
    ax2.set_xlabel('Percentage of Socioeconomically Disadvantaged Students', fontsize=12)
    ax2.set_ylabel('Average Test Score', fontsize=12)
    ax2.grid(True, axis='y', alpha=0.3)
    ax2.legend(['ELA Scores', 'Math Scores'], fontsize=10)
    ax2.tick_params(axis='both', which='major', labelsize=10)
    
    # Add value labels
    for container in ax2.containers:
        ax2.bar_label(container, fmt='%.1f', fontsize=9)
    
    plt.tight_layout()
    plt.savefig("../output/test_scores_by_sed.png", dpi=300)
    plt.close()
    
    # 4. Distribution of key variables - Fix the histogram visualizations
    fig, axs = plt.subplots(2, 3, figsize=(16, 12))
    
    # Teacher salary distribution - improved formatting
    axs[0,0].hist(df_merge['BTCHSAL'], bins=20, alpha=0.7, color='#1f77b4')
    axs[0,0].set_title('Beginning Teacher Salary Distribution', fontsize=12)
    axs[0,0].set_xlabel('Normalized Salary', fontsize=10)
    axs[0,0].set_ylabel('Number of Schools', fontsize=10)
    axs[0,0].grid(True, alpha=0.3)
    axs[0,0].tick_params(axis='both', which='major', labelsize=9)
    
    axs[0,1].hist(df_merge['MTCHSAL'], bins=20, alpha=0.7, color='green')
    axs[0,1].set_title('Mid-Career Teacher Salary Distribution', fontsize=12)
    axs[0,1].set_xlabel('Normalized Salary', fontsize=10)
    axs[0,1].set_ylabel('Number of Schools', fontsize=10)
    axs[0,1].grid(True, alpha=0.3)
    axs[0,1].tick_params(axis='both', which='major', labelsize=9)
    
    axs[0,2].hist(df_merge['HTCHSAL'], bins=20, alpha=0.7, color='red')
    axs[0,2].set_title('High-Level Teacher Salary Distribution', fontsize=12)
    axs[0,2].set_xlabel('Normalized Salary', fontsize=10)
    axs[0,2].set_ylabel('Number of Schools', fontsize=10)
    axs[0,2].grid(True, alpha=0.3)
    axs[0,2].tick_params(axis='both', which='major', labelsize=9)
    
    # Test score distributions
    axs[1,0].hist(df_merge['SMATH_Y2'].astype(float), bins=20, alpha=0.7, color='purple')
    axs[1,0].set_title('State Math Score Distribution', fontsize=12)
    axs[1,0].set_xlabel('Score', fontsize=10)
    axs[1,0].set_ylabel('Number of Schools', fontsize=10)
    axs[1,0].grid(True, alpha=0.3)
    axs[1,0].tick_params(axis='both', which='major', labelsize=9)
    
    axs[1,1].hist(df_merge['SELA_Y2'].astype(float), bins=20, alpha=0.7, color='orange')
    axs[1,1].set_title('State ELA Score Distribution', fontsize=12)
    axs[1,1].set_xlabel('Score', fontsize=10)
    axs[1,1].set_ylabel('Number of Schools', fontsize=10)
    axs[1,1].grid(True, alpha=0.3)
    axs[1,1].tick_params(axis='both', which='major', labelsize=9)
    
    # Fix the SED distribution visualization
    axs[1,2].hist(df_merge['PERSD'].astype(float) * 100, bins=20, alpha=0.7, color='blue')
    axs[1,2].set_title('Distribution of Socioeconomically Disadvantaged %', fontsize=12)
    axs[1,2].set_xlabel('Percentage of Students', fontsize=10)
    axs[1,2].set_ylabel('Number of Schools', fontsize=10)
    axs[1,2].grid(True, alpha=0.3)
    axs[1,2].tick_params(axis='both', which='major', labelsize=9)
    
    plt.tight_layout()
    plt.savefig("../output/variable_distributions.png", dpi=300)
    plt.close()
    
    # 5. Create a more clear relationship visualization between SED and test scores
    plt.figure(figsize=(10, 8))
    
    # Test the data directly before any transformations
    print("\n===== DATA VERIFICATION FOR SED vs MATH SCORES =====")
    print(f"Number of rows in dataframe: {len(df_merge)}")
    
    # Check for any issues in the data
    print("\nData type of PERSD:", df_merge['PERSD'].dtype)
    print("Data type of SMATH_Y2:", df_merge['SMATH_Y2'].dtype)
    print(f"PERSD min: {df_merge['PERSD'].min()}, max: {df_merge['PERSD'].max()}")
    
    # Create a clean subset of only the needed data
    plot_df = df_merge[['PERSD', 'SMATH_Y2']].copy()
    
    # Fix PERSD scaling if needed - ensure it's in 0-100 percentage form for plotting
    # The PERSD (Percentage of Socioeconomically Disadvantaged) column may be in different formats
    # This code standardizes it to ensure consistent visualization and analysis
    if plot_df['PERSD'].max() > 100:
        print("WARNING: PERSD values appear to exceed 100% - scaling down")
        plot_df['PERSD_PCT'] = plot_df['PERSD'].clip(upper=100)  # Cap at 100%
    elif plot_df['PERSD'].max() <= 1:
        print("WARNING: PERSD values appear to be in 0-1 scale - converting to percentage")
        plot_df['PERSD_PCT'] = plot_df['PERSD'] * 100
    else:
        # Already in percentage form (1-100)
        plot_df['PERSD_PCT'] = plot_df['PERSD']
    
    # Remove any rows with NaN values
    print(f"\nRows before NaN removal: {len(plot_df)}")
    plot_df = plot_df.dropna()
    print(f"Rows after NaN removal: {len(plot_df)}")
    
    # Check if we still have data after filtering
    if len(plot_df) == 0:
        print("ERROR: No valid data points after filtering!")
        plt.text(50, 50, "NO VALID DATA AVAILABLE", 
                 ha='center', va='center', fontsize=20, color='red')
        plt.title('No Data Available for Visualization', fontsize=16)
    else:
        # Print data range to understand the scales
        print(f"\nPERSD range: {plot_df['PERSD_PCT'].min():.2f}% to {plot_df['PERSD_PCT'].max():.2f}%")
        print(f"SMATH_Y2 range: {plot_df['SMATH_Y2'].min():.2f} to {plot_df['SMATH_Y2'].max():.2f}")
        
        # Generate the plot with clearer visualization
        # Use dark edge colors to make points more visible and increase size
        plt.scatter(plot_df['PERSD_PCT'], plot_df['SMATH_Y2'], 
                  s=80,                 # Larger markers
                  alpha=0.6,            # Semi-transparent
                  color='blue',         # Blue fill
                  edgecolor='black',    # Black border
                  linewidth=1,          # Border width
                  label='Schools')      # Label for legend
        
        # Calculate and add regression line
        z = np.polyfit(plot_df['PERSD_PCT'], plot_df['SMATH_Y2'], 1)
        p = np.poly1d(z)
        x_range = np.linspace(plot_df['PERSD_PCT'].min(), plot_df['PERSD_PCT'].max(), 100)
        
        plt.plot(x_range, p(x_range), 'r-', linewidth=2,
                label=f'Trend Line (y={z[0]:.3f}x+{z[1]:.1f})')
        
        # Calculate correlation
        corr = plot_df['PERSD_PCT'].corr(plot_df['SMATH_Y2'])
        print(f"\nCorrelation coefficient: {corr:.4f}")
        
        # Add correlation text
        plt.annotate(f"Correlation: {corr:.2f}",
                    xy=(0.05, 0.95), 
                    xycoords='axes fraction',
                    bbox=dict(boxstyle="round,pad=0.3", fc="white", alpha=0.8),
                    fontsize=12)
        
        plt.title('Relationship Between Socioeconomic Status and Math Scores', fontsize=16)
        plt.xlabel('Percentage of Socioeconomically Disadvantaged Students', fontsize=12)
        plt.ylabel('State Math Scores', fontsize=12)
        plt.grid(True, alpha=0.3)
        plt.legend(fontsize=10)
    
    # Set proper x-axis limits
    plt.xlim(0, 100)
    
    plt.tight_layout()
    plt.savefig("../output/sed_mathscores_relationship.png", dpi=300)
    plt.close()

    print("All visualizations have been saved to the output directory.")
    
plt.ioff()  # Turn off interactive mode at the end

