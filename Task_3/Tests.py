import unittest
import random

from Question2 import weighted_round_robin


class TestWRR(unittest.TestCase):
    def test_given_example(self):
        rights = [1, 2, 4]
        valuations = [[11, 11, 22, 33, 44], [11, 22, 44, 55, 66], [11, 33, 22, 11, 66]]
        y = 0.5
        allocation = weighted_round_robin(rights, valuations, y)

        self.assertEqual(len(allocation[0]), 1)
        self.assertEqual(len(allocation[1]), 1)
        self.assertEqual(len(allocation[2]), 3)
        # On the first iteration, Player 2 has the highest quotient,
        # he gets to choose an item first. he chooses item 4
        # which has their maximum value of 66.
        self.assertEqual(valuations[2][allocation[2][0]], 66)

        self.assertEqual(valuations[1][allocation[1][0]], 55)

    def test_randomized_valuations(self):
        rights = [1, 2, 3]
        valuations = []
        for _ in rights:
            valuations.append([random.randint(1, 100) for _ in range(5)])
        y = random.random()
        allocation = weighted_round_robin(rights, valuations, y)

        # Test player 2 gets the item with their max value
        max_value = max(valuations[2])
        self.assertEqual(valuations[2][allocation[2][0]], max_value)

        # Test player 2 gets at least one item
        self.assertGreater(len(allocation[2]), 0)

    def test_duplicate_max_values(self):
        rights = [1, 2, 3]
        valuations = [[10, 10, 5], [10, 7, 6], [10, 10, 10]]
        y = 0.1

        allocation = weighted_round_robin(rights, valuations, y)

        self.assertEqual(allocation[0], [2])
        self.assertEqual(valuations[1][allocation[1][0]], 7)
        self.assertEqual(len(allocation[0]), 1)
        self.assertEqual(len(allocation[1]), 1)
        self.assertEqual(len(allocation[2]), 1)

    def test_3_players_3_identical_items_equal_rights(self):
        rights = [1, 1, 1]
        valuations = [[1, 1, 1], [1, 1, 1], [1, 1, 1]]
        y = 0.1
        allocation = weighted_round_robin(rights, valuations, y)
        self.assertEqual(allocation, [[0], [1], [2]])

    def test_different_items_and_equal_rights(self):
        rights = [1, 1, 1]
        valuations = [[1, 2, 3], [3, 2, 1], [2, 1, 3]]
        y = 0.5
        allocation = weighted_round_robin(rights, valuations, y)
        self.assertEqual(allocation, [[2], [0], [1]])

    def test_3_players_3_identical_items_unequal_rights(self):
        rights = [1, 2, 3]
        valuations = [[1, 1, 1], [1, 1, 1], [1, 1, 1]]
        y = 0.1
        allocation = weighted_round_robin(rights, valuations, y)
        self.assertEqual(allocation[2], [0])
        self.assertEqual(allocation[1], [1])
        self.assertEqual(allocation[0], [2])

    def test_one_item_two_players(self):
        rights = [5, 1]
        valuations = [[10], [5]]
        y = 0.1
        allocation = weighted_round_robin(rights, valuations, y)
        self.assertEqual(allocation, [[0], []])

    def test_one_player_three_items(self):
        rights = [1]
        valuations = [[5, 3, 7]]
        y = 0.1
        allocation = weighted_round_robin(rights, valuations, y)
        # Test the order of allocation
        self.assertEqual(allocation, [[2, 0, 1]])

    def test_three_players_no_items(self):
        rights = [1, 1, 1]
        valuations = [[], [], []]
        y = 0.1
        allocation = weighted_round_robin(rights, valuations, y)
        self.assertEqual(allocation, [[], [], []])


if __name__ == '__main__':
    unittest.main()
