import doctest
import functools
import operator
from collections import deque
from typing import List


def egalitarian_allocation(valuations: List[List[float]], purging_rule1: bool = True, purging_rule2: bool = True):
    """
    Find an egalitarian allocation of items between two players based on their valuations.

    Args:
    - valuations (list of lists): A list of two lists representing the valuations of each player for each item.
    - purging_rule1 (bool): Whether to apply the first pruning rule.
    - purging_rule2 (bool): Whether to apply the second pruning rule.

    Returns:
    - tuple: A tuple containing two lists, representing the items allocated to each player in the egalitarian allocation.

    Examples:
    >>> egalitarian_allocation([[4, 5, 6, 7, 8], [8, 7, 6, 5, 4]], purging_rule1=True, purging_rule2=True)
    Player 0 gets items [3, 4] with value 15
    Player 1 gets items [0, 1, 2] with value 21

    >>> egalitarian_allocation([[1, 1, 1, 1], [1, 1, 1, 1]], purging_rule1=True, purging_rule2=True)
    Player 0 gets items [1, 2] with value 2
    Player 1 gets items [0, 3] with value 2

    """
    num_items = len(valuations[0])  # Number of items

    initial_state = [0, [], []]  # Initial state - empty allocation for both players
    states = deque()  # Queue for saving states
    states.append(initial_state)  # Add initial state

    best_alloc = None
    final_allocations = set()  # Set of fair allocations with num_items items allocated

    player1_values = valuations[0]
    player2_values = valuations[1]

    while states:
        state = states.popleft()
        num_allocated, player1_alloc, player2_alloc = state

        remaining_items = set(range(num_items)) - set(player1_alloc + player2_alloc)

        if apply_pruning_rule(state, player1_values, player2_values, remaining_items, purging_rule1, purging_rule2):
            if num_allocated == num_items:
                final_allocations.add((len(player1_alloc) + len(player2_alloc), tuple(sorted(player1_alloc)),
                                       tuple(sorted(player2_alloc))))
            else:
                explore_next_states(states, state, remaining_items, purging_rule2)

    best_alloc = find_best_allocation_max_min(final_allocations, valuations)

    print_allocation(best_alloc, valuations)


def apply_pruning_rule(state, player1_values, player2_values, remaining_items, purging_rule1, purging_rule2):
    """
    Apply pruning rules to determine if the state should be explored further.
    """
    if not purging_rule1:
        return True

    player1_optimal = calculate_optimal_value(remaining_items, state[1], player1_values)
    player2_optimal = calculate_optimal_value(remaining_items, state[2], player2_values)

    is_player1_fair = player1_optimal >= 0.5 * sum(player1_values)
    is_player2_fair = player2_optimal >= 0.5 * sum(player2_values)

    return is_player1_fair and is_player2_fair


def calculate_optimal_value(remaining_items, allocated_items, player_values):
    """
    Calculate the optimistic allocation for a player considering already allocated items.
    """
    remaining_values = sum(player_values[i] for i in remaining_items)
    allocated_values = sum(player_values[i] for i in allocated_items)
    return remaining_values + allocated_values


def explore_next_states(states, state, remaining_items, purging_rule2):
    """
    Explore next states and add them to the queue for BFS.
    """
    for item in remaining_items:
        new_state1 = [state[0] + 1, state[1] + [item], state[2]]
        new_state2 = [state[0] + 1, state[1], state[2] + [item]]
        if not purging_rule2 or (new_state1 not in states and new_state2 not in states):
            states.append(new_state1)
            states.append(new_state2)


def find_best_allocation_max_min(final_allocations, valuations):
    """
    Find the allocation with the highest value from the set of final allocations.
    """
    best_alloc = None
    max_min_value = float('-inf')

    for allocation in final_allocations:
        if len(allocation[1]) == 0 or len(allocation[2]) == 0:
            continue
        min_values = min(sum(valuations[0][i] for i in allocation[1]), sum(valuations[1][i] for i in allocation[2]))
        if best_alloc is None or max_min_value < min_values:
            max_min_value = min_values
            best_alloc = [list(allocation[1]), list(allocation[2])]

    return best_alloc


def print_allocation(best_alloc, valuations):
    """
    Print the allocation result.
    """
    if best_alloc is None:
        print("No fair allocation exists")
        return

    print("Player 0 gets items", best_alloc[0], "with value", sum(valuations[0][i] for i in best_alloc[0]))
    print("Player 1 gets items", best_alloc[1], "with value", sum(valuations[1][i] for i in best_alloc[1]))


"""
Question 2 Extra - Product Maximizing Allocation 

"""


def calculate_product(items, player_values):
    """
    Calculate the product of the values of items for a player.
    """
    return functools.reduce(operator.mul, (player_values[i] for i in items), 1)


def find_best_allocation_product(final_allocations, valuations):
    """
    Find the allocation with the highest value from the set of final allocations.
    """
    best_alloc = None
    max_product = float('-inf')

    for allocation in final_allocations:
        if len(allocation[1]) == 0 or len(allocation[2]) == 0:
            continue
        product = calculate_product(allocation[1], valuations[0]) * calculate_product(allocation[2], valuations[1])
        if best_alloc is None or max_product < product:
            max_product = product
            best_alloc = [list(allocation[1]), list(allocation[2])]

    return best_alloc


def product_maximizing_allocation(valuations: List[List[float]], purging_rule1: bool = True,
                                  purging_rule2: bool = True):
    """
    Finds an allocation of items between two players that maximizes the product of their values.

    Args:
    - valuations (list of lists): A list of two lists representing the valuations of each player for each item.
    - purging_rule1 (bool): Whether to apply the first pruning rule.
    - purging_rule2 (bool): Whether to apply the second pruning rule.

    Returns:
    - tuple: A tuple containing two lists, representing the items allocated to each player in the product-maximizing allocation.
    """
    num_items = len(valuations[0])  # Number of items

    initial_state = [0, [], []]  # Initial state - empty allocation for both players
    states = deque()  # Queue for saving states
    states.append(initial_state)  # Add initial state

    best_alloc = None
    final_allocations = set()  # Set of fair allocations with num_items items allocated

    player1_values = valuations[0]
    player2_values = valuations[1]

    while states:  # While there are states to explore
        state = states.popleft()
        num_allocated, player1_alloc, player2_alloc = state  # Unpack state

        remaining_items = set(range(num_items)) - set(player1_alloc + player2_alloc)

        if apply_pruning_rule(state, player1_values, player2_values, remaining_items, purging_rule1, purging_rule2):
            if num_allocated == num_items:  # If the allocation is complete
                final_allocations.add((len(player1_alloc) + len(player2_alloc), tuple(sorted(player1_alloc)),
                                       tuple(sorted(player2_alloc))))
            else:
                explore_next_states(states, state, remaining_items, purging_rule2)

    best_alloc = find_best_allocation_product(final_allocations, valuations)

    print_allocation(best_alloc, valuations)


if __name__ == "__main__":
    doctest.testmod()
    # egalitarian_allocation([[4, 5, 6, 7, 8], [8, 7, 6, 5, 4]], purging_rule1=True, purging_rule2=True)
    # product_maximizing_allocation([[4, 5, 6, 7, 8], [8, 7, 6, 5, 4]], purging_rule1=True, purging_rule2=True)
