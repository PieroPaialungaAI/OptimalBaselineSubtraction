import numpy as np 
import pandas as pd 
from constants import * 

def standardize_data(df,city):
    df = df.copy()
    df.set_index('datetime', inplace=True)
    start_date = df.index.min().normalize()
    end_date = df.index.max().normalize() + pd.Timedelta(days=1)
    full_range = pd.date_range(start=start_date, end=end_date - pd.Timedelta(hours=1), freq='H')
    df_standardized = df.reindex(full_range)
    df_standardized.index.name = 'datetime'
    df_standardized[city] = df_standardized[city].interpolate()  # or use fillna()
    df_standardized = df_standardized.fillna(method = 'bfill').reset_index()
    return df_standardized