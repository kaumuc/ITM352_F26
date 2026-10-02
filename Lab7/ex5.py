celebs = ("Lebron James", "Tiger Woods", "Tom Brady", "Messi", "Cristiano Ronaldo")
ages = (41, 50, 49, 39, 41)

celeb_list = []
for celeb in celebs:
    celeb_list.append(celeb)

ages_list = [age for age in ages]

celebs_dict = {"celebs": celeb_list, "ages": ages_list}
print(celebs_dict)
