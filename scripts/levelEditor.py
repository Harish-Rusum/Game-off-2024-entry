import pygame
import sys

pygame.init()

TileSize = 40
ViewX, ViewY = 15, 15
TilesX, TilesY = 40, 40
PalWidth = 12 * 40
ExtraWidth = 10
ScreenX, ScreenY = TileSize * ViewX + PalWidth + ExtraWidth, TileSize * ViewY
Fps = 60
Black = (0, 0, 0)

screen = pygame.display.set_mode((ScreenX, ScreenY))
pygame.display.set_caption("Tile Grid System")
clock = pygame.time.Clock()

Matrix = [[(-1, -1) for _ in range(TilesX)] for _ in range(TilesY)]

from tilemap import Grid
from tilemap import Palette

tileMap = Grid(TilesX, TilesY, TileSize, 5, Matrix, ScreenX - PalWidth - ExtraWidth, ScreenY)
picker = Palette(ScreenX, ScreenY, PalWidth, tileMap, TileSize)

blackSpace = pygame.Rect(ScreenX - (PalWidth + ExtraWidth), 0, PalWidth, ScreenY)

mouse_held = False
r_held = False

def main():
    global mouse_held,r_held
    running = True
    while running:
        screen.fill(Black)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouseX, mouseY = pygame.mouse.get_pos()
                mouse_held = True
                picker.getClick(mouseX, mouseY, tileMap)
            if event.type == pygame.MOUSEBUTTONUP:
                mouse_held = False

        if mouse_held:
            mouseX, mouseY = pygame.mouse.get_pos()
            picker.getClick(mouseX, mouseY, tileMap)

        keys = pygame.key.get_pressed()
        if keys[pygame.K_a]:
            tileMap.scroll("left")
        if keys[pygame.K_d]:
            tileMap.scroll("right")
        if keys[pygame.K_w]:
            tileMap.scroll("up")
        if keys[pygame.K_s]:
            tileMap.scroll("down")
        if keys[pygame.K_r]:
            if not r_held:
                mouseX, mouseY = pygame.mouse.get_pos()
                picker.rotate(mouseX, mouseY, tileMap)
                r_held = True
        if not keys[pygame.K_r]:
            r_held = False
        tileMap.render(screen)
        pygame.draw.rect(screen, (0, 0, 0), blackSpace)
        picker.render(screen)
        pygame.display.flip()
        clock.tick(Fps)

    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()
