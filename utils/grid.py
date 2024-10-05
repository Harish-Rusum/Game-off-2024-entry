import pygame

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
