import doctest
import networkx as nx


def is_pareto_efficient(valuations: list[list[float]], allocation: list[list[float]]) -> bool:
    """
       Check if the given allocation is Pareto efficient based on the provided valuations.

       Args:
       valuations (List[List[float]]): List of lists representing valuations of players for items.
       allocation (List[List[float]]): List of lists representing the allocation of items to players.

       Returns:
       bool: True if the allocation is Pareto efficient, False otherwise.

       Examples:
        >>> is_pareto_efficient([[10, 20, 30, 40], [40, 30, 20, 10]], [[0, 0.7, 1, 1], [1, 0.3, 0, 0]])
        The allocation is Pareto efficient
        True

        # Ami, Tami and Rami examples from the lecture
        >>> is_pareto_efficient([[3, 1, 6], [6, 3, 1], [1, 6, 3]], [[1, 0, 0], [0, 1, 0], [0, 0, 1]])
        0 -> 1 (0.50)
        1 -> 2 (0.50)
        2 -> 0 (0.50)
        The allocation is not Pareto efficient, the cycle is: [0, 1, 2] and the product is: 0.125
        The improved allocation is: [[0.99, 0, 0.01], [0.01, 0.99, 0], [0, 0.01, 0.99]]
        False

        >>> is_pareto_efficient([[3, 1, 6], [6, 3, 1], [1, 6, 3]], [[0, 0, 1], [1, 0, 0], [0, 1, 0]])
        The allocation is Pareto efficient
        True

    """

    # Base case: if one of the items is not allocated to any player, the allocation is not Pareto efficient
    for item in range(len(valuations[0])):
        if sum(allocation[i][item] for i in range(len(valuations))) == 0:
            print("The allocation is not Pareto efficient, one of the items is not allocated to any player")
            return False

    num_players = len(valuations)
    graph = nx.DiGraph()

    # Create directed graph: each node represents a player
    graph.add_nodes_from(range(num_players))

    # Add edges: weight is minimum ratio between player i and player j where i receives part of the item
    for i in range(num_players):
        for j in range(num_players):
            if i != j:
                graph.add_edge(i, j, weight=min(
                    valuations[i][k] / valuations[j][k] for k in range(num_players) if allocation[i][k] != 0))

    # Check Pareto efficiency: product of weights in cycles should be >= 1
    for cycle in nx.simple_cycles(graph):
        product = 1
        for i in range(len(cycle)):
            u, v = cycle[i], cycle[(i + 1) % len(cycle)]  # Current edge (u, v)
            product *= graph.edges[u, v]['weight']
        if product < 1:
            # Print arrows indicating the direction of edges
            for i in range(len(cycle)):
                u, v = cycle[i], cycle[(i + 1) % len(cycle)]  # Current edge (u, v)
                print(f"{u} -> {v} ({graph.edges[u, v]['weight']:.2f})")

            print("The allocation is not Pareto efficient, the cycle is: " + str(cycle) + " and the product is: " + str(
                product))

            # Send the cycle to improve_allocation function to find and improve allocation
            improve_allocation(valuations, allocation, cycle)

            return False  # This current allocation is not Pareto efficient

    print("The allocation is Pareto efficient")
    return True  # Pareto efficient


def improve_allocation(valuations, current_allocation, cycle):
    """
        Improve the allocation by redistributing items within the given cycle.

        Args:
        valuations (List[List[float]]): List of lists representing valuations of players for items.
        current_allocation (List[List[float]]): Current allocation of items to players.
        cycle (List[int]): List of player indices forming a cycle in the graph.

        Returns:
        List[List[float]]: The improved allocation after redistribution.
    """

    num_items = len(valuations[0])

    # Define the minimum transfer amount
    min_transfer_amount = 0.01  # You can Adjust this value

    # Iterate over the players in the cycle and redistribute items
    for i in range(len(cycle)):
        player_from = cycle[i]
        player_to = cycle[(i + 1) % len(cycle)]  # Next player in the cycle

        # Iterate over the items and redistribute them
        for item in range(num_items):
            # Check if the player has the item and transfer a minimum amount
            if current_allocation[player_from][item] > min_transfer_amount:
                transfer_amount = min_transfer_amount
                current_allocation[player_from][item] -= transfer_amount
                current_allocation[player_to][item] += transfer_amount
                break  # Move to the next player after transferring an item

    print("The improved allocation is: " + str(current_allocation))
    return current_allocation


if __name__ == '__main__':
    doctest.testmod()
