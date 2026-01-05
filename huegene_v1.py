import numpy as np
import pygame as pg
import sys

from core import save_screen

pg.init()

screen_width, screen_height = 2000, 1000
screen = pg.display.set_mode((screen_width, screen_height))

pixels = np.zeros((screen_width, screen_height, 3), dtype=np.uint8)

rand_x = np.random.randint(0, screen_width)
rand_y = np.random.randint(0, screen_height)
pixels[rand_x, rand_y] = (np.random.rand(3) * 255).astype(np.uint8)

frontier = [(rand_x, rand_y)]

neighbors = [(dx, dy) for dx in [-1, 0, 1] for dy in [-1, 0, 1] if dx or dy]
surf = pg.Surface((screen_width, screen_height))

clock = pg.time.Clock()
saved_screen = False

while True:
    if not saved_screen and len(frontier) == 0:
        save_screen(screen)
        saved_screen = True

    for event in pg.event.get():
        if event.type == pg.QUIT:
            sys.exit()

    new_frontier = list()

    for x, y in reversed(frontier):
        for dx, dy in neighbors:
            nx, ny = x + dx, y + dy
            if 0 <= nx < screen_width and 0 <= ny < screen_height:
                if not pixels[nx, ny].any():
                    # noise = np.array([np.random.randint(-10, 10) for _ in range(3)])
                    noise = np.array([np.random.normal() for _ in range(3)]) * 25
                    # noise = (np.random.rand(3) * 10).astype(np.uint8)
                    new_color = np.clip(pixels[x, y] + noise, 0, 255)
                    pixels[nx, ny, 0] = new_color[0]
                    pixels[nx, ny, 1] = pixels[x, y, 1]
                    pixels[nx, ny, 2] = pixels[x, y, 2]
                    new_frontier.append((nx, ny))
    frontier = new_frontier

    pg.surfarray.blit_array(surf, pixels)
    screen.blit(surf, (0, 0))
    pg.display.flip()

    clock.tick(60) 
