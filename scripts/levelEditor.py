import pygame
import sys

pygame.init()

TileSize = 40
ViewX, ViewY = 15, 15
TilesX, TilesY = 40, 40
PalWidth = 12 * 40
ExtraWidth = 10
ScreenX, ScreenY = TileSize * ViewX + PalWidth + ExtraWidth, TileSize * ViewY
Fps = 60
Black = (0, 0, 0)

screen = pygame.display.set_mode((ScreenX, ScreenY))
pygame.display.set_caption("Tile Grid System")
clock = pygame.time.Clock()

Matrix = [[(-1, -1) for _ in range(TilesX)] for _ in range(TilesY)]


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
        for y in range(self.tilesY):
            for x in range(self.tilesX):
                tileIndex, rotation = self.grid[y][x]
                tileIndexStr = "empty" if tileIndex == -1 else f"{tileIndex:04d}"
                tile = Tile(tileIndexStr, self.tileSize, self.tileSize, rotation)
                screen.blit(tile.img, (x * self.tileSize + self.offX, y * self.tileSize + self.offY))


class Palette:
    def __init__(self, width, height, palWidth, grid, tileSize):
        self.width = width
        self.palWidth = palWidth
        self.grid = grid
        self.tileSize = tileSize
        self.tilesX = width // tileSize
        self.tilesY = height // tileSize
        self.selected = -1

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
                num += 1

    def getClick(self, mouseX, mouseY, grid):
        if mouseX < (self.width - self.palWidth):
            adjMouseX = mouseX - grid.offX
            adjMouseY = mouseY - grid.offY
            tileX = adjMouseX // TileSize
            tileY = adjMouseY // TileSize
            if 0 <= tileX < grid.tilesX and 0 <= tileY < grid.tilesY:
                grid.grid[tileY][tileX] = (int(self.selected), 1)
        else:
            adjMouseX = mouseX - (self.width - self.palWidth)
            adjMouseY = mouseY
            tileX = adjMouseX // TileSize
            tileY = adjMouseY // TileSize
            num = (tileX * self.tilesY) + tileY
            zeros = "0" * (4 - len(str(num)))
            self.selected = zeros + str(num)
    
    def rotate(self, mouseX, mouseY, grid):
        adjMouseX = mouseX - grid.offX
        adjMouseY = mouseY - grid.offY
        tileX = adjMouseX // TileSize
        tileY = adjMouseY // TileSize
        if 0 <= tileX < grid.tilesX and 0 <= tileY < grid.tilesY:
            tileIndex, rotation = grid.grid[tileY][tileX]
            grid.grid[tileY][tileX] = (tileIndex, (rotation + 1) % 3)


tileMap = Grid(TilesX, TilesY, TileSize, 5, Matrix, ScreenX - PalWidth - ExtraWidth, ScreenY)
picker = Palette(ScreenX, ScreenY, PalWidth, tileMap, TileSize)

blackSpace = pygame.Rect(ScreenX - (PalWidth + ExtraWidth), 0, PalWidth, ScreenY)

mouse_held = False
r_held = False

def main():
    global mouse_held,r_held
    running = True
    while running:
        screen.fill(Black)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouseX, mouseY = pygame.mouse.get_pos()
                mouse_held = True
                picker.getClick(mouseX, mouseY, tileMap)
            if event.type == pygame.MOUSEBUTTONUP:
                mouse_held = False

        if mouse_held:
            mouseX, mouseY = pygame.mouse.get_pos()
            picker.getClick(mouseX, mouseY, tileMap)

        keys = pygame.key.get_pressed()
        if keys[pygame.K_a]:
            tileMap.scroll("left")
        if keys[pygame.K_d]:
            tileMap.scroll("right")
        if keys[pygame.K_w]:
            tileMap.scroll("up")
        if keys[pygame.K_s]:
            tileMap.scroll("down")
        if keys[pygame.K_r]:
            if not r_held:
                mouseX, mouseY = pygame.mouse.get_pos()
                picker.rotate(mouseX, mouseY, tileMap)
                r_held = True
        if not keys[pygame.K_r]:
            r_held = False
        tileMap.render(screen)
        pygame.draw.rect(screen, (0, 0, 0), blackSpace)
        picker.render(screen)
        pygame.display.flip()
        clock.tick(Fps)

    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()
