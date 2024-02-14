import networkx as nx


def find_shortest_path(graph, start_node, end_node):
    """
    Finds the shortest path between two nodes in a weighted graph.

    Args:
        graph (nx.Graph): The networkx graph object.
        start_node (str): The starting node.
        end_node (str): The ending node.

    Returns:
        tuple: A tuple containing the total weight of the shortest path and
               a list of edges along the path with their weights.

    Example:
    >>> edges = [("A", "B", {"weight": 3}), ("B", "C", {"weight": 2}), ("C", "D", {"weight": 1})]
    >>> G = nx.Graph()
    >>> G.add_edges_from(edges)
    >>> find_shortest_path(G, 'A', 'D')
    (6, [('A', 'B', 3), ('B', 'C', 2), ('C', 'D', 1)])
    """

    # Check if start_node and end_node are in the graph
    if not graph.has_node(start_node) or not graph.has_node(end_node):
        raise ValueError("Start or end node not found in the graph.")

    try:
        # Calculate the shortest path and its weight
        shortest_path = nx.shortest_path(graph, start_node, end_node, weight="weight")
        shortest_path_weight = sum(graph[u][v]["weight"] for u, v in zip(shortest_path, shortest_path[1:]))
        # Extract edges and their weights along the shortest path
        edge_weights = [(u, v, graph[u][v]["weight"]) for u, v in zip(shortest_path, shortest_path[1:])]
        return shortest_path_weight, edge_weights

    except nx.NetworkXNoPath:
        return None, None


def vcg_cheapest_path(graph, start_node, end_node):
    """
    Explores alternative shortest paths by iteratively removing edges from the original shortest path.

    Args:
        graph (nx.Graph): The networkx graph object.
        start_node (str): The starting node.
        end_node (str): The ending node.

    Example:
    >>> edges = [("A", "B", {"weight": 3}),("A", "C", {"weight": 5}),("A", "D", {"weight": 10}),("B", "C", {"weight": 1}),("C", "D", {"weight": 1}),("B", "D", {"weight": 4}),]
    >>> G = nx.Graph()
    >>> G.add_edges_from(edges)
    >>> vcg_cheapest_path(G, 'A', 'D')
    Original shortest path: [('A', 'B', 3), ('B', 'C', 1), ('C', 'D', 1)]
    Original shortest path weight: 5
    After removing ('A', 'B'):
      New path: [('A', 'C', 5), ('C', 'D', 1)]
      Weight difference: -4
    After removing ('B', 'C'):
      New path: [('A', 'C', 5), ('C', 'D', 1)]
      Weight difference: -2
    After removing ('C', 'D'):
      New path: [('A', 'B', 3), ('B', 'D', 4)]
      Weight difference: -3
    """

    # Find the original shortest path
    shortest_path_weight, shortest_path = find_shortest_path(graph, start_node, end_node)
    if not shortest_path:
        print("No path found between", start_node, "and", end_node)
        return

    print("Original shortest path:", shortest_path)
    print("Original shortest path weight:", shortest_path_weight)

    for edge in shortest_path:
        removed_edge = edge[0], edge[1]
        graph_copy = graph.copy()
        graph_copy.remove_edge(*removed_edge)

        # Find the new shortest path after removing the edge
        new_weight, new_path = find_shortest_path(graph_copy, start_node, end_node)
        # Calculate the weight difference
        weight_difference = shortest_path_weight - (
                    new_weight + graph.get_edge_data(removed_edge[0], removed_edge[1]).get('weight'))

        if new_path:
            print(f"After removing {removed_edge}:")
            print(f"  New path:", new_path)
        else:
            print(f"After removing {removed_edge}: No path found.")
        print(f"  Weight difference:", weight_difference)


if __name__ == "__main__":
    import doctest
    doctest.testmod()