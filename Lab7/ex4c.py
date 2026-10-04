

def check_budget(recent_purchases, budget):
    total_spent = 0
    results = []

    for purchase in recent_purchases:
        total_spent += purchase
        if total_spent > budget:
            results.append(f"This purchase {purchase} is over budget!")
            break
        results.append(f"This purchase {purchase} is within budget.")

    return results


if __name__ == "__main__":
    recent_purchases = [36.13, 23.87, 183.35, 22.93, 11.62]
    budget = 50
    for result in check_budget(recent_purchases, budget):
        print(result)