import numpy as np
import pygame as pg
import sys
import os

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
picture_take = False
while True:
    if len(frontier) == 0 and not picture_take:
        fname = 1
        while os.path.isfile(str(fname) + ".png"):
            fname += 1
        pg.image.save(screen, str(fname) + '.png')
        picture_take = True

    for event in pg.event.get():
        if event.type == pg.QUIT:
            sys.exit()

    new_frontier = list()

    np.random.shuffle(frontier)

    for x, y in frontier:
        for dx, dy in neighbors:
            nx, ny = x + dx, y + dy
            if 0 <= nx < screen_width and 0 <= ny < screen_height:
                if not pixels[nx, ny].any():
                    if np.random.random() > 0.9:
                        # noise = np.array([np.random.uniform(-1, 1) * 2 for _ in range(3)], dtype='uint8') # Option 1
                        noise = np.array([np.random.normal() for _ in range(3)]) * 10
                        # noise = (np.random.rand(3) * 2).astype(np.uint8) # Option 2
                        new_color = np.clip(pixels[x, y] + noise, 0, 255)
                        pixels[nx, ny] = new_color
                        new_frontier.append((nx, ny))
                    else:
                        # pass
                        new_frontier.append((nx, ny))
    frontier = new_frontier

    pg.surfarray.blit_array(surf, pixels)
    screen.blit(surf, (0, 0))
    pg.display.flip()

