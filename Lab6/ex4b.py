def isLeapYear(year):
	if year % 4 == 0:
		if year % 100 == 0:
			if year % 400 == 0:
				return "Leap year"
			else:
				return "Not a leap year"
		else:
			return "Leap year"
	else:
		return "Not a leap year"


def find_closest_leap_year(year):
	distance = 0

	while True:
		previous_year = year - distance
		next_year = year + distance

		if previous_year >= 1 and isLeapYear(previous_year) == "Leap year":
			return previous_year
		if isLeapYear(next_year) == "Leap year":
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
	print(f"{year}: {isLeapYear(year)}")
