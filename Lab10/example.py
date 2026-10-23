import numpy as np
import pandas as pd

# Example 1: Use NumPy to calculate with a list of fares.
fares = np.array([3.25, 8.05, 20.05])

print("NumPy example")
print("Fares:", fares)
print("Total fares:", fares.sum())
print("Average fare:", fares.mean())
print("Largest fare:", fares.max())

# Example 2: Use pandas to organize trip information in a table.
trips = pd.DataFrame({
    "Fare": [3.25, 8.05, 20.05],
    "Trip Miles": [0.0, 1.5, 8.5]
})

print("\npandas example")
print(trips)
print("Total fares:", trips["Fare"].sum())
print("Average fare:", trips["Fare"].mean())
print("Longest trip:", trips["Trip Miles"].max(), "miles")