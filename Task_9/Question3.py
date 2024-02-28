import networkx as nx
import matplotlib.pyplot as plt


def find_decomposition(budget, preferences):
    n = len(preferences)  # Number of persons

    total_budget = sum(budget)

    G = nx.DiGraph()  # Create a directed graph

    # Add nodes for persons and subjects
    for i in range(n):
        G.add_node('p' + str(i))  # Person node
    for j in range(len(budget)):
        G.add_node('s' + str(j))  # Subject node

    # Add edges from source 's' to persons with capacity c/n
    for i in range(n):
        G.add_edge('s', 'p' + str(i), capacity=total_budget / n)

    # Add edges from persons to subjects based on preferences
    for i, person_pref in enumerate(preferences):
        for subject in person_pref:
            G.add_edge('p' + str(i), 's' + str(subject), capacity=total_budget / n)

    # Add edges from subjects to sink 't' with capacity equal to the subject's budget
    for j, subj_budget in enumerate(budget):
        G.add_edge('s' + str(j), 't', capacity=subj_budget)

    # Draw the graph for visualization
    pos = nx.spring_layout(G)
    nx.draw(G, pos, with_labels=True, node_size=800)
    labels = nx.get_edge_attributes(G, 'capacity')
    nx.draw_networkx_edge_labels(G, pos, edge_labels=labels)
    plt.show()

    # Find the maximum flow in the network
    max_flow_value, max_flow_dict = nx.maximum_flow(G, 's', 't')

    decomposition = []

    # Check if the maximum flow equals the total budget
    if max_flow_value != total_budget:
        print("Budget is not decomposed.")

    else:
        # Decompose the flow and update the decomposition matrix
        for i in range(len(preferences)):
            row = []
            for j in range(len(budget)):
                flow_value = max_flow_dict.get('p' + str(i), {}).get('s' + str(j),
                                                                     0)  # Get the flow value from person i to subject j
                row.append(flow_value)
            decomposition.append(row)

        print("Decomposition:")
        for i, row in enumerate(decomposition):
            for j, val in enumerate(row):
                if val > 0:
                    print(f"Person {i} contributes {val} to Subject {j}")

    return decomposition


if __name__ == "__main__":
    # Example from the task
    budget = [400, 50, 50, 0]
    preferences = [{0, 1}, {0, 2}, {0, 3}, {1, 2}, {0}]

    # budget = [300, 200, 100, 50]
    # preferences = [{0, 1, 2}, {0, 2, 3}, {1, 3}, {0, 1, 2}]
    #
    # budget = [400, 300, 200]
    # preferences = [{0, 1}, {0, 2}, {1}]

    # # budget that cannot be decomposed
    # budget = [50, 10, 0]
    # preferences = [{0, 1}, {1, 2}, {0, 2}]

    # # a simple change from the previous example to make it decomposable
    # budget = [50, 10, 0]
    # preferences = [{0, 1}, {0, 1}, {0, 2}]

    find_decomposition(budget, preferences)
