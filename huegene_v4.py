import numpy as np
import pygame as pg
import datetime
from numba import jit, njit

@njit
def mutatefast(pixels, frontier):
    max_x, max_y = pixels.shape[0], pixels.shape[1]
    directions = [(-1,-1), (-1,0), (-1,1), (0,-1), (0,1), (1,-1), (1,0), (1,1)]

    # Preallocate a generous size for new_frontier
    new_frontier = np.empty((len(frontier) * 8, 2), dtype=np.int32)
    new_len = 0

    for i in range(len(frontier)):
        x, y = frontier[i]
        for j in range(8):
            dx, dy = directions[j]
            nx, ny = x + dx, y + dy
            if 0 <= nx < max_x and 0 <= ny < max_y:
                if not (pixels[nx, ny] != 0).any():  # pixel is black
                    # Generate fake noise, since Numba can't do random here
                    noise = np.array([(x * y + dx + dy + c) % 10 for c in range(3)], dtype=np.uint8)
                    for c in range(3):
                        pixels[nx, ny, c] = min(255, pixels[x, y, c] + noise[c])
                    new_frontier[new_len] = (nx, ny)
                    new_len += 1

    return pixels, new_frontier[:new_len]

@jit
def mutate(pixels, frontier):
    new_frontier = []

    for x, y in frontier:
        for dx, dy in [(-1,-1), (-1,0), (-1,1), (0,-1), (0,1), (1,-1), (1,0), (1,1)]:
            nx = dx + x
            ny = dy + y
            if nx < 0 or nx >= pixels.shape[0] or ny < 0 or ny >= pixels.shape[1]: continue
            if pixels[nx, ny].any(): continue
            noise = (np.random.rand(3) * 10).astype(np.uint8)
            new_color = pixels[x, y] + noise
            pixels[nx, ny] = new_color
            new_frontier.append((nx, ny))
    return pixels, new_frontier

def main():
    pg.init()
    screen_width = 3024//2
    screen_height = 1964//2
    screen = pg.display.set_mode((screen_width, screen_height))
    clock = pg.time.Clock()

    pixels = np.zeros((screen_width, screen_height, 3), dtype=np.uint8)

    seed_x = np.random.randint(0,screen_width)
    seed_y = np.random.randint(0,screen_height)
    seed_x = screen_width//4
    seed_y = screen_height//4
    color = (np.random.rand(3) * 255).astype(np.uint8)
    pixels[seed_x, seed_y] = color
    frontier = [(seed_x, seed_y)]

    saved = False

    while True:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()

        if not saved and len(frontier) == 0:
            pg.image.save(screen, str(datetime.datetime.now()) + '.png')
            saved = True

        pixels, frontier = mutatefast(pixels, frontier)
        print(len(frontier))
        pg.surfarray.blit_array(screen, pixels)
        pg.display.flip()
        # clock.tick(10)

main()