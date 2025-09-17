import json


def find_nearest_number(numbers, target):
    larger_numbers = [num for num in numbers if num > target]
    if larger_numbers:
        return min(larger_numbers, key=lambda x: abs(x - target))
    elif len(numbers) == 1:
        return -1
    return min(numbers, key=lambda x: abs(x - target))


def tuples_to_ints(tuple_list):
    return [item[0] for item in tuple_list]
