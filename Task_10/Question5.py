import statistics
from typing import List
import doctest


def create_linear_functions(total_budget: float, threshold: float, num_citizens: int) -> List[float]:
    """
    Creates linear functions based on the threshold and total budget.

    :param total_budget: Total budget for allocation.
    :param threshold: Threshold value for creating linear functions.
    :param num_citizens: Number of citizens.
    :return: List of linear functions.
    """
    linear_functions = []
    for i in range(1, num_citizens):
        linear_functions.append(total_budget * min(1, i * threshold))
    return linear_functions


def merge_votes_with_functions(citizen_votes: List[List[float]], linear_functions: List[float]) -> List[List[float]]:
    """
    Merges citizen votes with linear functions.

    :param citizen_votes: List of lists representing citizen votes on different topics.
    :param linear_functions: List of linear functions.
    :return: Merged list.
    """
    merged_votes = []
    for i in range(len(citizen_votes[0])):
        topic_votes = [citizen[i] for citizen in citizen_votes]
        merged_votes.append(sorted(topic_votes + linear_functions))
    return merged_votes


def binary_search_for_t(total_budget: float, citizen_votes: List[List[float]]) -> List[float]:
    """
    Utilizes binary search to find the optimal threshold for budget allocation.

    :param total_budget: Total budget for allocation.
    :param citizen_votes: List of lists representing citizen votes on different topics.
    """

    start = 0
    end = 1
    num_citizens = len(citizen_votes)

    while end > start:
        threshold = (start + end) / 2
        linear_functions = create_linear_functions(total_budget, threshold, num_citizens)
        merged_votes = merge_votes_with_functions(citizen_votes, linear_functions)

        medians_list = [statistics.median(lst) for lst in merged_votes]
        medians_sum = sum(medians_list)

        if medians_sum < total_budget:
            start = threshold
        elif medians_sum > total_budget:
            end = threshold
        else:
            print("The right t is:", threshold)
            return medians_list


def compute_budget(total_budget: float, citizen_votes: List[List[float]]) -> List[float]:
    """
    Computes the budget allocation based on citizen votes and total budget.

    :param total_budget: Total budget available for allocation.
    :param citizen_votes: List of lists representing citizen votes on different topics.
    :return: List of medians for each topic.

    Examples: (taken from leature)
    >>> citizen_votes = [[100, 0, 0], [0, 0, 100]]
    >>> compute_budget(100, citizen_votes)
    The right t is: 0.5
    [50.0, 0, 50.0]

    >>> citizen_votes = [[0, 0, 6, 0, 0, 6, 6, 6, 6], [0, 6, 0, 6, 6, 6, 6, 0, 0], [6, 0, 0, 6, 6, 0, 0, 6, 6]]
    >>> compute_budget(30, citizen_votes)
    The right t is: 0.06666666666666667
    [2.0, 2.0, 2.0, 4.0, 4.0, 4.0, 4.0, 4.0, 4.0]

    >>> citizen_votes = [[0, 0, 30], [15, 15, 0], [15, 15, 0]]
    >>> compute_budget(30, citizen_votes)
    The right t is: 0.2
    [12.0, 12.0, 6.0]

    >>> citizen_votes = [[3, 0, 27], [0, 20, 10], [15, 15, 0]]
    >>> compute_budget(30, citizen_votes)
    The right t is: 0.2222222222222222
    [6.666666666666666, 13.333333333333332, 10]

    """
    return binary_search_for_t(total_budget, citizen_votes)


if __name__ == "__main__":
    doctest.testmod()
