# Create a dataframe with 4 columns and 5 rows

import pandas as pd

data = {
    'Name': ['Alice', 'Bob', 'Charlie', 'David', 'Eva'],
    'Age': [25, 30, 35, 40, 22],
    'City': ['New York', 'Los Angeles', 'Chicago', 'Houston', 'Phoenix'],
    'Salary': [70000, 80000, 90000, 100000, 60000]
}

# Convert the dictionary into a pandas DataFrame
df = pd.DataFrame(data)

# Display the DataFrame
print(df)