import pygame
from scripts.enemy import Enemy
from scripts.tilemap import Grid
from utils.spritesheet import SpriteSheet

from levels.level1 import matrix as level1
from levels.level2 import matrix as level2
from levels.level3 import matrix as level3
from levels.level4 import matrix as level4
from levels.level5 import matrix as level5
from levels.level6 import matrix as level6
from levels.level7 import matrix as level7
from levels.level8 import matrix as level8

class LevelManager:
    def __init__(self, screen):
        self.levels = {
            1: {
                "enemies": [Enemy((240, 520), (240, 360), 1, "right")],
                "matrix": level1,
                "goal": (750-15, 320-15),
            },
            2: {
                "enemies": [Enemy((440, 240), (440, 560), 1, "right")],
                "matrix": level2,
                "goal": (750-15, 400-15),
            },
            3: {
                "enemies": [Enemy((560, 400), (560, 760), 2, "right")],
                "matrix": level3,
                "goal": (450-15, 200-15),
            },
            4: {
                "enemies": [
                    Enemy((240, 520,), (240, 480,), 2, "right"),
                    Enemy((515, 400,), (515, 760,), 1, "right"),
                ],
                "matrix": level4,
                "goal": (290-15, 200-15),
            },
            5: {
                "enemies": [
                    Enemy((240, 520), (240, 440), 1, "right"),
                ],
                "matrix": level5,
                "goal": (530-15, 240-15),
            },
            6: {
                "enemies": [
                    Enemy((240, 520), (240, 640), 2, "right"),
                ],
                "matrix": level6,
                "goal": (610-15, 360-15),
            },
            7: {
                "enemies": [
                    Enemy((280, 520), (280, 440), 3, "right"),
                    Enemy((480, 400), (480, 560), 1, "right"),
                ],
                "matrix": level7,
                "goal": (760-15, 400-15),
            },
            8: {
                "enemies": [
                    Enemy((200, 520), (200, 480), 3, "right"),
                    Enemy((315, 240), (315, 415), 1, "right"),
                ],
                "matrix": level8,
                "goal": (200-15, 120-15),
            },
        }

        self.currentLevel = 1
        self.tileSize = 40
        self.viewX, self.viewY = 20, 15
        self.tilesX, self.tilesY = 40, 40
        self.screenX, self.tilesY = self.tileSize * self.viewX, self.tileSize * self.viewY
        self.screen = screen
        self.matrix = [[[(-1, -1), (-1, -1), (0,0), (-1, -1)] for _ in range(self.tilesX)] for _ in range(self.tilesY)]
        self.enemies = []
        self.grid = Grid(self.tilesX,self.tilesY,self.tileSize,self.matrix,screenWidth=self.screenX,screenHeight=self.tileSize)
        self.goal = (0,0,0,0)
        self.loadLevel(self.currentLevel)
        self.sheet = SpriteSheet().split("assets/nextLevel/diamond.png",1,8,32,32)
        self.frame = 0
        self.animationTimer = 0
        self.goalImg = self.sheet[self.frame]
        self.goalImg = pygame.transform.smoothscale_by(self.goalImg, (1.5,1.5))

    def resetLevel(self):
        self.loadLevel(self.currentLevel)

    def loadLevel(self, level):
        levelData = self.levels.get(level)
        if not levelData:
            return
        self.grid = Grid(self.tilesX, self.tilesY, self.tileSize, levelData["matrix"], self.screenX, self.tilesY)
        self.enemies = [Enemy(enemy.pos,enemy.moveRange,enemy.enemyType,enemy.direction) for enemy in levelData["enemies"]]
        self.goal = levelData["goal"]

    def nextLevel(self):
        if self.currentLevel + 1 in self.levels:
            self.loadLevel(self.currentLevel + 1)
            self.currentLevel += 1
        else:
            self.resetLevel()

    def drawGoal(self,surf):
        self.animationTimer = (self.animationTimer + 1) % 1000
        if self.animationTimer % 10 == 0:
            self.frame = (self.frame + 1) % 7
            self.goalImg = self.sheet[self.frame]
            self.goalImg = pygame.transform.smoothscale_by(self.goalImg, (1.5,1.5))

        surf.blit(self.goalImg,self.levels[self.currentLevel]["goal"])
    
    def checkNextLevel(self,player):
        playermask = pygame.mask.from_surface(player.img)
        selfmask = pygame.mask.from_surface(self.goalImg)
        if playermask.overlap(selfmask,(player.rect.x-self.goal[0],player.rect.y-self.goal[1])):
            return True
        else:
            return False

    def prevLevel(self):
        if self.currentLevel > 1:
            self.loadLevel(self.currentLevel - 1)
            self.currentLevel -= 1
