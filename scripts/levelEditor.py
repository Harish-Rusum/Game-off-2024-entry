import pygame
import sys
import os

pygame.init()

TileSize = 40
ViewX, ViewY = 15, 15
TilesX, TilesY = 40, 40
PalWidth = 12 * 40
ExtraWidth = 10
ScreenX, ScreenY = TileSize * ViewX + PalWidth + ExtraWidth, TileSize * ViewY
Fps = 60
Black = (0, 0, 0)

filename="levels/" + input("Enter in a levelname : ") + ".py"
screen = pygame.display.set_mode((ScreenX, ScreenY))
pygame.display.set_caption("Tile Grid System")
clock = pygame.time.Clock()

Matrix = [[(-1, -1) for _ in range(TilesX)] for _ in range(TilesY)]

from tilemap import Grid
from tilemap import Palette

tileMap = Grid(TilesX, TilesY, TileSize, 5, Matrix, ScreenX - PalWidth - ExtraWidth, ScreenY)
picker = Palette(ScreenX, ScreenY, PalWidth, tileMap, TileSize)

blackSpace = pygame.Rect(ScreenX - (PalWidth + ExtraWidth), 0, PalWidth, ScreenY)

mouseHeld = 0
rHeld = 0

def main():
    global mouseHeld,rHeld
    running = True
    while running:
        screen.fill(Black)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1: 
                    mouseHeld = 1
                if event.button ==  2:
                    mouseHeld = 3
                if event.button == 3:
                    mouseHeld = 2

            if event.type == pygame.MOUSEBUTTONUP:
                mouseHeld = 0

        if mouseHeld == 1:
            mouseX, mouseY = pygame.mouse.get_pos()
            if mouseX < (picker.width - picker.palWidth):
                picker.tileAction(mouseX, mouseY, tileMap,"replaceTile")
            else:
                picker.tileAction(mouseX,mouseY,tileMap,"selectPalette")

        if mouseHeld == 2:
            mouseX, mouseY = pygame.mouse.get_pos()
            if mouseX < (picker.width - picker.palWidth):
                picker.tileAction(mouseX, mouseY, tileMap,"deleteTile")

        if mouseHeld == 3:
            mouseX, mouseY = pygame.mouse.get_pos()
            if mouseX < (picker.width - picker.palWidth):
                picker.tileAction(mouseX, mouseY, tileMap,"selectGrid")

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
            if rHeld == 0:
                mouseX, mouseY = pygame.mouse.get_pos()
                picker.rotate(mouseX, mouseY, tileMap)
                rHeld = 1
        if not keys[pygame.K_r]:
            rHeld = 0
        if keys[pygame.K_q]:
            matrix = tileMap.grid
            directory = os.path.dirname(filename)
            if directory:
                os.makedirs(directory, exist_ok=True)
            try:
                with open(filename, "w") as f:
                    f.write("matrix = [\n")
                    for row in matrix:
                        f.write(f"    {row},\n")
                    f.write("]\n")
                print(f"Level written successfully to {filename}!")
            except Exception as e:
                print(f"Error writing level: {e}")
            running = False

        tileMap.render(screen)
        pygame.draw.rect(screen, (0, 0, 0), blackSpace)
        picker.render(screen)
        pygame.display.flip()
        clock.tick(Fps)

    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()

