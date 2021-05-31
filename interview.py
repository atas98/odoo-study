# -*- coding: utf-8 -*-

# Task 1
# Create a method that sums every 3rd, 5th, and 9th integer of list
def sums(numbers, sum_positions=(3, 5, 9)):
    return tuple(
        sum(number for i, number in enumerate(numbers) if i % pos == 0)
        for pos in sum_positions
    )

# Task 2
# Return 3 keys with minimum value in decreasing order
from operator import itemgetter

def min_keys(input_dict, length=3, reverse=True):
    return tuple(key
                 for key, _ in sorted(input_dict.items(),
                                      key=itemgetter(1),    
                                      reverse=reverse)[:length])


if __name__ == "__main__":
    # Test task 1
    numbers = list(range(1, 101))
    print(f'task #1: {sums(numbers)}')

    # Test task 2
    input_dict = {i: 20-i for i in range(20)}
    print(input_dict)
    print(f'task #2: {min_keys(input_dict)}')
