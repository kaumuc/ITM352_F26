# Simple dictionary example

country_capitals = {
    "Germany": "Berlin", "population": 83000000,
    "Canada": "Ottawa", "population": 38000000,
    "France": "Paris", "population": 68000000,
}

print("Country Capitals:", country_capitals)
print(country_capitals["Canada"])

country_capitals["England"] = {"capital": "London", "population": 56000000}
print(country_capitals["England"])

print("Germany" in country_capitals)
print("Spain" not in country_capitals)