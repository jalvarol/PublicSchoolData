"""
Data preparation module for Public School Data Analysis project.

This module handles data loading, cleaning, transformation, and preprocessing
of California public school data including:
- Expenditure data
- Teacher salary data
- Chronic absence rates
- Test score results
- Socioeconomically disadvantaged student data

Functions:
- load_raw_datasets: Load raw datasets from files
- clean_datasets: Apply initial cleaning to individual datasets
- convert_data_types: Ensure proper data types for analysis
- handle_missing_values: Strategy for handling missing data
- merge_datasets: Combine all datasets into a unified dataframe
- normalize_columns: Apply normalization to specified columns
- load_data: Main function that orchestrates the entire data preparation pipeline
"""

import pandas as pd
import numpy as np
import os
from typing import Dict, List, Optional, Tuple
from sklearn.preprocessing import MinMaxScaler
import logging

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger('data_preparation')

def load_raw_datasets() -> Dict[str, pd.DataFrame]:
    """
    Load all raw datasets from files.
    
    Returns:
        Dict[str, pd.DataFrame]: Dictionary containing all loaded dataframes
    
    Raises:
        FileNotFoundError: If any required data file is missing
        pd.errors.ParserError: If there are issues parsing the data files
    """
    try:
        # Try changing to data directory first like in the original DMProject.py
        original_dir = os.getcwd()
        try:
            os.chdir('data')
            data_dir = ''  # If successful, use relative paths without '../data/'
        except:
            data_dir = '../data/'  # Otherwise, use the '../data/' prefix
        
        # Datasets with footers
        df_expend = pd.read_csv(f'{data_dir}Expenditure_Data.txt', skipfooter=5, engine='python')
        df_salary = pd.read_csv(f'{data_dir}Salary_Data.txt', skipfooter=5, engine='python')
        
        # Dataset with pipe separator
        df_ca = pd.read_csv(f'{data_dir}Chronic_Absent.txt', sep='|')
        
        # Dataset with tab separator
        df_test_scores = pd.read_csv(f'{data_dir}Test_Score_Results.txt', sep='\t')
        
        # Socioeconomically disadvantaged data
        df_sed = pd.read_csv(f'{data_dir}Subgroup_Data.txt', usecols=['CDSCODE', 'PERSD'])
        
        # Standardize column names to uppercase
        for df in [df_expend, df_salary, df_ca, df_test_scores, df_sed]:
            df.columns = df.columns.str.upper()
        
        # If we changed directory, change back
        if data_dir == '':
            os.chdir(original_dir)
            
        logger.info("All datasets loaded successfully")
        
        return {
            'expenditure': df_expend,
            'salary': df_salary,
            'chronic_absence': df_ca,
            'test_scores': df_test_scores,
            'socioeconomic': df_sed
        }
        
    except FileNotFoundError as e:
        logger.error(f"Data file not found: {e}")
        # If we changed directory, change back before raising
        if 'original_dir' in locals() and data_dir == '':
            os.chdir(original_dir)
        raise
    except pd.errors.ParserError as e:
        logger.error(f"Error parsing data file: {e}")
        # If we changed directory, change back before raising
        if 'original_dir' in locals() and data_dir == '':
            os.chdir(original_dir)
        raise
    except Exception as e:
        logger.error(f"Unexpected error loading data: {e}")
        # If we changed directory, change back before raising
        if 'original_dir' in locals() and data_dir == '':
            os.chdir(original_dir)
        raise

def clean_datasets(datasets: Dict[str, pd.DataFrame]) -> Dict[str, pd.DataFrame]:
    """
    Perform initial cleaning on raw datasets.
    
    Args:
        datasets: Dictionary of raw dataframes
        
    Returns:
        Dict[str, pd.DataFrame]: Dictionary of cleaned dataframes
    """
    try:
        # Data reduction - remove unnecessary columns
        datasets['expenditure'].drop(['SARCYEAR', 'C', 'D', 'S', 'STEXP'], axis=1, inplace=True)
        
        # Select only needed columns
        datasets['salary'] = datasets['salary'][['CDSCODE', 'BTCHSAL', 'MTCHSAL', 'HTCHSAL']]
        datasets['test_scores'] = datasets['test_scores'][['CDSCODE', 'SELA_Y2', 'SMATH_Y2', 'DELA_Y2', 'DMATH_Y2']]
        datasets['chronic_absence'] = datasets['chronic_absence'][['CDSCODE', 'RALL', 'REL', 'RSED']]
        
        # Replace placeholders with NaN
        datasets['test_scores'].replace(['--', '0'], np.nan, inplace=True)
        
        logger.info("Initial dataset cleaning completed")
        return datasets
        
    except KeyError as e:
        logger.error(f"Missing expected column: {e}")
        raise
    except Exception as e:
        logger.error(f"Error during dataset cleaning: {e}")
        raise

def handle_missing_values(datasets: Dict[str, pd.DataFrame]) -> Dict[str, pd.DataFrame]:
    """
    Apply strategies for handling missing values in each dataset.
    
    Args:
        datasets: Dictionary of dataframes with potential missing values
        
    Returns:
        Dict[str, pd.DataFrame]: Dictionary of dataframes with missing values handled
    """
    try:
        # Replace NaNs in SED with zeros (assuming 0% socioeconomically disadvantaged)
        datasets['socioeconomic'].replace([np.nan], 0, inplace=True)
        
        # Fill missing numeric values with column means for expenditure and salary data
        for df_name in ['expenditure', 'salary']:
            datasets[df_name].fillna(datasets[df_name].mean(numeric_only=True), inplace=True)
        
        logger.info("Missing values handled successfully")
        return datasets
        
    except Exception as e:
        logger.error(f"Error handling missing values: {e}")
        raise

def convert_data_types(datasets: Dict[str, pd.DataFrame]) -> Dict[str, pd.DataFrame]:
    """
    Ensure all columns have appropriate data types for analysis.
    
    Args:
        datasets: Dictionary of dataframes
        
    Returns:
        Dict[str, pd.DataFrame]: Dictionary of dataframes with corrected data types
    """
    try:
        # Convert test score columns to numeric
        for col in ['SELA_Y2', 'SMATH_Y2', 'DELA_Y2', 'DMATH_Y2']:
            datasets['test_scores'][col] = pd.to_numeric(datasets['test_scores'][col], errors='coerce')
            
        # Convert salary columns to numeric
        for col in ['BTCHSAL', 'MTCHSAL', 'HTCHSAL']:
            datasets['salary'][col] = pd.to_numeric(datasets['salary'][col], errors='coerce')
            
        # Convert chronic absence columns to numeric
        for col in ['RALL', 'REL', 'RSED']:
            datasets['chronic_absence'][col] = pd.to_numeric(datasets['chronic_absence'][col], errors='coerce')
            
        # Convert socioeconomic data to numeric
        datasets['socioeconomic']['PERSD'] = pd.to_numeric(datasets['socioeconomic']['PERSD'], errors='coerce')
        
        # Convert expenditure columns to numeric
        for col in ['DSAL', 'STSAL']:
            datasets['expenditure'][col] = pd.to_numeric(datasets['expenditure'][col], errors='coerce')
            
        logger.info("Data type conversion completed")
        return datasets
        
    except Exception as e:
        logger.error(f"Error converting data types: {e}")
        raise

def merge_datasets(datasets: Dict[str, pd.DataFrame]) -> pd.DataFrame:
    """
    Merge all datasets into a single dataframe.
    
    Args:
        datasets: Dictionary of processed dataframes
        
    Returns:
        pd.DataFrame: Single merged dataframe with all variables
    """
    try:
        # Log dataset sizes before merging
        for name, df in datasets.items():
            logger.info(f"Dataset '{name}' has {len(df)} rows before merging")
        
        # Sequentially merge all dataframes on CDSCODE
        df_merged = datasets['expenditure'].merge(datasets['salary'], on='CDSCODE', how='inner')
        logger.info(f"After merging expenditure and salary: {len(df_merged)} rows")
        
        df_merged = df_merged.merge(datasets['test_scores'], on='CDSCODE', how='inner')
        logger.info(f"After merging test_scores: {len(df_merged)} rows")
        
        df_merged = df_merged.merge(datasets['socioeconomic'], on='CDSCODE', how='inner')
        logger.info(f"After merging socioeconomic: {len(df_merged)} rows")
        
        df_merged = df_merged.merge(datasets['chronic_absence'], on='CDSCODE', how='inner')
        logger.info(f"After merging chronic_absence: {len(df_merged)} rows")
        
        # Check for potential issues before removing NaN values
        for col in df_merged.columns:
            nan_count = df_merged[col].isna().sum()
            if nan_count > 0:
                logger.warning(f"Column {col} has {nan_count} NaN values ({nan_count/len(df_merged)*100:.1f}%)")
        
        # Remove rows with any remaining NaN values
        initial_row_count = len(df_merged)
        df_merged.dropna(inplace=True)
        rows_dropped = initial_row_count - len(df_merged)
        
        logger.info(f"Datasets merged successfully. {rows_dropped} rows with NaN values removed.")
        logger.info(f"Final merged dataset has {len(df_merged)} rows")
        return df_merged
        
    except Exception as e:
        logger.error(f"Error merging datasets: {e}")
        raise

def normalize_columns(df: pd.DataFrame, columns: List[str]) -> pd.DataFrame:
    """
    Normalize specified columns using Min-Max scaling.
    
    Args:
        df: Input dataframe
        columns: List of columns to normalize
        
    Returns:
        pd.DataFrame: Dataframe with normalized columns
    """
    try:
        scaler = MinMaxScaler()
        df[columns] = scaler.fit_transform(df[columns])
        
        logger.info(f"Normalized columns: {', '.join(columns)}")
        return df
        
    except Exception as e:
        logger.error(f"Error normalizing columns: {e}")
        raise

def load_data() -> Optional[pd.DataFrame]:
    """
    Complete data preparation pipeline: load, clean, merge, and preprocess all datasets.
    
    Returns:
        Optional[pd.DataFrame]: Fully prepared dataset ready for analysis
    """
    try:
        # Step 1: Load raw datasets
        datasets = load_raw_datasets()
        
        # Step 2: Clean datasets
        datasets = clean_datasets(datasets)
        
        # Step 3: Handle missing values
        datasets = handle_missing_values(datasets)
        
        # Step 4: Convert data types
        datasets = convert_data_types(datasets)
        
        # Step 5: Merge all datasets
        df_merged = merge_datasets(datasets)
        
        # Step 6: Normalize columns with large values
        columns_to_normalize = ['DSAL', 'STSAL', 'BTCHSAL', 'MTCHSAL', 'HTCHSAL']
        df_merged = normalize_columns(df_merged, columns_to_normalize)
        
        # Final verification - ensure all columns are numeric except CDSCODE
        for col in df_merged.columns:
            if col != 'CDSCODE':
                df_merged[col] = pd.to_numeric(df_merged[col], errors='coerce')
        
        # Check if we still have data after all the processing
        if len(df_merged) == 0:
            logger.error("Final dataset is empty! Check the data processing pipeline.")
            return None
            
        # Log data sample and summary
        logger.info(f"Data preparation complete. Final dataset shape: {df_merged.shape}")
        logger.info(f"PERSD range: {df_merged['PERSD'].min()} to {df_merged['PERSD'].max()}")
        logger.info(f"SMATH_Y2 range: {df_merged['SMATH_Y2'].min()} to {df_merged['SMATH_Y2'].max()}")
        
        return df_merged
        
    except Exception as e:
        logger.error(f"Error in data preparation pipeline: {e}")
        logger.exception("Stack trace:")
        return None

def validate_final_dataset(df: pd.DataFrame) -> bool:
    """
    Validate the final dataset to ensure it meets quality standards.
    
    Args:
        df: Processed dataframe
        
    Returns:
        bool: True if dataset passes validation
    """
    try:
        # Check for remaining missing values
        if df.isnull().any().any():
            logger.warning("Dataset contains missing values")
            return False
            
        # Check that key columns exist
        required_columns = ['CDSCODE', 'PERSD', 'SMATH_Y2', 'SELA_Y2', 'HTCHSAL', 'RALL']
        for col in required_columns:
            if col not in df.columns:
                logger.warning(f"Required column {col} missing from dataset")
                return False
                
        # Check minimum dataset size
        if len(df) < 100:  # Arbitrary threshold for a meaningful analysis
            logger.warning(f"Dataset may be too small for reliable analysis: {len(df)} rows")
            
        logger.info("Dataset validation passed")
        return True
        
    except Exception as e:
        logger.error(f"Error validating dataset: {e}")
        return False

if __name__ == "__main__":
    # Test data loading and preparation
    print("Testing data preparation pipeline...")
    df = load_data()
    if df is not None:
        print(f"Data preparation successful. Dataset shape: {df.shape}")
        validate_final_dataset(df)
        print("\nData preview:")
        print(df.head())
        print("\nData types:")
        print(df.dtypes)
        print("\nMissing values:")
        print(df.isnull().sum())
    else:
        print("Data preparation failed. Check logs for details.")
