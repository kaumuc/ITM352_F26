import requests
from bs4 import BeautifulSoup

url = "https://www.hicentral.com/hawaii-mortgage-rates.php"

# 1. Retrieve the page and find its mortgage-rate table
response = requests.get(url, timeout=30)
response.raise_for_status()
soup = BeautifulSoup(response.text, "html.parser")

rate_table = soup.find("table")
if rate_table is None:
    raise ValueError("The mortgage-rate table was not found.")

# 2. Extract each row and print the bank and its rates
current_bank = None
print("Bank | Term/Type | Interest Rate | Points | APR")

for row in rate_table.select("tbody tr"):
    cells = row.find_all("td")
    if not cells:
        continue

    bank_cell = row.find("td", rowspan=True)
    if bank_cell is not None:
        bank_name = bank_cell.find("b")
        if bank_name is None:
            raise ValueError("A lender name was not found in the table.")
        current_bank = bank_name.get_text(strip=True)
        cells = cells[1:]

    if current_bank is None or len(cells) < 4:
        raise ValueError("A mortgage-rate row is missing lender or rate data.")

    term, interest_rate, points, apr = (
        cell.get_text(" ", strip=True) for cell in cells[:4]
    )
    interest_rate = f"{interest_rate}%" if interest_rate else "Not listed"
    points = f"{points}%" if points else "Not listed"
    apr = f"{apr}%" if apr else "Not listed"
    print(f"{current_bank} | {term} | {interest_rate} | {points} | {apr}")