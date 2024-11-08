import pygame

tile_cache = {}

class Tile:
    def __init__(self, tileIndex, scaleX, scaleY, rotation) -> None:
        self.img = self.getImg(tileIndex, scaleX, scaleY, rotation)
        self.rect = self.img.get_rect()

    def getImg(self, tileIndex, scaleX, scaleY, rotation):
        global tile_cache
        cacheKey = (tileIndex, scaleX, scaleY, rotation)

        if cacheKey in tile_cache:
            return tile_cache[cacheKey]

        if tileIndex == "empty":
            surface = pygame.Surface((scaleX, scaleY))
            surface.fill((0, 0, 0))
        else:
            loaded = pygame.image.load(f"assets/tile_{tileIndex}.png").convert_alpha()
            scaled = pygame.transform.smoothscale(loaded, (scaleX, scaleY))
            surface = pygame.transform.rotate(scaled, (rotation - 1) * -90)

        tile_cache[cacheKey] = surface
        return surface

class Grid:
    def __init__(self, tilesX, tilesY, tileSize, matrix, screenWidth, screenHeight):
        self.tilesX = tilesX
        self.tilesY = tilesY
        self.tileSize = tileSize
        self.grid = [[[(-1, -1), (-1, -1), (0, 0)] for _ in range(tilesX)] for _ in range(tilesY)]
        self.screenHeight = screenHeight
        self.screenWidth = screenWidth
        self.loadGrid(matrix)

    def loadGrid(self, matrix):
        for y in range(len(matrix)):
            for x in range(len(matrix[0])):
                self.grid[y][x][0] = matrix[y][x][0]
                self.grid[y][x][1] = matrix[y][x][1]

    def render(self, screen):
        startX = 0
        startY = 0
        endX = self.tilesX
        endY = self.tilesY

        for y in range(startY, endY):
            for x in range(startX, endX):
                tileIndex, rotation = self.grid[y][x][0]
                tileIndexStr = "empty" if tileIndex == -1 else f"{tileIndex:04d}"
                tile = Tile(tileIndexStr, self.tileSize, self.tileSize, rotation)
                self.grid[y][x][2] = (x * self.tileSize, y * self.tileSize)
                screen.blit(tile.img, (self.grid[y][x][2]))

        for y in range(startY, endY):
            for x in range(startX, endX):
                tileIndex, rotation = self.grid[y][x][1]
                tileIndexStr = "empty" if tileIndex == -1 else f"{tileIndex:04d}"
                if tileIndexStr == "empty":
                    continue
                tile = Tile(tileIndexStr, self.tileSize, self.tileSize, rotation)
                self.grid[y][x][2] = (x * self.tileSize, y * self.tileSize)
                screen.blit(tile.img, (self.grid[y][x][2]))

    def getSurroundingTiles(self, screen_x, screen_y):
        center_tile_x = screen_x // self.tileSize
        center_tile_y = screen_y // self.tileSize

        surrounding_tiles = []
        for dy in range(-1, 2):
            for dx in range(-1, 2):
                tile_x = int(center_tile_x + dx)
                tile_y = int(center_tile_y + dy)
                
                if 0 <= tile_x < self.tilesX and 0 <= tile_y < self.tilesY:
                    surrounding_tiles.append(self.grid[tile_y][tile_x])
        
        return surrounding_tiles

class Palette:
    def __init__(self, width, height, palWidth, grid, tileSize):
        self.width = width
        self.palWidth = palWidth
        self.grid = grid
        self.tileSize = tileSize
        self.tilesX = width // tileSize
        self.tilesY = height // tileSize
        self.selected = -1
        self.decorTiles = {
            32, 44, 45, 46, 27, 84, 85, 86, 87, 88, 124, 125, 126, 127, 128, 129
        }

    def render(self, surf):
        num = 0
        for x in range(0, self.tilesX):
            for y in range(0, self.tilesY):
                curX = x * self.tileSize + (self.width - self.palWidth)
                curY = y * self.tileSize
                if num == 180:
                    continue
                zeros = 4 - len(str(num))
                string = "0" * zeros + str(num)
                loaded = pygame.image.load(f"assets/tile_{string}.png").convert_alpha()
                scaled = pygame.transform.smoothscale(loaded, (self.tileSize, self.tileSize))
                surf.blit(scaled, (curX, curY))
                if num == int(self.selected):
                    white = "#FFFFFF"
                    pygame.draw.rect(surf, white, (curX, curY, self.tileSize, self.tileSize), 4, border_radius=3)
                num += 1

    def tileAction(self, mouseX, mouseY, grid, action):
        if action == "replaceTile":
            tileX = mouseX // self.tileSize
            tileY = mouseY // self.tileSize
            if int(self.selected) in self.decorTiles:
                if 0 <= tileX < grid.tilesX and 0 <= tileY < grid.tilesY:
                    grid.grid[tileY][tileX][1] = (int(self.selected), 1)
            else:
                if 0 <= tileX < grid.tilesX and 0 <= tileY < grid.tilesY:
                    grid.grid[tileY][tileX][0] = (int(self.selected), 1)

        if action == "selectPalette":
            adjMouseX = mouseX - (self.width - self.palWidth)
            tileX = adjMouseX // self.tileSize
            tileY = mouseY // self.tileSize
            num = (tileX * self.tilesY) + tileY
            zeros = "0" * (4 - len(str(num)))
            self.selected = zeros + str(num)

        if action == "selectGrid":
            tileX = mouseX // self.tileSize
            tileY = mouseY // self.tileSize
            num = grid.grid[tileY][tileX][0][0]
            if num == -1:
                return
            zeros = "0" * (4 - len(str(num)))
            self.selected = zeros + str(num)

        if action == "deleteTile":
            tileX = mouseX // self.tileSize
            tileY = mouseY // self.tileSize
            if 0 <= tileX < grid.tilesX and 0 <= tileY < grid.tilesY:
                grid.grid[tileY][tileX][0] = (-1, -1)
                grid.grid[tileY][tileX][1] = (-1, -1)

    def rotate(self, mouseX, mouseY, grid):
        tileX = mouseX // self.tileSize
        tileY = mouseY // self.tileSize
        if 0 <= tileX < grid.tilesX and 0 <= tileY < grid.tilesY:
            tileIndex, rotation = grid.grid[tileY][tileX][0]
            grid.grid[tileY][tileX][0] = (tileIndex, (rotation + 1) % 4)
