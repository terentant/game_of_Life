import pygame as pg
import tkinter as tk
import sys
import os
import random

BLACK = (0, 0, 0)
GREY = (200, 200, 200)
WHITE = (255, 255, 255)
blockSize = 20
borderSize = blockSize // 10
N_ROWS = 18
N_COLUMNS = 32
pg_height = N_ROWS * (blockSize + borderSize) - borderSize
pg_width = N_COLUMNS * (blockSize + borderSize) - borderSize
GENERATION = 0
PLAY = True
tick = 500

C1 = [[False] * N_ROWS for _ in range(N_COLUMNS)]
C2 = [[False] * N_ROWS for _ in range(N_COLUMNS)]

CELLS = [C1,  C2]


def coordinates(position):
    return position[0] // (blockSize + borderSize), \
           position[1] // (blockSize + borderSize)


def draw_grid():
    for x in range(N_COLUMNS):
        pg.draw.line(screen, GREY,
                     [0, x * (blockSize + borderSize) + blockSize],
                     [N_COLUMNS * (blockSize + borderSize) - borderSize,
                      x * (blockSize + borderSize) + blockSize],
                     borderSize)
        for y in range(N_ROWS):
            rect = pg.Rect(x * (blockSize + borderSize),
                           y * (blockSize + borderSize),
                           blockSize, blockSize)
            pg.draw.rect(screen, BLACK if CELLS[GENERATION][x][y] else WHITE, rect)
    for y in range(N_COLUMNS):
        pg.draw.line(screen, GREY,
                     [y * (blockSize + borderSize) + blockSize, 0],
                     [y * (blockSize + borderSize) + blockSize,
                      N_ROWS * (blockSize + borderSize) - borderSize],
                     borderSize)


def new_generation():
    global GENERATION
    # print('~' * 32)
    # for y in range(N_ROWS):
    #     for x in range(N_COLUMNS):
    #         print(int(CELLS[GENERATION][x][y]), end=' ')
    #     print()
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


root = tk.Tk()
embed_pygame = tk.Frame(root, width=pg_width, height=pg_height)
embed_pygame.pack(side=tk.TOP)

os.environ['SDL_WINDOWID'] = str(embed_pygame.winfo_id())
os.environ['SDL_VIDEODRIVER'] = 'windib'
pg.display.init()
screen = pg.display.set_mode((pg_width, pg_height))
screen.fill(WHITE)


def play_pause(menu):
    global PLAY
    if PLAY:
        menu.entryconfig(5, label="Play")
    else:
        menu.entryconfig(5, label="Pause")
    PLAY = not PLAY


def speed(n):
    global tick
    tick = 500 if tick == 4000 or tick < 70 else int(tick * n)


def random_field():
    global CELLS
    CELLS[GENERATION] = [[random.choice([True, False])
                          for _ in range(N_ROWS)]
                         for _ in range(N_COLUMNS)]


def blank_field():
    global CELLS
    CELLS[GENERATION] = [[False] * N_ROWS for _ in range(N_COLUMNS)]


def filled_field():
    global CELLS
    CELLS[GENERATION] = [[True] * N_ROWS for _ in range(N_COLUMNS)]


def glider():
    global CELLS
    CELLS[GENERATION] = [[False] * N_ROWS for _ in range(N_COLUMNS)]
    CELLS[GENERATION][2][5] = True
    CELLS[GENERATION][3][3] = True
    CELLS[GENERATION][3][5] = True
    CELLS[GENERATION][4][4] = True
    CELLS[GENERATION][4][5] = True


main_menu = tk.Menu()

window_menu = tk.Menu(tearoff=0)
window_menu.add_command(label="Change dimensions")
window_menu.add_separator()
window_menu.add_command(label="Random", command=random_field)
window_menu.add_command(label="Blank", command=blank_field)
window_menu.add_command(label="Filled", command=filled_field)
main_menu.add_cascade(label="Window", menu=window_menu)

figures_menu = tk.Menu(tearoff=0)
figures_menu.add_command(label="Glider", command=glider)
main_menu.add_cascade(label="Figures", menu=figures_menu)

main_menu.add_command(label="   |   ", activebackground=main_menu.cget("background"))
main_menu.add_command(label="Slower", command=lambda: speed(2))
main_menu.add_command(label="Pause", command=lambda: play_pause(main_menu))
main_menu.add_command(label="Faster", command=lambda: speed(0.5))
root.config(menu=main_menu)


def pygame_loop():
    global tick
    screen.fill(WHITE)
    draw_grid()
    pg.display.flip()
    root.update()
    if PLAY:
        new_generation()
    for event in pg.event.get():
        if event.type == pg.QUIT:
            sys.exit()
        if event.type == pg.MOUSEBUTTONDOWN and event.button == 1:
            x, y = coordinates(event.pos)
            CELLS[GENERATION][x][y] = not CELLS[GENERATION][x][y]

    pg.display.update()
    root.after(tick, pygame_loop)


pygame_loop()
tk.mainloop()
