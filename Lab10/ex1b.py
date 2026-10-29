import numpy as np

income_percentiles = [
    (10, 14629),
    (20, 25600),
    (30, 37002),
    (40, 50000),
    (50, 63179),
    (60, 79542),
    (70, 100162),
    (80, 130000),
    (90, 184292),
]

income_array = np.array(income_percentiles)

print("Dimensions:", income_array.shape)
print("Number of elements:", income_array.size)

print("\nPercentile  Household Income")
for percentile, income in income_array:
    print(f"{percentile:>10}  {income:>15,}")