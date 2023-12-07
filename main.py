import pygame as pg
import sys
import random

BLACK = (0, 0, 0)
GREY = (200, 200, 200)
WHITE = (255, 255, 255)
blockSize = 20
WINDOW_HEIGHT = 400
N_ROWS = 16
WINDOW_WIDTH = 400
N_COLUMNS = 9
GENERATION = 0

C = [[random.choice([True, False])
            for _ in range(N_COLUMNS)]
           for _ in range(N_ROWS)]
CELLS = [C,C]
# for i in range(16):
#     for j in range(9):
#         print(CELLS[i][j], end=' ')
#     print()


def main():
    global SCREEN, CLOCK
    pg.init()
    SCREEN = pg.display.set_mode(
        (N_ROWS * blockSize, N_COLUMNS * blockSize))
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
    for x in range(N_ROWS):
        for y in range(N_COLUMNS):
            rect = pg.Rect(x*blockSize, y*blockSize, blockSize, blockSize)
            pg.draw.rect(SCREEN, BLACK if CELLS[GENERATION][x][y] else WHITE, rect)


def newGeneration():
    for x in range(N_ROWS):
        for y in range(N_COLUMNS):
            neightbours = CELLS[GENERATION][x-1][y-1]+\
                          CELLS[GENERATION][x][y-1]+ \
                          CELLS[GENERATION][(x + 1)%N_ROWS][y - 1] + \
                          CELLS[GENERATION][x-1][y] + \
                          CELLS[GENERATION][(x + 1)%N_ROWS][y] + \
                          CELLS[GENERATION][x - 1][(y + 1)%N_COLUMNS] + \
                          CELLS[GENERATION][x][(y + 1)%N_COLUMNS] + \
                          CELLS[GENERATION][(x + 1)%N_ROWS][(y + 1)%N_COLUMNS]

            if neightbours == 3:
                CELLS[1 - GENERATION][x][y] = True
            elif neightbours == 2 and CELLS[GENERATION][x][y]:
                CELLS[1 - GENERATION][x][y] = True
            else:
                CELLS[1 - GENERATION][x][y] = False

main()
