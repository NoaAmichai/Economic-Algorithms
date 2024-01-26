import time
import matplotlib.pyplot as plt
from first_answer import egalitarian_allocation


# Function to measure the runtime of egalitarian_allocation for a given number of items and purging rules
def measure_runtime(num_items, purging_rule1, purging_rule2):
    valuations = [[1] * num_items, [2] * num_items]  # Example valuations for equal values for all items
    start_time = time.time()
    egalitarian_allocation(valuations, puring_rule1=purging_rule1, puring_rule2=purging_rule2)
    end_time = time.time()
    return end_time - start_time


# Generate data points for different numbers of items and purging rule combinations
num_items_range = [2, 4, 6, 7]  # Range of number of items to test
purging_rule_combinations = [(True, True), (False, True), (True, False), (False, False)]
plot_labels = ["puring_rule1=True, puring_rule2=True",
               "puring_rule1=False, puring_rule2=True",
               "puring_rule1=True, puring_rule2=False",
               "puring_rule1=False, puring_rule2=False"]

# Plot the data for each combination of purging rules
for i, (purging_rule_combination, label) in enumerate(zip(purging_rule_combinations, plot_labels)):
    runtimes = [measure_runtime(num_items, *purging_rule_combination) for num_items in num_items_range]
    plt.plot(num_items_range, runtimes, linestyle='-', label=label)

# Show legend and labels
plt.title('Runtime of egalitarian_allocation for different purging rule combinations', fontsize=14)
plt.xlabel('Number of items', fontsize=12)
plt.ylabel('Runtime (seconds)', fontsize=12)
plt.legend(fontsize=10)
plt.tight_layout()  # Adjust layout to prevent overlap
plt.savefig('runtime_plot.png')  # Save plot to file
plt.show()
