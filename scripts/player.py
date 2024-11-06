import pygame
from utils.spritesheet import SpriteSheet
class Player:
    def __init__(self, x, y, playerX, playerY):
        self.rotation = -1
        self.x = x
        self.y = y
        self.state = 0
        self.spriteSheet = SpriteSheet()
        self.sheet = self.spriteSheet.split("assets/Characters/sheet.png",1,4,24,24)
        self.frame = 0
        self.animationFrames = 4
        self.direction = 0
        self.counter = 0
        self.playerX = playerX
        self.playerY = playerY
        self.img = self.sheet[self.frame]
        self.img = pygame.transform.smoothscale(self.img, (self.playerX, self.playerY))
        self.rect = self.img.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y

    def render(self, surf):
        img = self.sheet[self.frame]
        img = pygame.transform.smoothscale(img, (self.playerX, self.playerY))
        if self.direction == -1:
            img = pygame.transform.rotate(img, -180)
            img = pygame.transform.flip(img, False, True)
        surf.blit(img, (self.x, self.y))

    def move(self, dx, dy, grid):
        if dx > 0: self.direction = 0
        if dx < 0: self.direction = -1
        if self.counter % 10 == 0:
            self.frame = (self.frame + 1) % self.animationFrames
        self.counter = (self.counter + 1) % 100000

        surrounding = grid.getSurroundingTiles(self.x, self.y)
        
        newX = self.x + dx
        newY = self.y + dy
        futureRX = self.rect.move(dx, 0)
        futureRY = self.rect.move(0, dy)

        canMoveX = True
        for element in surrounding:
            if element[0][0] == -1:
                continue
            tileRect = pygame.Rect(element[2][0], element[2][1], grid.tileSize, grid.tileSize)
            if futureRX.colliderect(tileRect):
                canMoveX = False
                break

        canMoveY = True
        for element in surrounding:
            if element[0][0] == -1:
                continue
            tileRect = pygame.Rect(element[2][0], element[2][1], grid.tileSize, grid.tileSize)
            if futureRY.colliderect(tileRect):
                canMoveY = False
                break 

        if canMoveX:
            self.x = newX
            self.rect.x = self.x
        if canMoveY:
            self.y = newY
            self.rect.y = self.y
