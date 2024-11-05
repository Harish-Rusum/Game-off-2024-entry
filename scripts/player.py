import pygame
from scripts.tilemap import Tile


class Player:
    def __init__(self, x, y, tileSize):
        self.img = pygame.image.load("assets/Characters/tile_0000.png").convert_alpha()
        self.img = pygame.transform.smoothscale(self.img, (tileSize, tileSize))
        self.rotation = -1
        self.x = x
        self.y = y
        self.rect = self.img.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y

    def render(self, surf,grid):
        surf.blit(self.img, (self.x, self.y))

    # def move(self, dx, dy, grid,surf):
    #     surrounding = grid.getSurroundingTiles(self.x,self.y)
    #
    #     for element in surrounding:
    #         if element[0][0] == -1:
    #             continue
    #         rect = pygame.rect.Rect(element[2][0],element[2][1],grid.tileSize,grid.tileSize)
    #         if self.rect.colliderect(rect):
    #             if dx < 0:
    #                 if rect.x < self.x:
    #                     return
    #             if dx > 0:
    #                 if rect.x > self.x:
    #                     return
    #             if dy > 0:
    #                 if rect.y > self.y:
    #                     return
    #             if dy < 0:
    #                 if rect.y < self.y:
    #                     return
    #
    #     self.x += dx
    #     self.y += dy
    #     self.rect.x = self.x
    #     self.rect.y = self.y
    #

    def move(self, dx, dy, grid, surf):
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
