import numpy as np
import pygame as pg

def main():
    pg.init()
    screen_width = 2000
    screen_height = 1000
    screen = pg.display.set_mode((screen_width, screen_height))
    clock = pg.time.Clock()

    pixels = np.zeros((screen_width, screen_height, 3), dtype=np.uint8)

    seed_x = np.random.randint(0,screen_width)
    seed_y = np.random.randint(0,screen_height)
    color = (np.random.rand(3) * 255).astype(np.uint8)
    pixels[seed_x, seed_y] = color
    frontier = [(seed_x, seed_y)]

    neighbors = [(-1,-1), (-1,0), (-1,1), (0,-1), (0,1), (1,-1), (1,0), (1,1)]

    while True:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()

        new_frontier = []

        for x, y in frontier:
            for dx, dy in neighbors:
                nx = dx + x
                ny = dy + y
                if nx < 0 or nx >= screen_width or ny < 0 or ny >= screen_height: continue
                if pixels[nx, ny].any(): continue
                noise = (np.random.rand(3) * 10).astype(np.uint8)
                new_color = pixels[x, y] + noise
                pixels[nx, ny] = new_color
                new_frontier.append((nx, ny))
        
        frontier = new_frontier
        print(frontier)
        pg.surfarray.blit_array(screen, pixels)
        pg.display.flip()
        clock.tick(60)

main()