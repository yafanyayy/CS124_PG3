import sys
import random
import time

# Global
max_iter=25000

def main():
    # Routine
    if len(sys.argv) != 4:
        print("Usage: partition.py [flag] [algorithm] [inputfile]")
        sys.exit(1)
    if sys.argv[1] == "0":
        f = open(sys.argv[3], "r")
        input = [int(line) for line in f]
        if sys.argv[2] == "0":
            print(karmarkar_karp(input))
        elif sys.argv[2] == "1":
            print(repeated_random(input))
        elif sys.argv[2] == "2":
            print(hill_climbing(input))
        elif sys.argv[2] == "3":
            print(simulated_annealing(input))
        elif sys.argv[2] == "11":
            print(p_repeated_random(input))
        elif sys.argv[2] == "12":
            print(p_hill_climbing(input))
        elif sys.argv[2] == "13":
            print(p_simulated_annealing(input))

# Heap Implementation
def build_heap(input):
    for i in range(len(input)//2, -1, -1):
        max_heapify(input, i)


def max_heapify(array, i):
    try:
        left = array[2 * i + 1]
    except:
        left = None
    try:
        right = array[2 * i + 2]
    except:
        right = None
    if left and left > array[i]:
        max_index = 2 * i + 1
    else:
        max_index = i
    if right and right > array[max]:
        max_index = 2 * i + 2
    if max_index != i:
        array[i], array[max_index] = array[max_index], array[i]
        max_heapify(array, max_index)


def extract_max(array):
    root = array[0]
    array[0] = array[-1]
    # Remove two, add one each time until only a number, which is the residue left
    del array[-1]
    max_heapify(array, 0)
    return root


def insert(array, sum):
    new = len(array)
    array.append(sum)
    while new != 0 and array[(new - 1) // 2] < array[new]:
        array[(new - 1) // 2], array[new] = array[new], array[(new - 1) // 2]
        new = (new - 1) // 2

# Algo
def karmarkar_karp(input):
    build_heap(input)
    while len(input) > 1:
        max1 = extract_max(input)
        max2 = extract_max(input)
        insert(input, max1 - max2)
    return input[0]

def residue(array, solution):
    return abs(sum(array[i] * solution[i] for i in range(len(array))))


def repeated_random(input):
    r = sum(i for i in len(input))
    for i in range(max_iter):
        # The standard representation
        solution = [random.randrange(-1, 2, 2) for i in range(len(input))]
        r1 = residue(input, solution)
        if r1 < r:
            r = r1
    return r


def hill_climbing(input):
    solution = [random.randrange(-1, 2, 2) for i in range(len(input))]
    r = residue(input, solution)
    for i in range(max_iter):
        indices = random.sample(range(len(input)), 2)
        solution[indices[0]] *= -1
        if indices[0] < indices[1]:
        # An index can either be +1 or -1 with possibility of 1/2, so this can be used to represent the probability of 1/2 that we swap the second index
            solution[indices[1]] *= -1
        neighbour = residue(input, solution)
        if neighbour < r:
            r = neighbour
    return r



def simulated_annealing(input):
    solution = [random.randrange(-1, 2, 2) for i in range(len(input))]
    r = r_min = residue(input, solution)
    for i in range(max_iter):
        indices = random.sample(range(len(input)), 2)
        solution[indices[0]] *= -1
        if indices[0] < indices[1]:
        # An index can either be +1 or -1 with possibility of 1/2, so this can be used to represent the probability of 1/2 that we swap the second index
            solution[indices[1]] *= -1
        neighbour = residue(input, solution)
        if neighbour < r:
            r = neighbour
        else random.random() < math.exp(-(neighbour - r) / ((10 ** 10) * (0.8 ** ((i + 1) // 300)))):
            r = neighbour
        if r < r_min:
            r_min = r
    return r_min
