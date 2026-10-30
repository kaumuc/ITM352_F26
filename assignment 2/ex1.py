import pandas as pd

file_id = "1Fv_vhoN4sTrUaozFPfzr0NCyHJLIeXEA"
url = f"https://drive.google.com/uc?export=download&id={file_id}"
sales_df = pd.read_csv(url)
first_10_rows = sales_df.head(10)
output_file = "sales_data_test.csv"

first_10_rows.to_csv(output_file, index=False)
print(f"Saved the first 10 rows to {output_file}")
