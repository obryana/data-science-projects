from fractions import Fraction

def calc_first_radius(pegs):
    subtotal = 0
    for i in range(1, len(pegs)-1):
        subtotal += 2 * (-1)**(i+1) * pegs[i]
    return subtotal

def calc_next_radius(pegs, length_pegs, radius):
    current_radius = radius
    for i in range(0, length_pegs-2):
        midpoint = pegs[i+1] - pegs[i]
        next_radius = midpoint - current_radius
        if (current_radius < 1 or next_radius < 1):
            return [-1, -1]
        else:
            current_radius = next_radius

def answer(pegs):
    length_pegs = len(pegs)
    subtotal = calc_first_radius(pegs)
    if length_pegs % 2 == 0:
        multiplier = pegs[length_pegs-1] - pegs[0]
        radius = Fraction((float(multiplier+subtotal)/3)*(2)).limit_denominator()
    else:
        multiplier = - pegs[length_pegs-1] - pegs[0]
        radius = Fraction(float(multiplier+subtotal)*(2)).limit_denominator()
    radius_check = calc_next_radius(pegs, length_pegs, radius)
    if radius_check == [-1, -1]:
        return [-1, -1]
    return [radius.numerator, radius.denominator]