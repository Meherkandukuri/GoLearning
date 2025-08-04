import pandas as pd

class DataCleanupBot:
    def clean_data(self, df, column_map):
        # Standardize column names
        df = df.rename(columns={v: k for k, v in column_map.items() if v in df.columns})
        
        # Clean employee IDs
        if 'EMP ID' in df.columns:
            df['EMP ID'] = df['EMP ID'].astype(str).str.strip().str.upper()
            
        # Clean dates
        date_cols = [col for col in df.columns if any(char in str(col) for char in ["/", "-"])]
        for col in date_cols:
            df[col] = df[col].astype(str).str.strip()
            
        return df