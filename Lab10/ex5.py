from pathlib import Path

import pandas as pd

csv_path = Path(__file__).with_name("homes_data.csv")
homes_df = pd.read_csv(csv_path)

print(homes_df.head())