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

        self.acc = 0.2
        self.decc = 0.1
        self.maxspeed = 4
        self.xVel = 0
        self.yVel = 0

    def render(self, surf):
        img = self.sheet[self.frame]
        img = pygame.transform.smoothscale(img, (self.playerX, self.playerY))
        if self.direction == -1:
            img = pygame.transform.rotate(img, -180)
            img = pygame.transform.flip(img, False, True)
        surf.blit(img, (self.x, self.y))

    # def move(self, dx, dy, grid,surf):
    #     if dx != 0:
    #         self.xVel += self.acc * dx
    #         self.xVel = max(-self.maxspeed, min(self.xVel, self.maxspeed))
    #     else:
    #         if self.xVel > 0:
    #             self.xVel = max(self.xVel - self.decc, 0)
    #         elif self.xVel < 0:
    #             self.xVel = min(self.xVel + self.decc, 0)
    #
    #     if dy != 0:
    #         self.yVel += self.acc * dy
    #         self.yVel = max(-self.maxspeed, min(self.yVel, self.maxspeed))
    #     else:
    #         if self.yVel > 0:
    #             self.yVel = max(self.yVel - self.decc, 0)
    #         elif self.yVel < 0:
    #             self.yVel = min(self.yVel + self.decc, 0)
    #
    #     if dx > 0: self.direction = 0
    #     if dx < 0: self.direction = -1
    #      
    #     if self.counter % 10 == 0:
    #         self.frame = (self.frame + 1) % self.animationFrames
    #     self.counter = (self.counter + 1) % 100000
    #
    #     surrounding = grid.getSurroundingTiles(self.x, self.y)
    #
    #     newX = self.xVel + self.x
    #     newY = self.yVel + self.y
    #
    #     futureRX = self.rect.move(self.xVel, 0)
    #     futureRY = self.rect.move(0, self.yVel)
    #
    #     for element in surrounding:
    #         tileRect = pygame.Rect(element[2][0], element[2][1], grid.tileSize, grid.tileSize)
    #         if element[0][0] == -1:
    #             continue
    #         if futureRX.colliderect(tileRect):
    #             if newX > 0:
    #                 newX = tileRect.right - 2
    #             else:
    #                 newX = tileRect.left - 2
    #             break
    #
    #
    #     for element in surrounding:
    #         tileRect = pygame.Rect(element[2][0], element[2][1], grid.tileSize, grid.tileSize)
    #         if element[0][0] == -1:
    #             continue
    #         if futureRY.colliderect(tileRect):
    #             if newY > 0:
    #                 newY = tileRect.bottom - 2
    #             else:
    #                 newY = tileRect.top - 2
    #             break
    #
    #     self.x = newX
    #     self.rect.x = self.x
    #     self.y = newY
    #     self.rect.y = self.y
    #

    def move(self, dx, dy, grid):
        if dx != 0:
            self.xVel += self.acc * dx
            self.xVel = max(-self.maxspeed, min(self.xVel, self.maxspeed))
        else:
            if self.xVel > 0:
                self.xVel = max(self.xVel - self.decc, 0)
            elif self.xVel < 0:
                self.xVel = min(self.xVel + self.decc, 0)

        if dy != 0:
            self.yVel += self.acc * dy
            self.yVel = max(-self.maxspeed, min(self.yVel, self.maxspeed))
        else:
            if self.yVel > 0:
                self.yVel = max(self.yVel - self.decc, 0)
            elif self.yVel < 0:
                self.yVel = min(self.yVel + self.decc, 0)

        if dx > 0: 
            self.direction = 0
        elif dx < 0: 
            self.direction = -1

        if self.counter % 10 == 0:
            self.frame = (self.frame + 1) % self.animationFrames
        self.counter += 1

        newX = self.x + self.xVel
        self.rect.x = newX
        surrounding = grid.getSurroundingTiles(self.x, self.y)
        for element in surrounding:
            tileRect = pygame.Rect(element[2][0], element[2][1], grid.tileSize, grid.tileSize)
            if element[0][0] != -1 and self.rect.colliderect(tileRect):
                if self.xVel > 0:
                    self.rect.right = tileRect.left
                elif self.xVel < 0:
                    self.rect.left = tileRect.right
                self.xVel = 0
                break
        self.x = self.rect.x

        newY = self.y + self.yVel
        self.rect.y = newY
        for element in surrounding:
            tileRect = pygame.Rect(element[2][0], element[2][1], grid.tileSize, grid.tileSize)
            if element[0][0] != -1 and self.rect.colliderect(tileRect):
                if self.yVel > 0:
                    self.rect.bottom = tileRect.top
                elif self.yVel < 0:
                    self.rect.top = tileRect.bottom
                self.yVel = 0
                break
        self.y = self.rect.y

    def update(self, dx,dy,grid,screen):
        self.render(screen)
        self.move(dx,dy,grid)
