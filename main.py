import pygame
import sys
from scripts.tilemap import Grid
from scripts.player import Player
from scripts.cursor import Cursor
from utils.fov import Overlay
from utils.menu import Menu
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
player = Player(TileSize, TileSize,1,0,315)
cursor = Cursor()

def main():
    running = True
    pauseMenu = False
    holdingEsc = False
    menu = Menu(screen)
    while running:
        screen.fill(Black)
        right = 0

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        keys = pygame.key.get_pressed()
        jump = False
        if keys[pygame.K_a] or keys[pygame.K_h] or keys[pygame.K_LEFT]:
            right = -1
        elif keys[pygame.K_d] or keys[pygame.K_l] or keys[pygame.K_RIGHT]:
            right = 1
        else:
            right = 0

        if keys[pygame.K_w] or keys[pygame.K_k] or keys[pygame.K_UP]:
            jump = True
        else:
            jump = False
        
        if keys[pygame.K_ESCAPE]:
            if not holdingEsc:
                holdingEsc = True
                pauseMenu = not pauseMenu
        else:
            holdingEsc = False

        screen.fill("#000000")
        grid.render(screen)
        player.render(screen)
        menu.render()
        if not menu.menuOpen:
            player.update(right,grid,screen,jump=jump)

        # mouseX,mouseY = pygame.mouse.get_pos()
        # mousefov.render(screen,[mouseX,mouseY])

        cursor.render(screen)
        pygame.display.flip()
        clock.tick(Fps)

    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()
