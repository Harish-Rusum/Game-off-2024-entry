import pygame
import sys

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
    def __init__(self, tileType, scaleX, scaleY):
        
        self.typelist = {
            "water": "assets/tile_0073.png",
            "water2": "assets/tile_0033.png",
            "empty" : "empty"
        }
        self.img = self.getImg(self.typelist[tileType], scaleX, scaleY)

    def getImg(self, tileType, scaleX, scaleY):
        if tileType == "empty":
            surface = pygame.Surface((scaleX, scaleY))
            surface.fill((000, 000, 000))  
            return surface
        else:
            
            loaded = pygame.image.load(f"{tileType}").convert_alpha()
            scaled = pygame.transform.smoothscale(loaded, (scaleX, scaleY))
            return scaled


class Grid:
    def __init__(self, tilesX, tilesY, tileSize):
        self.grid = [[Tile("empty", tileSize, tileSize) for _ in range(tilesX)] for _ in range(tilesY)]
        for i in range(tilesX):
            self.grid[tilesY - 1][i] = Tile("water", tileSize, tileSize) 
        for i in range(tilesX):
            self.grid[tilesY - 2][i] = Tile("water", tileSize, tileSize) 
        for i in range(tilesX):
            self.grid[tilesY - 3][i] = Tile("water2", tileSize, tileSize) 
    def render(self, surf):
        
        for y in range(len(self.grid)):
            for x in range(len(self.grid[y])):
                tile = self.grid[y][x]
                surf.blit(tile.img, (TILE_SIZE * x, TILE_SIZE * y))



g = Grid(GRID_WIDTH, GRID_HEIGHT, TILE_SIZE)

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

