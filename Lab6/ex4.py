def is_leap_year(year):
	return (year % 4 == 0 and year % 100 != 0) or year % 400 == 0


def find_closest_leap_year(year):
	distance = 0

	while True:
		previous_year = year - distance
		next_year = year + distance

		if previous_year >= 1 and is_leap_year(previous_year):
			return previous_year
		if is_leap_year(next_year):
			return next_year

		distance += 1


birth_year = 2003
closest_leap_year = find_closest_leap_year(birth_year)

print(f"Birth year: {birth_year}")
print(f"Closest leap year: {closest_leap_year}")

test_years = [birth_year]
if closest_leap_year != birth_year:
	test_years.append(closest_leap_year)
else:
	test_years.append(birth_year + 1)

for year in test_years:
	if is_leap_year(year):
		print(f"{year} is a leap year.")
	else:
		print(f"{year} is not a leap year.")
