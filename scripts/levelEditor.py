import pygame
import random
import sys

pygame.init()

TileSize = 40
ViewX, ViewY = 15, 15
TilesX, TilesY = 40, 40
PalWidth = 200
BufferSpace = 10
ScreenX, ScreenY = TileSize * ViewX + PalWidth + BufferSpace, TileSize * ViewY
Fps = 60
Black = (0, 0, 0)

screen = pygame.display.set_mode((ScreenX, ScreenY))
pygame.display.set_caption("Tile Grid System")
clock = pygame.time.Clock()

Matrix = [[(random.choice([x for x in range(1, 180)]), random.choice([-1, 1, 2, 3])) for _ in range(TilesX)] for _ in range(TilesY)]

class Tile:
    def __init__(self, tileIndex, scaleX, scaleY, rotation):
        self.img = self.getImg(tileIndex, scaleX, scaleY, rotation)

    def getImg(self, tileIndex, scaleX, scaleY, rotation):
        if tileIndex == "empty":
            surface = pygame.Surface((scaleX, scaleY))
            surface.fill((0, 0, 0))
            return surface
        else:
            loaded = pygame.image.load(f"assets/tile_{tileIndex}.png").convert_alpha()
            scaled = pygame.transform.smoothscale(loaded, (scaleX, scaleY))
            rotated = pygame.transform.rotate(scaled, (rotation - 1) * -90)
            return rotated

class Grid:
    def __init__(self, tilesX, tilesY, tileSize, scrollSpeed, matrix, screenWidth, screenHeight):
        self.tilesX = tilesX
        self.tilesY = tilesY
        self.tileSize = tileSize
        self.grid = [[Tile("empty", tileSize, tileSize, 0) for _ in range(tilesX)] for _ in range(tilesY)]
        self.offX = 0
        self.offY = 0
        self.screenHeight = screenHeight
        self.screenWidth = screenWidth
        self.scrollSpeed = scrollSpeed
        self.loadGrid(matrix)
        self.clampY = (self.tilesY - (self.screenHeight / self.tileSize)) * self.tileSize
        self.clampX = (self.tilesX - (self.screenWidth / self.tileSize)) * self.tileSize

    def loadGrid(self, matrix):
        for y in range(len(matrix)):
            for x in range(len(matrix[0])):
                tup = matrix[y][x]
                rotation = tup[1]
                tileIndex = tup[0]
                if str(tileIndex) == "-1":
                    self.grid[y][x] = Tile("empty", self.tileSize, self.tileSize, rotation)
                    continue
                else:
                    string = str(matrix[y][x][0])
                    zeros = "0" * (4 - len(string))
                    final = zeros + string
                    self.grid[y][x] = Tile(final, self.tileSize, self.tileSize, matrix[y][x][1])

    def scroll(self, direction):
        if direction == "left":
            self.offX += self.scrollSpeed
            self.offX = min(0, self.offX)
        elif direction == "right":
            self.offX -= self.scrollSpeed
            self.offX = max(-self.clampX, self.offX)
        elif direction == "up":
            self.offY += self.scrollSpeed
            self.offY = min(0, self.offY)
        elif direction == "down":
            self.offY -= self.scrollSpeed
            self.offY = max(-self.clampY, self.offY)

    def render(self, screen):
        for y, row in enumerate(self.grid):
            for x, tile in enumerate(row):
                screen.blit(tile.img, (x * self.tileSize + self.offX, y * self.tileSize + self.offY))

class Palette:
    def __init__(self, width, height, palWidth, grid, tileSize):
        self.width = width
        self.palWidth = palWidth
        self.grid = grid
        self.tileSize = tileSize
        self.tilesX = width // tileSize
        self.tilesY = height // tileSize

    def render(self, surf):
        for x in range(0, self.tilesX):
            for y in range(0, self.tilesY):
                curX = x * self.tileSize + (self.width - self.palWidth)
                curY = y * self.tileSize
                square = pygame.Rect(curX, curY, self.tileSize, self.tileSize)
                pygame.draw.rect(surf, (255, 255, 255), square)

tileMap = Grid(TilesX, TilesY, TileSize, 5, Matrix, ScreenX - PalWidth - BufferSpace, ScreenY)
picker = Palette(ScreenX, ScreenY, PalWidth, tileMap, TileSize)

blackSpace = pygame.Rect(ScreenX - (PalWidth + BufferSpace), 0, PalWidth , ScreenY)

def main():
    running = True
    while running:
        screen.fill(Black)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        keys = pygame.key.get_pressed()
        if keys[pygame.K_a]:
            tileMap.scroll("left")
        if keys[pygame.K_d]:
            tileMap.scroll("right")
        if keys[pygame.K_w]:
            tileMap.scroll("up")
        if keys[pygame.K_s]:
            tileMap.scroll("down")

        tileMap.render(screen)
        pygame.draw.rect(screen, (0, 0, 0), blackSpace)
        picker.render(screen)
        pygame.display.flip()
        clock.tick(Fps)

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()
