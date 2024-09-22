import pygame
import sys
import os

pygame.init()
filename = input("Enter the filename (e.g., 'levels/level1.py'): ")

TILE_SIZE = 32
GRID_WIDTH, GRID_HEIGHT = 18, 18
PALETTE_WIDTH = 5
SCREEN_WIDTH, SCREEN_HEIGHT = (
    TILE_SIZE * GRID_WIDTH + TILE_SIZE * PALETTE_WIDTH,
    TILE_SIZE * GRID_HEIGHT,
)
FPS = 60
BLACK = "#000000"

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Tile Grid System")

clock = pygame.time.Clock()


TILE_COUNT = 180
tileImages = []
for i in range(TILE_COUNT):
    tileName = f"tile_{i:04d}.png"
    tilePath = os.path.join("assets", tileName)
    if os.path.exists(tilePath):
        img = pygame.image.load(tilePath).convert_alpha()
        tileImages.append(pygame.transform.smoothscale(img, (TILE_SIZE, TILE_SIZE)))
    else:

        img = pygame.Surface((TILE_SIZE, TILE_SIZE))
        img.fill((0, 0, 0))
        tileImages.append(img)


blackTile = pygame.Surface((TILE_SIZE, TILE_SIZE))
blackTile.fill((0, 0, 0))


class Tile:
    def __init__(self, tileImg, tileIndex):
        self.img = tileImg
        self.tile_index = tileIndex
        self.rotation = 0

    def rotate(self):
        self.rotation = (self.rotation + 90) % 360
        self.img = pygame.transform.rotate(self.img, -90)

    def getRotationState(self):
        return self.rotation // 90 + 1


class Grid:
    def __init__(self, tilesX, tilesY):
        self.grid = [
            [Tile(blackTile, -1) for _ in range(tilesX)] for _ in range(tilesY)
        ]

    def setTile(self, x, y, tileIndex):
        self.grid[y][x] = Tile(tileImages[tileIndex], tileIndex)

    def rotateTiles(self, x, y):
        if self.grid[y][x].tile_index != -1:
            self.grid[y][x].rotate()

    def render(self, surf):
        for y in range(len(self.grid)):
            for x in range(len(self.grid[y])):
                tile = self.grid[y][x]
                if tile.tile_index == -1:
                    surf.blit(blackTile, (TILE_SIZE * x, TILE_SIZE * y))
                else:
                    surf.blit(tile.img, (TILE_SIZE * x, TILE_SIZE * y))

    def printMatrix(self):

        matrix = [
            [(tile.tile_index, tile.getRotationState()) for tile in row]
            for row in self.grid
        ]
        return matrix


class Palette:
    def __init__(self):
        self.tiles_per_row = PALETTE_WIDTH
        self.selected_tile_index = 0

    def render(self, surf):
        for i, tile_img in enumerate(tileImages):
            palette_x = GRID_WIDTH * TILE_SIZE + (i % self.tiles_per_row) * TILE_SIZE
            palette_y = (i // self.tiles_per_row) * TILE_SIZE
            surf.blit(tile_img, (palette_x, palette_y))

    def selectTiles(self, mouse_x, mouse_y):

        if mouse_x >= GRID_WIDTH * TILE_SIZE:
            col = (mouse_x - GRID_WIDTH * TILE_SIZE) // TILE_SIZE
            row = mouse_y // TILE_SIZE
            index = row * self.tiles_per_row + col
            if 0 <= index < TILE_COUNT:
                self.selected_tile_index = index


g = Grid(GRID_WIDTH, GRID_HEIGHT)
palette = Palette()


def main():
    running = True
    mouse_held = False
    while running:
        screen.fill(BLACK)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_x, mouse_y = event.pos
                mouse_held = True
                if mouse_x < GRID_WIDTH * TILE_SIZE:

                    grid_x, grid_y = mouse_x // TILE_SIZE, mouse_y // TILE_SIZE
                    g.setTile(grid_x, grid_y, palette.selected_tile_index)
                else:

                    palette.selectTiles(mouse_x, mouse_y)

            elif event.type == pygame.MOUSEBUTTONUP:
                mouse_held = False

            elif event.type == pygame.MOUSEMOTION and mouse_held:

                mouse_x, mouse_y = event.pos
                if mouse_x < GRID_WIDTH * TILE_SIZE:
                    grid_x, grid_y = mouse_x // TILE_SIZE, mouse_y // TILE_SIZE
                    g.setTile(grid_x, grid_y, palette.selected_tile_index)

            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:

                    mouse_x, mouse_y = pygame.mouse.get_pos()
                    if mouse_x < GRID_WIDTH * TILE_SIZE:
                        grid_x, grid_y = mouse_x // TILE_SIZE, mouse_y // TILE_SIZE
                        g.rotateTiles(grid_x, grid_y)

                elif event.key == pygame.K_q:
                    matrix = g.printMatrix()
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
        g.render(screen)
        palette.render(screen)

        pygame.display.flip()
        clock.tick(FPS)

    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()
