import pygame

class Enemy:
    def __init__(self, pos, moveRange, enemyType, direction):
        self.pos = pos
        self.moveRange = moveRange
        self.enemyType = enemyType
        self.direction = direction
        self.reset()

    def reset(self):
        self.x = self.pos[0]
        self.y = self.pos[1]
        self.characters = {
            1: [
                pygame.transform.smoothscale(pygame.image.load('assets/Characters/tile_0018.png').convert_alpha(), (50, 50)),
                pygame.transform.smoothscale(pygame.image.load('assets/Characters/tile_0019.png').convert_alpha(), (50, 50)),
                pygame.transform.smoothscale(pygame.image.load('assets/Characters/tile_0020.png').convert_alpha(), (50, 50)),
            ],
            2: [
                pygame.transform.smoothscale(pygame.image.load('assets/Characters/tile_0025.png').convert_alpha(), (50, 50)),
                pygame.transform.smoothscale(pygame.image.load('assets/Characters/tile_0026.png').convert_alpha(), (50, 50)),
                pygame.transform.smoothscale(pygame.image.load('assets/Characters/tile_0026.png').convert_alpha(), (50, 50)),
            ],
            3: [
                pygame.transform.smoothscale(pygame.image.load('assets/Characters/tile_0015.png').convert_alpha(), (50, 50)),
                pygame.transform.smoothscale(pygame.image.load('assets/Characters/tile_0016.png').convert_alpha(), (50, 50)),
                pygame.transform.smoothscale(pygame.image.load('assets/Characters/tile_0017.png').convert_alpha(), (50, 50)),
            ]
        }

        self.frames = self.characters[self.enemyType]
        self.state = 0
        self.rect = self.frames[self.state].get_rect()
        self.rect.x = self.x-10
        self.rect.y = self.y-10
        self.rightMax = self.moveRange[1]
        self.leftMax = self.moveRange[0]
        self.maxVel = 2
        self.dead = False
        self.deadTime = 0.5
        self.animationTimer = 0

    def flip(self, direction):
        if direction == "right":
            return pygame.transform.flip(self.frames[self.state], True, False)
        if direction == "left":
            return pygame.transform.flip(self.frames[self.state], False, False)

    def render(self, surf, offset=[0, 0]):
        img = self.flip(self.direction)
        surf.blit(img, (self.rect.x + offset[0], self.rect.y + offset[1]))

    def move(self):
        step = self.maxVel
        if self.direction == "right":
            self.x += step
            if self.x >= self.rightMax:
                self.x = self.rightMax
                self.direction = "left"
        elif self.direction == "left":
            self.x -= step
            if self.x <= self.leftMax:
                self.x = self.leftMax
                self.direction = "right"

        if self.animationTimer % 8 == 0:
            self.state = (self.state + 1) % len(self.frames)

        self.rect.x = round(self.x) - 10
        self.rect.y = self.y - 10

    def die(self):
        self.dead = True
        self.state = 2

    def update(self, surf):
        if not self.dead:
            self.move()
        else:
            self.deadTime = max(0, self.deadTime - (1 / 60))
        if self.deadTime > 0:
            self.render(surf)
        self.animationTimer = (self.animationTimer + 1) % 1000
