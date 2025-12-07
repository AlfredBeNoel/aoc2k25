import os
import time

def day1_helper(turns, direction, pointer):
    action = -1 if direction == "L" else 1
    count = 0

    pointer += action * turns
    pointer %= 100
    if pointer == 0:
        count += 1
    return count, pointer


def day2_helper(turns, direction, pointer):
    action = -1 if direction == "L" else 1
    cross = 0

    # full circle turns
    cross += turns // 100

    # last remaining turns
    remainder = turns % 100
    if remainder > 0:
        was_0 = pointer == 0
        pointer += action * remainder
        if pointer >= 100 or pointer <= 0:
            if (not was_0):
                cross += 1
            pointer = pointer % 100
            
    return cross, pointer

def main(input_path):
    count = 0
    pointer = 50
    # day 1
    with open(input_path, "r") as f:
        for line in f:
            turns = int(line[1:])
            curr, pointer = day1_helper(turns, line[0], pointer)
            count += curr
    print(count)
    

    cross = 0
    pointer = 50
    # day 2
    with open(input_path, "r") as f:
        for line in f:
            turns = int(line[1:])
            currCross, pointer = day2_helper(turns, line[0], pointer)
            cross += currCross
    print(cross)

if __name__ == "__main__":
    input_path = os.path.join(os.path.dirname(__file__), "input.txt")
    main(input_path)