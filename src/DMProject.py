#CSCI 185 - Web and Data Mining

from sklearn.preprocessing import MinMaxScaler
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import os

#Reading in Data
try: os.chdir('data')    
except:
    pass

#These files have footers
df_Expend = pd.read_csv('../data/Expenditure_Data.txt', skipfooter = 5, engine = 'python')
df_Salary = pd.read_csv('../data/Salary_Data.txt', skipfooter = 5, engine = 'python')
df_CA = pd.read_csv('../data/Chronic_Absent.txt', sep = '|')

#Does not contain footers
df_Test_Scores = pd.read_csv('../data/Test_Score_Results.txt', sep = '\t')


#Updating Columns to be the same format
df_Salary.columns = df_Salary.columns.str.upper()
df_Expend.columns = df_Expend.columns.str.upper()
df_Test_Scores.columns = df_Test_Scores.columns.str.upper()
df_CA.columns = df_CA.columns.str.upper()

#Pre-Processing

#Data Reduction
#3 Values STEXP, DSAL, STSAL
df_Expend.drop(['SARCYEAR','C', 'D', 'S', 'STEXP'], axis = 1,inplace=True)

#3 Values BTCHSAL, MTCHSAL, HTCHSAL
df_Salary = df_Salary[['CDSCODE', 'BTCHSAL', 'MTCHSAL','HTCHSAL']]

#4 Values SELA_Y2, SMATH_Y2, DELA_Y2, DMATH_Y2
df_Test_Scores = df_Test_Scores[['CDSCODE','SELA_Y2', 'SMATH_Y2','DELA_Y2','DMATH_Y2']]

#1 Value PERSD
df_SED = pd.read_csv('../data/Subgroup_Data.txt', usecols = ['CDSCODE', 'PERSD'])

# Values RALL, REL,RSED
df_CA = df_CA[['CDSCODE', 'RALL', 'REL', 'RSED', ]]

#Since we are looking for correlations for test scores we use NaN for missing test score
#values. When we merge, we will remove any row that has NaN values
df_Test_Scores.replace(['--','0'], np.nan, inplace=True)

#Filling in NaN values since there is a possibility there are test scores but 0 SED #students
df_SED.replace([np.nan], 0, inplace=True)

#Filling NaN values with Means
df_Expend.fillna(df_Expend.mean(numeric_only = True),inplace=True)
df_Salary.fillna(df_Salary.mean(numeric_only = True),inplace=True)

#List of all Data Frames
#Keep adding data frames to here after reduction
data_frames = [df_Expend, df_Salary, df_Test_Scores, df_SED, df_CA]

#Merging all DataFrames
df_merge = df_Expend.merge(df_Salary).merge(df_Test_Scores).merge(df_SED).merge(df_CA)

#Removing NaN values
df_merge.dropna(inplace=True)

#Normalizing attributes with values in the thousands
scaler = MinMaxScaler()

#Insert Attributes to Normalize
columns_to_normalize = ['DSAL', 'STSAL', 'BTCHSAL', 'MTCHSAL', 'HTCHSAL']

#Normalize
df_merge[columns_to_normalize] = scaler.fit_transform(df_merge[columns_to_normalize])

# Adding a main guard to make the script directly executable
if __name__ == "__main__":
    print("Running Public School Data Analysis...")
    
    # Create output directory at the beginning to avoid FileNotFoundError
    import os
    os.makedirs("../output", exist_ok=True)
    
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
    plt.show()
    
    # 2. Create a pair plot to visualize relationships between test scores and key factors
    plt.figure(figsize=(20, 15))
    
    # Test scores vs Teacher salaries
    plt.subplot(2, 2, 1)
    plt.scatter(df_merge['HTCHSAL'], df_merge['SMATH_Y2'], alpha=0.5, c='blue')
    plt.title('High Teacher Salary vs. State Math Scores', fontsize=14)
    plt.xlabel('High Teacher Salary (Normalized)')
    plt.ylabel('State Math Scores')
    plt.grid(True, alpha=0.3)
    
    plt.subplot(2, 2, 2)
    plt.scatter(df_merge['HTCHSAL'], df_merge['SELA_Y2'], alpha=0.5, c='green')
    plt.title('High Teacher Salary vs. State ELA Scores', fontsize=14)
    plt.xlabel('High Teacher Salary (Normalized)')
    plt.ylabel('State ELA Scores')
    plt.grid(True, alpha=0.3)
    
    # Test scores vs Chronic Absence Rate
    plt.subplot(2, 2, 3)
    plt.scatter(df_merge['RALL'], df_merge['SMATH_Y2'], alpha=0.5, c='red')
    plt.title('Chronic Absence Rate vs. State Math Scores', fontsize=14)
    plt.xlabel('Chronic Absence Rate (All Students)')
    plt.ylabel('State Math Scores')
    plt.grid(True, alpha=0.3)
    
    plt.subplot(2, 2, 4)
    plt.scatter(df_merge['RALL'], df_merge['SELA_Y2'], alpha=0.5, c='purple')
    plt.title('Chronic Absence Rate vs. State ELA Scores', fontsize=14)
    plt.xlabel('Chronic Absence Rate (All Students)')
    plt.ylabel('State ELA Scores')
    plt.grid(True, alpha=0.3)
    
    plt.tight_layout()
    plt.savefig("../output/test_scores_relationships.png", dpi=300)
    plt.show()
    
    # 3. Bar charts for comparing average test scores by socioeconomic factors
    plt.figure(figsize=(14, 10))
    
    # Create SED categories for grouping
    df_merge['SED_Category'] = pd.cut(df_merge['PERSD'], 
                                      bins=[0, 0.25, 0.5, 0.75, 1.0], 
                                      labels=['0-25%', '25-50%', '50-75%', '75-100%'])
    
    # Group by SED category and calculate mean test scores
    sed_groups = df_merge.groupby('SED_Category')[['SELA_Y2', 'SMATH_Y2', 'DELA_Y2', 'DMATH_Y2']].mean()
    
    plt.subplot(2, 1, 1)
    sed_groups[['SELA_Y2', 'SMATH_Y2']].plot(kind='bar', ax=plt.gca())
    plt.title('State Test Scores by Socioeconomically Disadvantaged Student Percentage', fontsize=14)
    plt.xlabel('Percentage of Socioeconomically Disadvantaged Students')
    plt.ylabel('Average Test Score')
    plt.grid(True, axis='y', alpha=0.3)
    plt.legend(['ELA Scores', 'Math Scores'])
    
    plt.subplot(2, 1, 2)
    sed_groups[['DELA_Y2', 'DMATH_Y2']].plot(kind='bar', ax=plt.gca())
    plt.title('District Test Scores by Socioeconomically Disadvantaged Student Percentage', fontsize=14)
    plt.xlabel('Percentage of Socioeconomically Disadvantaged Students')
    plt.ylabel('Average Test Score')
    plt.grid(True, axis='y', alpha=0.3)
    plt.legend(['ELA Scores', 'Math Scores'])
    
    plt.tight_layout()
    plt.savefig("../output/test_scores_by_sed.png", dpi=300)
    plt.show()
    
    # 4. Distribution of key variables
    plt.figure(figsize=(16, 12))
    
    # Teacher salary distribution
    plt.subplot(2, 3, 1)
    df_merge['BTCHSAL'].hist(bins=30, alpha=0.7)
    plt.title('Beginning Teacher Salary Distribution', fontsize=12)
    plt.xlabel('Normalized Salary')
    plt.grid(True, alpha=0.3)
    
    plt.subplot(2, 3, 2)
    df_merge['MTCHSAL'].hist(bins=30, alpha=0.7, color='green')
    plt.title('Mid-Career Teacher Salary Distribution', fontsize=12)
    plt.xlabel('Normalized Salary')
    plt.grid(True, alpha=0.3)
    
    plt.subplot(2, 3, 3)
    df_merge['HTCHSAL'].hist(bins=30, alpha=0.7, color='red')
    plt.title('High-Level Teacher Salary Distribution', fontsize=12)
    plt.xlabel('Normalized Salary')
    plt.grid(True, alpha=0.3)
    
    # Test score distributions
    plt.subplot(2, 3, 4)
    df_merge['SMATH_Y2'].hist(bins=30, alpha=0.7, color='purple')
    plt.title('State Math Score Distribution', fontsize=12)
    plt.xlabel('Score')
    plt.grid(True, alpha=0.3)
    
    plt.subplot(2, 3, 5)
    df_merge['SELA_Y2'].hist(bins=30, alpha=0.7, color='orange')
    plt.title('State ELA Score Distribution', fontsize=12)
    plt.xlabel('Score')
    plt.grid(True, alpha=0.3)
    
    plt.subplot(2, 3, 6)
    df_merge['PERSD'].hist(bins=30, alpha=0.7, color='blue')
    plt.title('Distribution of Socioeconomically Disadvantaged %', fontsize=12)
    plt.xlabel('Proportion of Students')
    plt.grid(True, alpha=0.3)
    
    plt.tight_layout()
    plt.savefig("../output/variable_distributions.png", dpi=300)
    plt.show()

