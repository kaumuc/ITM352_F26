def list_size_category(items):
	list_length = len(items)

	if list_length < 5:
		return "fewer than 5"
	elif list_length <= 10:
		return "between 5 and 10"
	else:
		return "more than 10"


values = ["apple", 42, 3.14, True, "banana", 7, "cherry", 2.5, False, "date", 99, "elderberry"]

test_cases = [
	[values[:4], "fewer than 5"],
	[values[:5], "between 5 and 10"],
	[values[:10], "between 5 and 10"],
	[values, "more than 10"],
]

for test_list, expected_result in test_cases:
	result = list_size_category(test_list)
	assert result == expected_result, f"Expected {expected_result}, got {result}"
	print(f"Test passed for {len(test_list)} elements: {result}")
