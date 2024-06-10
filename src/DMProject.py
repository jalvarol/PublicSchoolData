#CSCI 185 - Web and Data Mining

from sklearn.preprocessing import MinMaxScaler
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import os

#Reading in Data
try: os.chdir('GroupMining')    
except:
    pass

#These files have footers
df_Expend = pd.read_csv('Expenditure_Data.txt', skipfooter = 5, engine = 'python')
df_Salary = pd.read_csv('Salary_Data.txt', skipfooter = 5, engine = 'python')
df_CA = pd.read_csv('Chronic_Absent.txt', sep = '|')

#Does not contain footers
df_Test_Scores = pd.read_csv('Test_Score_Results.txt', sep = '\t')


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
df_SED = pd.read_csv('Subgroup_Data.txt', usecols = ['CDSCODE', 'PERSD'])

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

display(df_merge.corr())

plt.matshow(df_merge.corr())
plt.show()