# Algorithm:
# 1. Subtract the amount owed from 100 cents to find the change due.
# 2. Starting with the largest coin, divide the remaining change by its value.
# 3. Keep the quotient as the number of those coins and the remainder as the
#    amount still to make change for.
# 4. Repeat for quarters, dimes, nickels, and pennies.

def make_change(change_cents):
    coins = (
        (25, "quarter"),
        (10, "dime"),
        (5, "nickel"),
        (1, "penny"),
    )
    counts = []

    for value, name in coins:
        count, change_cents = divmod(change_cents, value)
        counts.append((count, name))

    return counts


try:
    amount_owed = int(input("Enter the amount owed in cents (out of $1.00): "))
except ValueError:
    print("Please enter a whole number of cents.")
    raise SystemExit(1)

if not 0 <= amount_owed <= 100:
    print("The amount owed must be between 0 and 100 cents.")
    raise SystemExit(1)

change_due = 100 - amount_owed
print(f"Change due: {change_due} cents")

for count, coin in make_change(change_due):
    if count:
        coin_name = "pennies" if coin == "penny" and count != 1 else coin
        if count != 1 and coin != "penny":
            coin_name += "s"
        print(f"{count} {coin_name}")
