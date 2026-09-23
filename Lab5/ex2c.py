

trip_duration = [1.1, 0.8, 2.5, 2.6]
trip_fares = ("$6.25", "$5.25", "$10.50", "$8.05")

trips = dict(zip(trip_duration, trip_fares))
print(trips)

trip_num = int(input("What trip do you want?"))

print("the duration of the", trip_num, "trip is:", trip_duration[trip_num-1], "miles")
print("the fare of the trip is:", trip_fares[trip_num-1])