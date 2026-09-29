

# a
emotions = ("happy", "sad", "fear", "surprise")
print(str(emotions[-1] == "happy" and len(emotions) > 3).lower())

# b
emotions = ("happy", "sad", "fear", "surprise")
if emotions[-1] == "happy" and len(emotions) > 3:
	print("true")
else:
	print("false")
