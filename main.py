import pygame
import sys
pygame.init()


TILE_SIZE = 32
GRID_WIDTH, GRID_HEIGHT = 18, 18
SCREEN_WIDTH, SCREEN_HEIGHT = TILE_SIZE * GRID_WIDTH, TILE_SIZE * GRID_HEIGHT
FPS = 60
BLACK = "#000000"

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Tile Grid System")
clock = pygame.time.Clock()

from utils.grid import Grid

def main():
    running = True
    while running:
        screen.fill(BLACK)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False


        pygame.display.flip()
        clock.tick(FPS)

    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()
