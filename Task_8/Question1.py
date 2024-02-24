def elect_next_budget_item(votes: list[set[str]], balances: list[float], costs: dict[str, float]):
    """
    Elects the next item to purchase based on the provided votes, balances, and costs.
    Updates balances accordingly and prints the chosen item and the updated balances.
    """
    # Incremental amount to increase balances if needed
    increment_amount = 0.01
    count_increases = 0

    while True:
        # Check if an item can be purchased with current balances
        for item, cost in costs.items():
            total_balance = sum(balances[i] for i in range(len(votes)) if item in votes[i])
            if round(total_balance) >= cost:
                # Print the chosen item and the updated balances
                print(f"After adding {increment_amount * count_increases:.2f} to each citizen, \"{item}\" is chosen.")
                for i, vote in enumerate(votes):
                    if item in vote:
                        balances[i] = 0  # Reset balance to 0 for citizens who voted for the chosen item
                for i, balance in enumerate(balances):
                    print(f"Citizen {i} has {balance:.2f} remaining balance.")
                return

        # If nothing can be purchased, increase balances until something can be purchased
        for i in range(len(balances)):
            balances[i] += increment_amount
        count_increases += 1


if __name__ == "__main__":
    # Here the example of the function like we saw in class, step by step

    votes = [{"A", "B", "C", "D", "E"}] * 51 + [{"F", "G", "H", "I", "J"}] * 49
    balances = [0.0] * 51 + [0.0] * 49
    costs = {"A": 100, "B": 100, "C": 100, "D": 100, "E": 100, "F": 100, "G": 100, "H": 100, "I": 100, "J": 100}

    # votes = [{"B", "C", "D", "E"}] * 51 + [{"F", "G", "H", "I", "J"}] * 49
    # balances = [0.0] * 51 + [1.96] * 49
    # costs = {"B": 100, "C": 100, "D": 100, "E": 100, "F": 100, "G": 100, "H": 100, "I": 100, "J": 100}

    # votes = [{"B", "C", "D", "E"}] * 51 + [{"G", "H", "I", "J"}] * 49
    # balances = [0.08] * 51 + [0.0] * 49
    # costs = {"B": 100, "C": 100, "D": 100, "E": 100, "G": 100, "H": 100, "I": 100, "J": 100}

    # votes = [{"C", "D", "E"}] * 51 + [{"G", "H", "I", "J"}] * 49
    # balances = [0.0] * 51 + [1.88] * 49
    # costs = {"C": 100, "D": 100, "E": 100, "G": 100, "H": 100, "I": 100, "J": 100}

    # Other example:

    # votes = [{"Park", "Trees"}, {"Trees"}, {"Park", "Lights"}, {"Lights"}, {"Park"}]
    # balances = [1.5, 2.4, 3.3, 4.2, 5.1]
    # costs = {"Park": 1000, "Trees": 2000, "Lights": 3000}

    elect_next_budget_item(votes, balances, costs)
