import pygame as pg
import tkinter as tk
import os
import random
from figures import *

BLACK = (0, 0, 0)
GREY = (200, 200, 200)
WHITE = (255, 255, 255)
blockSize = 16
borderSize = blockSize // 10
N_ROWS = 36
N_COLUMNS = 64
pg_height = N_ROWS * (blockSize + borderSize) - borderSize
pg_width = N_COLUMNS * (blockSize + borderSize) - borderSize
GENERATION = 0
PLAY = True
tick = 500

CELLS = [[[False] * N_ROWS for _ in range(N_COLUMNS)],
         [[False] * N_ROWS for _ in range(N_COLUMNS)]]


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
root.title("Conway's Game of Life")
embed_pygame = tk.Frame(root, width=pg_width, height=pg_height)
embed_pygame.pack(side=tk.TOP)

os.environ['SDL_WINDOWID'] = str(embed_pygame.winfo_id())
os.environ['SDL_VIDEODRIVER'] = 'windib'
pg.display.init()
screen = pg.display.set_mode((pg_width, pg_height))
screen.fill(WHITE)


def set_dimensions(rows, columns, pixels):
    global blockSize, borderSize, N_ROWS, N_COLUMNS, pg_height, \
        pg_width, CELLS, screen, embed_pygame
    N_ROWS = rows if rows > 10 else 10
    N_COLUMNS = columns if columns > 10 else 10
    blockSize = pixels if pixels > 4 else 4
    borderSize = blockSize // 10 if blockSize >= 10 else 1
    pg_height = N_ROWS * (blockSize + borderSize) - borderSize
    pg_width = N_COLUMNS * (blockSize + borderSize) - borderSize
    CELLS = [[[False] * N_ROWS for _ in range(N_COLUMNS)],
             [[False] * N_ROWS for _ in range(N_COLUMNS)]]
    embed_pygame.configure(width=pg_width, height=pg_height)


def dimensions():
    dimension_window = tk.Tk()
    dimension_window.title("Change dimensions")

    tk.Label(dimension_window, text=f'Now there are {N_ROWS} rows'
                                    f', and  {N_COLUMNS} columns').pack(side=tk.TOP, anchor=tk.W)
    tk.Label(dimension_window, text=f'With size of'
                                    f' the cell {blockSize} pixels').pack(side=tk.TOP, anchor=tk.W)

    rows_frame = tk.Frame(dimension_window)
    rows_entry = tk.Entry(rows_frame)
    rows_entry.insert(0, N_ROWS)
    rows_entry.pack(side=tk.LEFT, anchor=tk.W)
    tk.Label(rows_frame, text='Rows', padx=10).pack(side=tk.LEFT)
    rows_frame.pack(side=tk.TOP, anchor=tk.W)

    columns_frame = tk.Frame(dimension_window)
    columns_entry = tk.Entry(columns_frame)
    columns_entry.insert(0, N_COLUMNS)
    columns_entry.pack(side=tk.LEFT, anchor=tk.W)
    tk.Label(columns_frame, text='Columns', padx=10).pack(side=tk.LEFT)
    columns_frame.pack(side=tk.TOP, anchor=tk.W)

    pixels_frame = tk.Frame(dimension_window)
    pixels_entry = tk.Entry(pixels_frame)
    pixels_entry.insert(0, blockSize)
    pixels_entry.pack(side=tk.LEFT, anchor=tk.W)
    tk.Label(pixels_frame, text='Pixels for cell', padx=10).pack(side=tk.LEFT)
    pixels_frame.pack(side=tk.TOP, anchor=tk.W)

    def comma():
        set_dimensions(int(rows_entry.get()),
                       int(columns_entry.get()),
                       int(pixels_entry.get()))
        dimension_window.destroy()

    change_button = tk.Button(dimension_window, text='Change!', command=comma)
    change_button.pack(side=tk.TOP)


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


def figure(name):
    global CELLS
    CELLS[GENERATION] = [[False] * N_ROWS for _ in range(N_COLUMNS)]
    for cell in figures_dict[name]:
        CELLS[GENERATION][cell[0]][cell[1]] = True


main_menu = tk.Menu()

window_menu = tk.Menu(tearoff=0)
window_menu.add_command(label="Change dimensions", command=dimensions)
window_menu.add_separator()
window_menu.add_command(label="Random", command=random_field)
window_menu.add_command(label="Blank", command=blank_field)
window_menu.add_command(label="Filled", command=filled_field)
main_menu.add_cascade(label="Window", menu=window_menu)

figures_menu = tk.Menu(tearoff=0)
spaceships_menu = tk.Menu(tearoff=0)
figures_menu.add_cascade(label="Spaceships", menu=spaceships_menu)
spaceships_menu.add_command(label="Glider",
                            command=lambda: figure('glider'))
spaceships_menu.add_command(label="Lightweight spaceship",
                            command=lambda: figure('lightweight'))
spaceships_menu.add_command(label="Middleweight spaceship",
                            command=lambda: figure('middleweight'))
spaceships_menu.add_command(label="Heavyweight spaceship",
                            command=lambda: figure('heavyweight'))
spaceships_menu.add_command(label="Dart",
                            command=lambda: figure('dart'))
oscillators_menu = tk.Menu(tearoff=0)
figures_menu.add_cascade(label="Oscillators", menu=oscillators_menu)
oscillators_menu.add_command(label="Blinker",
                             command=lambda: figure('blinker'))
oscillators_menu.add_command(label="Blinker побольше",
                             command=lambda: figure('blinkerB'))
oscillators_menu.add_command(label="Pulsar",
                             command=lambda: figure('pulsar'))
oscillators_menu.add_command(label="Unix",
                             command=lambda: figure('unix'))
oscillators_menu.add_command(label="Figure eight",
                             command=lambda: figure('eight'))
figures_menu.add_command(label="Gosper glider gun",
                         command=lambda: figure('The Gun'))
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
        if event.type == pg.MOUSEBUTTONDOWN and event.button == 1:
            x, y = coordinates(event.pos)
            # print(f'({x}, {y}),', end=' ')
            CELLS[GENERATION][x][y] = not CELLS[GENERATION][x][y]

    pg.display.update()
    root.after(tick, pygame_loop)


pygame_loop()
tk.mainloop()
