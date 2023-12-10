import pygame as pg
import sys
import random

BLACK = (0, 0, 0)
GREY = (200, 200, 200)
WHITE = (255, 255, 255)
blockSize = 20
WINDOW_HEIGHT = 400
N_ROWS = 9
WINDOW_WIDTH = 400
N_COLUMNS = 16
GENERATION = 0
# random
# C = [[random.choice([True, False])
#             for _ in range(N_ROWS)]
#            for _ in range(N_COLUMNS)]

C1 = [[False] * N_ROWS for _ in range(N_COLUMNS)]
C2 = [[False] * N_ROWS for _ in range(N_COLUMNS)]
C1[2][5] = True
C1[3][3] = True
C1[3][5] = True
C1[4][4] = True
C1[4][5] = True

CELLS = [C1,  C2]
# for i in range(16):
#     for j in range(9):
#         print(CELLS[i][j], end=' ')
#     print()


def main():
    global SCREEN, CLOCK
    pg.init()
    SCREEN = pg.display.set_mode(
        (N_COLUMNS * blockSize, N_ROWS * blockSize))
    CLOCK = pg.time.Clock()
    SCREEN.fill(WHITE)

    while True:
        drawGrid()
        pg.time.delay(500)
        newGeneration()
        for event in pg.event.get():
            if event.type == pg.QUIT:
                sys.exit()

        pg.display.update()


def drawGrid():
    for x in range(N_COLUMNS):
        for y in range(N_ROWS):
            rect = pg.Rect(x*blockSize, y*blockSize, blockSize, blockSize)
            pg.draw.rect(SCREEN, BLACK if CELLS[GENERATION][x][y] else WHITE, rect)


def newGeneration():
    global GENERATION
    for y in range(N_ROWS):
        for x in range(N_COLUMNS):
            neighbours = CELLS[GENERATION][(x - 1) % N_COLUMNS][(y - 1) % N_ROWS] \
                         + CELLS[GENERATION][x % N_COLUMNS][(y - 1) % N_ROWS] \
                         + CELLS[GENERATION][(x + 1) % N_COLUMNS][(y - 1) % N_ROWS] \
                         + CELLS[GENERATION][(x - 1) % N_COLUMNS][y % N_ROWS] \
                         + CELLS[GENERATION][(x + 1) % N_COLUMNS][y % N_ROWS] \
                         + CELLS[GENERATION][(x - 1) % N_COLUMNS][(y + 1) % N_ROWS] \
                         + CELLS[GENERATION][x % N_COLUMNS][(y + 1) % N_ROWS] \
                         + CELLS[GENERATION][(x + 1) % N_COLUMNS][(y + 1) % N_ROWS]
            if neighbours == 3:
                CELLS[1 - GENERATION][x][y] = True
            elif neighbours == 2 and CELLS[GENERATION][x][y]:
                CELLS[1 - GENERATION][x][y] = True
            else:
                CELLS[1 - GENERATION][x][y] = False
    GENERATION = 1 - GENERATION


main()
