import pygame
import sys
import os

pygame.init()


TILE_SIZE = 32
GRID_WIDTH, GRID_HEIGHT = 18, 18  
PALETTE_WIDTH = 5  
SCREEN_WIDTH, SCREEN_HEIGHT = TILE_SIZE * GRID_WIDTH + TILE_SIZE * PALETTE_WIDTH, TILE_SIZE * GRID_HEIGHT
FPS = 60
BLACK = ""

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Tile Grid System")

clock = pygame.time.Clock()


TILE_COUNT = 180
tile_images = []
for i in range(TILE_COUNT):
    tile_name = f"tile_{i:04d}.png"  
    tile_path = os.path.join("assets", tile_name)
    if os.path.exists(tile_path):
        img = pygame.image.load(tile_path).convert_alpha()
        tile_images.append(pygame.transform.smoothscale(img, (TILE_SIZE, TILE_SIZE)))
    else:
        
        img = pygame.Surface((TILE_SIZE, TILE_SIZE))
        img.fill((0, 0, 0))
        tile_images.append(img)


black_tile = pygame.Surface((TILE_SIZE, TILE_SIZE))
black_tile.fill((0, 0, 0))


class Tile:
    def __init__(self, tile_img, tile_index):
        self.img = tile_img
        self.tile_index = tile_index
        self.rotation = 0  

    def rotate(self):
        
        self.rotation = (self.rotation + 90) % 360
        self.img = pygame.transform.rotate(self.img, -90)  

    def get_rotation_state(self):
        
        return self.rotation // 90 + 1

class Grid:
    def __init__(self, tilesX, tilesY, tileSize):
        
        self.grid = [[Tile(black_tile, -1) for _ in range(tilesX)] for _ in range(tilesY)]

    def set_tile(self, x, y, tile_index):
        
        self.grid[y][x] = Tile(tile_images[tile_index], tile_index)

    def rotate_tile(self, x, y):
        
        if self.grid[y][x].tile_index != -1:
            self.grid[y][x].rotate()

    def render(self, surf):
        
        for y in range(len(self.grid)):
            for x in range(len(self.grid[y])):
                tile = self.grid[y][x]
                if tile.tile_index == -1:
                    surf.blit(black_tile, (TILE_SIZE * x, TILE_SIZE * y))  
                else:
                    surf.blit(tile.img, (TILE_SIZE * x, TILE_SIZE * y))

    def output_matrix(self):
        
        matrix = [[(tile.tile_index, tile.get_rotation_state()) for tile in row] for row in self.grid]
        return matrix


class Palette:
    def __init__(self):
        self.tiles_per_row = PALETTE_WIDTH
        self.selected_tile_index = 0

    def render(self, surf):
        for i, tile_img in enumerate(tile_images):
            palette_x = GRID_WIDTH * TILE_SIZE + (i % self.tiles_per_row) * TILE_SIZE
            palette_y = (i // self.tiles_per_row) * TILE_SIZE
            surf.blit(tile_img, (palette_x, palette_y))

    def select_tile(self, mouse_x, mouse_y):
        
        if mouse_x >= GRID_WIDTH * TILE_SIZE:
            col = (mouse_x - GRID_WIDTH * TILE_SIZE) // TILE_SIZE
            row = mouse_y // TILE_SIZE
            index = row * self.tiles_per_row + col
            if 0 <= index < TILE_COUNT:
                self.selected_tile_index = index
                print(f"Selected tile: tile_{self.selected_tile_index:04d}")


g = Grid(GRID_WIDTH, GRID_HEIGHT, TILE_SIZE)
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
                    g.set_tile(grid_x, grid_y, palette.selected_tile_index)
                else:
                    
                    palette.select_tile(mouse_x, mouse_y)

            elif event.type == pygame.MOUSEBUTTONUP:
                mouse_held = False

            elif event.type == pygame.MOUSEMOTION and mouse_held:
                
                mouse_x, mouse_y = event.pos
                if mouse_x < GRID_WIDTH * TILE_SIZE:
                    grid_x, grid_y = mouse_x // TILE_SIZE, mouse_y // TILE_SIZE
                    g.set_tile(grid_x, grid_y, palette.selected_tile_index)

            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    
                    mouse_x, mouse_y = pygame.mouse.get_pos()
                    if mouse_x < GRID_WIDTH * TILE_SIZE:
                        grid_x, grid_y = mouse_x // TILE_SIZE, mouse_y // TILE_SIZE
                        g.rotate_tile(grid_x, grid_y)

                elif event.key == pygame.K_o:
                    
                    matrix = g.output_matrix()
                    for row in matrix:
                        print(row)

                elif event.key == pygame.K_q:
                    
                    matrix = g.output_matrix()
                    print("Final Tile Matrix with Rotations:")
                    for row in matrix:
                        print(row)
                    running = False

        
        g.render(screen)
        palette.render(screen)
        
        pygame.display.flip()
        clock.tick(FPS)

    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()
