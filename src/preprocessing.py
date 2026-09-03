"""Data cleaning and preprocessing for mine safety data."""

import pandas as pd
import numpy as np
from datetime import datetime

class DataPreprocessor:
    """Clean and preprocess mine safety sensor data."""
    
    def __init__(self):
        self.cleaning_report = {}
    
    def clean_data(self, df):
        """Perform comprehensive data cleaning."""
        df = df.copy()
        print("Starting data cleaning...")
        print(f"Initial records: {len(df)}")
        
        # 1. Handle missing values
        print("\n1. Handling missing values...")
        initial_missing = df.isnull().sum().sum()
        df = df.dropna(subset=['timestamp', 'mine_zone', 'gas_level'])
        df = df.ffill(limit=2)
        df = df.dropna()
        final_missing = df.isnull().sum().sum()
        self.cleaning_report['missing_values_dropped'] = initial_missing - final_missing
        print(f"Removed {self.cleaning_report['missing_values_dropped']} null values")
        
        # 2. Remove duplicates
        print("\n2. Removing duplicates...")
        initial_records = len(df)
        df = df.drop_duplicates(subset=['timestamp', 'mine_zone'])
        self.cleaning_report['duplicates_removed'] = initial_records - len(df)
        print(f"Removed {self.cleaning_report['duplicates_removed']} duplicate records")
        
        # 3. Standardize timestamp
        print("\n3. Standardizing timestamps...")
        df['timestamp'] = pd.to_datetime(df['timestamp'])
        
        # 4. Validate sensor ranges and remove outliers
        print("\n4. Validating sensor ranges...")
        initial_records = len(df)
        
        # Valid ranges
        df = df[(df['gas_level'] >= 0) & (df['gas_level'] <= 5000)]
        df = df[(df['temperature'] >= -10) & (df['temperature'] <= 50)]
        df = df[(df['humidity'] >= 0) & (df['humidity'] <= 100)]
        df = df[(df['vibration'] >= 0) & (df['vibration'] <= 20)]
        df = df[(df['pressure'] >= 95) & (df['pressure'] <= 110)]
        df = df[(df['worker_count'] >= 0) & (df['worker_count'] <= 100)]
        
        self.cleaning_report['invalid_ranges_removed'] = initial_records - len(df)
        print(f"Removed {self.cleaning_report['invalid_ranges_removed']} records with invalid values")
        
        # 5. Standardize text fields
        print("\n5. Standardizing text fields...")
        df['mine_zone'] = df['mine_zone'].str.strip().str.upper()
        df['equipment_status'] = df['equipment_status'].str.strip().str.upper()
        df['risk_level'] = df['risk_level'].str.strip().str.upper()
        
        # Validate zones
        valid_zones = ['ZONE A', 'ZONE B', 'ZONE C', 'ZONE D', 'ZONE E']
        df = df[df['mine_zone'].isin(valid_zones)]
        
        # 6. Handle outliers using IQR
        print("\n6. Handling outliers (IQR method)...")
        initial_records = len(df)
        df = self._remove_outliers_iqr(df)
        self.cleaning_report['outliers_removed'] = initial_records - len(df)
        print(f"Removed {self.cleaning_report['outliers_removed']} outliers")
        
        # 7. Sort by timestamp
        df = df.sort_values('timestamp').reset_index(drop=True)
        
        print(f"\nCleaning complete!")
        print(f"Final records: {len(df)}")
        print(f"Total records removed: {sum(self.cleaning_report.values())}")
        
        return df
    
    def _remove_outliers_iqr(self, df, columns=['gas_level', 'temperature', 'vibration']):
        """Remove outliers using Interquartile Range (IQR) method."""
        for col in columns:
            Q1 = df[col].quantile(0.25)
            Q3 = df[col].quantile(0.75)
            IQR = Q3 - Q1
            lower_bound = Q1 - 1.5 * IQR
            upper_bound = Q3 + 1.5 * IQR
            df = df[(df[col] >= lower_bound) & (df[col] <= upper_bound)]
        return df
    
    def generate_cleaning_report(self):
        """Return cleaning report."""
        return self.cleaning_report


if __name__ == "__main__":
    # Example usage
    df = pd.read_csv('data/raw/mine_safety_raw.csv')
    preprocessor = DataPreprocessor()
    clean_df = preprocessor.clean_data(df)
    clean_df.to_csv('data/processed/mine_safety_clean.csv', index=False)
    print("\nCleaned data saved to data/processed/mine_safety_clean.csv")
