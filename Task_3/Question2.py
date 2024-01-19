import numpy as np


"""
Question 2: Weighted Round-Robin Algorithm

Implement the weighted round-robin algorithm for distributing items among players. 

The algorithm takes three inputs:
@rights: A list of player rights, indicating the allocation rights for each player. 
@valuations: A list of player valuations for each item, representing the preferences of each player for the available items.
@y: A balancing parameter that influences the allocation strategy.

In each iteration, the algorithm selects the player with the highest quotient of rights divided by (items_per_player + y) and gives that player the item with the highest value. 
If there are multiple items with the same value, the algorithm prioritizes the item with 
the lowest index. In cases where multiple players have the same quotient, the algorithm assigns the item to the 
player with the lowest index.

The output is a list of lists, representing the final allocation of items to players.
"""


def weighted_round_robin(rights: list[float], valuations: list[list[float]], y: float):
    """
       Allocates items to players using a weighted round-robin algorithm.

       Parameters:
       - rights (list): List of rights for each player.
       - valuations (list): List of lists representing player valuations for each item.
       - y (float): Balancing parameter.

       Returns:
       - list: Allocation of items to players.

       Examples:

       Deffrent rights and different valuations
       >>> weighted_round_robin([1, 2, 3],[[10, 10, 5], [10, 7, 6], [10, 10, 10]], 0.1)
       Player 2 takes item 0 with value 10
       Player 1 takes item 1 with value 7
       Player 0 takes item 2 with value 5
       [[2], [1], [0]]

       Equal rights and  valuations
       >>> weighted_round_robin([1, 1, 1], [[1, 1, 1], [1, 1, 1], [1, 1, 1]], 0.1)
       Player 0 takes item 0 with value 1
       Player 1 takes item 1 with value 1
       Player 2 takes item 2 with value 1
       [[0], [1], [2]]

       Equal rights and different valuations
       >>> weighted_round_robin([1, 1, 1], [[1, 2, 3], [3, 2, 1], [2, 1, 3]], 0.5)
       Player 0 takes item 2 with value 3
       Player 1 takes item 0 with value 3
       Player 2 takes item 1 with value 1
       [[2], [0], [1]]

       """
    if len(valuations) == 0 or len(rights) == 0:
        return []

    n_players = len(rights)
    n_items = len(valuations[0])

    # Initialize empty allocation for each player
    allocation = [[] for _ in range(n_players)]

    # Track remaining items to allocate
    remaining = [True] * n_items

    while any(remaining):
        # Calculate the number of items allocated to each player
        items_per_player = np.array([len(a) for a in allocation])

        # Calculate the quotients for each player
        quotients = rights / (items_per_player + y)

        best_player = np.argmax(quotients)
        best_item = find_best_item(valuations[best_player], remaining)

        # Allocate the best item if found
        if best_item is not None:
            print(f"Player {best_player} takes item {best_item} with value {valuations[best_player][best_item]}")
            allocation[best_player].append(best_item)
            remaining[best_item] = False

    return allocation


def find_best_item(player_valuations, remaining_items):
    best_item = -1
    best_value = -1

    # Iterate over player valuations to find the best item
    for j in range(len(player_valuations)):
        # Check if the item is available and has a higher value
        if remaining_items[j] and player_valuations[j] > best_value:
            best_item = j
            best_value = player_valuations[j]

    return best_item


if __name__ == "__main__":
    import doctest

    doctest.testmod()
