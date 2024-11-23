import pygame

class Enemy:
    def __init__(self, pos, moveRange, num, direction):
        self.pos = pos
        self.moveRange = moveRange
        self.num = num
        self.direction = direction
        self.reset()

    def reset(self):
        self.x = self.pos[0]
        self.y = self.pos[1]
        self.characters = {
            1: [
                pygame.transform.smoothscale(pygame.image.load('assets/Characters/tile_0018.png').convert_alpha(), (40, 40)),
                pygame.transform.smoothscale(pygame.image.load('assets/Characters/tile_0019.png').convert_alpha(), (40, 40)),
                pygame.transform.smoothscale(pygame.image.load('assets/Characters/tile_0020.png').convert_alpha(), (40, 40)),
            ]
        }
        self.frames = self.characters[self.num]
        self.state = 0
        self.rect = self.frames[self.state].get_rect()
        self.rect.x = self.x
        self.rect.y = self.y
        self.rightMax = self.moveRange[1]
        self.leftMax = self.moveRange[0]
        self.xVel = 0
        self.maxVel = 2
        self.acceleration = 0.05
        self.deceleration = 0.1
        self.dead = False
        self.deadTime = 0.1
        self.animationTimer = 0

    def flip(self,direction):
        if direction == "right":
            return pygame.transform.flip(self.frames[self.state], True, False)
        if direction == "left":
            return pygame.transform.flip(self.frames[self.state], False, False)

    def render(self, surf):
        img = self.flip(self.direction)
        surf.blit(img, self.rect)

    def move(self):
        if self.direction == "right":
            self.xVel = min(self.xVel + self.acceleration, self.maxVel)
            self.x += self.xVel
            if self.x >= self.rightMax:
                self.x = self.rightMax
                self.direction = "left"
        elif self.direction == "left":
            self.xVel = min(self.xVel + self.acceleration, self.maxVel)
            self.x -= self.xVel
            if self.x <= self.leftMax:
                self.x = self.leftMax
                self.direction = "right"

        if self.animationTimer % 10 == 0:
            self.state = (self.state + 1) % len(self.frames)

        self.rect.x = round(self.x)
        self.rect.y = self.y

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
