values = ["apple", 42, 3.14, True, "banana", 7, "cherry", 2.5, False, "date", 99, "elderberry"]

test_lists = (values[:3], values[:5], values[:10], values)

for test_list in test_lists:
	list_length = len(test_list)

	if list_length < 5:
		print(f"{list_length} elements: fewer than 5")
	elif list_length <= 10:
		print(f"{list_length} elements: between 5 and 10")
	else:
		print(f"{list_length} elements: more than 10")

# c
test_cases = [values[:4], values[:5], values[:10], values]
expected_results = [
	"fewer than 5",
	"between 5 and 10",
	"between 5 and 10",
	"more than 10",
]


for test_list, expected_result in zip(test_cases, expected_results):
	list_length = len(test_list)

	if list_length < 5:
		result = "fewer than 5"
	elif list_length <= 10:
		result = "between 5 and 10"
	else:
		result = "more than 10"

	assert result == expected_result
	print(f"Test passed for {len(test_list)} elements")
