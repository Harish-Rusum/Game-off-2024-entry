import pygame
import random
import sys
from scripts.tilemap import Grid
from levels.thing import matrix

pygame.init()

TileSize = 40
ViewX, ViewY = 15, 15
TilesX, TilesY = 40, 40
ScreenX, ScreenY = TileSize * ViewX, TileSize * ViewY
Fps = 60
Black = "#000000"

screen = pygame.display.set_mode((ScreenX, ScreenY))
pygame.display.set_caption("Tile Grid System")
clock = pygame.time.Clock()

# matrix = [[(random.choice([x for x in range(1, 180)]), random.choice([-1, 1, 2, 3])) for _ in range(TilesX)] for _ in range(TilesY)]
grid = Grid(TilesX, TilesY, TileSize, 5, matrix, ScreenX, ScreenY)


def main():
    running = True
    while running:
        screen.fill(Black)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        keys = pygame.key.get_pressed()
        if keys[pygame.K_a]:
            grid.scroll("left")
        if keys[pygame.K_d]:
            grid.scroll("right")
        if keys[pygame.K_w]:
            grid.scroll("up")
        if keys[pygame.K_s]:
            grid.scroll("down")

        grid.render(screen)
        pygame.display.flip()
        clock.tick(Fps)

    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()
