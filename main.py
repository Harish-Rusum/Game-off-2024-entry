import pygame
import sys
from scripts.tilemap import Grid
from scripts.player import Player
from utils.fov import Overlay
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
fov = Overlay(ScreenX,ScreenY,200,[ScreenX // 2, ScreenY // 2])
p = Player(0,0,TileSize)

def main():
    running = True
    while running:
        screen.fill(Black)
        
        right, left = 0, 0

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        keys = pygame.key.get_pressed()
        
        if keys[pygame.K_a]:
            right = -5
        elif keys[pygame.K_d]:
            right = 5
        
        if keys[pygame.K_w]:
            left = -5
        elif keys[pygame.K_s]:
            left = 5

        if keys[pygame.K_UP]:
            fov.FovRad += 5
        if keys[pygame.K_DOWN]:
            fov.FovRad -= 5

        grid.render(screen)

        p.move(right, left, grid)
        # fov.render(screen)
        p.render(screen)
        pygame.display.flip()
        clock.tick(Fps)

    pygame.quit()
    sys.exit()
if __name__ == "__main__":
    main()
