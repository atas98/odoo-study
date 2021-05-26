# -*- coding: utf-8 -*-

# Task 1
### Create a method that sums every 3rd, 5th, and 9th integer of list
def sums(numbers, sum_positions=(3, 5, 9)):
    return tuple(sum(number for i, number in enumerate(numbers) if i%pos == 0) for pos in sum_positions)

# Task 2
### ?? Someth about dicts sorts(desc) and keys

if __name__ == "__main__":
    numbers = list(range(1, 101))
    print(sums(numbers))