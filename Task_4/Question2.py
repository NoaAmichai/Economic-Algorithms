from collections import deque


def egalitarian_allocation(valuations: list[list[float]]):
    """
    Find an egalitarian allocation of items between two players based on their valuations.

    Args:
    - valuations (list of lists): A list of two lists representing the valuations of each player for each item.

    Returns:
    - tuple: A tuple containing two lists, representing the items allocated to each player in the egalitarian allocation.
    """

    num_items = len(valuations[0])  # Number of items

    # Initial state - empty allocation for both players
    initial_state = [0, list(), list()]

    states = deque()  # Queue for saving states
    states.append(initial_state)  # Add initial state

    best_alloc = None

    final_allocations = set()  # Set of fair allocations with that have num_items items allocated

    player1_values = valuations[0]
    player2_values = valuations[1]
    count = 0
    while states:
        count += 1
        state = states.popleft()
        num_allocated, player1_alloc, player2_alloc = state  # Unpack state

        # Calculate the remaining items that are not allocated yet
        remaining_items = set(range(num_items)) - set(player1_alloc + player2_alloc)

        # Pruning rule - if the optimistic allocation is not fair for one or both players, skip this state
        is_optimal_fair = optimistic_pruning_rule(state, player1_values, player2_values,
                                                  remaining_items)

        if is_optimal_fair:  # If the optimistic allocation is fair
            if num_allocated == num_items:  # If the allocation is complete (all items are allocated)
                # Convert allocations to tuples for set comparison
                allocation1 = (
                    len(player1_alloc) + len(player2_alloc), tuple(sorted(player1_alloc)), tuple(sorted(player2_alloc)))
                allocation2 = (
                    len(player1_alloc) + len(player2_alloc), tuple(sorted(player2_alloc)), tuple(sorted(player1_alloc)))
                # Add allocations to the set of final allocations
                final_allocations.add(allocation1)
                final_allocations.add(allocation2)

            else:
                for item in remaining_items:
                    player1_alloc.append(item)  # Allocate item to player 1
                    new_state1 = [num_allocated + 1, sorted(player1_alloc), sorted(player2_alloc)]
                    if new_state1 not in states:  # Pruning rule - no duplicate states
                        states.append(new_state1)
                    player1_alloc.pop()  # Deallocate item from player 1

                    player2_alloc.append(item)  # Allocate item to player 2
                    new_state2 = [num_allocated + 1, sorted(player1_alloc), sorted(player2_alloc)]
                    if new_state2 not in states:  # Pruning rule - no duplicate states
                        states.append(new_state2)
                    player2_alloc.pop()  # Deallocate item from player 2

    print(count)
    max_min_value = float('-inf')  # Max min value of the final allocations

    # Find the allocation with the highest value from the set of final allocations
    for allocation in final_allocations:
        # Calculate the min value of the allocation
        min_values = min([min(valuations[0][i] for i in allocation[1]), min(valuations[1][i] for i in allocation[2])])

        # Take the allocation with the highest min value
        if best_alloc is None or max_min_value < min_values:
            max_min_value = min_values
            best_alloc = [list(allocation[1]), list(allocation[2])]

    if best_alloc is None:
        print("No fair allocation exists")
        return

    print("Player 0 gets items", best_alloc[0], "with value", sum(valuations[0][i] for i in best_alloc[0]))
    print("Player 1 gets items", best_alloc[1], "with value", sum(valuations[1][i] for i in best_alloc[1]))


def calculate_value(items, player_values):
    """Calculate the total value of items for a player."""
    return sum(player_values[i] for i in items)


def optimistic_pruning_rule(state, player1_values, player2_values, remaining_items):
    num_allocated, player1_alloc, player2_alloc = state  # Unpack state
    # Calculate the optimistic allocation for each player considering already allocated items
    player1_remaining_values = calculate_value(remaining_items, player1_values)
    player1_allocated_values = calculate_value(player1_alloc, player1_values)
    player1_optimal = player1_remaining_values + player1_allocated_values

    player2_remaining_values = calculate_value(remaining_items, player2_values)
    player2_allocated_values = calculate_value(player2_alloc, player2_values)
    player2_optimal = player2_remaining_values + player2_allocated_values

    # Check if the optimistic allocation is fair for both players
    is_player1_fair = player1_optimal >= 0.5 * (sum(player1_values))
    is_player2_fair = player2_optimal >= 0.5 * (sum(player2_values))
    return is_player1_fair and is_player2_fair


if __name__ == "__main__":
    # valuation = [[4, 5, 6, 7, 8], [8, 7, 6, 5, 4]]
    valuation = [[1,1], [1,1]]
    egalitarian_allocation(valuation)
