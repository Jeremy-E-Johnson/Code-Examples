"""
Programmer: Jeremy Johnson
Title: Sum of Four Squares Calculator
Purpose: Takes a natural number input and outputs 4 integers whose squares sum to the input
"""

from math import *
from random import *

def create_list_of_perfect_squares(natural_number):
    """
    :param natural_number: Positive integer
    :return: List of perfect squares whose index is their square root, stops when
    values reach size of input.
    """
    stop_number = int(sqrt(natural_number) + 1)
    retval = []
    for numb in range(0, stop_number):
        retval.append(numb**2)
    return retval


def square_finder(difference, remaining_squares, perfect_squares):
    """
    :param difference: Remaining distance to cover with squares
    :param remaining_squares: Number of squares left to check
    :param perfect_squares: Perfect squares less than target
    :return: List of four or less squares that add up to initial target
    """
    shortened_list = perfect_squares[:int(sqrt(difference)) + 1]
    shortened_list.reverse()
    if remaining_squares > 1:
        for square in shortened_list:
            if square == difference:
                #print 'end found', square
                return True, [square]
            else:
                new_difference = difference - square
                if new_difference < 0:
                    print 'error in difference size'
                #print 'going deeper...', square
                next_level = square_finder(new_difference, remaining_squares - 1, perfect_squares)
                #print next_level
                if next_level[0]:
                    next_level[1].append(square)
                    return True, next_level[1]
                else:
                    continue
        return False, []
    else:
        for square in shortened_list:
            if square == difference:
                #print 'end found`', square
                return True, [square]
            else:
                return False, []


def four_squares(target):
    """
    :param target: Natural number to find as a sum of four squares
    :return: Tuple of numbers that when squared sum to target
    """
    perfect_squares = create_list_of_perfect_squares(target)
    
    for i in range(1, 5): #for searching least squares
        solution = square_finder(target, i, perfect_squares)
        if solution[0]:
            break
        else:
            continue

    #solution = square_finder(target, 4, perfect_squares) #for faster searching
    #print solution
    squares = solution[1]
    numbers = []
    for numb in squares:
        numbers.append(int(sqrt(numb)))
    numbers.reverse()
    #while len(numbers) < 4:
    #   numbers.append(0)
    return numbers


def main():
    input_integer = raw_input('What natural number do you want split into four squares? :')

    try:
        target = int(input_integer)
    except:
        print 'Please input a natural number.'
        target = 0
        main()

    if target < 0 or target != float(input_integer):
        print 'Please input a natural number.'
        main()

    squares = four_squares(target)

    #print squares
    total = 0
    format_list = []
    format_list.extend(squares)
    for numb in squares:
        total += numb**2
        format_list.append(numb**2)
    format_list.append(total)
    format_tuple = tuple(format_list)
    #print format_tuple

    #print squares
    #print len(squares)
    print squares, '=', total
    print format_tuple[0], '^2 +', format_tuple[1], '^2 +', format_tuple[2], '^2 +', format_tuple[3], \
       '^2 =', format_tuple[4], '+', format_tuple[5], '+', format_tuple[6], '+', format_tuple[7], \
       '=', format_tuple[8]  # Really bad print formatting

    repeat = raw_input('Do you want to see another number? (y/n): ')
    if repeat.lower() == 'y' or repeat.lower() == 'yes':
        main()
    else:
        quit()

    main()
#main()

inputs = range(1, 10001)#[randint(0, 10000) for x in range(10)]
dick = {}

for i in inputs:
    dick[i] = len(four_squares(i))

    
