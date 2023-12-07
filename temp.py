import random

CELLS = [[random.choice([True, False]) for _ in range(10)] for _ in range(3)]
for i in range(3):
    for j in range(10):
        print(CELLS[i][j], end=' ')
    print()
print(CELLS[-1][1]+ sum(CELLS[0][0:2]))

xs = [x for x in range(10)]
print(xs)
print(xs[-1:3])