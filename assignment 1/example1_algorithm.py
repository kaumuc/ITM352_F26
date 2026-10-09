def make_change(amount_cents):
    if amount_cents < 0:
        raise ValueError("The amount cannot be negative.")

    coins = (
        ("quarter", 25),
        ("dime", 10),
        ("nickel", 5),
        ("penny", 1),
    )
    change = {}

    for coin_name, coin_value in coins:
        count, amount_cents = divmod(amount_cents, coin_value)
        if count:
            change[coin_name] = count

    return change


def main():
    while True:
        try:
            amount_cents = int(input("Enter an amount in cents: "))
            if amount_cents < 0:
                print("Please enter zero or a positive whole number.")
                continue
            break
        except ValueError:
            print("Please enter a whole number of cents.")

    change = make_change(amount_cents)

    if not change:
        print("No coins needed.")
        return

    print(f"Change for {amount_cents} cents:")
    for coin_name, count in change.items():
        if coin_name == "penny" and count != 1:
            coin_name = "pennies"
        elif count != 1:
            coin_name += "s"
        print(f"{count} {coin_name}")


if __name__ == "__main__":
    main()