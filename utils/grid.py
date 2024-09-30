import pygame

class Tile:
    def __init__(self, tileIndex, scaleX, scaleY,rotation):
        self.img = self.getImg(tileIndex, scaleX, scaleY,rotation)

    def getImg(self, tileIndex, scaleX, scaleY,rotation):
        if tileIndex == "empty":
            surface = pygame.Surface((scaleX, scaleY))
            surface.fill((000, 000, 000))
            return surface
        else:
            loaded = pygame.image.load(f"assets/tile_{tileIndex}.png").convert_alpha()
            scaled = pygame.transform.smoothscale(loaded, (scaleX, scaleY))
            scaled = pygame.transform.rotate(scaled,(rotation - 1) * -90)
            return scaled

class Grid:
    def __init__(self, tilesX, tilesY, tileSize, matrix):
        self.tileX = tileSize
        self.tileY = tileSize
        self.grid = [[Tile("empty", self.tileY, self.tileX,0) for _ in range(tilesX)] for _ in range(tilesY)]
        self.loadGrid(matrix)

    def loadGrid(self, matrix):
        for y in range(len(matrix)):
            for x in range(len(matrix[0])):
                tup = matrix[y][x]
                rotation = tup[1]
                tileIndex = tup[0]
                if str(tileIndex) == "-1":
                    self.grid[y][x] = Tile("empty", self.tileY, self.tileX,rotation)
                    continue
                else:
                    string = str(matrix[y][x][0])
                    zeros = "0" * (4 - len(string))
                    final = zeros + string
                    self.grid[y][x] = Tile(final,self.tileY, self.tileX,matrix[y][x][1])

    def render(self, surf):
        for y in range(len(self.grid)):
            for x in range(len(self.grid[y])):
                tile = self.grid[y][x]
                surf.blit(tile.img, (self.tileX * x, self.tileY * y))

