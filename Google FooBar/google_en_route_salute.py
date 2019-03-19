def answer(hall_list):
    salutes = 0
    for idx, char in enumerate(hall_list):
        if char == '>':
            for char2 in hall_list[idx+1:]:
                if char2 == '<':
                    salutes+=2
    return salutes

print(answer('>----<'))