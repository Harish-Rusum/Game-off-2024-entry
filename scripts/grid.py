import pygame

tile_cache = {}

class Tile:
    def __init__(self, tileIndex, scaleX, scaleY, rotation):
        self.img = self.getImg(tileIndex, scaleX, scaleY, rotation)

    def getImg(self, tileIndex, scaleX, scaleY, rotation):
        global tile_cache
        cache_key = (tileIndex, scaleX, scaleY, rotation)

        if cache_key in tile_cache:
            return tile_cache[cache_key]

        if tileIndex == "empty":
            surface = pygame.Surface((scaleX, scaleY))
            surface.fill((0, 0, 0))  
        else:
            loaded = pygame.image.load(f"assets/tile_{tileIndex}.png").convert_alpha()
            scaled = pygame.transform.smoothscale(loaded, (scaleX, scaleY))
            surface = pygame.transform.rotate(scaled, (rotation - 1) * -90)

        tile_cache[cache_key] = surface
        return surface

class Grid:
    def __init__(self, tilesX, tilesY, tileSize, scrollSpeed, matrix, screenWidth, screenHeight):
        self.tilesX = tilesX
        self.tilesY = tilesY
        self.tileSize = tileSize
        self.grid = [[(-1, 0) for _ in range(tilesX)] for _ in range(tilesY)]  
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
                self.grid[y][x] = matrix[y][x]

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
        startX = max(0, int(-self.offX // self.tileSize))
        startY = max(0, int(-self.offY // self.tileSize))
        endX = min(self.tilesX, int((self.screenWidth - self.offX) // self.tileSize + 1))
        endY = min(self.tilesY, int((self.screenHeight - self.offY) // self.tileSize + 1))

        for y in range(startY, endY):
            for x in range(startX, endX):
                tileIndex, rotation = self.grid[y][x]
                tileIndexStr = "empty" if tileIndex == -1 else f"{tileIndex:04d}"
                tile = Tile(tileIndexStr, self.tileSize, self.tileSize, rotation)
                screen.blit(tile.img, (x * self.tileSize + self.offX, y * self.tileSize + self.offY))
