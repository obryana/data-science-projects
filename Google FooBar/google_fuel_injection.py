def peek(num_pellets):
    operations_peek = 1
    while num_pellets % 2 == 0:
        num_pellets /= 2
        operations_peek += 1
    return (operations_peek, num_pellets)


def answer(num_pellets):
    num_pellets = int(num_pellets)
    operations = 0
    while num_pellets > 1:
        if num_pellets % 2 == 0:
            num_pellets /= 2
            operations += 1
        else:
            peek_add = peek(num_pellets+1)
            peek_sub = peek(num_pellets-1)
            if peek_add[1] == peek_sub[1]:
                operations += min(peek_add[0],peek_sub[0])
                num_pellets = peek_add[1]
            else:
                if peek_add[0] > peek_sub[0]:
                    operations += peek_add[0]
                    num_pellets = peek_add[1]
                else:
                    operations += peek_sub[0]
                    num_pellets = peek_sub[1]
    return operations
            

print(answer(47))
print(answer(4))
print(answer(15))