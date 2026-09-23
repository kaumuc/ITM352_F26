# Write Python code to define a list of taxi trip durations in miles. Also define a tuple of fares for the same number of trips

trip_duration = [1.1, 0.8, 2.5, 2.6]
trip_fares = ("$6.25", "$5.25", "$10.50", "$8.05")

trips = {
    "miles": trip_duration,
    "fares": trip_fares
}

print(trips)
print(trips["miles"][2])

print("the duration of the 3rd trip is:", trips["miles"][2], "miles")
print("the fare of the 3rd trip is:", trips["fares"][2])