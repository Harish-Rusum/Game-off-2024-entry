import pygame
import sys
import os

pygame.init()

tileSize = 35
viewX, viewY = 20, 15
tilesX, tilesY = 40, 40
palWidth = 7 * tileSize
bufferWidth = 10
screenX, screenY = tileSize * viewX + palWidth + bufferWidth, tileSize * viewY
fps = 60
black = (0, 0, 0)

filename = f"levels/{input('Enter a level name: ')}.py"

screen = pygame.display.set_mode((screenX, screenY))
pygame.display.set_caption("Tile Grid System")
clock = pygame.time.Clock()

# matrix = [[[(-1, -1), (-1, -1), (0,0), (-1, -1)] for _ in range(tilesX)] for _ in range(tilesY)]
from level9 import matrix

from tilemap import Grid, Palette

tileMap = Grid(tilesX, tilesY, tileSize, matrix, screenX - palWidth - bufferWidth, screenY)
picker = Palette(screenX, screenY, palWidth, tileMap, tileSize)

paletteArea = pygame.Rect(screenX - (palWidth + bufferWidth), 0, palWidth, screenY)

mouseHeld = 0
rotateHeld = False

def main():
    global mouseHeld, rotateHeld
    running = True

    while running:
        screen.fill(black)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    mouseHeld = 1 
                elif event.button == 2:
                    mouseHeld = 3
                elif event.button == 3:
                    mouseHeld = 2
            elif event.type == pygame.MOUSEBUTTONUP:
                mouseHeld = 0

        handleMouse()

        handleKeyboard()

        tileMap.render(screen)
        pygame.draw.rect(screen, black, paletteArea)
        picker.render(screen)

        pygame.display.flip()
        clock.tick(fps)

    pygame.quit()
    sys.exit()

def handleMouse():
    global mouseHeld
    mouseX, mouseY = pygame.mouse.get_pos()
    if mouseHeld == 0:
        return
    if mouseHeld == 1 and mouseX < (picker.width - picker.palWidth):
        picker.tileAction(mouseX, mouseY, tileMap, "replaceTile")
    elif mouseHeld == 2 and mouseX < (picker.width - picker.palWidth):
        picker.tileAction(mouseX, mouseY, tileMap, "deleteTile")
    elif mouseHeld == 3 and mouseX < (picker.width - picker.palWidth):
        picker.tileAction(mouseX, mouseY, tileMap, "selectGrid")
    elif mouseX >= (picker.width - picker.palWidth):
        picker.tileAction(mouseX, mouseY, tileMap, "selectPalette")

def handleKeyboard():
    global rotateHeld

    keys = pygame.key.get_pressed()

    if keys[pygame.K_r] and not rotateHeld:
        mouseX, mouseY = pygame.mouse.get_pos()
        picker.rotate(mouseX, mouseY, tileMap)
        rotateHeld = True
    if not keys[pygame.K_r]:
        rotateHeld = False

    if keys[pygame.K_q]:
        save_level()
        pygame.quit()
        sys.exit()

def save_level():
    try:
        directory = os.path.dirname(filename)
        if directory:
            os.makedirs(directory, exist_ok=True)
        with open(filename, "w") as file:
            file.write("matrix = [\n")
            for row in tileMap.grid:
                file.write(f"    {row},\n")
            file.write("]\n")
        print(f"Level successfully saved to {filename}!")
    except Exception as e:
        print(f"Error saving level: {e}")

if __name__ == "__main__":
    main()
