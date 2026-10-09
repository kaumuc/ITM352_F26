# This function calculates the fewest coins needed to make the given amount.
# It takes an amount in cents and returns a dictionary of coin counts.
def make_change(amount_cents):
    # If the user enters a negative number, we stop with an error.
    if amount_cents < 0:
        raise ValueError("The amount cannot be negative.")

    # These are the coin values in order from largest to smallest.
    # The program will try quarters first, then dimes, nickels, and pennies.
    coins = (
        ("quarter", 25),
        ("dime", 10),
        ("nickel", 5),
        ("penny", 1),
    )

    # This dictionary stores how many of each coin are needed.
    # Example: {"quarter": 2, "dime": 1}
    change = {}

    # For each coin type, we see how many times it fits into the remaining amount.
    # divmod(amount, value) returns two values:
    #   - count = how many times the coin fits
    #   - amount = the remaining cents left after removing those coins
    for coin_name, coin_value in coins:
        count, amount_cents = divmod(amount_cents, coin_value)
        if count:
            change[coin_name] = count

    # Return the final coin breakdown.
    return change


# This is the main program that runs when the file is executed.
def main():
    # Keep asking until the user enters a valid non-negative whole number.
    while True:
        try:
            # Read the user input and convert it to an integer.
            amount_cents = int(input("Enter an amount in cents: "))
            # Reject negative amounts.
            if amount_cents < 0:
                print("Please enter zero or a positive whole number.")
                continue
            break
        except ValueError:
            # If the user enters something that is not a whole number, ask again.
            print("Please enter a whole number of cents.")

    # Calculate the coins needed for this amount.
    change = make_change(amount_cents)

    # If the amount is zero, no coins are needed.
    if not change:
        print("No coins needed.")
        return

    # Print the amount of change.
    print(f"Change for {amount_cents} cents:")
    for coin_name, count in change.items():
        # Fix the word so it reads correctly for singular and plural forms.
        # Example: 1 penny, 2 pennies
        if coin_name == "penny" and count != 1:
            coin_name = "pennies"
        elif count != 1:
            coin_name += "s"
        print(f"{count} {coin_name}")


# This line ensures the main function runs only when the file is run directly.
# It does not run when the file is imported into another file.
if __name__ == "__main__":
    main()