import numpy as np


def weighted_round_robin(rights: list[float], valuations: list[list[float]], y: float):
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


# if __name__ == "__main__":
#     weighted_round_robin(
#         rights=[1, 2, 4],
#         valuations=[[11, 11, 22, 33, 44], [11, 22, 44, 55, 66], [11, 33, 22, 11, 66]],
#         y=0.5)
