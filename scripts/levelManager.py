from scripts.enemy import Enemy
from scripts.tilemap import Grid

from levels.level1 import matrix as level1
from levels.level2 import matrix as level2
from levels.level3 import matrix as level3
from levels.level4 import matrix as level4
from levels.level5 import matrix as level5

from copy import deepcopy

class LevelManager:
    def __init__(self, screen):
        self.levels = {
            1: {
                "enemies": [Enemy((240, 520), (240, 360), 1, "right")],
                "matrix": level1,
                "goal": (740, 780, 300, 340),
            },
            2: {
                "enemies": [Enemy((440, 240), (440, 560), 1, "right")],
                "matrix": level2,
                "goal": (740, 780, 380, 420),
            },
            3: {
                "enemies": [Enemy((510, 400), (510, 760), 1, "right")],
                "matrix": level3,
                "goal": (415, 455, 180, 220),
            },
            4: {
                "enemies": [
                    Enemy((240, 520,), (240, 480,), 1, "right"),
                    Enemy((515, 400,), (515, 760,), 1, "right"),
                ],
                "matrix": level4,
                "goal": (240, 280, 200, 240),
            },
            5: {
                "enemies": [
                    Enemy((240, 520), (240, 440), 1, "right"),
                ],
                "matrix": level5,
                "goal": (510, 550, 240, 280),
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

    def resetLevel(self):
        self.loadLevel(self.currentLevel)

    def loadLevel(self, level):
        levelData = self.levels.get(level)
        if not levelData:
            return
        self.grid = Grid(self.tilesX, self.tilesY, self.tileSize, levelData["matrix"], self.screenX, self.tilesY)
        self.enemies = deepcopy(levelData["enemies"])
        self.goal = levelData["goal"]

    def nextLevel(self):
        if self.currentLevel + 1 in self.levels:
            self.loadLevel(self.currentLevel + 1)
            self.currentLevel += 1
        else:
            self.resetLevel()
