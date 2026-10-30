import pandas as pd
import numpy as np
import ssl

# Ignore SSL certificate errors
ssl._create_default_https_context = ssl._create_unverified_context

csv_file = "https://drive.google.com/file/d/1ujY0WCcePdotG2xdbLyeECFW9lCJ4t-K/view?usp=drive_link"

try:
    df = pd.read_csv(csv_file, engine='pyarrow', on_bad_lines='skip')
    df['order_date'] = pd.to_datetime(df['order_date'], errors='coerce')
    print(df.head())

    
    # Calculate the average order amount
    avg_order_amount = df['order_amount'].mean()
    print(f"Average Order Amount: {avg_order_amount}")