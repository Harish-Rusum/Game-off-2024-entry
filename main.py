import pygame
import sys
from levels.level2 import matrix

pygame.init()


TILE_SIZE = 32
GRID_WIDTH, GRID_HEIGHT = 18, 18
SCREEN_WIDTH, SCREEN_HEIGHT = TILE_SIZE * GRID_WIDTH, TILE_SIZE * GRID_HEIGHT
FPS = 60
BLACK = "#000000"

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Tile Grid System")


clock = pygame.time.Clock()


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
                if str(matrix[y][x][0]) == "-1":
                    self.grid[y][x] = Tile("empty", self.tileY, self.tileX,matrix[y][x][1])
                    continue
                else:
                    string = str(matrix[y][x][0])
                    zeros = "0" * (4 - len(string))
                    self.grid[y][x] = Tile(zeros + string, self.tileY, self.tileX,matrix[y][x][1])

    def render(self, surf):
        for y in range(len(self.grid)):
            for x in range(len(self.grid[y])):
                tile = self.grid[y][x]
                surf.blit(tile.img, (TILE_SIZE * x, TILE_SIZE * y))


g = Grid(GRID_WIDTH, GRID_HEIGHT, TILE_SIZE, matrix)


def main():
    running = True
    while running:
        screen.fill(BLACK)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        g.render(screen)

        pygame.display.flip()
        clock.tick(FPS)

    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()
