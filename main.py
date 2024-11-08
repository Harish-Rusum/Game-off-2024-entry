import pygame
import sys
from scripts.tilemap import Grid
from scripts.player import Player
from scripts.cursor import Cursor
from utils.fov import Overlay
from levels.thing import matrix

pygame.init()

TileSize = 35
ViewX, ViewY = 20, 15
TilesX, TilesY = 40, 40
ScreenX, ScreenY = TileSize * ViewX, TileSize * ViewY
Fps = 60
Black = "#000000"

screen = pygame.display.set_mode((ScreenX, ScreenY))
pygame.display.set_caption("Tile Grid System")
clock = pygame.time.Clock()
pygame.mouse.set_visible(False)
grid = Grid(TilesX, TilesY, TileSize, matrix, ScreenX, ScreenY)
mousefov = Overlay(ScreenX, ScreenY, 250, [ScreenX // 2, ScreenY // 2])
p = Player(0, 0, 35, 35)
cursor = Cursor()


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
            mousefov.FovRad += 5
        if keys[pygame.K_DOWN]:
            mousefov.FovRad -= 5

        screen.fill("#000000")        
        grid.render(screen)
        p.move(right, left, grid)
        p.render(screen)
        mousex,mousey = pygame.mouse.get_pos()
        mousefov.update([mousex,mousey])
        mousefov.render(screen)
        cursor.render(screen)
        pygame.display.flip()
        clock.tick(Fps)

    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()

# I WONT BLOODY USE VSCODE YOU BLOODY IDIOT PRANE
