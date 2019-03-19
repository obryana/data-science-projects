import math
import sys

def calculate_squares(area, squares):
    side = math.floor(math.sqrt(area))
    squares.append(side**2)
    if math.sqrt(area) % 1 != 0:
        new_area = area-(side**2)
        calculate_squares(new_area, squares)
    else:
        return

def answer(area):
    squares = []
    calculate_squares(int(area), squares)
    print(squares)

if __name__ == "__main__":
    answer(sys.argv[1])