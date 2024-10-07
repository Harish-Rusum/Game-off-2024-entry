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
            loaded = pygame.image.load(f"assets/tile_{tileIndex}.png")
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
        self.selected = None

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

    def getClick(self,mouseX, mouseY):
        if mouseX < (self.width - self.palWidth):
            adjMouseX = mouseX - tileMap.offX
            adjMouseY = mouseY - tileMap.offY
            tileX = adjMouseX // TileSize
            tileY = adjMouseY // TileSize
            if 0 <= tileX < tileMap.tilesX and 0 <= tileY < tileMap.tilesY:
                return tileX, tileY
            else:
                return None
        else:
            adjMouseX = mouseX - (self.width - self.palWidth)
            adjMouseY = mouseY
            tileX = adjMouseX // TileSize
            tileY = adjMouseY // TileSize
            num = (tileX * self.tilesY) + tileY
            zeros = "0" * (4 - len(str(num)))
            string = zeros + str(num)
            self.selected = (f"assets/tile_{string}.png")

tileMap = Grid(TilesX, TilesY, TileSize, 5, Matrix, ScreenX - PalWidth - ExtraWidth, ScreenY)
picker = Palette(ScreenX, ScreenY, PalWidth, tileMap, TileSize)

blackSpace = pygame.Rect(ScreenX - (PalWidth + ExtraWidth), 0, PalWidth, ScreenY)




def main():
    running = True
    while running:
        screen.fill(Black)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouseX, mouseY = pygame.mouse.get_pos()
                tile = picker.getClick(mouseX, mouseY)
                if tile:
                    print(f"Clicked on tile: {tile}")

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
