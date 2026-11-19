# Scrape names and email addresses of ITM people
import urllib.request
from bs4 import BeautifulSoup

itm_url = "https://shidler.hawaii.edu/itm/people"
print("Retrieving", itm_url)

# 1. Parse the page into a BeautifulSoup object and show the first few HTML lines
with urllib.request.urlopen(itm_url) as itm_page:
    soup = BeautifulSoup(itm_page, "html.parser")

print("Soup object:", type(soup))
print("First lines of prettified HTML:")
print("\n".join(soup.prettify().splitlines()[:10]))

# 2. Find all ITM people cards and print the count and first card
people_cards = soup.find_all("article", class_="node-faculty")
print("Number of ITM people:", len(people_cards))

if not people_cards:
    raise RuntimeError("No ITM people cards were found.")

print("First card HTML:")
print(people_cards[0].prettify())

# 3. Print each person's name and email address
print("ITM people and email addresses:")
for card in people_cards:
    name = card.select_one("h2.title")
    email = card.select_one(".field-email .field-item")
    if name is None or email is None:
        raise ValueError("An ITM people card is missing a name or email.")
    print(f"{name.get_text(strip=True)}: {email.get_text(strip=True)}")
